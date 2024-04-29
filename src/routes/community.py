from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse, Response

from src.database import get_db, Session
from src.models import Community
from src.schemas.errors import ErrorMessage
from src.schemas.community import CommunityInput, CommunityPatchInput, CommunityOutput, CommunityOutputWithStateAndCity

router = APIRouter(prefix='/community')


@router.get('/', response_model=List[CommunityOutputWithStateAndCity])
async def get_all_communities(
    db: Session = Depends(get_db),
    municipality_id: Optional[UUID] = Query(default=None)
):
    if municipality_id:
        communities = Community.get_by_municipality_id(db, municipality_id)
    else:
        communities = Community.get_all(db)

    response = list()

    for community in communities:
        community_city = community.municipality
        community_uf = community_city.uf_rel

        community_resp = CommunityOutputWithStateAndCity(
            id=community.id,
            name=community.name,
            description=community.description,
            municipality_id=community.municipality_id,
            municipality=community_city.name,
            uf=community_uf.uf_name
        )
        response.append(community_resp)

    return response


@router.get('/{community_id}', response_model=CommunityOutputWithStateAndCity, responses={404: {'model': ErrorMessage}})
async def get_community(
        community_id: UUID,
        db: Session = Depends(get_db)
):
    community = Community.get_by_id(db, community_id)

    if not community:
        return JSONResponse(
            status_code=404,
            content={"message": "Community not found"}
        )

    community_city = community.municipality
    community_uf = community_city.uf_rel

    response = CommunityOutputWithStateAndCity(
        id=community.id,
        name=community.name,
        description=community.description,
        municipality_id=community.municipality_id,
        municipality=community_city.name,
        uf=community_uf.uf_name
    )
    return response


@router.post('/', response_model=CommunityOutput)
async def create_community(
        community: CommunityInput,
        db: Session = Depends(get_db)
):
    community_model = Community(**community.dict())
    saved, error = community_model.save(db)

    if saved:
        return saved
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving community",
                     "detail": error}
        )


@router.patch('/{community_id}', response_model=CommunityOutput, responses={404: {'model': ErrorMessage}})
async def update_community(
        community_id: UUID,
        community_payload: CommunityPatchInput,
        db: Session = Depends(get_db)
):
    community = Community.get_by_id(db, community_id)

    if not community:
        return JSONResponse(
            status_code=404,
            content={"message": "community not found"}
        )

    updated, error = community.update(db, community_payload.dict(exclude_none=True))

    if updated:
        return updated
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating community",
                     "detail": error}
        )


@router.delete('/{community_id}', status_code=204, response_class=Response, responses={404: {'model': ErrorMessage}})
async def delete_community(
        community_id: UUID,
        db: Session = Depends(get_db)
):
    community = Community.get_by_id(db, community_id)

    if not community:
        return JSONResponse(
            status_code=404,
            content={"message": "Community not found"}
        )

    deleted, error = community.delete(db)

    if deleted:
        return None
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating community",
                     "detail": error}
        )
