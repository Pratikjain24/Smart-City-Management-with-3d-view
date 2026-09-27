from fastapi import APIRouter
from app.api.v1.endpoints import (
    cities, roads, utilities, transport, 
    incidents, environment, temporal, inspector, search, civic
)
from app.api.v1.ws import live_stream

api_router = APIRouter()

api_router.include_router(cities.router, prefix="/cities", tags=["Cities & Boundaries"])
api_router.include_router(roads.router, prefix="/roads", tags=["Road Network"])
api_router.include_router(utilities.router, prefix="/utilities", tags=["Underground Utilities"])
api_router.include_router(transport.router, prefix="/transport", tags=["Public Transportation"])
api_router.include_router(civic.router, prefix="/civic", tags=["Civic & Emergency Facilities"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["Incidents & Road Damage"])
api_router.include_router(environment.router, prefix="/environment", tags=["Environment & AQI"])
api_router.include_router(temporal.router, prefix="/temporal", tags=["4D Time Machine"])
api_router.include_router(inspector.router, prefix="/objects", tags=["Universal Object Inspector"])
api_router.include_router(search.router, prefix="/search", tags=["Global Search"])
api_router.include_router(live_stream.router, prefix="/ws", tags=["WebSocket Telemetry"])
