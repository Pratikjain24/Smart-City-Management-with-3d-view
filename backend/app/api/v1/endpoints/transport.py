from fastapi import APIRouter
from app.seed.mumbai_dataset import TRANSIT_DATA
from app.services.telemetry_simulator import telemetry_hub

router = APIRouter()

@router.get("/all")
def get_all_transit():
    return {
        "status": "success",
        "data": TRANSIT_DATA
    }

@router.get("/metro")
def get_metro_lines():
    return {
        "status": "success",
        "total": len(TRANSIT_DATA["metro_lines"]),
        "data": TRANSIT_DATA["metro_lines"]
    }

@router.get("/suburban-railway")
def get_suburban_railway():
    return {
        "status": "success",
        "total": len(TRANSIT_DATA["suburban_railway"]),
        "data": TRANSIT_DATA["suburban_railway"]
    }

@router.get("/buses")
def get_best_buses():
    return {
        "status": "success",
        "total": len(TRANSIT_DATA["best_buses"]),
        "data": TRANSIT_DATA["best_buses"]
    }

@router.get("/live-feed")
def get_live_transit_feed():
    tick = telemetry_hub.get_live_tick()
    return {
        "status": "success",
        "timestamp": tick["timestamp"],
        "provenance": tick["provenance"],
        "data": tick["live_transit"]
    }
