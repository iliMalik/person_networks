from typing import Dict, List
from db.graph_driver import neo4j_driver
from models.pyd_models import Organization




def organization_get_all() -> List[Organization]:
    query = """MATCH (o:Organization) RETURN o"""
    print("Running organization_get_all")

    with neo4j_driver.get_driver().session() as session:
        result = session.run(query)
        return [Organization(**dict(record["o"])) for record in result]

def get_organizations_by_person_id(person_id: str) -> List[Organization]:
    query = """
    MATCH (p:Person {person_id: $person_id})-[:BELONGS_TO]->(o:Organization)
    RETURN o
    """
    with neo4j_driver.get_driver().session() as session:
        result = session.run(query, person_id=person_id)
        return [Organization(**dict(record["o"])) for record in result]