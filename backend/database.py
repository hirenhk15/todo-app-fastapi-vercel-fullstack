import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load enviornment variables
load_dotenv()

user = os.environ["DATABASE_USER"]
password = os.environ["DATABASE_PASSWORD"]
host = os.environ["DATABASE_HOST"]
port = os.environ["DATABASE_PORT"]
db_name = os.environ["DATABASE_NAME"]

# Create database engine to connect with it
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()