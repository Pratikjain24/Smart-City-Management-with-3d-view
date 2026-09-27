from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.seed.mumbai_dataset import CIVIC_FACILITIES
from app.services.graph_service import graph_engine

router = APIRouter()

@router.get("")
def get_all_civic_facilities(facility_type: Optional[str] = Query(None, description="Filter by facility type: HOSPITAL, COMMAND_CENTER, POLICE_HQ")):
    facilities = CIVIC_FACILITIES
    if facility_type:
        facilities = [f for f in facilities if f.get("type", "").upper() == facility_type.upper()]
    return {
        "status": "success",
        "total": len(facilities),
        "data": facilities
    }

@router.get("/geojson")
def get_civic_facilities_geojson():
    features = []
    for fac in CIVIC_FACILITIES:
        props = dict(fac)
        coords = props.pop("coordinates", [72.8777, 19.0760])
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": coords
            },
            "properties": props
        })
    return {
        "type": "FeatureCollection",
        "features": features
    }

@router.get("/{facility_id}")
def get_civic_facility_by_id(facility_id: str):
    obj = graph_engine.get_universal_object(facility_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Civic facility '{facility_id}' not found")
    return {
        "status": "success",
        "data": obj
    }
