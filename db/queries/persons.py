

def create_person(tx, name: str, age: int):
    person_id = str(uuid.uuid4())
    tx.run(
        """
        CREATE (p:Person {id: $id, name: $name, age: $age})
        """,
        id=person_id,
        name=name,
        age=age
    )

def find_person(tx, name: str):
    result = tx.run("MATCH (p:Person {name: $name}) RETURN p", name=name)
    return result.single()

def delete_person_and_sessions(tx, person_id: str):
    tx.run(
        """
        MATCH (p:Person {id: $id})-[:HAS_SESSION]->(s:Session)
        DETACH DELETE s
        DETACH DELETE p
        """,
        id=person_id
    )
