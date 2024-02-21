from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import DB_CONNECTION_URL

engine = create_engine(DB_CONNECTION_URL)
Session = sessionmaker(bind=engine)
BaseModel = declarative_base()


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
