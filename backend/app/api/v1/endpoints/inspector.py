from fastapi import APIRouter, HTTPException
from app.services.graph_service import graph_engine

router = APIRouter()

@router.get("/{object_id}")
def inspect_object(object_id: str):
    obj = graph_engine.get_universal_object(object_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Entity with object_id '{object_id}' not found in Mumbai digital twin")
    return {
        "status": "success",
        "data": obj
    }
