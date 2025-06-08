from typing import List, Dict

from fastapi import APIRouter, HTTPException, Query
from models.pyd_models import PersonCreate, Person
from db.queries.query_person import person_add, persons_get_all, search_person_by_multiple_words, get_person_network
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

@router.get("/search", response_model=List[Dict[str, str]])
async def api_search_person(name: str = Query(..., min_length=1, description="Partial or full person name to search")):
    try:
        results = search_person_by_multiple_words(name)
        return results
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/network")
def fetch_person_network(ids: List[str] = Query(...)):
    results = get_person_network(ids)
    return results