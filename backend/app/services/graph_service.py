"""
MahaTwin Spatial Graph Engine
Resolves relationships between infrastructure entities:
Roads <-> Intersections <-> Underground Utilities <-> Transit <-> Emergency Facilities
"""

from typing import Dict, Any, List, Optional
from shapely.geometry import Point, LineString
from app.seed.mumbai_dataset import (
    ROADS_DATA, UTILITIES_DATA, TRANSIT_DATA, 
    INCIDENTS_DATA, CIVIC_FACILITIES, MUMBAI_METADATA,
    ENVIRONMENT_DATA
)

class SpatialGraphEngine:
    def __init__(self):
        self._init_road_cache()
        self._init_utility_cache()
        self._init_facility_cache()

    def _init_road_cache(self):
        self.roads_by_id = {r["id"]: r for r in ROADS_DATA}
        self.road_geometries = {}
        for r in ROADS_DATA:
            if len(r["coordinates"]) >= 2:
                self.road_geometries[r["id"]] = LineString(r["coordinates"])

    def _init_utility_cache(self):
        self.utilities_by_id = {}
        for category, u_list in UTILITIES_DATA.items():
            for u in u_list:
                self.utilities_by_id[u["id"]] = u

    def _init_facility_cache(self):
        self.facilities_by_id = {f["id"]: f for f in CIVIC_FACILITIES}

    def get_road_details(self, road_id: str) -> Optional[Dict[str, Any]]:
        road = self.roads_by_id.get(road_id)
        if not road:
            return None
        
        # Resolve connected road summaries
        connected = []
        for c_id in road.get("connected_road_ids", []):
            c_road = self.roads_by_id.get(c_id)
            if c_road:
                connected.append({
                    "id": c_road["id"],
                    "name": c_road["name"],
                    "type": c_road["type"],
                    "traffic_level": c_road["traffic_level"],
                    "avg_speed_kmh": c_road["avg_speed_kmh"]
                })

        # Find incidents intersecting or near this road
        incidents = [
            inc for inc in INCIDENTS_DATA 
            if inc.get("related_road_id") == road_id
        ]

        result = dict(road)
        result["connected_roads_resolved"] = connected
        result["active_incidents_resolved"] = incidents
        return result

    def get_universal_object(self, object_id: str) -> Optional[Dict[str, Any]]:
        """
        Universal Inspector query for ANY entity in MahaTwin:
        Road, Utility line/plant, Transit line/train/station, Incident, Civic facility.
        """
        # 1. Check Roads
        if object_id in self.roads_by_id:
            road = self.get_road_details(object_id)
            return {
                "object_id": object_id,
                "name": road["name"],
                "category": "ROAD_NETWORK",
                "sub_type": road["type"],
                "status": road["traffic_status"],
                "data_provenance": road["data_provenance"],
                "freshness": road["freshness"],
                "details": road,
                "graph_connections": {
                    "connected_roads": road.get("connected_roads_resolved", []),
                    "nearby_infrastructure": road.get("nearby_infrastructure", {}),
                    "incidents": road.get("active_incidents_resolved", [])
                }
            }

        # 2. Check Utilities
        if object_id in self.utilities_by_id:
            u = self.utilities_by_id[object_id]
            return {
                "object_id": object_id,
                "name": u["name"],
                "category": f"UTILITY_{u['utility_type']}",
                "sub_type": u["type"],
                "status": u.get("status", "Active"),
                "data_provenance": u.get("data_provenance", "AUTHORITATIVE"),
                "freshness": u.get("freshness", "Realtime"),
                "details": u,
                "graph_connections": {
                    "upstream_source": u.get("upstream_source"),
                    "downstream_zones": u.get("downstream_zones", []),
                    "connected_assets": u.get("connected_assets", [])
                }
            }

        # 3. Check Transit Metro Lines
        for m in TRANSIT_DATA.get("metro_lines", []):
            if m["id"] == object_id:
                return {
                    "object_id": object_id,
                    "name": m["name"],
                    "category": "TRANSIT_METRO",
                    "sub_type": m["type"],
                    "status": m["status"],
                    "data_provenance": m.get("data_provenance", "MMRC_LIVE"),
                    "freshness": m.get("freshness", "Realtime"),
                    "details": m,
                    "graph_connections": {
                        "stations": m.get("stations", []),
                        "active_trains": m.get("active_trains", [])
                    }
                }

        # 3. Check Transit Metro Lines & Trains & Stations
        clean_id = object_id.replace("veh_", "")
        for m in TRANSIT_DATA.get("metro_lines", []):
            if m["id"] == object_id:
                return {
                    "object_id": object_id,
                    "name": m["name"],
                    "category": "TRANSIT_METRO",
                    "sub_type": m["type"],
                    "status": m["status"],
                    "data_provenance": m.get("data_provenance", "SAMPLE_BUNDLED_DATA"),
                    "freshness": m.get("freshness", "Bundled sample — not a live feed"),
                    "details": m,
                    "graph_connections": {
                        "stations": m.get("stations", []),
                        "active_trains": m.get("active_trains", [])
                    }
                }
            # Check individual metro trains
            for tr in m.get("active_trains", []):
                if tr.get("train_id") == clean_id or tr.get("train_id") == object_id:
                    return {
                        "object_id": object_id,
                        "name": f"Metro Train {tr['train_id']} ({m['name']})",
                        "category": "TRANSIT_METRO_TRAIN",
                        "sub_type": "Active Electric Rolling Stock (CBTC)",
                        "status": "In Service Underground",
                        "data_provenance": "SIMULATED_TELEMETRY",
                        "freshness": "Realtime (1s WebSocket sync)",
                        "details": {
                            "train_id": tr["train_id"],
                            "parent_line": m["name"],
                            "direction": tr.get("direction", "Cuffe Parade <-> SEEPZ"),
                            "speed_kmh": tr.get("speed_kmh", 55),
                            "occupancy_pct": tr.get("occupancy_pct", 78),
                            "signaling_headway": "90 sec CBTC Virtual Block",
                            "status": "In Transit Underground (-20m)"
                        },
                        "graph_connections": {
                            "parent_metro_line": m["name"],
                            "corridor_id": m["id"],
                            "nearest_stations": [s["name"] for s in m.get("stations", [])[:4]]
                        }
                    }
            # Check metro stations
            for st in m.get("stations", []):
                st_id = f"{m['id']}_{st['name'].lower().replace(' ', '_')}"
                if object_id.lower() in (st_id, st["name"].lower(), f"station_{st['name'].lower().replace(' ', '_')}"):
                    return {
                        "object_id": object_id,
                        "name": f"Metro Station: {st['name']}",
                        "category": "TRANSIT_STATION",
                        "sub_type": "Underground Metro Station (Platform Screen Doors)",
                        "status": "Operational",
                        "data_provenance": "SAMPLE_BUNDLED_DATA",
                        "freshness": "Authoritative Static",
                        "details": {
                            "station_name": st["name"],
                            "parent_line": m["name"],
                            "coordinates": st.get("coords", []),
                            "accessibility": "Full Divyangjan Barrier-Free / Tactile Paths",
                            "multimodal_interchange": "BEST Feeder Bus + Suburban Rail Connector"
                        },
                        "graph_connections": {
                            "parent_line": m["name"],
                            "adjacent_stations": [s["name"] for s in m.get("stations", []) if s["name"] != st["name"]][:3]
                        }
                    }

        # 4. Check Suburban Railways & Trains & Stations
        for r in TRANSIT_DATA.get("suburban_railway", []):
            if r["id"] == object_id:
                return {
                    "object_id": object_id,
                    "name": r["name"],
                    "category": "TRANSIT_RAILWAY",
                    "sub_type": r["type"],
                    "status": r["status"],
                    "data_provenance": r.get("data_provenance", "SAMPLE_BUNDLED_DATA"),
                    "freshness": r.get("freshness", "Bundled sample — not a live feed"),
                    "details": r,
                    "graph_connections": {
                        "stations": r.get("stations", []),
                        "active_trains": r.get("active_trains", [])
                    }
                }
            # Check individual suburban trains
            for tr in r.get("active_trains", []):
                if tr.get("train_id") == clean_id or tr.get("train_id") == object_id:
                    return {
                        "object_id": object_id,
                        "name": f"Suburban Local {tr['train_id']} ({r['name']})",
                        "category": "TRANSIT_RAIL_TRAIN",
                        "sub_type": tr.get("type", "Fast Local 15-Car AC"),
                        "status": tr.get("status", "On Time"),
                        "data_provenance": "SIMULATED_TELEMETRY",
                        "freshness": "Realtime (1s WebSocket sync)",
                        "details": {
                            "train_id": tr["train_id"],
                            "type": tr.get("type", "Fast Local 15-Car AC"),
                            "parent_line": r["name"],
                            "speed_kmh": tr.get("speed_kmh", 65),
                            "occupancy": tr.get("occupancy", "Super Dense Crush Load (120%)"),
                            "status": tr.get("status", "Nominal")
                        },
                        "graph_connections": {
                            "parent_line": r["name"],
                            "corridor_id": r["id"],
                            "route_stations": [s["name"] for s in r.get("stations", [])[:5]]
                        }
                    }
            # Check railway stations
            for st in r.get("stations", []):
                st_id = f"{r['id']}_{st['name'].lower().replace(' ', '_')}"
                if object_id.lower() in (st_id, st["name"].lower(), f"station_{st['name'].lower().replace(' ', '_')}"):
                    return {
                        "object_id": object_id,
                        "name": f"Railway Station: {st['name']}",
                        "category": "TRANSIT_STATION",
                        "sub_type": "Suburban Rail Terminus / Major Hub",
                        "status": "Operational",
                        "data_provenance": "SAMPLE_BUNDLED_DATA",
                        "freshness": "Authoritative Static",
                        "details": {
                            "station_name": st["name"],
                            "parent_railway": r["name"],
                            "coordinates": st.get("coords", []),
                            "daily_ridership": r.get("daily_ridership", 3500000) // 10
                        },
                        "graph_connections": {
                            "parent_line": r["name"],
                            "interchange_routes": [r["name"], "BEST Feeder Network"]
                        }
                    }

        # 4b. Check BEST Buses
        for b_route in TRANSIT_DATA.get("best_buses", []):
            for b in b_route.get("active_buses", []):
                if b.get("bus_id") == clean_id or b.get("bus_id") == object_id:
                    return {
                        "object_id": object_id,
                        "name": f"BEST Electric AC Bus ({b_route['route_no']})",
                        "category": "TRANSIT_BUS",
                        "sub_type": "Olectra 12m Electric Low-Floor AC",
                        "status": "In Service Surface",
                        "data_provenance": "SIMULATED_TELEMETRY",
                        "freshness": "Realtime (1s WebSocket sync)",
                        "details": {
                            "bus_id": b["bus_id"],
                            "route_no": b_route["route_no"],
                            "route_name": b_route.get("route_name", ""),
                            "destination": b.get("destination", ""),
                            "speed_kmh": b.get("speed_kmh", 28),
                            "occupancy": b.get("occupancy", "Seats Available (65%)"),
                            "propulsion": "100% Zero Emission Battery Electric"
                        },
                        "graph_connections": {
                            "route": b_route["route_no"],
                            "destination": b.get("destination", ""),
                            "interchanges": ["Bandra Station", "BKC Connector", "CSMT"]
                        }
                    }

        # 5. Check Incidents
        for inc in INCIDENTS_DATA:
            if inc["id"] == object_id:
                return {
                    "object_id": object_id,
                    "name": inc["title"],
                    "category": "INCIDENT_ALERT",
                    "sub_type": inc["category"],
                    "status": inc["status"],
                    "data_provenance": inc.get("data_provenance", "SAMPLE_BUNDLED_DATA"),
                    "freshness": inc.get("freshness", "Bundled sample — not a live feed"),
                    "details": inc,
                    "graph_connections": {
                        "related_road": self.roads_by_id.get(inc.get("related_road_id", "")),
                        "coordinates": inc["coordinates"]
                    }
                }

        # 6. Check Civic Facilities
        if object_id in self.facilities_by_id:
            fac = self.facilities_by_id[object_id]
            return {
                "object_id": object_id,
                "name": fac["name"],
                "category": f"CIVIC_{fac['type']}",
                "sub_type": fac["category"],
                "status": "Operational",
                "data_provenance": fac.get("data_provenance", "SAMPLE_BUNDLED_DATA"),
                "freshness": fac.get("freshness", "Bundled sample — not a live feed"),
                "details": fac,
                "graph_connections": {
                    "connected_roads": fac.get("connected_roads", []),
                    "nearby_utilities": fac.get("nearby_utilities", [])
                }
            }

        # 7. Check Environment AQI Stations
        for st in ENVIRONMENT_DATA.get("aqi_stations", []):
            if st["id"] == object_id or st["id"] == clean_id:
                return {
                    "object_id": object_id,
                    "name": f"SAFAR AQI Station: {st['name']}",
                    "category": "ENVIRONMENT_AQI",
                    "sub_type": "Continuous Ambient Air Quality Monitoring Station (CAAQMS)",
                    "status": f"AQI {st['aqi']} ({st['status']})",
                    "data_provenance": "SAMPLE_BUNDLED_DATA",
                    "freshness": "Hourly Averaged Sample",
                    "details": st,
                    "graph_connections": {
                        "pm25": f"{st['pm25']} µg/m³",
                        "pm10": f"{st['pm10']} µg/m³",
                        "prominent_pollutant": st.get("prominent_pollutant", "PM2.5")
                    }
                }

        # 8. Check Environment Flood Hotspots
        for fh in ENVIRONMENT_DATA.get("flood_risk_hotspots", []):
            if fh["id"] == object_id or fh["id"] == clean_id:
                return {
                    "object_id": object_id,
                    "name": f"Flood Risk Hotspot: {fh['name']}",
                    "category": "ENVIRONMENT_FLOOD",
                    "sub_type": "Low-Lying Subsurface Waterlogging Zone",
                    "status": f"Risk: {fh['risk_level']}",
                    "data_provenance": "SAMPLE_BUNDLED_DATA",
                    "freshness": "Hydraulic Model Calibrated",
                    "details": fh,
                    "graph_connections": {
                        "swd_drainage_system": fh.get("pumping_station", "BRIMSTOWAD"),
                        "retention_sump_capacity": fh.get("retention_sump_capacity", "20 ML")
                    }
                }

        # 9. Check Administrative Wards
        for w in MUMBAI_METADATA.get("admin_wards", []):
            if w["id"] == object_id:
                return {
                    "object_id": object_id,
                    "name": w["name"],
                    "category": "ADMIN_WARD",
                    "sub_type": "BMC Municipal Administrative Ward",
                    "status": "Active Administrative Jurisdiction",
                    "data_provenance": "AUTHORITATIVE_BMC",
                    "freshness": "Municipal Reference Datum",
                    "details": w,
                    "graph_connections": {
                        "ward_id": w["id"],
                        "center_coordinates": w["center"]
                    }
                }

        return None

    def search_all(self, query: str) -> List[Dict[str, Any]]:
        """
        Global search across all Mumbai entities:
        Roads, Utilities, Transit, Incidents, Facilities, Wards.
        """
        q = query.lower().strip()
        if not q:
            return []

        results = []

        # Search Wards
        for ward in MUMBAI_METADATA.get("admin_wards", []):
            if q in ward["name"].lower() or q in ward["id"].lower():
                results.append({
                    "id": ward["id"],
                    "title": ward["name"],
                    "category": "Ward / District",
                    "type": "ADMIN_WARD",
                    "coordinates": ward["center"],
                    "description": "BMC Municipal Administrative Ward"
                })

        # Search Roads
        for r in ROADS_DATA:
            if q in r["name"].lower() or q in r["type"].lower() or q in r["category"].lower():
                results.append({
                    "id": r["id"],
                    "title": r["name"],
                    "category": "Road / Expressway",
                    "type": "ROAD",
                    "coordinates": r["coordinates"][0],
                    "description": f"{r['type']} • {r['traffic_status']} traffic • {r['lanes']} lanes"
                })

        # Search Utilities
        for cat, u_list in UTILITIES_DATA.items():
            for u in u_list:
                if q in u["name"].lower() or q in u.get("type", "").lower() or q in cat:
                    coords = u["coordinates"][0] if isinstance(u["coordinates"][0], list) else u["coordinates"]
                    results.append({
                        "id": u["id"],
                        "title": u["name"],
                        "category": f"Utility ({cat.upper()})",
                        "type": "UTILITY",
                        "coordinates": coords[:2],
                        "description": f"Subsurface depth: {u.get('depth_meters', 0)}m • {u.get('type')}"
                    })

        # Search Transit Metro & Rail
        for m in TRANSIT_DATA.get("metro_lines", []):
            if q in m["name"].lower():
                results.append({
                    "id": m["id"],
                    "title": m["name"],
                    "category": "Metro Transit",
                    "type": "TRANSIT_METRO",
                    "coordinates": m["coordinates"][0][:2],
                    "description": f"{m['status']} • {len(m['stations'])} stations"
                })
            for st in m.get("stations", []):
                if q in st["name"].lower():
                    results.append({
                        "id": f"{m['id']}_{st['name'].replace(' ', '_')}",
                        "title": f"Metro Station: {st['name']}",
                        "category": "Transit Station",
                        "type": "TRANSIT_STATION",
                        "coordinates": st["coords"],
                        "description": f"Station on {m['name']}"
                    })

        for r in TRANSIT_DATA.get("suburban_railway", []):
            if q in r["name"].lower():
                results.append({
                    "id": r["id"],
                    "title": r["name"],
                    "category": "Suburban Railway",
                    "type": "TRANSIT_RAIL",
                    "coordinates": r["coordinates"][0],
                    "description": f"{r['daily_ridership']:,} daily commuters"
                })
            for st in r.get("stations", []):
                if q in st["name"].lower():
                    results.append({
                        "id": f"{r['id']}_{st['name'].replace(' ', '_')}",
                        "title": f"Rail Station: {st['name']}",
                        "category": "Railway Station",
                        "type": "TRANSIT_STATION",
                        "coordinates": st["coords"],
                        "description": f"Station on {r['name']}"
                    })

        # Search Civic Facilities
        for fac in CIVIC_FACILITIES:
            if q in fac["name"].lower() or q in fac.get("category", "").lower():
                results.append({
                    "id": fac["id"],
                    "title": fac["name"],
                    "category": "Civic Facility",
                    "type": fac["type"],
                    "coordinates": fac["coordinates"],
                    "description": f"{fac['category']}"
                })

        # Search Incidents
        for inc in INCIDENTS_DATA:
            if q in inc["title"].lower() or q in inc["location_name"].lower() or q in inc["category"].lower():
                results.append({
                    "id": inc["id"],
                    "title": inc["title"],
                    "category": "Incident / Alert",
                    "type": "INCIDENT",
                    "coordinates": inc["coordinates"],
                    "description": f"{inc['severity']} • {inc['status']}"
                })

        return results[:15]

graph_engine = SpatialGraphEngine()
