
from fastapi import APIRouter, HTTPException
from models.pyd_models import Responses
from db.queries.query_responses import responses_save


router = APIRouter(
    prefix="/responses",
    tags=["responses"]
)


@router.post("/")
async def save_session_responses(request: Responses):
    try:
        responses_save(str(request.session_id), request.answers)
        return {"message": "Responses saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save responses: {str(e)}")

