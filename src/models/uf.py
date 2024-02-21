from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel


class UF(BaseModel, BaseSQLModel):
    __tablename__ = 'uf'

    # Define columns
    uf_name = Column(String(255), unique=True, nullable=False)
    uf = Column(String(2),  primary_key=True)

    municipalities = relationship("Municipality", back_populates="uf_rel")