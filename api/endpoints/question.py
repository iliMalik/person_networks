# api/endpoints/question.py

from fastapi import APIRouter
from db.drivers import get_driver
from neo4j import Session
from db.queries.questions import fetch_all_questions

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

@router.get("/", summary="Get all questions from Neo4j")
async def get_all_questions():
    driver = get_driver()
    with driver.session() as session:  # type: Session
        questions = session.execute_read(fetch_all_questions)
    return {"questions": questions}

