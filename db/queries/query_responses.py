from typing import Dict, List
from neo4j import Session as Neo4jSession
from db.graph_driver import neo4j_driver
from models.pyd_models import Responses

def responses_save(session_id: str, answers: Dict[str, str]) -> None:
    query = """
        MATCH (s:Session {session_id: $session_id})
        MATCH (q:Question {question_id: $question_id})
        MERGE (s)-[r:ANSWERED]->(q)
        SET r.choice = $choice_value
    """

    def save(tx, sess_id: str, ques_id: str, choice_valu: str) -> None:
        tx.run(query, session_id=sess_id, question_id=ques_id, choice_value=choice_valu)
    print(answers.items())

    with neo4j_driver.get_driver().session() as session:
        for question_id, choice_value in answers.items():
            session.write_transaction(save, session_id, question_id, choice_value)

def responses_session_id(session_id: str) -> List[Responses]:
    query = """
    MATCH (s:Session {session_id: $session_id})-[r:ANSWERED]->(q:Question)
    RETURN q.question_id, r.choice AS answer
    ORDER BY q.question_id
    """

    try:
        with neo4j_driver.get_driver().session() as session:
            result = session.run(query, session_id=session_id)
            answers: Dict[str, str] = {}

            for record in result:
                question_id = record["q.question_id"]
                answer = record["answer"]
                answers[question_id] = answer

            if not answers:
                return []

            response = Responses(answers=answers)
            return [response]

    except Exception as e:
        print(f"Error executing query: {e}")
        return []
