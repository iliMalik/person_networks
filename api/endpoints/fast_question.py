# api/endpoints/question.py
from typing import List
from fastapi import APIRouter, HTTPException
from models.pyd_models import Question
from db.queries.query_questions import questions_get_all

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


@router.get("/", response_model=List[Question])
async def fetch_all_questions():
    try:
        return questions_get_all()
    except Exception as e:
        print("Exception caught in endpoint:", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch questions: {str(e)}")