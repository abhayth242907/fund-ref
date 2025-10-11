from functools import lru_cache
from pydantic_settings import BaseSettings
from app.database.connection import Neo4jConnection

class Settings(BaseSettings):
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "hackathon2023"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

def get_db():
    settings = get_settings()
    db = Neo4jConnection(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password
    )
    try:
        yield db
    finally:
        db.close()