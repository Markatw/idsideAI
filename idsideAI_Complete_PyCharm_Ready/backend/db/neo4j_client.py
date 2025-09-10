import os
from dotenv import load_dotenv
from idsideAI_Complete_PyCharm_Ready.backend.compat.optional_deps import neo4j as _neo4j

GraphDatabase = _neo4j.GraphDatabase if _neo4j else None

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "changeme")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def get_session():
    return driver.session()


# Safe guard for driver init
try:
    if GraphDatabase:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    else:
        driver = None
except Exception:
    driver = None
