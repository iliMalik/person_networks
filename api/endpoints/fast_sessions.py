from typing import List

from fastapi import APIRouter, HTTPException
from models.pyd_models import SessionCreate, Session
from db.queries.query_session import session_add, session_delete_unlinked
import asyncio

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
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