from typing import List
from models.pyd_models import Country
from db.graph_driver import neo4j_driver



def country_get_all() -> List[Country]:
    query = """MATCH (c:Country) RETURN c"""
    print("Running country_get_all")

    with neo4j_driver.get_driver().session() as session:
        result = session.run(query)
        return [Country(**dict(record["c"])) for record in result]


def get_countries_by_person_id(person_id: str) -> List[Country]:
    query = """
    MATCH (p:Person {person_id: $person_id})-[:ASSOCIATED_WITH]->(c:Country)
    RETURN c
    """
    with neo4j_driver.get_driver().session() as session:
        result = session.run(query, person_id=person_id)
        return [Country(**dict(record["c"])) for record in result]
