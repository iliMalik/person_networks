from typing import Dict, List
from uuid import UUID

from models.pyd_models import Responses
from db.graph_driver import neo4j_driver


def responses_save(session_id: str, answers: Dict[str, str]) -> None:
    query = """
        MATCH (s:Session {session_id: $session_id})
        MATCH (q:Question {question_id: $question_id})
        MERGE (s)-[r:ANSWERED]->(q)
        SET r.choice = $choice_value
    """

    def save(tx, session_id: str, question_id: str, choice_value: str) -> None:
        tx.run(query, session_id=session_id, question_id=question_id, choice_value=choice_value)

    with neo4j_driver.get_driver().session() as session:
        for question_id, choice_value in answers.items():
            session.write_transaction(save, session_id, question_id, choice_value)


def responses_session_id(session_id: str) -> List[Responses]:
    query = """
MATCH (s:Session {session_id: $session_id})-[r:ANSWERED]->(q:Question)
RETURN q.question_id, q.question_text, r.choice AS answer
ORDER BY q.question_id
"""

    try:
        with neo4j_driver.get_driver().session() as session:
            result = session.run(query, session_id=session_id)
            # Initialize answers dictionary
            answers: Dict[str, Dict[str, str]] = {}

            # Collect all answers for the session
            for record in result:
                question_id = record["q.question_id"]
                question_text = record["q.question_text"]
                answer = record["answer"]
                answers[question_id]={
                    "answer": answer,
                    "question_text": question_text
                }
            if not answers:
                print(f"No responses found for session_id: {session_id}")
                return []

            # Create Responses object
            response = Responses(answers=answers)
            return [response]

    except Exception as e:
        print(f"Error executing query: {e}")
        return []

