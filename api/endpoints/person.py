

from fastapi import APIRouter
from db.drivers import get_driver
from neo4j import Session
from db.queries.persons import fetch_all_persons, create_person

router = APIRouter(
    prefix="/persons",
    tags=["persons"]
)
driver = get_driver()
@router.get("/", summary="get_all")
async def get_all_persons():

    with driver.session() as session:  # type: Session
        persons = session.execute_read(fetch_all_persons)
    return {"persons": persons}

@router.post("/person/{name}/{age}")
def add_person(name: str, age: int):

    with driver.session() as session:
        session.write_transaction(create_person, name, age)
    return {"message": f"Person {name} added."}


#
# @app.get("/person/{name}")
# def get_person(name: str):
#     with driver.session() as session:
#         record = session.read_transaction(find_person, name)
#         if record:
#             return {"name": record["p"]["name"], "age": record["p"]["age"]}
#         return {"error": "Person not found"}
#
# @app.delete("/person/{person_id}")
# def remove_person_and_sessions(person_id: str):
#     with driver.session() as session:
#         session.write_transaction(delete_person_and_sessions, person_id)
#     return {"message": f"Person {person_id} and associated sessions deleted."}