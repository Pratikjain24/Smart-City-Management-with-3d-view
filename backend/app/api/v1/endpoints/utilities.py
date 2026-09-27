from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.seed.mumbai_dataset import UTILITIES_DATA
from app.services.graph_service import graph_engine

router = APIRouter()

@router.get("/all")
def get_all_utilities():
    return {
        "status": "success",
        "categories": list(UTILITIES_DATA.keys()),
        "data": UTILITIES_DATA
    }

@router.get("/geojson/{category}")
def get_utility_geojson(category: str):
    cat_clean = category.lower()
    if cat_clean not in UTILITIES_DATA:
        raise HTTPException(status_code=404, detail=f"Utility category '{category}' not found. Valid: {list(UTILITIES_DATA.keys())}")
    
    items = UTILITIES_DATA[cat_clean]
    features = []
    for item in items:
        coords = item["coordinates"]
        geom_type = "Point" if len(coords) == 1 else "LineString"
        geom_coords = coords[0] if geom_type == "Point" else coords
        
        props = dict(item)
        props.pop("coordinates", None)
        
        features.append({
            "type": "Feature",
            "geometry": {
                "type": geom_type,
                "coordinates": geom_coords
            },
            "properties": props
        })
    
    return {
        "type": "FeatureCollection",
        "category": cat_clean,
        "features": features
    }

@router.get("/{category}")
def get_utilities_by_category(category: str):
    cat_clean = category.lower()
    if cat_clean not in UTILITIES_DATA:
        raise HTTPException(status_code=404, detail=f"Utility category '{category}' not found. Valid: {list(UTILITIES_DATA.keys())}")
    return {
        "status": "success",
        "category": cat_clean,
        "total": len(UTILITIES_DATA[cat_clean]),
        "data": UTILITIES_DATA[cat_clean]
    }

@router.get("/{category}/{utility_id}")
def get_utility_detail(category: str, utility_id: str):
    obj = graph_engine.get_universal_object(utility_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Utility asset with id '{utility_id}' not found")
    return {
        "status": "success",
        "data": obj
    }
