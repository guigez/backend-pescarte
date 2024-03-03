from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.database import BaseModel


# Association table for the many-to-many relationship
FishHabitat = Table(
    'fish_habitat',
    BaseModel.metadata,
    Column('fish_id', UUID(as_uuid=True), ForeignKey('fish.id'), primary_key=True),
    Column('habitat_id', UUID(as_uuid=True), ForeignKey('habitat.id'), primary_key=True)
)
