from fastapi import APIRouter
from app.seed.mumbai_dataset import ENVIRONMENT_DATA

router = APIRouter()

@router.get("/summary")
def get_environment_summary():
    return {
        "status": "success",
        "data": ENVIRONMENT_DATA
    }

@router.get("/aqi")
def get_aqi_stations():
    return {
        "status": "success",
        "total": len(ENVIRONMENT_DATA["aqi_stations"]),
        "data": ENVIRONMENT_DATA["aqi_stations"]
    }

@router.get("/flood-risk")
def get_flood_risk_hotspots():
    return {
        "status": "success",
        "total": len(ENVIRONMENT_DATA["flood_risk_hotspots"]),
        "data": ENVIRONMENT_DATA["flood_risk_hotspots"]
    }
