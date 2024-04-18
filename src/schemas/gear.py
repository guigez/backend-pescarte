
from pydantic import BaseModel, UUID4


class GearInput(BaseModel):
    name: str


class GearSchema(BaseModel):
    id: UUID4
    name: str

    class Config:
        orm_mode = True
