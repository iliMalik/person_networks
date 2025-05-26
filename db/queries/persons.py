
from utils.uuid import get_uuid

def fetch_all_persons(tx):
    query = """
        MATCH (p:Person)
        RETURN p.id AS person_id, p.name AS person_name, p.age AS person_age
        ORDER BY p.name
    """
    result = tx.run(query)
    return [{"person_id": record["person_id"],
            "person_name": record["person_name"],
            "age": record["person_age"]} for record in result]


def create_person(tx, name: str, age: int):
    person_id = str(get_uuid())
    tx.run(
        """
        CREATE (p:Person {id: $id, name: $name, age: $age})
        """,
        id=person_id,
        name=name,
        age=age
    )




#
#
# def create_person(tx, name: str, age: int):
#     person_id = str(uuid.uuid4())
#     tx.run(
#         """
#         CREATE (p:Person {id: $id, name: $name, age: $age})
#         """,
#         id=person_id,
#         name=name,
#         age=age
#     )
#
# def find_person(tx, name: str):
#     result = tx.run("MATCH (p:Person {name: $name}) RETURN p", name=name)
#     return result.single()
#
# def delete_person_and_sessions(tx, person_id: str):
#     tx.run(
#         """
#         MATCH (p:Person {id: $id})-[:HAS_SESSION]->(s:Session)
#         DETACH DELETE s
#         DETACH DELETE p
#         """,
#         id=person_id
#     )
