from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from app.database.connection import get_db

router = APIRouter(prefix="/subfunds", tags=["subfunds"])

@router.get("/search")
async def search_subfunds(
    subfund_id: Optional[str] = Query(None),
    currency: Optional[str] = Query(None),
    fund_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db = Depends(get_db)
) -> Dict[str, Any]:
    """Search subfunds with filters"""
    
    where_clauses = []
    params = {}
    
    if subfund_id:
        where_clauses.append("sf.subfund_id CONTAINS $subfund_id")
        params['subfund_id'] = subfund_id
    
    if currency:
        where_clauses.append("sf.currency = $currency")
        params['currency'] = currency
    
    if fund_id:
        where_clauses.append("f.fund_id = $fund_id")
        params['fund_id'] = fund_id
    
    where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Calculate skip
    skip = (page - 1) * page_size
    params['skip'] = skip
    params['limit'] = page_size
    
    # Get total count
    count_query = f"""
    MATCH (sf:SubFund)
    OPTIONAL MATCH (sf)-[:PARENT_FUND]->(f:Fund)
    WHERE {where_clause}
    RETURN count(sf) as total
    """
    
    count_result = db.run(count_query, **params)
    total = count_result.single()['total']
    
    # Get data
    query = f"""
    MATCH (sf:SubFund)
    OPTIONAL MATCH (sf)-[:PARENT_FUND]->(f:Fund)
    WHERE {where_clause}
    RETURN sf, f
    ORDER BY sf.subfund_id
    SKIP $skip
    LIMIT $limit
    """
    
    result = db.run(query, **params)
    
    subfunds = []
    for record in result:
        subfund = dict(record['sf'])
        subfund['parent_fund'] = dict(record['f']) if record['f'] else None
        subfunds.append(subfund)
    
    return {
        'subfunds': subfunds,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }

@router.get("/")
async def list_subfunds(
    skip: int = 0,
    limit: int = 10,
    db = Depends(get_db)
) -> List[Dict[str, Any]]:
    """List all subfunds"""
    query = """
    MATCH (sf:SubFund)
    OPTIONAL MATCH (sf)-[:PARENT_FUND]->(f:Fund)
    RETURN sf, f
    ORDER BY sf.subfund_id
    SKIP $skip
    LIMIT $limit
    """
    
    result = db.run(query, skip=skip, limit=limit)
    
    subfunds = []
    for record in result:
        subfund = dict(record['sf'])
        subfund['parent_fund'] = dict(record['f']) if record['f'] else None
        subfunds.append(subfund)
    
    return subfunds

@router.get("/{subfund_id}")
async def get_subfund(subfund_id: str, db = Depends(get_db)) -> Dict[str, Any]:
    """Get subfund by ID with full details"""
    query = """
    MATCH (sf:SubFund {subfund_id: $subfund_id})
    OPTIONAL MATCH (sf)-[:PARENT_FUND]->(f:Fund)
    OPTIONAL MATCH (f)-[:MANAGED_BY]->(m:ManagementEntity)
    OPTIONAL MATCH (sf)-[:HAS_SHARE_CLASS]->(sc:ShareClass)
    RETURN sf, f, m, collect(DISTINCT sc) as share_classes
    """
    
    result = db.run(query, subfund_id=subfund_id)
    record = result.single()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"SubFund with ID {subfund_id} not found")
    
    subfund = dict(record['sf'])
    subfund['parent_fund'] = dict(record['f']) if record['f'] else None
    subfund['management_entity'] = dict(record['m']) if record['m'] else None
    subfund['share_classes'] = [dict(sc) for sc in record['share_classes'] if sc]
    
    return subfund

@router.get("/{subfund_id}/children")
async def get_subfund_children(subfund_id: str, db = Depends(get_db)) -> Dict[str, Any]:
    """Get child subfunds"""
    query = """
    MATCH (sf:SubFund {subfund_id: $subfund_id})
    OPTIONAL MATCH (child:SubFund)-[:PARENT_FUND]->(sf)
    RETURN sf, collect(DISTINCT child) as children
    """
    
    result = db.run(query, subfund_id=subfund_id)
    record = result.single()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"SubFund with ID {subfund_id} not found")
    
    subfund = dict(record['sf'])
    children = [dict(child) for child in record['children'] if child]
    
    return {
        'subfund': subfund,
        'children': children
    }

@router.get("/{subfund_id}/hierarchy")
async def get_subfund_full_hierarchy(subfund_id: str, depth: int = 3, db = Depends(get_db)) -> Dict[str, Any]:
    """Get complete subfund hierarchy (parents and children)"""
    query = f"""
    MATCH (sf:SubFund {{subfund_id: $subfund_id}})
    
    // Get parent chain
    OPTIONAL MATCH parent_path = (sf)-[:PARENT_FUND*1..{depth}]->(parent)
    WITH sf, collect(DISTINCT {{
        node: parent,
        depth: length(parent_path),
        type: labels(parent)[0]
    }}) as parents
    
    // Get children
    OPTIONAL MATCH child_path = (child)-[:PARENT_FUND*1..{depth}]->(sf)
    WITH sf, parents, collect(DISTINCT {{
        node: child,
        depth: length(child_path),
        type: labels(child)[0]
    }}) as children
    
    RETURN sf, parents, children
    """
    
    result = db.run(query, subfund_id=subfund_id)
    record = result.single()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"SubFund with ID {subfund_id} not found")
    
    subfund = dict(record['sf'])
    
    parents = []
    for item in record['parents']:
        if item['node']:
            parent_data = dict(item['node'])
            parent_data['depth'] = item['depth']
            parent_data['type'] = item['type']
            parents.append(parent_data)
    
    children = []
    for item in record['children']:
        if item['node']:
            child_data = dict(item['node'])
            child_data['depth'] = item['depth']
            child_data['type'] = item['type']
            children.append(child_data)
    
    return {
        'subfund': subfund,
        'parents': parents,
        'children': children,
        'depth': depth
    }