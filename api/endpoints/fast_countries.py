from typing import List

from fastapi import APIRouter, HTTPException
from models.pyd_models import Country
from db.queries.query_countries import country_get_all

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