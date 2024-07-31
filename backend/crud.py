from models import ToDo
from schemas import ToDoRequest, ToDoResponse
from sqlalchemy.orm import Session


# Create CRUD methods
def create_todo(db: Session, todo: ToDoRequest):
    db_todo = ToDo(name=todo.name, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def read_todos(db: Session, completed: bool):
    if completed is None:
        return db.query(ToDo).all()
    else:
        return db.query(ToDo).filter(ToDo.completed == completed).all()
    
def read_todo(db: Session, id: int):
    return db.query(ToDo).filter(ToDo.id == id).first()

def update_todo(db: Session, id: int, todo: ToDoRequest):
    db_todo = db.query(ToDo).filter(ToDo.id == id).first()
    if db_todo is None:
        return None
    
    db.query(ToDo).filter(ToDo.id == id).update({'name': todo.name, 'completed': todo.completed})
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, id: int):
    db_todo = db.query(ToDo).filter(ToDo.id == id).first()
    if db_todo is None:
        return None
    
    db.query(ToDo).filter(ToDo.id == id).delete()
    db.commit()
    return True