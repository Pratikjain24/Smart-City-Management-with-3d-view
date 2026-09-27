import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["system"] == "MahaTwin Mumbai"


def test_database_health_is_explicit_when_database_is_unavailable():
    response = client.get("/health/database")
    assert response.status_code in (200, 503)
    if response.status_code == 503:
        assert response.json()["detail"]["status"] == "unavailable"

def test_get_mumbai_metadata():
    response = client.get("/api/v1/cities/mumbai")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "Mumbai Metropolitan City"
    assert len(data["data"]["admin_wards"]) > 0

def test_get_roads():
    response = client.get("/api/v1/roads")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 5
    
    # Test specific road details
    road_id = data["data"][0]["id"]
    detail_res = client.get(f"/api/v1/roads/{road_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["data"]["id"] == road_id

def test_get_road_geojson():
    response = client.get("/api/v1/roads/geojson")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 0

def test_get_utilities():
    response = client.get("/api/v1/utilities/all")
    assert response.status_code == 200
    data = response.json()
    assert "water" in data["categories"]
    assert "sewer" in data["categories"]
    assert "drainage" in data["categories"]

def test_get_transit():
    response = client.get("/api/v1/transport/metro")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 2

def test_get_incidents():
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 3

def test_universal_inspector():
    # Test inspecting a road
    response = client.get("/api/v1/objects/road_weh_01")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["category"] == "ROAD_NETWORK"
    assert "graph_connections" in data["data"]

def test_global_search():
    response = client.get("/api/v1/search?q=Bandra")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert any("Bandra" in r["title"] for r in data["results"])

def test_temporal_scenarios():
    response = client.get("/api/v1/temporal/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert "live_2026" in data["scenarios"]
    assert "historical_2020" in data["scenarios"]


def test_missing_entities_return_a_typed_404():
    response = client.get("/api/v1/objects/does-not-exist")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_bundled_data_and_telemetry_are_honestly_labeled():
    roads = client.get("/api/v1/roads").json()["data"]
    assert roads[0]["data_provenance"] == "SAMPLE_BUNDLED_DATA"

    with client.websocket_connect("/api/v1/ws/live-stream") as websocket:
        payload = websocket.receive_json()
    assert payload["type"] == "MAHATWIN_TELEMETRY_PULSE"
    assert payload["data_mode"] == "SIMULATED"
    assert payload["provenance"] == "SIMULATED_TELEMETRY"
    assert "road_traffic_pulse" in payload
    assert len(payload["road_traffic_pulse"]) > 0

def test_civic_facilities_endpoints():
    # 1. Get all civic facilities
    response = client.get("/api/v1/civic")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total"] >= 5

    # 2. Filter by type
    hosp_res = client.get("/api/v1/civic?facility_type=HOSPITAL")
    assert hosp_res.status_code == 200
    assert all(f["type"] == "HOSPITAL" for f in hosp_res.json()["data"])

    # 3. GeoJSON
    geo_res = client.get("/api/v1/civic/geojson")
    assert geo_res.status_code == 200
    assert geo_res.json()["type"] == "FeatureCollection"
    assert len(geo_res.json()["features"]) >= 5

    # 4. By ID
    fac_id = data["data"][0]["id"]
    single_res = client.get(f"/api/v1/civic/{fac_id}")
    assert single_res.status_code == 200
    assert single_res.json()["data"]["object_id"] == fac_id

def test_universal_inspector_extended_entities():
    # Inspect Metro Train
    train_res = client.get("/api/v1/objects/veh_M3-TRN-101")
    assert train_res.status_code == 200
    assert train_res.json()["data"]["category"] == "TRANSIT_METRO_TRAIN"

    # Inspect BEST Bus
    bus_res = client.get("/api/v1/objects/veh_MH-01-EA-4210")
    assert bus_res.status_code == 200
    assert bus_res.json()["data"]["category"] == "TRANSIT_BUS"

    # Inspect AQI station
    aqi_res = client.get("/api/v1/objects/aqi_bkc")
    assert aqi_res.status_code == 200
    assert aqi_res.json()["data"]["category"] == "ENVIRONMENT_AQI"

    # Inspect Flood risk hotspot
    fld_res = client.get("/api/v1/objects/fld_milan")
    assert fld_res.status_code == 200
    assert fld_res.json()["data"]["category"] == "ENVIRONMENT_FLOOD"

    # Inspect Admin Ward
    ward_res = client.get("/api/v1/objects/ward_a")
    assert ward_res.status_code == 200
    assert ward_res.json()["data"]["category"] == "ADMIN_WARD"

def test_road_connectivity_and_nearby_assets():
    res = client.get("/api/v1/roads/road_weh_01/connected")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["primary_road_id"] == "road_weh_01"
    assert len(data["connected_roads"]) > 0
    assert any(cr["id"] == "road_bwsl_01" for cr in data["connected_roads"])
    assert "nearby_infrastructure" in data
