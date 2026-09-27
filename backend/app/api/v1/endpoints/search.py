from fastapi import APIRouter, Query
from app.services.graph_service import graph_engine

router = APIRouter()

@router.get("")
def search_digital_twin(q: str = Query(..., min_length=1, description="Search term for roads, buildings, utilities, transit, facilities")):
    results = graph_engine.search_all(q)
    return {
        "status": "success",
        "query": q,
        "total": len(results),
        "results": results
    }
