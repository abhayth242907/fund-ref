from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from app.database.connection import get_db

router = APIRouter(prefix="/funds", tags=["funds"])

@router.get("/search")
async def search_funds(
    fund_code: Optional[str] = Query(None),
    fund_id: Optional[str] = Query(None),
    isin: Optional[str] = Query(None),
    fund_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    mgmt_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db = Depends(get_db)
) -> Dict[str, Any]:
    """Search funds with filters"""
    
    where_clauses = []
    params = {}
    
    if fund_code:
        where_clauses.append("f.fund_code CONTAINS $fund_code")
        params['fund_code'] = fund_code
    
    if fund_id:
        where_clauses.append("f.fund_id = $fund_id")
        params['fund_id'] = fund_id
    
    if isin:
        where_clauses.append("f.isin_master CONTAINS $isin")
        params['isin'] = isin
    
    if fund_type:
        where_clauses.append("f.fund_type = $fund_type")
        params['fund_type'] = fund_type
    
    if status:
        where_clauses.append("f.status = $status")
        params['status'] = status
    
    if mgmt_id:
        where_clauses.append("f.mgmt_id = $mgmt_id")
        params['mgmt_id'] = mgmt_id
    
    where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Calculate skip
    skip = (page - 1) * page_size
    params['skip'] = skip
    params['limit'] = page_size
    
    # Get total count
    count_query = f"""
    MATCH (f:Fund)
    WHERE {where_clause}
    RETURN count(f) as total
    """
    
    count_result = db.run(count_query, **params)
    total = count_result.single()['total']
    
    # Get data
    query = f"""
    MATCH (f:Fund)
    WHERE {where_clause}
    OPTIONAL MATCH (f)-[:MANAGED_BY]->(m:ManagementEntity)
    RETURN f, m
    ORDER BY f.fund_id
    SKIP $skip
    LIMIT $limit
    """
    
    result = db.run(query, **params)
    
    funds = []
    for record in result:
        fund = dict(record['f'])
        fund['management_entity'] = dict(record['m']) if record['m'] else None
        funds.append(fund)
    
    return {
        'funds': funds,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }

@router.get("/")
async def list_funds(skip: int = 0, limit: int = 10, db = Depends(get_db)) -> List[Dict[str, Any]]:
    """List all funds"""
    query = """
    MATCH (f:Fund)
    OPTIONAL MATCH (f)-[:MANAGED_BY]->(m:ManagementEntity)
    RETURN f, m
    ORDER BY f.fund_id
    SKIP $skip
    LIMIT $limit
    """
    
    result = db.run(query, skip=skip, limit=limit)
    
    funds = []
    for record in result:
        fund = dict(record['f'])
        fund['management_entity'] = dict(record['m']) if record['m'] else None
        funds.append(fund)
    
    return funds

@router.get("/code/{fund_code}")
async def get_fund_by_code(fund_code: str, db = Depends(get_db)) -> Dict[str, Any]:
    """Get fund by fund code"""
    query = """
    MATCH (f:Fund {fund_code: $fund_code})
    OPTIONAL MATCH (f)-[:MANAGED_BY]->(m:ManagementEntity)
    OPTIONAL MATCH (f)-[:HAS_LEGAL_ENTITY]->(le:LegalEntity)
    OPTIONAL MATCH (f)-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    OPTIONAL MATCH (sf:SubFund)-[:PARENT_FUND]->(f)
    RETURN f, m, le, collect(DISTINCT sc) as share_classes, collect(DISTINCT sf) as subfunds
    """
    
    result = db.run(query, fund_code=fund_code)
    record = result.single()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Fund with code {fund_code} not found")
    
    fund = dict(record['f'])
    fund['management_entity'] = dict(record['m']) if record['m'] else None
    fund['legal_entity'] = dict(record['le']) if record['le'] else None
    fund['share_classes'] = [dict(sc) for sc in record['share_classes'] if sc]
    fund['subfunds'] = [dict(sf) for sf in record['subfunds'] if sf]
    
    return fund

@router.get("/{fund_id}/hierarchy/children")
async def get_fund_hierarchy_children(fund_id: str, depth: int = 1, db = Depends(get_db)) -> Dict[str, Any]:
    """Get fund hierarchy - children (subfunds)"""
    query = f"""
    MATCH (f:Fund {{fund_id: $fund_id}})
    OPTIONAL MATCH path = (f)<-[:PARENT_FUND*1..{depth}]-(sf:SubFund)
    WITH f, collect(DISTINCT {{
        subfund: sf,
        depth: length(path)
    }}) as subfunds_with_depth
    OPTIONAL MATCH (f)-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    RETURN f, subfunds_with_depth, collect(DISTINCT sc) as share_classes
    """
    
    result = db.run(query, fund_id=fund_id)
    record = result.single()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Fund with ID {fund_id} not found")
    
    fund = dict(record['f'])
    subfunds = []
    
    for item in record['subfunds_with_depth']:
        if item['subfund']:
            subfund_data = dict(item['subfund'])
            subfund_data['depth'] = item['depth']
            subfunds.append(subfund_data)
    
    fund['share_classes'] = [dict(sc) for sc in record['share_classes'] if sc]
    
    return {
        'root': fund,
        'children': subfunds,
        'depth': depth
    }

@router.get("/{fund_id}")
async def get_fund(fund_id: str, db = Depends(get_db)) -> Dict[str, Any]:
    """Get fund by ID"""
    query = """
    MATCH (f:Fund {fund_id: $fund_id})
    OPTIONAL MATCH (f)-[:MANAGED_BY]->(m:ManagementEntity)
    OPTIONAL MATCH (f)-[:HAS_LEGAL_ENTITY]->(le:LegalEntity)
    OPTIONAL MATCH (f)-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    OPTIONAL MATCH (sf:SubFund)-[:PARENT_FUND]->(f)
    RETURN f, m, le, collect(DISTINCT sc) as share_classes, collect(DISTINCT sf) as subfunds
    """
    
    result = db.run(query, fund_id=fund_id)
    record = result.single()
    
    if not record:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    fund = dict(record['f'])
    fund['management_entity'] = dict(record['m']) if record['m'] else None
    fund['legal_entity'] = dict(record['le']) if record['le'] else None
    fund['share_classes'] = [dict(sc) for sc in record['share_classes'] if sc]
    fund['subfunds'] = [dict(sf) for sf in record['subfunds'] if sf]
    
    return fund