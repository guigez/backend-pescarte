from sqlalchemy import Column, String
from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel


class UF(BaseModel, BaseSQLModel):
    __tablename__ = 'uf'

    # Define columns
    uf_name = Column(String(255), primary_key=True)
    uf = Column(String(2), unique=True, nullable=False)
