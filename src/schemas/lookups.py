from pydantic import BaseModel, UUID4, validator


class UFSchema(BaseModel):
    uf: str
    uf_name: str

    class Config:
        orm_mode = True


class CitySchema(BaseModel):
    id: UUID4
    uf: str
    name: str

    class Config:
        orm_mode = True
