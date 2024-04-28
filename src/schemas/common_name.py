from typing import List

from pydantic import BaseModel, UUID4, validator
import enum


class SuggestCommonNameBody(BaseModel):
    name: str
    email: str
    fish_id: UUID4
    community_id: UUID4
    suggested_name: str


class SuggestedCommonNameResponse(BaseModel):
    id: UUID4
    name: str
    email: str
    suggested_name: str
    status: str
    fish_id: UUID4
    community_id: UUID4

    @validator('status', pre=True, always=True)
    def convert_status_to_string(cls, value):
        if isinstance(value, enum.Enum):
            return value.value
        return value

    class Config:
        orm_mode = True


class SuggestedNameIdList(BaseModel):
    ids: List[UUID4]
