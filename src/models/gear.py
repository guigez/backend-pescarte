import uuid
from typing import List

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base_sql_model import BaseSQLModel
from src.models.fish_gear import FishGear
from src.database import BaseModel, Session


class Gear(BaseModel, BaseSQLModel):
    __tablename__ = 'gear'

    # Define columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)

    fishes = relationship("Fish", secondary=FishGear, back_populates="gears")

    @classmethod
    def get_all(cls, db: Session) -> List["Gear"]:
        return db.query(cls).all()

    @classmethod
    def get_by_id(cls, db: Session, gear_id: UUID) -> "Gear":
        return db.query(cls).filter_by(id=gear_id).first()

    @classmethod
    def get_by_ids(cls, db: Session, gear_ids: List[UUID]) -> List["Gear"]:
        gears = db.query(cls).filter(cls.id.in_(gear_ids)).all()
        return gears
