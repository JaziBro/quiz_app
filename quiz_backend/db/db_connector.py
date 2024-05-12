from dotenv import find_dotenv, load_dotenv
from sqlmodel import Session, create_engine, SQLModel
from quiz_backend.settings import db, testDB
from fastapi import FastAPI
import os

def get_session():
    with Session(engine) as session:
        yield session

_ = load_dotenv(find_dotenv())

connection_string = str(os.environ["DATABASE_URL"]).replace("postgresql","postgresql+psycopg2")

if db is None:
    raise RuntimeError("Database environment variable is not set")

engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300,)
  
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

