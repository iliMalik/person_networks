
from fastapi import APIRouter
from db.drivers import get_driver
from neo4j import Session
from db.queries.questions import fetch_all_questions

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

@app.post("/submit_session/")
async def submit_session(request: Request):
    data = await request.json()
    person_id = data.get("person_id")
    responses = data.get("responses", [])

    if not person_id or not responses:
        return {"error": "person_id and responses are required."}

    session_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    with driver.session() as session:
        def tx_fn(tx):
            # 1. Create Session node
            tx.run(
                """
                CREATE (s:Session {session_id: $session_id, timestamp: $timestamp})
                """,
                session_id=session_id,
                timestamp=timestamp,
            )

            # 2. Connect Person to Session
            tx.run(
                """
                MATCH (p:Person {person_id: $person_id})
                MATCH (s:Session {session_id: $session_id})
                MERGE (p)-[:CONDUCTED]->(s)
                """,
                person_id=person_id,
                session_id=session_id,
            )

            # 3. Loop through responses
            for r in responses:
                question_id = r.get("question_id")
                answer = r.get("answer", "").lower()
                if answer not in ["yes", "no"] or not question_id:
                    continue

                rel_type = "RESPONDED_YES" if answer == "yes" else "RESPONDED_NO"

                tx.run(
                    f"""
                    MATCH (q:Question {{question_id: $question_id}})
                    MATCH (s:Session {{session_id: $session_id}})
                    MERGE (s)-[:{rel_type}]->(q)
                    """,
                    question_id=question_id,
                    session_id=session_id,
                )

        session.write_transaction(tx_fn)

    return {"status": "success", "session_id": session_id}