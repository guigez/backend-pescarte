from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse, Response

from src.database import get_db, Session
from src.models import Habitat
from src.schemas.errors import ErrorMessage
from src.schemas.habitat import HabitatInput, HabitatOutput

router = APIRouter(prefix='/habitat')


@router.get('/', response_model=List[HabitatOutput])
async def get_all_habitats(db: Session = Depends(get_db)):
    return Habitat.get_all(db)


@router.get('/{habitat_id}', response_model=HabitatOutput, responses={404: {'model': ErrorMessage}})
async def get_habitat(
        habitat_id: UUID,
        db: Session = Depends(get_db)
):
    habitat = Habitat.get_by_id(db, habitat_id)
    if habitat:
        return habitat
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Habitat not found"}
        )


@router.post('/', response_model=HabitatOutput)
async def create_habitat(
        habitat: HabitatInput,
        db: Session = Depends(get_db)
):
    habitat_model = Habitat(**habitat.dict())
    saved, error = habitat_model.save(db)

    if saved:
        return saved
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving habitat",
                     "detail": error}
        )


@router.patch('/{habitat_id}', response_model=HabitatOutput, responses={404: {'model': ErrorMessage}})
async def update_habitat(
        habitat_id: UUID,
        habitat_payload: HabitatInput,
        db: Session = Depends(get_db)
):
    habitat = Habitat.get_by_id(db, habitat_id)

    if not habitat:
        return JSONResponse(
            status_code=404,
            content={"message": "habitat not found"}
        )

    updated, error = habitat.update(db, habitat_payload.dict(exclude_none=True))

    if updated:
        return updated
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating habitat",
                     "detail": error}
        )


@router.delete('/{habitat_id}', status_code=204, response_class=Response, responses={404: {'model': ErrorMessage}})
async def delete_habitat(
        habitat_id: UUID,
        db: Session = Depends(get_db)
):
    habitat = Habitat.get_by_id(db, habitat_id)

    if not habitat:
        return JSONResponse(
            status_code=404,
            content={"message": "Habitat not found"}
        )

    deleted, error = habitat.delete(db)

    if deleted:
        return None
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating habitat",
                     "detail": error}
        )
