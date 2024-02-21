from src.database import get_db, Session


from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from src.models.community import Community
from src.models.fish import Fish
from src.models.gear import Gear
from src.models.habitat import Habitat
from src.models.fish_common_name_by_community import FishCommonNameByCommunity
from src.models.suggested_common_names import SuggestedCommonNames

app = FastAPI(title='Catalogo Pescarte API', version='0.0.1')


@app.get('/healthcheck')
async def health_check():
    return {"message": "Up and running"}


@app.post('/teste')
async def test_endpoint(db: Session = Depends(get_db)):

    new_model = Community(name="Comunidade 1", municipality_id="f9de9d6d-659b-43ef-a1cd-aa7a3a837b52")
    saved, error = new_model.save(db)


    if saved:
        return new_model
    else:
        return JSONResponse(
            status_code=400,
            content={"message": error}
        )


@app.post('/add-fish-with-habitats')
async def add_fish_with_habitats(db: Session = Depends(get_db)):
    # Create new fish
    new_fish = db.query(Fish).filter(Fish.scientific_name == "Salmo salar2").first()

    # Fetch or create the community
    community = db.query(Community).filter(Community.name == "Community 1").first()
    if not community:
        community = Community(name="Community 1")
        community.save(db)

    new_suggested_name = SuggestedCommonNames(
        id="unique-id-for-this-suggestion",
        name="John Doe",
        email="john.doe@example.com",
        suggested_name="Local Name for Fish",
        fish_id=new_fish.id,
        community_id=community.id
    )
    saved, error = new_suggested_name.save(db)

    if saved:
        return new_suggested_name
    else:
        return JSONResponse(
            status_code=400,
            content={"message": error}
        )


