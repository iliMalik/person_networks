from typing import List

from fastapi import APIRouter, HTTPException
from models.pyd_models import Country
from db.queries.query_countries import country_get_all, get_countries_by_person_id

router = APIRouter(
    prefix="/countries",
    tags=["Countries"]
)

@router.get("/", response_model=List[Country])
async def api_country_get_all():
    try:
        return country_get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{person_id}", response_model=List[Country])
async def api_get_organizations_by_person_id(person_id: str):
    try:
        countries = get_countries_by_person_id(person_id)
        if not countries:
            raise HTTPException(status_code=404, detail="No countries found for this person_id")
        return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))