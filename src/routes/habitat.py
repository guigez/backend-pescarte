from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.database import get_db, Session
from src.models import Habitat
from src.schemas.habitat import HabitatInput

router = APIRouter(prefix='/habitat')


@router.get('/')
async def get_all_habitats(db: Session = Depends(get_db)):
    return Habitat.get_all(db)


@router.get('/{habitat_id}')
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


@router.post('/')
async def create_habitat(
        habitat: HabitatInput,
        db: Session = Depends(get_db)
):
    habitat_model = Habitat(**habitat.dict())
    saved, error = habitat_model.save(db)

    if saved:
        return habitat_model
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving habitat",
                     "detail": error}
        )


@router.patch('/{habitat_id}')
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
        return {"message": "Habitat updated"}
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating habitat",
                     "detail": error}
        )


@router.delete('/{habitat_id}')
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
        return {"message": "Habitat deleted"}
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating habitat",
                     "detail": error}
        )
