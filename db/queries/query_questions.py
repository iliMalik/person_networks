from typing import List
from models.pyd_models import Question
from db.graph_driver import Neo4jDriver


def questions_get_all() -> List[Question]:
    query = """
            MATCH (q:Question)
            RETURN q.question_id AS question_id, q.question_text AS question_text
            ORDER BY q.text
        """
    driver = Neo4jDriver()
    with driver.get_driver().session() as session:
        result = session.run(query)
        return [Question(question_id=record["question_id"], question_text=record["question_text"]) for record in result]