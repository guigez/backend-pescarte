from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.models.uf import UF
from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel


class Municipality(BaseModel, BaseSQLModel):
    __tablename__ = 'municipality'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    uf = Column(String(255), ForeignKey('uf.uf_name'))

    uf_rel = relationship("UF", back_populates="municipalities")
