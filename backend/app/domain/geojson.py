"""Pure GeoJSON mappers — the single assembly point for FeatureCollections.

Endpoints hand over plain records; this module owns geometry extraction and
property shaping so no endpoint hand-builds Feature dicts. All functions are
pure (no imports from services or data).
"""
from typing import Any, Dict, List, Sequence


def linestring_feature(record: Dict[str, Any], id_key: str = "id") -> Dict[str, Any]:
    """Feature with a LineString geometry from record["coordinates"] (2D points)."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": record["coordinates"],
        },
        "properties": _properties(record, id_key),
    }


def point_feature(
    record: Dict[str, Any],
    id_key: str = "id",
    fallback_point: Sequence[float] = (72.8777, 19.0760),
) -> Dict[str, Any]:
    """Feature with a Point geometry from record["coordinates"]."""
    coords = record.get("coordinates") or list(fallback_point)
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coords,
        },
        "properties": _properties(record, id_key),
    }


def utility_feature(record: Dict[str, Any]) -> Dict[str, Any]:
    """Feature for a utility record: Point for single-coordinate assets, LineString otherwise."""
    coords = record["coordinates"]
    if isinstance(coords[0], (list, tuple)):
        if len(coords) == 1:
            # A lone [lon, lat, depth] point is still a Point, not a one-point LineString.
            geometry = {"type": "Point", "coordinates": list(coords[0])}
        else:
            # 3D points [lon, lat, depth]; GeoJSON accepts the 3-tuple as-is.
            geometry = {"type": "LineString", "coordinates": coords}
    else:
        # Degenerate shape: bare [lon, lat(, depth)] pair — treat as a Point.
        geometry = {"type": "Point", "coordinates": coords}
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": _properties(record, "id"),
    }


def feature_collection(features: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": "FeatureCollection", "features": features}


def _properties(record: Dict[str, Any], id_key: str) -> Dict[str, Any]:
    props = dict(record)
    props.pop("coordinates", None)
    if id_key in props:
        props = {"id": props.pop(id_key), **props}
    return props
