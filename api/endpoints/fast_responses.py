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
        # Extract only answer values from the nested dict
        flat_answers = {
            question_id: answer_obj["answer"]
            for question_id, answer_obj in request.answers.items()
        }

        responses_save(str(request.session_id), flat_answers)
        return {"message": "Responses saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save responses: {str(e)}")

@router.get("/{session_id}", response_model=List[Responses])
async def screening_by_session(session_id:str):
    try:
        return responses_session_id(session_id)
    except Exception as e:
        print("Exception caught in endpoint:", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch sessions: {str(e)}")