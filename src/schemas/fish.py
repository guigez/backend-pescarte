from typing import List, Optional

from pydantic import BaseModel, UUID4, Field

from src.schemas.gear import GearSchema


class FishInput(BaseModel):
    scientific_name: str
    native: bool

    gears: Optional[List[UUID4]]
    habitats: Optional[List[UUID4]]


class FishOutput(BaseModel):
    id: UUID4
    scientific_name: str
    native: bool

    gears: Optional[List[GearSchema]] = Field(default=[])
    habitats: Optional[List[GearSchema]] = Field(default=[])

    class Config:
        orm_mode = True
