"""
MahaTwin Mumbai - Complete End-to-End Integration Verification Suite
Simulates the complete user operational workflow:
1. Load City Metadata & Administrative Wards
2. Load Connected Road Network & Validate Geometry
3. Select & Highlight Primary Road & Traverse Connected Graph
4. Query Subsurface Utilities across all Domains (Water, Sewer, Drainage, Power, Telecom)
5. Inspect Infrastructure Assets via Universal Object Inspector
6. Query Civic Facilities & Emergency Response Centers
7. Switch Temporal Scenarios (4D Time Machine: Historical, Live, Future)
8. Connect to Live Telemetry WebSocket and verify Realtime Telemetry Pulse & Honesty
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_complete_digital_twin_end_to_end_flow():
    # --- STEP 1: Load City & Administrative Boundaries ---
    city_res = client.get("/api/v1/cities/mumbai")
    assert city_res.status_code == 200
    city_data = city_res.json()["data"]
    assert city_data["name"] == "Mumbai Metropolitan City"
    assert len(city_data["admin_wards"]) >= 10

    # --- STEP 2: Load Connected Road Network ---
    roads_res = client.get("/api/v1/roads")
    assert roads_res.status_code == 200
    roads = roads_res.json()["data"]
    assert len(roads) >= 10
    
    # Verify GeoJSON format
    geojson_res = client.get("/api/v1/roads/geojson")
    assert geojson_res.status_code == 200
    assert geojson_res.json()["type"] == "FeatureCollection"
    assert len(geojson_res.json()["features"]) == len(roads)

    # --- STEP 3: Select Primary Road & Traverse Connected Graph ---
    primary_road_id = "road_weh_01"
    connected_res = client.get(f"/api/v1/roads/{primary_road_id}/connected")
    assert connected_res.status_code == 200
    connected_data = connected_res.json()
    assert connected_data["primary_road_id"] == primary_road_id
    assert len(connected_data["connected_roads"]) >= 3
    # Bandra-Worli Sea Link must be connected to Western Express Highway
    connected_ids = [r["id"] for r in connected_data["connected_roads"]]
    assert "road_bwsl_01" in connected_ids
    assert "nearby_infrastructure" in connected_data

    # --- STEP 4: Inspect Entity via Universal Object Inspector ---
    inspect_res = client.get(f"/api/v1/objects/{primary_road_id}")
    assert inspect_res.status_code == 200
    obj_data = inspect_res.json()["data"]
    assert obj_data["object_id"] == primary_road_id
    assert obj_data["category"] == "ROAD_NETWORK"
    assert obj_data["data_provenance"] == "SAMPLE_BUNDLED_DATA"
    assert "graph_connections" in obj_data

    # --- STEP 5: Underground Mode & Utility Network Isolation ---
    utils_all_res = client.get("/api/v1/utilities/all")
    assert utils_all_res.status_code == 200
    utils_data = utils_all_res.json()["data"]
    for required_category in ["water", "sewer", "drainage", "electricity", "telecom"]:
        assert required_category in utils_data
        assert len(utils_data[required_category]) > 0

    # Isolate Water Utility
    water_res = client.get("/api/v1/utilities/water")
    assert water_res.status_code == 200
    assert water_res.json()["total"] >= 3
    water_trunk = water_res.json()["data"][0]
    
    # Inspect Water Trunk Pipeline
    water_inspect = client.get(f"/api/v1/objects/{water_trunk['id']}")
    assert water_inspect.status_code == 200
    assert "UTILITY_WATER" in water_inspect.json()["data"]["category"]

    # --- STEP 6: Civic & Emergency Facilities ---
    civic_res = client.get("/api/v1/civic")
    assert civic_res.status_code == 200
    civic_data = civic_res.json()["data"]
    assert len(civic_data) >= 5
    hospitals = [c for c in civic_data if c["type"] == "HOSPITAL"]
    assert len(hospitals) >= 3

    # --- STEP 7: 4D Time Machine Scenarios ---
    temp_res = client.get("/api/v1/temporal/scenarios")
    assert temp_res.status_code == 200
    scenarios = temp_res.json()["scenarios"]
    assert "historical_2020" in scenarios
    assert "live_2026" in scenarios
    assert "future_2028" in scenarios
    assert "future_2030" in scenarios

    # Verify Historical scenario (pre-coastal road construction)
    hist_res = client.get("/api/v1/temporal/scenario/historical_2020")
    assert hist_res.status_code == 200
    assert hist_res.json()["data"]["year"] == 2020

    # --- STEP 8: Live Telemetry WebSocket Stream & Data Honesty ---
    with client.websocket_connect("/api/v1/ws/live-stream") as ws:
        tick = ws.receive_json()
        assert tick["type"] == "MAHATWIN_TELEMETRY_PULSE"
        # Verify strict honest labeling
        assert tick["data_mode"] == "SIMULATED"
        assert tick["provenance"] == "SIMULATED_TELEMETRY"
        assert "city_metrics" in tick
        assert "live_transit" in tick
        assert len(tick["live_transit"]["metro_trains"]) >= 2
        assert len(tick["live_transit"]["suburban_trains"]) >= 1
        assert len(tick["live_transit"]["best_buses"]) >= 2
        assert "road_traffic_pulse" in tick

        # Inspect live vehicle received from WebSocket
        train_id = tick["live_transit"]["metro_trains"][0]["train_id"]
        veh_inspect = client.get(f"/api/v1/objects/veh_{train_id}")
        assert veh_inspect.status_code == 200
        assert veh_inspect.json()["data"]["category"] == "TRANSIT_METRO_TRAIN"
