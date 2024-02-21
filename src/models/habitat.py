from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

from src.models.base_sql_model import BaseSQLModel
from src.models.fish_habitat import FishHabitat
from src.database import BaseModel


class Habitat(BaseModel, BaseSQLModel):
    __tablename__ = 'habitat'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)

    fishes = relationship("Fish", secondary=FishHabitat, back_populates="habitats")
