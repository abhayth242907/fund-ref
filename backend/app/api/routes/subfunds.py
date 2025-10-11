from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.subfund import (
    SubFund,
    SubFundCreate,
    SubFundUpdate,
    SubFundDetail
)
from app.database.connection import Neo4jConnection
from app.config import get_db

router = APIRouter(prefix="/subfunds", tags=["subfunds"])

@router.get("/", response_model=List[SubFundDetail])
async def list_subfunds(
    skip: int = 0,
    limit: int = 10,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (sf:SubFund)-[:BELONGS_TO]->(f:Fund)
    OPTIONAL MATCH (sf)-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    WITH sf, f, count(sc) as total_share_classes
    RETURN sf {
        .*,
        master_fund_name: f.name,
        total_share_classes: total_share_classes
    } as subfund
    SKIP $skip
    LIMIT $limit
    """
    result = db.execute_query(query, {"skip": skip, "limit": limit})
    return [r["subfund"] for r in result]

@router.get("/{subfund_id}", response_model=SubFundDetail)
async def get_subfund(subfund_id: str, db: Neo4jConnection = Depends(get_db)):
    query = """
    MATCH (sf:SubFund {id: $subfund_id})-[:BELONGS_TO]->(f:Fund)
    OPTIONAL MATCH (sf)-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    WITH sf, f, count(sc) as total_share_classes
    RETURN sf {
        .*,
        master_fund_name: f.name,
        total_share_classes: total_share_classes
    } as subfund
    """
    result = db.execute_query(query, {"subfund_id": subfund_id})
    if not result:
        raise HTTPException(status_code=404, detail="Sub-fund not found")
    return result[0]["subfund"]

@router.post("/", response_model=SubFund)
async def create_subfund(subfund: SubFundCreate, db: Neo4jConnection = Depends(get_db)):
    # Check if master fund exists
    check_query = """
    MATCH (f:Fund {id: $master_fund_id})
    RETURN f
    """
    result = db.execute_query(check_query, {"master_fund_id": subfund.master_fund_id})
    if not result:
        raise HTTPException(status_code=404, detail="Master fund not found")

    # Create subfund
    query = """
    MATCH (f:Fund {id: $master_fund_id})
    CREATE (sf:SubFund)
    SET sf = $subfund_data,
        sf.created_at = datetime(),
        sf.id = randomUUID()
    CREATE (sf)-[:BELONGS_TO]->(f)
    RETURN sf {.*} as subfund
    """
    result = db.execute_query(query, {
        "master_fund_id": subfund.master_fund_id,
        "subfund_data": subfund.model_dump(exclude={'master_fund_id'})
    })
    return result[0]["subfund"]

@router.put("/{subfund_id}", response_model=SubFund)
async def update_subfund(
    subfund_id: str,
    subfund: SubFundUpdate,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (sf:SubFund {id: $subfund_id})
    SET sf += $subfund_data,
        sf.updated_at = datetime()
    RETURN sf {.*} as subfund
    """
    result = db.execute_query(query, {
        "subfund_id": subfund_id,
        "subfund_data": subfund.model_dump(exclude_unset=True)
    })
    if not result:
        raise HTTPException(status_code=404, detail="Sub-fund not found")
    return result[0]["subfund"]

@router.get("/{subfund_id}/share-classes", response_model=List['ShareClass'])
async def get_subfund_share_classes(
    subfund_id: str,
    db: Neo4jConnection = Depends(get_db)
):
    query = """
    MATCH (sf:SubFund {id: $subfund_id})-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    RETURN sc {.*} as share_class
    """
    result = db.execute_query(query, {"subfund_id": subfund_id})
    return [r["share_class"] for r in result]