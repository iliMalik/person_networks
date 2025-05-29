from datetime import datetime, timezone

import neo4j

from db.graph_driver import neo4j_driver
from models.pyd_models import Session, SessionCreate
from utils.uuid import get_uuid





def session_add(session: SessionCreate) -> Session:
    query = """
    MATCH (p:Person {person_id: $person_id})
    CREATE (s:Session {session_id: $session_id, person_id:$person_id, session_timestamp: $session_timestamp})
    CREATE (p)-[:CONDUCTED]->(s)
    RETURN s
    
    """
    session_data = session.model_dump()
    session_data["person_id"] = str(session_data["person_id"])
    session_data['session_id'] = get_uuid()
    session_data['session_timestamp'] = datetime.now(timezone.utc)


    with neo4j_driver.get_driver().session() as session:
        result = session.run(query, **session_data)
        record = result.single()
        print(record)
        if record:
            node = record["s"]
            node_data = dict(node.items())
            # Convert neo4j.time.DateTime → datetime.datetime
            if isinstance(node_data["session_timestamp"], neo4j.time.DateTime):
                node_data["session_timestamp"] = node_data["session_timestamp"].to_native()
            return Session(**node_data)
        raise Exception("Failed to create session")


#for deleting all sessions that have no linked questions
def session_delete_unlinked():
    query = """
    MATCH (s:Session) 
    WHERE NOT (s)--(:Question) 
    DELETE s """
    with neo4j_driver.get_driver().session() as session:
        result = session.run(query)
        summary = result.consume()
        print(f"Deleted {summary} sessions with no linked questions")
        return summary.counters.nodes_deleted

# def create_assessment_session(tx, person_id: str, responses: dict):
#     """
#     Create a Session node, link it to the given Person node,
#     and connect it to Question nodes with the appropriate relationship
#     (ANSWERED_YES or ANSWERED_NO) for each response.
#
#     Args:
#     - person_id (str): UUID of the person
#     - responses (dict): {question_id: "Yes"/"No"}
#     """
#
#     timestamp = datetime.now(timezone.utc).isoformat()
#     session_id = str(get_uuid())
#
#
#     query = "MATCH (p:Person {id: $person_id}) RETURN p.name"
#     result = tx.run(query, person_id=person_id)
#     record = result.single()
#     if not record:
#         raise HTTPException(status_code=404, detail="Person not found")
#
#     query2 = "CREATE (s:Session {session_id"
#
#     return "osiodpop"

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
