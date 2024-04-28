from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel, UUID4, Field

from src.schemas.gear import GearSchema


class SuggestedNames(BaseModel):
    community: str
    names: List[str]


class FishInput(BaseModel):
    scientific_name: str
    native: bool

    gears: Optional[List[UUID4]]
    habitats: Optional[List[UUID4]]


class FishOutput(BaseModel):
    id: UUID4
    scientific_name: str
    native: bool
    image_data: Optional[str] = None  # Base64-encoded image data

    gears: Optional[List[GearSchema]] = Field(default=[])
    habitats: Optional[List[GearSchema]] = Field(default=[])
    suggested_names: Optional[List[SuggestedNames]] = Field(default=[])

    class Config:
        orm_mode = True
