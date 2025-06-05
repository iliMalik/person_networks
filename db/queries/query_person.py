from enum import Enum
from typing import List

from utils.uuid import get_uuid
from models.pyd_models import PersonCreate, Person
from db.graph_driver import neo4j_driver



def person_add(person: PersonCreate) -> Person:
    query = """
    CREATE (p:Person {person_id: $person_id, person_name: $person_name, person_phone: $person_phone})
    RETURN p
    """
    person_data = person.model_dump()
    person_data["person_id"] = get_uuid()

    with neo4j_driver.get_driver().session() as session:
        result = session.run(query, **person_data)
        record = result.single()
        if record:
            return Person(**dict(record["p"]))
        raise Exception("Failed to create person")

def persons_get_all() -> List[Person]:
    query = """MATCH (p:Person) RETURN p"""
    print("Running persons_get_all")

    with neo4j_driver.get_driver().session() as session:
        result = session.run(query)
        return [Person(**dict(record["p"])) for record in result]

