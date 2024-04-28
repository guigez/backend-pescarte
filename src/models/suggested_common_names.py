import uuid
import enum
from typing import List

from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel, Session


class SuggestedCommonNameStatus(enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class SuggestedCommonNames(BaseModel, BaseSQLModel):
    __tablename__ = 'suggested_common_names'

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    suggested_name = Column(String(255))
    status = Column(Enum(SuggestedCommonNameStatus), default=SuggestedCommonNameStatus.PENDING)
    fish_id = Column(UUID(as_uuid=True), ForeignKey('fish.id'))
    community_id = Column(UUID(as_uuid=True), ForeignKey('community.id'))

    # Define relationships
    fish = relationship("Fish", back_populates="suggested_names")
    community = relationship("Community", back_populates="suggested_names")

    @classmethod
    def update_status(cls, db: Session, ids: List[UUID], status: SuggestedCommonNameStatus):
        suggested_names = db.query(cls).filter(cls.id.in_(ids)).all()

        for name in suggested_names:
            name.status = status

        db.commit()
