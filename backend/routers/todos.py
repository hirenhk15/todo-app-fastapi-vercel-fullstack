import crud
from typing import List
from langchain_groq import ChatGroq
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ToDoRequest, ToDoResponse
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi import APIRouter, Depends, HTTPException, status


# Define LLM
llm = ChatGroq(temperature=0, model="mixtral-8x7b-32768")

# Define summarization chain
summarize_prompt_template = """
    Provide the summary for the following text:
    {text}
"""
summarize_prompt = PromptTemplate.from_template(summarize_prompt_template)
summarize_chain = summarize_prompt | llm | StrOutputParser()

# Define chain to write short poem
write_poem_prompt_template = """
    Write a short poem for the following text:
    {text}
"""
write_poem_prompt = PromptTemplate.from_template(write_poem_prompt_template)
write_poem_chain = write_poem_prompt | llm | StrOutputParser()

router = APIRouter(
    prefix="/todos"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.create_todo(db, todo)
    return todo

@router.get("", response_model=List[ToDoResponse])
def get_todos(completed: bool = None, db: Session = Depends(get_db)):
    todos = crud.read_todos(db, completed)
    return todos

@router.get("/{id}")
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

@router.put("/{id}")
def update_todo(id: int, todo: ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="to do not found")
    
@router.post("/summarize-text")
async def summarize_text(text: str):
    summary = summarize_chain.invoke(text)
    return {"summary": summary}

@router.post("/write-poem/{id}")
async def write_poem_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    poem = write_poem_chain.invoke(todo.name)
    return {"poem": poem}