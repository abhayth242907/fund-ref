from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

logger = logging.getLogger(__name__)
from app.models.management import (
    ManagementEntity,
    ManagementEntityCreate,
    ManagementEntityUpdate,
    ManagementEntityResponse
)
from app.database.connection import Neo4jConnection
from app.config import get_db

router = APIRouter(prefix="/management", tags=["management"])

@router.post("/", response_model=ManagementEntityResponse)
async def create_management_entity(
    entity: ManagementEntityCreate,
    db: Neo4jConnection = Depends(get_db)
):
    try:
        query = """
        CREATE (m:ManagementEntity)
        SET m = $entity_data,
            m.created_at = datetime(),
            m.id = randomUUID()
        RETURN m {.*} as management
        """
        result = db.execute_query(query, {
            "entity_data": entity.model_dump()
        })
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to create management entity: No result returned"
            )
        return result[0]["management"]
    except Exception as e:
        logger.error(f"Failed to create management entity: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create management entity: {str(e)}"
        )

@router.get("/", response_model=List[ManagementEntityResponse])
async def list_management_entities(db: Neo4jConnection = Depends(get_db)):
    query = """
    MATCH (m:ManagementEntity)
    OPTIONAL MATCH (m)-[:MANAGES]->(f:Fund)
    WITH m, count(f) as total_funds
    RETURN m {.*, total_funds: total_funds} as management
    """
    result = db.execute_query(query)
    return [r["management"] for r in result]

@router.get("/{mgmt_id}/funds", response_model=List[ManagementEntityResponse])
async def get_management_funds(mgmt_id: str, db: Neo4jConnection = Depends(get_db)):
    query = """
    MATCH (m:ManagementEntity {id: $mgmt_id})-[:MANAGES]->(f:Fund)
    RETURN f {.*} as fund
    """
    result = db.execute_query(query, {"mgmt_id": mgmt_id})
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Management entity not found or has no funds"
        )
    return [r["fund"] for r in result]