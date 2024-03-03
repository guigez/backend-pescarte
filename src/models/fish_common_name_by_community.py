from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database import BaseModel
from src.models.base_sql_model import BaseSQLModel


class FishCommonNameByCommunity(BaseModel, BaseSQLModel):
    __tablename__ = 'fish_common_name_by_community'

    common_name = Column(String(255), primary_key=True, nullable=False)
    fish_id = Column(UUID(as_uuid=True), ForeignKey('fish.id'), primary_key=True)
    community_id = Column(UUID(as_uuid=True), ForeignKey('community.id'), primary_key=True)

    # Define relationships
    fish = relationship("Fish", back_populates="common_names")
    community = relationship("Community", back_populates="fish_common_names")
