from typing import Dict

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

