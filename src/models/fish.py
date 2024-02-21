from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

from src.models.base_sql_model import BaseSQLModel
from src.models.fish_habitat import FishHabitat
from src.models.fish_gear import FishGear
from src.models.fish_common_name_by_community import FishCommonNameByCommunity
from src.models.suggested_common_names import SuggestedCommonNames
from src.models.habitat import Habitat
from src.models.gear import Gear
from src.database import BaseModel


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
