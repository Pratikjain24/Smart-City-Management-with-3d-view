from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.seed.mumbai_dataset import ROADS_DATA
from app.services.graph_service import graph_engine

router = APIRouter()

@router.get("")
def get_all_roads(category: Optional[str] = None):
    roads = ROADS_DATA
    if category:
        roads = [r for r in roads if r.get("category", "").lower() == category.lower()]
    return {
        "status": "success",
        "total": len(roads),
        "data": roads
    }

@router.get("/geojson")
def get_roads_geojson():
    features = []
    for r in ROADS_DATA:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": r["coordinates"]
            },
            "properties": {
                "id": r["id"],
                "name": r["name"],
                "type": r["type"],
                "traffic_level": r["traffic_level"],
                "traffic_status": r["traffic_status"],
                "avg_speed_kmh": r["avg_speed_kmh"],
                "lanes": r["lanes"],
                "road_condition": r["road_condition"],
                "known_incidents": r["known_incidents"],
                "connected_road_ids": r.get("connected_road_ids", []),
                "data_provenance": r.get("data_provenance", "LIVE_CALIBRATED"),
                "freshness": r.get("freshness", "Realtime")
            }
        })
    return {
        "type": "FeatureCollection",
        "features": features
    }

@router.get("/{road_id}")
def get_road_by_id(road_id: str):
    road = graph_engine.get_road_details(road_id)
    if not road:
        raise HTTPException(status_code=404, detail=f"Road with id '{road_id}' not found")
    return {
        "status": "success",
        "data": road
    }

@router.get("/{road_id}/connected")
def get_connected_roads(road_id: str):
    road = graph_engine.get_road_details(road_id)
    if not road:
        raise HTTPException(status_code=404, detail=f"Road with id '{road_id}' not found")
    return {
        "status": "success",
        "primary_road_id": road_id,
        "connected_roads": road.get("connected_roads_resolved", []),
        "nearby_intersections": road.get("nearby_intersections", []),
        "nearby_infrastructure": road.get("nearby_infrastructure", {})
    }
