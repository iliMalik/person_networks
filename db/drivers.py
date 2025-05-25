from neo4j import GraphDatabase

from dotenv import load_dotenv

import os

load_dotenv()

NEO4J_BOLT_URL = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_BOLT_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def get_driver():
    return driver


