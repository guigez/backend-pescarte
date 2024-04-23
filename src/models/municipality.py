import uuid
from typing import List

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel, Session
from src.models import Community


class Municipality(BaseModel, BaseSQLModel):
    __tablename__ = 'municipality'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    uf = Column(String(255), ForeignKey('uf.uf'))

    uf_rel = relationship("UF", back_populates="municipalities")
    communities = relationship("Community", back_populates="municipality")

    @classmethod
    def get_cities_by_uf(cls, db: Session, uf: str) -> List['Municipality']:
        return db.query(cls).filter(cls.uf == uf).all()

    @classmethod
    def get_cities_with_communities(cls, db: Session, uf: str):
        query = db.query(cls).join(Community, cls.id == Community.municipality_id).filter(cls.uf == uf)
        return query.all()
