from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse, Response

from src.database import get_db, Session
from src.models import SuggestedCommonNames, Community
from src.models.suggested_common_names import SuggestedCommonNameStatus
from src.schemas.common_name import SuggestCommonNameBody, SuggestedCommonNameResponse, SuggestedNameIdList


router = APIRouter(prefix='/suggested-common-name')


@router.get('/', response_model=List[SuggestedCommonNameResponse])
async def get_suggested_common_names(
        db: Session = Depends(get_db),
        status: Optional[SuggestedCommonNameStatus] = Query(None)
):
    if status:
        suggested_names: List[SuggestedCommonNames] = db.query(SuggestedCommonNames).filter(SuggestedCommonNames.status == status.value).all()
    else:
        suggested_names = db.query(SuggestedCommonNames).all()
    return suggested_names


@router.post('/')
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


@router.post('/approve')
async def approve_suggestions(
        ids: SuggestedNameIdList,
        db: Session = Depends(get_db)
):
    SuggestedCommonNames.update_status(db, ids.ids, SuggestedCommonNameStatus.APPROVED)
    return JSONResponse(
        status_code=200,
        content={"message": "Suggestions approved."}
    )


@router.post('/reject')
async def reject_suggestions(
        ids: SuggestedNameIdList,
        db: Session = Depends(get_db)
):
    SuggestedCommonNames.update_status(db, ids.ids, SuggestedCommonNameStatus.REJECTED)
    return JSONResponse(
        status_code=200,
        content={"message": "Suggestions rejected."}
    )
