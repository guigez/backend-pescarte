
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from src.routes.community import router as community_router
from src.routes.fish import router as fish_router
from src.routes.gear import router as gear_router
from src.routes.habitat import router as habitat_router
from src.routes.lookup import router as lookup_router
from src.routes.suggested_common_names import router as suggested_names_router


app = FastAPI(title='Catalogo Pescarte API', version='0.0.1')

app.include_router(community_router, tags=["Community"])
app.include_router(fish_router, tags=["Fish"])
app.include_router(gear_router, tags=["Gear"])
app.include_router(habitat_router, tags=["Habitat"])
app.include_router(lookup_router, tags=["Lookups"])
app.include_router(suggested_names_router, tags=["SuggestedNames"])


origins = [
    "*",
]

# Adicione o middleware CORS à sua aplicação FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/healthcheck')
async def health_check():
    return {"message": "Up and running"}
