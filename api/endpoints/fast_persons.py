from typing import List

from fastapi import APIRouter, HTTPException
from models.pyd_models import PersonCreate, Person
from db.queries.query_person import person_add, persons_get_all
import asyncio

router = APIRouter(
    prefix="/persons",
    tags=["Persons"]
)


@router.post("/", response_model=Person)
def create_person(person: PersonCreate):

    try:
        return person_add(person)
    except Exception as e:
        print("Exception caught in endpoint:", e)
        raise HTTPException(status_code=500, detail=f"Failed to add person: {str(e)}")


@router.get("/", response_model=List[Person])
async def fetch_all_persons():
    try:
        return persons_get_all()
    except Exception as e:
        print("Exception caught in endpoint:", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch persons: {str(e)}")


