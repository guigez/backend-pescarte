from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.database import get_db, Session
from src.models import Gear
from src.schemas.gear import GearInput

router = APIRouter(prefix='/gear')


@router.get('/')
async def get_all_gears(db: Session = Depends(get_db)):
    return Gear.get_all(db)


@router.get('/{gear_id}')
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


@router.post('/')
async def create_gear(
        gear: GearInput,
        db: Session = Depends(get_db)
):
    gear_model = Gear(**gear.dict())
    saved, error = gear_model.save(db)

    if saved:
        return gear_model
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving gear",
                     "detail": error}
        )


@router.patch('/{gear_id}')
async def update_gear(
        gear_id: UUID,
        gear_payload: GearInput,
        db: Session = Depends(get_db)
):
    gear = Gear.get_by_id(db, gear_id)

    if not gear:
        return JSONResponse(
            status_code=404,
            content={"message": "gear not found"}
        )

    updated, error = gear.update(db, gear_payload.dict(exclude_none=True))

    if updated:
        return {"message": "Gear updated"}
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating gear",
                     "detail": error}
        )


@router.delete('/{gear_id}')
async def delete_gear(
        gear_id: UUID,
        db: Session = Depends(get_db)
):
    gear = Gear.get_by_id(db, gear_id)

    if not gear:
        return JSONResponse(
            status_code=404,
            content={"message": "Gear not found"}
        )

    deleted, error = gear.delete(db)

    if deleted:
        return {"message": "Gear deleted"}
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating gear",
                     "detail": error}
        )
