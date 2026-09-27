from fastapi import APIRouter, HTTPException
from typing import Optional
from app.seed.mumbai_dataset import INCIDENTS_DATA
from app.services.graph_service import graph_engine

router = APIRouter()

@router.get("")
def get_all_incidents(severity: Optional[str] = None):
    items = INCIDENTS_DATA
    if severity:
        items = [i for i in items if i.get("severity", "").upper() == severity.upper()]
    return {
        "status": "success",
        "total": len(items),
        "data": items
    }

@router.get("/geojson")
def get_incidents_geojson():
    features = []
    for inc in INCIDENTS_DATA:
        props = dict(inc)
        props.pop("coordinates", None)
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": inc["coordinates"]
            },
            "properties": props
        })
    return {
        "type": "FeatureCollection",
        "features": features
    }

@router.get("/stats")
def get_incident_stats():
    total = len(INCIDENTS_DATA)
    critical = sum(1 for i in INCIDENTS_DATA if i.get("severity") == "CRITICAL")
    high = sum(1 for i in INCIDENTS_DATA if i.get("severity") == "HIGH")
    warning = sum(1 for i in INCIDENTS_DATA if i.get("severity") == "WARNING")
    moderate = sum(1 for i in INCIDENTS_DATA if i.get("severity") == "MODERATE")
    
    return {
        "status": "success",
        "total_active_incidents": total,
        "severity_breakdown": {
            "CRITICAL": critical,
            "HIGH": high,
            "WARNING": warning,
            "MODERATE": moderate
        }
    }

@router.get("/{incident_id}")
def get_incident_by_id(incident_id: str):
    obj = graph_engine.get_universal_object(incident_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Incident with id '{incident_id}' not found")
    return {
        "status": "success",
        "data": obj
    }
