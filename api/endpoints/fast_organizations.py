from typing import List

from fastapi import APIRouter, HTTPException
from models.pyd_models import Organization
from db.queries.query_organizations import organization_get_all, get_organizations_by_person_id


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"]
)


@router.get("/", response_model=List[Organization])
async def api_organization_get_all():
    try:
        return organization_get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{person_id}", response_model=List[Organization])
async def api_get_organizations_by_person_id(person_id: str):
    try:
        organizations = get_organizations_by_person_id(person_id)
        if not organizations:
            raise HTTPException(status_code=404, detail="No organizations found for this person_id")
        return organizations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))