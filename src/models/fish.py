import uuid
from typing import List

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, selectinload

from src.models.base_sql_model import BaseSQLModel
from src.models.fish_habitat import FishHabitat
from src.models.fish_gear import FishGear
from src.database import BaseModel, Session


class Fish(BaseModel, BaseSQLModel):
    __tablename__ = 'fish'

    # Define columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scientific_name = Column(String(255), unique=True, nullable=False)
    native = Column(Boolean)

    habitats = relationship("Habitat", secondary=FishHabitat, back_populates="fishes")
    gears = relationship("Gear", secondary=FishGear, back_populates="fishes")
    common_names = relationship("FishCommonNameByCommunity", back_populates="fish")
    suggested_names = relationship("SuggestedCommonNames", back_populates="fish")
    image = relationship("FishImage", back_populates="fish", uselist=False, cascade="all, delete-orphan")

    @classmethod
    def get_all(cls, db: Session) -> List["Fish"]:
        return db.query(cls).all()

    @classmethod
    def get_by_id(cls, db: Session, fish_id: UUID) -> "Fish":
        return db.query(cls).filter_by(id=fish_id).first()

    @classmethod
    def get_fishes_with_gears_and_habitats(cls, db: Session) -> List["Fish"]:
        return db.query(cls).options(
            selectinload(Fish.gears),
            selectinload(Fish.habitats)
        ).all()
