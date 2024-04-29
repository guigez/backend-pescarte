import base64
from uuid import UUID
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File
from starlette.responses import JSONResponse, Response
from sqlalchemy.orm import selectinload


from src.database import get_db, Session
from src.models import Fish, Habitat, FishImage
from src.models.suggested_common_names import SuggestedCommonNames, SuggestedCommonNameStatus
from src.models.gear import Gear
from src.schemas.errors import ErrorMessage
from src.schemas.fish import FishInput, FishOutput, SuggestedNames
from src.schemas.gear import GearSchema

router = APIRouter(prefix='/fish')


def build_gears(gears: List[Gear]):
    if not gears:
        return None

    result = list()

    for gear in gears:
        gear_schema = GearSchema(
            id=gear.id,
            name=gear.name
        )
        result.append(gear_schema)

    return result


def build_habitats(habitats: List[Habitat]):
    if not habitats:
        return None

    result = list()

    for habitat in habitats:
        habitat_schema = GearSchema(
            id=habitat.id,
            name=habitat.name
        )
        result.append(habitat_schema)

    return result


def build_suggested_names(suggested_names: List[SuggestedCommonNames]) -> Optional[List[SuggestedNames]]:
    if not suggested_names:
        return None

    names_grouped_by_community: Dict[str, List[str]] = dict()
    resp = list()

    for suggested_name in suggested_names:
        if suggested_name.status == SuggestedCommonNameStatus.APPROVED:
            community_name = suggested_name.community.name
            name = suggested_name.suggested_name

            if names_grouped_by_community.get(community_name) is not None:
                names_grouped_by_community[community_name].append(name)
            else:
                names_grouped_by_community[community_name] = [name]

    for community_name, suggested_names in names_grouped_by_community.items():
        suggested_name = SuggestedNames(
            community=community_name,
            names=suggested_names
        )

        resp.append(suggested_name)

    return resp


@router.get('/', response_model=List[FishOutput])
async def get_all(
        db: Session = Depends(get_db),
        scientific_name: Optional[str] = Query(None),
        common_name: Optional[str] = Query(None),
        community_id: Optional[UUID] = Query(None)
):
    query = db.query(Fish)

    if scientific_name:
        query = query.filter(Fish.scientific_name.ilike(f"%{scientific_name}%"))

    if common_name or community_id:
        query = query.join(Fish.suggested_names).filter(
            SuggestedCommonNames.status == SuggestedCommonNameStatus.APPROVED
        )

        if common_name:
            query = query.filter(SuggestedCommonNames.suggested_name.ilike(f"%{common_name}%"))

        if community_id:
            query = query.filter(SuggestedCommonNames.community_id == community_id)

    # Load gears and habitats
    query = query.options(selectinload(Fish.gears))
    query = query.options(selectinload(Fish.habitats))
    query = query.options(selectinload(Fish.habitats))
    query = query.options(selectinload(Fish.image))

    fishes = query.all()

    response = list()
    for fish in fishes:
        image_data = base64.b64encode(fish.image.image_data).decode('utf-8') if fish.image else None
        suggested_names: List[SuggestedCommonNames] = fish.suggested_names
        suggested_names_schemas = build_suggested_names(suggested_names)
        fish_output = FishOutput(
            id=fish.id,
            scientific_name=fish.scientific_name,
            native=fish.native,
            gears=build_gears(fish.gears),
            habitats=build_habitats(fish.habitats),
            suggested_names=suggested_names_schemas,
            image_data=image_data,
        )

        response.append(fish_output)

    return response


@router.get('/{fish_id}')
async def get_fish_by_id(
        fish_id: UUID,
        db: Session = Depends(get_db)
):
    fish = Fish.get_by_id(db, fish_id)
    if fish:
        image_data = base64.b64encode(fish.image.image_data).decode('utf-8') if fish.image else None
        suggested_names: List[SuggestedCommonNames] = fish.suggested_names
        suggested_names_schemas = build_suggested_names(suggested_names)
        fish_output = FishOutput(
            id=fish.id,
            scientific_name=fish.scientific_name,
            native=fish.native,
            gears=build_gears(fish.gears),
            habitats=build_habitats(fish.habitats),
            suggested_names=suggested_names_schemas,
            image_data=image_data,
        )
        return fish_output
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


@router.post("/{fish_id}/upload-image", status_code=201)
async def upload_fish_image(
    fish_id: UUID,
    file: UploadFile = File(..., description="The image file to upload"),
    db: Session = Depends(get_db)
):
    # Check if the fish exists
    fish = db.query(Fish).filter(Fish.id == fish_id).first()
    if not fish:
        return JSONResponse(
            status_code=404,
            content={"message": "Fish not found"}
        )

    # Read the image data
    image_data = await file.read()

    # Check if an image already exists and update or create a new one
    fish_image = db.query(FishImage).filter(FishImage.fish_id == fish_id).first()
    if fish_image:
        fish_image.image_data = image_data
        fish_image.content_type = file.content_type
    else:
        fish_image = FishImage(
            fish_id=fish_id,
            image_data=image_data,
            content_type=file.content_type
        )
        db.add(fish_image)

    # Commit changes to the database
    db.commit()

    return {"message": "Image uploaded successfully"}


@router.get("/{fish_id}/image", responses={200: {"content": {"image/*": {}}}, 404: {"description": "Fish not found"}})
async def get_fish_image(
    fish_id: UUID,
    db: Session = Depends(get_db)
):
    # Retrieve the fish image from the database
    fish_image = db.query(FishImage).filter(FishImage.fish_id == fish_id).first()
    if not fish_image:
        return JSONResponse(
            status_code=404,
            content={"message": "Fish image not found"}
        )

    # Return the image as a binary stream
    return Response(content=fish_image.image_data, media_type=fish_image.content_type)


@router.delete('/{fish_id}', status_code=204, response_class=Response, responses={404: {'model': ErrorMessage}})
async def delete_fish(
        fish_id: UUID,
        db: Session = Depends(get_db)
):
    # TODO: Found which type should I define as the return
    fish = Fish.get_by_id(db, fish_id)

    if not fish:
        return JSONResponse(
            status_code=404,
            content={"message": "Fish not found"}
        )

    deleted, error = fish.delete(db)

    if deleted:
        return None
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating fish",
                     "detail": error}
        )
