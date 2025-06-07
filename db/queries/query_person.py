from enum import Enum
from typing import List, Dict

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



def search_person_by_multiple_words(name: str) -> List[Dict[str, str]]:
    words = [w.strip() for w in name.split() if w.strip()]
    if not words:
        return []

    where_clauses = " AND ".join(
        [f"toLower(p.person_name) CONTAINS toLower($word{i})" for i in range(len(words))]
    )

    query = f"""
    MATCH (p:Person)
    WHERE {where_clauses}
    RETURN p.person_id AS id, p.person_name AS label
    LIMIT 20
    """

    params = {f"word{i}": word for i, word in enumerate(words)}

    results = []
    with neo4j_driver.get_driver().session() as session:
        result = session.run(query, **params)
        for record in result:
            results.append({
                "id": str(record["id"]),
                "label": record["label"]
            })
    return results