from datetime import datetime, timezone
from typing import List

import neo4j

from db.graph_driver import neo4j_driver
from models.pyd_models import Session, SessionCreate
from utils.uuid import get_uuid





def session_add(session: SessionCreate) -> Session:
    query = """
    MATCH (p:Person {person_id: $person_id})
    CREATE (s:Session {session_id: $session_id, person_id:$person_id, session_date: $session_date})
    CREATE (p)-[:CONDUCTED]->(s)
    RETURN s
    
    """
    session_data = session.model_dump()
    session_data["person_id"] = str(session_data["person_id"])
    session_data['session_id'] = get_uuid()
    session_data['session_date'] = datetime.now(timezone.utc)


    with neo4j_driver.get_driver().session() as session:
        result = session.run(query, **session_data)
        record = result.single()
        print(record)
        if record:
            node = record["s"]
            node_data = dict(node.items())
            # Convert neo4j.time.DateTime → datetime.datetime
            if isinstance(node_data["session_date"], neo4j.time.DateTime):
                node_data["session_date"] = node_data["session_date"].to_native()
            return Session(**node_data)
        raise Exception("Failed to create session")


#for deleting all sessions that have no linked questions
def session_delete_unlinked():
    query = """
    MATCH (s:Session) 
    WHERE NOT (s)--(:Question) 
    DETACH DELETE s """
    with neo4j_driver.get_driver().session() as session:
        result = session.run(query)
        summary = result.consume()
        print(f"Deleted {summary} sessions with no linked questions")
        return summary.counters.nodes_deleted


def sessions_by_pid(person_id: str) -> List[Session]:
    query = """
        MATCH (p:Person {person_id: $person_id})-[:CONDUCTED]->(s:Session)
        RETURN s
    """
    print(f"Running sessions query for person_id: {person_id}")

    with neo4j_driver.get_driver().session() as session:
        result = session.run(query, person_id=person_id)
        sessions = []
        for record in result:
            session_data = dict(record["s"])
            # Convert neo4j.time.DateTime to Python datetime
            if "session_date" in session_data and isinstance(session_data["session_date"], neo4j.time.DateTime):
                session_data["session_date"] = session_data["session_date"].to_native()
            sessions.append(Session(**session_data))
        return sessions