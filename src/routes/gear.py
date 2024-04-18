from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse, Response

from src.database import get_db, Session
from src.models import Gear
from src.schemas.errors import ErrorMessage
from src.schemas.gear import GearInput, GearSchema

router = APIRouter(prefix='/gear')


@router.get('/', response_model=List[GearSchema])
async def get_all_gears(db: Session = Depends(get_db)):
    return Gear.get_all(db)


@router.get('/{gear_id}', response_model=GearSchema, responses={404: {'model': ErrorMessage}})
async def get_gear(
        gear_id: UUID,
        db: Session = Depends(get_db)
):
    gear = Gear.get_by_id(db, gear_id)
    if gear:
        return gear
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Gear not found"}
        )


@router.post('/', response_model=GearSchema)
async def create_gear(
        gear: GearInput,
        db: Session = Depends(get_db)
):
    gear_model = Gear(**gear.dict())
    saved, error = gear_model.save(db)

    if saved:
        return saved
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving gear",
                     "detail": error}
        )


@router.patch('/{gear_id}', response_model=GearSchema, responses={404: {'model': ErrorMessage}})
async def update_gear(
        gear_id: UUID,
        gear_payload: GearInput,
        db: Session = Depends(get_db)
):
    gear = Gear.get_by_id(db, gear_id)

    if not gear:
        return JSONResponse(
            status_code=404,
            content={"message": "Gear not found"}
        )

    updated, error = gear.update(db, gear_payload.dict(exclude_none=True))

    if updated:
        return updated
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating gear",
                     "detail": error}
        )


@router.delete('/{gear_id}', status_code=204, response_class=Response, responses={404: {'model': ErrorMessage}})
async def delete_gear(
        gear_id: UUID,
        db: Session = Depends(get_db)
):
    # TODO: Found which type should I define as the return
    gear = Gear.get_by_id(db, gear_id)

    if not gear:
        return JSONResponse(
            status_code=404,
            content={"message": "Gear not found"}
        )

    deleted, error = gear.delete(db)

    if deleted:
        return None
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating gear",
                     "detail": error}
        )
