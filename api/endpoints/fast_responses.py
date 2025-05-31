from typing import List

from fastapi import APIRouter, HTTPException
from models.pyd_models import ResponsesSave, Responses
from db.queries.query_responses import responses_save, responses_session_id


router = APIRouter(
    prefix="/responses",
    tags=["Responses"]
)


@router.post("/")
async def save_session_responses(request: ResponsesSave):
    try:
        responses_save(request.session_id, request.answers)
        return {"message": "Responses saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save responses: {str(e)}")

@router.get("/{session_id}", response_model=List[Responses])
async def get_session_responses(session_id: str):
    responses = responses_session_id(session_id)
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found for given session_id")
    return responses