from src.database import get_db, Session


from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from src.models.fish import Fish

app = FastAPI(title='Catalogo Pescarte API', version='0.0.1')


@app.get('/healthcheck')
async def health_check():
    return {"message": "Up and running"}


@app.post('/teste')
async def test_endpoint(db: Session = Depends(get_db)):
    fish_model = Fish(scientific_name="Salmo salar", native=True)
    saved, error = fish_model.save(db)
    if saved:
        return fish_model
    else:
        return JSONResponse(
            status_code=400,
            content={"message": error}
        )
