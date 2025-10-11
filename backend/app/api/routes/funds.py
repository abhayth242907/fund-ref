from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.models.fund import Fund, FundCreate, FundUpdate, FundHierarchy
from app.database.connection import Neo4jConnection
from app.config import get_db

router = APIRouter(prefix="/funds", tags=["funds"])

@router.get("/{fund_id}", response_model=Fund)
async def get_fund(fund_id: str, db: Neo4jConnection = Depends(get_db)):
    query = """
    MATCH (f:Fund {id: $fund_id})
    RETURN f {.*} as fund
    """
    result = db.execute_query(query, {"fund_id": fund_id})
    if not result:
        raise HTTPException(status_code=404, detail="Fund not found")
    return result[0]["fund"]

@router.get("/{fund_id}/hierarchy", response_model=FundHierarchy)
async def get_fund_hierarchy(
    fund_id: str, 
    levels: int = 1,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (f:Fund {id: $fund_id})
    OPTIONAL MATCH (f)-[:HAS_SUBFUND*1..$levels]->(sf:Fund)
    OPTIONAL MATCH (f)-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    RETURN f as fund,
           collect(DISTINCT sf) as sub_funds,
           collect(DISTINCT sc) as share_classes
    """
    result = db.execute_query(query, {
        "fund_id": fund_id,
        "levels": levels
    })
    if not result:
        raise HTTPException(status_code=404, detail="Fund not found")
    return result[0]

@router.get("/search/", response_model=List[Fund])
async def search_funds(
    query: Optional[str] = None,
    type: Optional[str] = None,
    limit: int = 10,
    db: Neo4jConnection = Depends(get_db)
):
    cypher_query = """
    MATCH (f:Fund)
    WHERE 
        ($query IS NULL OR f.name CONTAINS $query)
        AND ($type IS NULL OR f.type = $type)
    RETURN f {.*} as fund
    LIMIT $limit
    """
    result = db.execute_query(cypher_query, {
        "query": query,
        "type": type,
        "limit": limit
    })
    return [r["fund"] for r in result]

@router.post("/", response_model=Fund)
async def create_fund(fund: FundCreate, db: Neo4jConnection = Depends(get_db)):
    # First check if management entity exists
    check_query = """
    MATCH (m:ManagementEntity {id: $mgmt_id})
    RETURN m
    """
    result = db.execute_query(check_query, {"mgmt_id": fund.management_entity_id})
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Management entity not found"
        )

    # Create fund
    query = """
    CREATE (f:Fund)
    SET f = $fund_data
    WITH f
    MATCH (m:ManagementEntity {id: $mgmt_id})
    CREATE (m)-[:MANAGES]->(f)
    RETURN f {.*} as fund
    """
    result = db.execute_query(query, {
        "fund_data": fund.model_dump(),
        "mgmt_id": fund.management_entity_id
    })
    return result[0]["fund"]

@router.put("/{fund_id}", response_model=Fund)
async def update_fund(
    fund_id: str,
    fund_update: FundUpdate,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (f:Fund {id: $fund_id})
    SET f += $fund_data
    RETURN f {.*} as fund
    """
    result = db.execute_query(query, {
        "fund_id": fund_id,
        "fund_data": fund_update.model_dump(exclude_unset=True)
    })
    if not result:
        raise HTTPException(status_code=404, detail="Fund not found")
    return result[0]["fund"]