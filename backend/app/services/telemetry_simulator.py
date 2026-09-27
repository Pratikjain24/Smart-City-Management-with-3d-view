"""
MahaTwin Real-time Telemetry & Transit Simulation Hub
Streams realistic high-frequency telemetry for transit vehicles,
traffic speeds, utility pressure sensors, and municipal heartbeats.
"""

import math
import time
from typing import Dict, Any, List
from app.seed.mumbai_dataset import TRANSIT_DATA, ROADS_DATA, UTILITIES_DATA, ENVIRONMENT_DATA

class TelemetrySimulator:
    def __init__(self):
        self.start_time = time.time()

    def get_live_tick(self) -> Dict[str, Any]:
        """
        Generates a live synchronized telemetry tick containing:
        - Animated bus & train GPS positions along trajectories
        - Fluctuating traffic speeds on expressways
        - Dynamic water pressure and electric grid loads
        - City-wide health index and data freshness timestamp
        """
        elapsed = time.time() - self.start_time
        timestamp_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # 1. Update Metro 3 Aqua Line Trains along coordinate splines
        metro_3_trains = []
        m3_coords = TRANSIT_DATA["metro_lines"][0]["coordinates"]
        n_m3 = len(m3_coords)
        for i, train in enumerate(TRANSIT_DATA["metro_lines"][0]["active_trains"]):
            # calculate fractional position along route
            speed_factor = 0.03
            t_offset = (elapsed * speed_factor + i * 0.33) % 1.0
            idx_float = t_offset * (n_m3 - 1)
            idx_base = int(idx_float)
            idx_next = min(idx_base + 1, n_m3 - 1)
            frac = idx_float - idx_base

            lon = m3_coords[idx_base][0] + frac * (m3_coords[idx_next][0] - m3_coords[idx_base][0])
            lat = m3_coords[idx_base][1] + frac * (m3_coords[idx_next][1] - m3_coords[idx_base][1])
            depth = m3_coords[idx_base][2]

            metro_3_trains.append({
                "train_id": train["train_id"],
                "line": "Metro Line 3 (Aqua Line)",
                "coordinates": [round(lon, 6), round(lat, 6), depth],
                "speed_kmh": round(55 + 15 * math.sin(elapsed + i), 1),
                "occupancy_pct": train["occupancy_pct"],
                "direction": train["direction"],
                "status": "In Transit Underground"
            })

        # 2. Update Suburban Rail Trains
        rail_trains = []
        wr_coords = TRANSIT_DATA["suburban_railway"][0]["coordinates"]
        n_wr = len(wr_coords)
        for i, train in enumerate(TRANSIT_DATA["suburban_railway"][0]["active_trains"]):
            speed_factor = 0.02
            t_offset = (elapsed * speed_factor + i * 0.5) % 1.0
            idx_float = t_offset * (n_wr - 1)
            idx_base = int(idx_float)
            idx_next = min(idx_base + 1, n_wr - 1)
            frac = idx_float - idx_base

            lon = wr_coords[idx_base][0] + frac * (wr_coords[idx_next][0] - wr_coords[idx_base][0])
            lat = wr_coords[idx_base][1] + frac * (wr_coords[idx_next][1] - wr_coords[idx_base][1])

            rail_trains.append({
                "train_id": train["train_id"],
                "type": train["type"],
                "line": "Western Railway Suburban Trunk",
                "coordinates": [round(lon, 6), round(lat, 6), 5.0],
                "speed_kmh": round(65 + 20 * math.sin(elapsed * 0.8 + i), 1),
                "occupancy": train["occupancy"],
                "status": train["status"]
            })

        # 3. Update BEST Electric Buses
        buses = []
        for i, bus_route in enumerate(TRANSIT_DATA["best_buses"]):
            for b in bus_route["active_buses"]:
                base_c = b["current_coord"]
                # Slight micro-jitter around route
                delta_lon = 0.003 * math.sin(elapsed * 0.05 + i)
                delta_lat = 0.003 * math.cos(elapsed * 0.05 + i)
                buses.append({
                    "bus_id": b["bus_id"],
                    "route_no": bus_route["route_no"],
                    "coordinates": [round(base_c[0] + delta_lon, 6), round(base_c[1] + delta_lat, 6), 2.0],
                    "speed_kmh": round(max(10, b["speed_kmh"] + 5 * math.sin(elapsed)), 1),
                    "occupancy": b["occupancy"],
                    "destination": b["destination"]
                })

        # 4. Dynamic Road Traffic Fluctuations
        traffic_pulse = []
        for road in ROADS_DATA:
            variation = math.sin(elapsed * 0.2 + hash(road["id"]) % 10)
            cur_speed = max(12, int(road["avg_speed_kmh"] + variation * 6))
            level = "GREEN" if cur_speed > 45 else ("YELLOW" if cur_speed > 30 else ("ORANGE" if cur_speed > 20 else "RED"))
            traffic_pulse.append({
                "road_id": road["id"],
                "name": road["name"],
                "current_speed_kmh": cur_speed,
                "traffic_level": level
            })

        # 5. Live City Sensor Metrics
        grid_load_mw = round(3420 + 180 * math.sin(elapsed * 0.1), 1)
        water_flow_mld = round(3850 + 90 * math.cos(elapsed * 0.1), 1)
        aqi_index = round(142 + 12 * math.sin(elapsed * 0.05), 0)

        return {
            "type": "MAHATWIN_TELEMETRY_PULSE",
            "timestamp": timestamp_iso,
            "provenance": "SIMULATED_TELEMETRY",
            "data_mode": "SIMULATED",
            "freshness_ms": 45,
            "city_metrics": {
                "traffic_congestion_index": 68,
                "air_quality_index": aqi_index,
                "grid_load_mw": grid_load_mw,
                "water_supply_flow_mld": water_flow_mld,
                "active_incidents_count": 5,
                "transit_on_time_performance_pct": 96.4
            },
            "live_transit": {
                "metro_trains": metro_3_trains,
                "suburban_trains": rail_trains,
                "best_buses": buses
            },
            "road_traffic_pulse": traffic_pulse
        }

telemetry_hub = TelemetrySimulator()
