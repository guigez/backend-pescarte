from typing import List, Optional


from fastapi import APIRouter, Depends, Query

from src.database import get_db, Session
from src.models import UF, Municipality
from src.schemas.lookups import UFSchema, CitySchema


router = APIRouter(prefix='/lookup')


@router.get('/uf', response_model=List[UFSchema])
async def get_states(
        db: Session = Depends(get_db),
        has_community: Optional[bool] = Query(default=None)
):
    if has_community:
        return UF.get_uf_with_communities(db)
    return UF.get_all(db)


@router.get('/cities', response_model=List[CitySchema])
async def get_cities(
        db: Session = Depends(get_db),
        uf: str = Query(),
        has_community: Optional[bool] = Query(default=None)
):
    if has_community:
        return Municipality.get_cities_with_communities(db, uf)

    return Municipality.get_cities_by_uf(db, uf)
