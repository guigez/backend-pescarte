from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.models.municipality import Municipality
from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel


class Community(BaseModel, BaseSQLModel):
    __tablename__ = 'community'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    municipality_id = Column(UUID(as_uuid=True), ForeignKey('municipality.id'))

    # Relationship - each Community is related to a Municipality
    municipality = relationship("Municipality", back_populates="communities")
