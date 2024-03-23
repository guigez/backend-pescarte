
from pydantic import BaseModel, UUID4


class HabitatInput(BaseModel):
    name: str


class HabitatOutput(BaseModel):
    id: UUID4
    name: str

    class Config:
        orm_mode = True
