from fastapi import APIRouter
from db.drivers import get_driver
from neo4j import Session
from db.queries.patient_sessions import create_assessment_session
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)




class AssessmentSessionRequest(BaseModel):
    person_id: str
    responses: Dict[str, str]

@router.post("/", summary="Create assessment session with responses")
async def create_session(data: AssessmentSessionRequest):
    driver = get_driver()
    try:
        with driver.session() as session:
            session_id = session.execute_write(create_assessment_session, data.person_id, data.responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "session_id": session_id}