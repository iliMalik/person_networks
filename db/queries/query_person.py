from enum import Enum
from typing import List

from utils.uuid import get_uuid
from models.pyd_models import PersonCreate, Person
from db.graph_driver import Neo4jDriver


def person_add(person: PersonCreate) -> Person:
    query = """
    CREATE (p:Person {person_id: $person_id, person_age: $person_age, person_first_name: $person_first_name, person_last_name: $person_last_name, person_gender: $person_gender, name: $person_first_name})
    RETURN p
    """
    person_data = person.model_dump()
    person_data["person_id"] = get_uuid()

    # convert enum to string
    if isinstance(person_data.get("person_gender"),Enum) :
        person_data["person_gender"] = person_data["person_gender"].value

    driver = Neo4jDriver()
    with driver.get_driver().session() as session:
        result = session.run(query, **person_data)
        record = result.single()
        if record:
            return Person(**dict(record["p"]))
        raise Exception("Failed to create person")

def persons_get_all() -> List[Person]:
    query = """MATCH (p:Person) RETURN p"""
    driver = Neo4jDriver()
    with driver.get_driver().session() as session:
        result = session.run(query)
        return [Person(**record["p"]) for record in result]





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
