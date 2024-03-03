from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.database import BaseModel


# Association table for the many-to-many relationship
FishGear = Table(
    'fish_gear',
    BaseModel.metadata,
    Column('fish_id', UUID(as_uuid=True), ForeignKey('fish.id'), primary_key=True),
    Column('gear_id', UUID(as_uuid=True), ForeignKey('gear.id'), primary_key=True)
)
