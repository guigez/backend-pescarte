from src.database import get_db, Session


from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from src.models.community import Community
from src.models.fish import Fish
from src.models.habitat import Habitat

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

    # Assuming habitats exist, fetch them by ID or name, or create new ones
    habitat1 = db.query(Habitat).filter(Habitat.name == "Coral Reef").first()
    if not habitat1:
        habitat1 = Habitat(name="Coral Reef")
        db.add(habitat1)

    habitat2 = db.query(Habitat).filter(Habitat.name == "Freshwater Lake").first()
    if not habitat2:
        habitat2 = Habitat(name="Freshwater Lake")
        db.add(habitat2)

    # Add habitats to the fish
    new_fish.habitats.extend([habitat1, habitat2])

    # Add the new fish (with habitats) to the session and commit
    db.add(new_fish)
    try:
        db.commit()
        return new_fish
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={"message": str(e)}
        )