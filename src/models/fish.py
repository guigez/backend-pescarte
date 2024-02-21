from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

from src.models.base_sql_model import BaseSQLModel

Base = declarative_base()


class Fish(Base, BaseSQLModel):
    __tablename__ = 'fish'

    # Define columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scientific_name = Column(String(255), unique=True, nullable=False)
    native = Column(Boolean)
