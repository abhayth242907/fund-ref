from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.legal_entity import (
    LegalEntity,
    LegalEntityCreate,
    LegalEntityUpdate
)
from app.database.connection import Neo4jConnection
from app.config import get_db

router = APIRouter(prefix="/legal-entities", tags=["legal-entities"])

@router.get("/", response_model=List[LegalEntity])
async def list_legal_entities(
    skip: int = 0,
    limit: int = 10,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (le:LegalEntity)
    RETURN le {.*} as legal_entity
    SKIP $skip
    LIMIT $limit
    """
    result = db.execute_query(query, {"skip": skip, "limit": limit})
    return [r["legal_entity"] for r in result]

@router.get("/{legal_entity_id}", response_model=LegalEntity)
async def get_legal_entity(
    legal_entity_id: str,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (le:LegalEntity {id: $legal_entity_id})
    RETURN le {.*} as legal_entity
    """
    result = db.execute_query(query, {"legal_entity_id": legal_entity_id})
    if not result:
        raise HTTPException(status_code=404, detail="Legal entity not found")
    return result[0]["legal_entity"]

@router.post("/", response_model=LegalEntity)
async def create_legal_entity(
    legal_entity: LegalEntityCreate,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    CREATE (le:LegalEntity)
    SET le = $legal_entity_data,
        le.created_at = datetime(),
        le.id = randomUUID()
    RETURN le {.*} as legal_entity
    """
    result = db.execute_query(query, {
        "legal_entity_data": legal_entity.model_dump()
    })
    return result[0]["legal_entity"]

@router.put("/{legal_entity_id}", response_model=LegalEntity)
async def update_legal_entity(
    legal_entity_id: str,
    legal_entity: LegalEntityUpdate,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (le:LegalEntity {id: $legal_entity_id})
    SET le += $legal_entity_data,
        le.updated_at = datetime()
    RETURN le {.*} as legal_entity
    """
    result = db.execute_query(query, {
        "legal_entity_id": legal_entity_id,
        "legal_entity_data": legal_entity.model_dump(exclude_unset=True)
    })
    if not result:
        raise HTTPException(status_code=404, detail="Legal entity not found")
    return result[0]["legal_entity"]

@router.delete("/{legal_entity_id}")
async def delete_legal_entity(
    legal_entity_id: str,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (le:LegalEntity {id: $legal_entity_id})
    DELETE le
    RETURN count(le) as deleted
    """
    result = db.execute_query(query, {"legal_entity_id": legal_entity_id})
    if result[0]["deleted"] == 0:
        raise HTTPException(status_code=404, detail="Legal entity not found")
    return {"message": "Legal entity deleted successfully"}