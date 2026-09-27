"""
Generator for database/init/002_seed_sample_mumbai_data.sql
Populates PostGIS infrastructure_assets, road_connections, and telemetry_observations.
"""
import json
from pathlib import Path
from app.seed.mumbai_dataset import ROADS_DATA, UTILITIES_DATA, CIVIC_FACILITIES

def generate_sql():
    sql_lines = [
        "-- ========================================================",
        "-- MAHATWIN MUMBAI - POSTGIS & TIMESCALEDB SEED DATA",
        "-- Stamped with source_kind = 'sample' (honest data labeling)",
        "-- ========================================================",
        "",
        "BEGIN;"
    ]

    # 1. Insert Roads
    for r in ROADS_DATA:
        r_id = r["id"].replace("'", "''")
        name = r["name"].replace("'", "''")
        status = r.get("traffic_status", "Operational").replace("'", "''")
        props = json.dumps({
            "category": r.get("category"),
            "type": r.get("type"),
            "lanes": r.get("lanes"),
            "avg_speed_kmh": r.get("avg_speed_kmh"),
            "speed_limit_kmh": r.get("speed_limit_kmh"),
            "traffic_level": r.get("traffic_level"),
            "road_condition": r.get("road_condition")
        }).replace("'", "''")
        coords = r["coordinates"]
        line_wkt = "LINESTRING(" + ", ".join(f"{pt[0]} {pt[1]}" for pt in coords) + ")"
        sql_lines.append(
            f"INSERT INTO infrastructure_assets (id, asset_type, name, status, source_kind, source_name, observed_at, properties, geometry) "
            f"VALUES ('{r_id}', 'ROAD', '{name}', '{status}', 'sample', 'MahaTwin Demonstrator Baseline', NOW(), '{props}'::jsonb, ST_GeomFromText('{line_wkt}', 4326)) "
            f"ON CONFLICT (id) DO NOTHING;"
        )

    # 2. Insert Road Connections
    road_ids = {r["id"] for r in ROADS_DATA}
    for r in ROADS_DATA:
        r_id = r["id"].replace("'", "''")
        for c_id in r.get("connected_road_ids", []):
            if c_id in road_ids and c_id != r["id"]:
                c_clean = c_id.replace("'", "''")
                sql_lines.append(
                    f"INSERT INTO road_connections (road_id, connected_road_id) VALUES ('{r_id}', '{c_clean}') ON CONFLICT DO NOTHING;"
                )

    # 3. Insert Utilities
    for cat, u_list in UTILITIES_DATA.items():
        for u in u_list:
            u_id = u["id"].replace("'", "''")
            name = u["name"].replace("'", "''")
            status = u.get("status", "Active").replace("'", "''")
            props = json.dumps({
                "utility_category": cat,
                "type": u.get("type"),
                "depth_meters": u.get("depth_meters", -5),
                "diameter_mm": u.get("diameter_mm"),
                "voltage_kv": u.get("voltage_kv"),
                "material": u.get("material")
            }).replace("'", "''")
            coords = u["coordinates"]
            if len(coords) > 1:
                geom_wkt = "LINESTRING(" + ", ".join(f"{pt[0]} {pt[1]}" for pt in coords) + ")"
            else:
                pt = coords[0]
                geom_wkt = f"POINT({pt[0]} {pt[1]})"
            sql_lines.append(
                f"INSERT INTO infrastructure_assets (id, asset_type, name, status, source_kind, source_name, observed_at, properties, geometry) "
                f"VALUES ('{u_id}', 'UTILITY_{cat.upper()}', '{name}', '{status}', 'sample', 'MahaTwin Demonstrator Baseline', NOW(), '{props}'::jsonb, ST_GeomFromText('{geom_wkt}', 4326)) "
                f"ON CONFLICT (id) DO NOTHING;"
            )

    # 4. Insert Civic Facilities
    for fac in CIVIC_FACILITIES:
        f_id = fac["id"].replace("'", "''")
        name = fac["name"].replace("'", "''")
        f_type = fac.get("type", "CIVIC").replace("'", "''")
        props = json.dumps({
            "category": fac.get("category"),
            "beds": fac.get("beds"),
            "emergency_trauma_level": fac.get("emergency_trauma_level")
        }).replace("'", "''")
        coords = fac["coordinates"]
        pt_wkt = f"POINT({coords[0]} {coords[1]})"
        sql_lines.append(
            f"INSERT INTO infrastructure_assets (id, asset_type, name, status, source_kind, source_name, observed_at, properties, geometry) "
            f"VALUES ('{f_id}', 'CIVIC_{f_type}', '{name}', 'Operational', 'sample', 'MahaTwin Demonstrator Baseline', NOW(), '{props}'::jsonb, ST_GeomFromText('{pt_wkt}', 4326)) "
            f"ON CONFLICT (id) DO NOTHING;"
        )

    # 5. Insert Baseline Telemetry Observations
    sql_lines.append("INSERT INTO telemetry_observations (observed_at, asset_id, metric_name, value, unit, source_kind, payload) VALUES (NOW(), 'road_weh_01', 'avg_speed', 34.0, 'km/h', 'sample', '{\"congestion_level\": \"ORANGE\"}'::jsonb) ON CONFLICT DO NOTHING;")
    sql_lines.append("INSERT INTO telemetry_observations (observed_at, asset_id, metric_name, value, unit, source_kind, payload) VALUES (NOW(), 'road_bwsl_01', 'avg_speed', 72.0, 'km/h', 'sample', '{\"congestion_level\": \"GREEN\"}'::jsonb) ON CONFLICT DO NOTHING;")
    sql_lines.append("INSERT INTO telemetry_observations (observed_at, asset_id, metric_name, value, unit, source_kind, payload) VALUES (NOW(), 'util_water_bhandup_trunk', 'flow_rate', 2450.0, 'm3/h', 'sample', '{\"pressure_bar\": 4.2}'::jsonb) ON CONFLICT DO NOTHING;")

    sql_lines.append("COMMIT;")
    sql_lines.append("")

    out_file = Path(__file__).resolve().parent.parent.parent.parent / "database" / "init" / "002_seed_sample_mumbai_data.sql"
    out_file.write_text("\n".join(sql_lines), encoding="utf-8")
    print(f"Successfully generated {out_file} ({len(sql_lines)} lines)")

if __name__ == "__main__":
    generate_sql()
