from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel, Session
from src.models import Community, Municipality


class UF(BaseModel, BaseSQLModel):
    __tablename__ = 'uf'

    # Define columns
    uf_name = Column(String(255), unique=True, nullable=False)
    uf = Column(String(2),  primary_key=True)

    municipalities = relationship("Municipality", back_populates="uf_rel")

    @classmethod
    def get_all(cls, db: Session) -> List['UF']:
        return db.query(UF).all()

    @classmethod
    def get_uf_with_communities(cls, db: Session) -> List['UF']:
        # Get cities with communities ids
        municipality_ids_result = (
            db.query(Municipality.uf)
            .join(Community, Municipality.id == Community.municipality_id)
            .distinct().all()
        )
        municipality_ids = [m_id[0] for m_id in municipality_ids_result]

        return db.query(UF).filter(cls.uf.in_(municipality_ids)).all()
