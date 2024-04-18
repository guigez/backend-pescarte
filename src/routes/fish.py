from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse, Response

from src.database import get_db, Session
from src.models import Fish, Habitat
from src.models.gear import Gear
from src.schemas.errors import ErrorMessage
from src.schemas.fish import FishInput, FishOutput

router = APIRouter(prefix='/fish')


@router.get('/', response_model=List[FishOutput])
async def get_all(db: Session = Depends(get_db)):
    fishes = Fish.get_fishes_with_gears_and_habitats(db)
    return fishes


@router.get('/{fish_id}')
async def get_fish_by_id(
        fish_id: UUID,
        db: Session = Depends(get_db)
):
    fish = Fish.get_by_id(db, fish_id)
    if fish:
        return fish
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Fish not found"}
        )


@router.post('/')
async def create_fish(fish_payload: FishInput, db: Session = Depends(get_db)):
    # Getting gears
    gears_ids = fish_payload.gears
    gears = Gear.get_by_ids(db, gears_ids)

    # Getting habitats
    habitats_id = fish_payload.habitats
    habitats = Habitat.get_by_ids(db, habitats_id)

    # Saving fish
    fish_model = Fish(**fish_payload.model_dump(exclude={'gears', 'habitats'}))
    _, error = fish_model.save(db)  # Test without this save

    if error:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving fish",
                     "detail": error}
        )

    for gear in gears:
        fish_model.gears.append(gear)

    for habitat in habitats:
        fish_model.habitats.append(habitat)

    _, error = fish_model.save(db)

    if error:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving fish",
                     "detail": error}
        )

    return fish_model
