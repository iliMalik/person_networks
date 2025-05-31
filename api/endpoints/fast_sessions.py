from typing import List

from fastapi import APIRouter, HTTPException
from models.pyd_models import SessionCreate, Session
from db.queries.query_session import session_add, session_delete_unlinked, sessions_by_pid


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


@router.post("/", response_model=Session)
def create_session(session: SessionCreate):

    try:
        return session_add(session)
    except Exception as e:
        print("Exception caught in endpoint:", e)
        raise HTTPException(status_code=500, detail=f"Failed to add person: {str(e)}")

@router.delete("/", status_code=200)
def delete_unlinked_sessions():
    try:
        return session_delete_unlinked()
    except Exception as e:
        print("Exception caught in endpoint:", e)
        raise HTTPException(status_code=500, detail=f"Failed to delete sessions: {str(e)}")

@router.get("/{person_id}", response_model=List[Session])
async def sessions_person(person_id:str):
    try:
        return sessions_by_pid(person_id)
    except Exception as e:
        print("Exception caught in endpoint:", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch sessions: {str(e)}")