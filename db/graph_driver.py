from neo4j import GraphDatabase

from dotenv import load_dotenv

import os

load_dotenv()

NEO4J_BOLT_URL = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Validate environment variables
if not all([NEO4J_BOLT_URL, NEO4J_USERNAME, NEO4J_PASSWORD]):
    raise ValueError("Missing Neo4j environment variables: NEO4J_URI, NEO4J_USERNAME, or NEO4J_PASSWORD")

# Initialize Neo4j driver
try:
    driver = GraphDatabase.driver(NEO4J_BOLT_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
except Exception as e:
    raise ValueError(f"Failed to connect to Neo4j. {e}")

class Neo4jDriver:
    def __init__(self):
        self.driver = driver

    def get_driver(self):
        return self.driver
    def close(self):
        self.driver.close()





