from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel


class Gear(BaseModel, BaseSQLModel):
    __tablename__ = 'gear'

    # Define columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)