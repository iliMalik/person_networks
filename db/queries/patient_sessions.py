from datetime import datetime, timezone
from utils.uuid import get_uuid
from fastapi import HTTPException

def get_all_questions(tx, section_id: str = None):
    """
    Fetch all questions; if section_id is given, fetch questions only for that section.
    """
    if section_id:
        query = """
        MATCH (q:Question)-[:PART_OF]->(s:Section {id: $section_id})
        RETURN q ORDER BY q.text
        """
        result = tx.run(query, section_id=section_id)
    else:
        query = """
        MATCH (q:Question)
        RETURN q ORDER BY q.text
        """
        result = tx.run(query)
    return [record["q"] for record in result]

def get_question_by_id(tx, question_id: str):
    """
    Fetch a question node by its UUID.
    """
    query = "MATCH (q:Question {id: $question_id}) RETURN q"
    result = tx.run(query, question_id=question_id)
    return result.single()



def create_assessment_session(tx, person_id: str, responses: dict):
    """
    Create a Session node, link it to the given Person node,
    and connect it to Question nodes with the appropriate relationship
    (ANSWERED_YES or ANSWERED_NO) for each response.

    Args:
    - person_id (str): UUID of the person
    - responses (dict): {question_id: "Yes"/"No"}
    """

    timestamp = datetime.now(timezone.utc).isoformat()
    session_id = str(get_uuid())


    query = "MATCH (p:Person {id: $person_id}) RETURN p.name"
    result = tx.run(query, person_id=person_id)
    record = result.single()
    if not record:
        raise HTTPException(status_code=404, detail="Person not found")

    query2 = "CREATE (s:Session {session_id"

    return "osiodpop"

    # # Step 1: Create session and link to person
    # tx.run("""
    #     MATCH (p:Person {id: $person_id})
    #     CREATE (s:Session {
    #         id: $session_id,
    #         timestamp: $timestamp
    #     })
    #     CREATE (p)-[:CONDUCTED]->(s)
    # """, person_id=person_id, session_id=session_id, timestamp=timestamp)
    #
    # # Step 2: Link session to all questions with YES/NO response
    # for question_id, answer in responses.items():
    #     print(f"question_id={question_id}, answer={answer} ({type(answer)})")
    #     rel_type = "ANSWERED_YES" if answer == "Yes" else "ANSWERED_NO"
    #
    #     tx.run(f"""
    #         MATCH (q:Question {{question_id: $question_id}})
    #         MATCH (s:Session {{id: $session_id}})
    #         CREATE (s)-[:{rel_type}]->(q)
    #     """, question_id=question_id, session_id=session_id)
    #
    # return session_id
