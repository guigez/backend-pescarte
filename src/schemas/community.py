from typing import Optional

from pydantic import BaseModel, UUID4


class CommunityInput(BaseModel):
    name: str
    description: Optional[str]
    municipality_id: UUID4


class CommunityPatchInput(BaseModel):
    name: Optional[str]
    description: Optional[str]
    municipality_id: Optional[UUID4]


class CommunityOutput(BaseModel):
    id: UUID4
    name: str
    description: Optional[str]
    municipality_id: Optional[UUID4]

    class Config:
        orm_mode = True


class CommunityOutputWithStateAndCity(BaseModel):
    id: UUID4
    name: str
    description: Optional[str]
    municipality_id: Optional[UUID4]
    municipality: str
    uf: str

    class Config:
        orm_mode = True
