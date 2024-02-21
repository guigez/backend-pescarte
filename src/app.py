from src.database import get_db, Session


from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from src.models.community import Community

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
