from typing import List, Optional

from src.database import get_db, Session


from fastapi import FastAPI, Depends, Query
from starlette.responses import JSONResponse

from src.models.community import Community
from src.models.fish import Fish
from src.models.gear import Gear
from src.models.habitat import Habitat
from src.models.fish_common_name_by_community import FishCommonNameByCommunity
from src.models.suggested_common_names import SuggestedCommonNames, SuggestedCommonNameStatus
from src.schemas import SuggestCommonNameBody, SuggestedCommonNameResponse

app = FastAPI(title='Catalogo Pescarte API', version='0.0.1')


@app.get('/healthcheck')
async def health_check():
    return {"message": "Up and running"}


@app.get('/suggested-common-names', response_model=List[SuggestedCommonNameResponse])
async def get_suggested_common_names(
        db: Session = Depends(get_db),
        status: Optional[SuggestedCommonNameStatus] = Query(None)
):
    # Query the database for all suggested common names
    if status:
        suggested_names = db.query(SuggestedCommonNames).filter(SuggestedCommonNames.status == status.value).all()
    else:
        # Get all suggested names if no status filter is provided
        suggested_names = db.query(SuggestedCommonNames).all()
    return suggested_names


@app.post('/suggested-common-names')
async def suggest_common_name(
        suggestion: SuggestCommonNameBody,
        db: Session = Depends(get_db)
):
    community = db.query(Community).filter(Community.id == suggestion.community_id).first()
    if not community:
        return JSONResponse(
            status_code=404,
            content={"message": "Community not found"}
        )

    suggested_common_name_model = SuggestedCommonNames(
        name=suggestion.name,
        email=suggestion.email,
        suggested_name=suggestion.suggested_name,
        fish_id=suggestion.fish_id,
        community_id=suggestion.community_id
    )
    saved, error = suggested_common_name_model.save(db)

    if saved:
        return suggested_common_name_model
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving task",
                     "detail": error}
        )
