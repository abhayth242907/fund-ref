from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.share_class import ShareClass, ShareClassCreate, ShareClassUpdate
from app.database.connection import Neo4jConnection
from app.config import get_db

router = APIRouter(prefix="/funds", tags=["share_classes"])

@router.get("/{fund_id}/share-classes", response_model=List[ShareClass])
async def get_fund_share_classes(fund_id: str, db: Neo4jConnection = Depends(get_db)):
    query = """
    MATCH (f:Fund {id: $fund_id})-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    RETURN sc {.*} as share_class
    """
    result = db.execute_query(query, {"fund_id": fund_id})
    return [r["share_class"] for r in result]

@router.post("/{fund_id}/share-classes", response_model=ShareClass)
async def create_share_class(
    fund_id: str,
    share_class: ShareClassCreate,
    db: Neo4jConnection = Depends(get_db)
):
    # First check if fund exists
    check_query = """
    MATCH (f:Fund {id: $fund_id})
    RETURN f
    """
    result = db.execute_query(check_query, {"fund_id": fund_id})
    if not result:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Create share class
    query = """
    MATCH (f:Fund {id: $fund_id})
    CREATE (sc:ShareClass)
    SET sc = $share_class_data
    CREATE (f)-[:HAS_SHARE_CLASS]->(sc)
    RETURN sc {.*} as share_class
    """
    result = db.execute_query(query, {
        "fund_id": fund_id,
        "share_class_data": share_class.model_dump()
    })
    return result[0]["share_class"]