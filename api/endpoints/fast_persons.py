

from fastapi import APIRouter, HTTPException
from models.pyd_models import PersonCreate, Person
from db.queries.query_person import person_add
import asyncio

router = APIRouter(
    prefix="/persons",
    tags=["persons"]
)


@router.post("/", response_model=Person)
def create_person(person: PersonCreate):

    try:
        return person_add(person)
    except Exception as e:
        print("Exception caught in endpoint:", e)
        raise HTTPException(status_code=500, detail=str(e))



