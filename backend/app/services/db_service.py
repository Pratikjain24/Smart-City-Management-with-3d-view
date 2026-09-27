"""
MahaTwin Spatial Database Service
Integrates with PostgreSQL/PostGIS & TimescaleDB when available,
providing spatial queries, telemetry observation logging, and health checks.
Gracefully falls back to the high-performance in-memory spatial graph when the database is unavailable.
"""
import logging
from typing import Dict, Any, List, Optional
from app.config import settings

logger = logging.getLogger("mahatwin.db")

class DatabaseService:
    def __init__(self):
        self._is_connected = False

    def check_connection(self) -> Dict[str, Any]:
        """Check connection to PostGIS and TimescaleDB."""
        try:
            import psycopg2
            with psycopg2.connect(settings.DATABASE_URL, connect_timeout=2) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT extname FROM pg_extension WHERE extname IN ('postgis', 'timescaledb')")
                    exts = {row[0] for row in cur.fetchall()}
            missing = {"postgis", "timescaledb"} - exts
            if missing:
                return {"status": "degraded", "missing_extensions": sorted(missing)}
            return {"status": "healthy", "extensions": sorted(exts)}
        except Exception as exc:
            return {"status": "unavailable", "detail": str(exc)}

    def get_spatial_roads(self) -> Optional[List[Dict[str, Any]]]:
        """Query road features with GeoJSON geometry from PostGIS."""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            with psycopg2.connect(settings.DATABASE_URL, connect_timeout=2) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT id, name, status, source_kind, source_name, properties,
                               ST_AsGeoJSON(geometry) as geojson
                        FROM infrastructure_assets
                        WHERE asset_type = 'ROAD'
                    """)
                    return cur.fetchall()
        except Exception as exc:
            logger.debug(f"PostGIS query fallback to in-memory: {exc}")
            return None

    def get_road_connections(self, road_id: str) -> Optional[List[str]]:
        """Query connected road IDs from PostGIS topology."""
        try:
            import psycopg2
            with psycopg2.connect(settings.DATABASE_URL, connect_timeout=2) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT connected_road_id 
                        FROM road_connections 
                        WHERE road_id = %s
                    """, (road_id,))
                    return [row[0] for row in cur.fetchall()]
        except Exception as exc:
            logger.debug(f"PostGIS topology query fallback to in-memory: {exc}")
            return None

db_service = DatabaseService()
