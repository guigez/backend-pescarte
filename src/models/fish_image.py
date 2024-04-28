import uuid

from sqlalchemy import Column, ForeignKey, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel


class FishImage(BaseModel, BaseSQLModel):
    __tablename__ = 'fish_images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fish_id = Column(UUID(as_uuid=True), ForeignKey('fish.id', ondelete="CASCADE"), unique=True)
    image_data = Column(LargeBinary, nullable=False)
    content_type = Column(String, nullable=False)

    # Relationship back to Fish
    fish = relationship("Fish", back_populates="image")
