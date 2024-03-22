from typing import List


from fastapi import APIRouter, Depends, Query

from src.database import get_db, Session
from src.models import UF, Municipality
from src.schemas import UFSchema, CitySchema


router = APIRouter(prefix='/lookup')


@router.get('/uf', response_model=List[UFSchema])
async def get_states(
        db: Session = Depends(get_db)
):
    states = db.query(UF).all()
    return states


@router.get('/cities', response_model=List[CitySchema])
async def get_cities(
        db: Session = Depends(get_db),
        uf: str = Query()
):
    cities = db.query(Municipality).filter(Municipality.uf == uf).all()
    return cities
