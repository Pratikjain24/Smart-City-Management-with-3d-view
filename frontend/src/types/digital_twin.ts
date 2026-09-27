export type TemporalMode = 'HISTORICAL' | 'LIVE' | 'FUTURE';
export type ViewMode = 'SURFACE' | 'UNDERGROUND' | 'UTILITY_ISOLATION';
export type UtilityType = 'water' | 'sewer' | 'drainage' | 'electricity' | 'telecom';

export interface RoadFeature {
  id: string;
  name: string;
  type: string;
  category: string;
  lanes: number;
  speed_limit_kmh: number;
  avg_speed_kmh: number;
  traffic_status: string;
  traffic_level: 'GREEN' | 'YELLOW' | 'ORANGE' | 'RED';
  road_condition: string;
  construction_status: string;
  maintenance_status: string;
  known_incidents: number;
  data_provenance: string;
  freshness: string;
  coordinates: number[][];
  connected_road_ids: string[];
  connected_roads_resolved?: {
    id: string;
    name: string;
    type: string;
    traffic_level: string;
    avg_speed_kmh: number;
  }[];
  nearby_intersections: string[];
  signals: string[];
  nearby_infrastructure: {
    bus_stops?: string[];
    railway_stations?: string[];
    metro?: string[];
    hospitals?: string[];
    utilities?: string[];
  };
}

export interface UtilityAsset {
  id: string;
  name: string;
  type: string;
  utility_type: 'WATER' | 'SEWER' | 'DRAINAGE' | 'ELECTRICITY' | 'TELECOM';
  depth_meters: number;
  status: string;
  data_provenance: string;
  freshness: string;
  coordinates: number[][];
  upstream_source?: string;
  downstream_zones?: string[];
  connected_assets?: string[];
  diameter_mm?: number;
  pressure_bar?: number;
  flow_rate_m3h?: number;
  voltage_kv?: number;
  current_load_mva?: number;
  fiber_count?: number;
}

export interface IncidentAlert {
  id: string;
  category: string;
  severity: 'CRITICAL' | 'HIGH' | 'WARNING' | 'MODERATE' | 'LOW';
  severity_score: number;
  title: string;
  location_name: string;
  coordinates: [number, number];
  related_road_id?: string;
  timestamp: string;
  status: string;
  source: string;
  reported_by: string;
  image_url?: string;
  work_order_id?: string;
  estimated_resolution?: string;
  data_provenance: string;
  freshness: string;
}

export interface AQIStation {
  id: string;
  name: string;
  coordinates: [number, number];
  aqi: number;
  category: string;
  pm25: number;
  pm10: number;
  no2: number;
  temp_c: number;
  humidity_pct: number;
  status: string;
}

export interface FloodRiskHotspot {
  id: string;
  name: string;
  coordinates: [number, number];
  risk_level: 'CRITICAL' | 'HIGH' | 'MODERATE' | 'LOW';
  tide_sensitivity: string;
  mitigation_installed: string;
  status: string;
}

export interface TransitVehicle {
  id: string;
  type: string;
  line_or_route: string;
  coordinates: [number, number, number];
  speed_kmh: number;
  occupancy?: string | number;
  status: string;
}

export interface UniversalObjectInspection {
  object_id: string;
  name: string;
  category: string;
  sub_type: string;
  status: string;
  data_provenance: string;
  freshness: string;
  details: Record<string, any>;
  graph_connections: {
    connected_roads?: any[];
    nearby_infrastructure?: Record<string, string[]>;
    upstream_source?: string;
    downstream_zones?: string[];
    connected_assets?: string[];
    stations?: any[];
    active_trains?: any[];
    incidents?: any[];
    related_road?: any;
  };
}

export interface LayerItem {
  id: string;
  name: string;
  category: 'TRANSPORTATION' | 'WATER' | 'SEWERAGE' | 'DRAINAGE' | 'ELECTRICITY' | 'TELECOM' | 'CIVIC' | 'INCIDENTS' | 'ENVIRONMENT';
  visible: boolean;
  opacity: number;
  color: string;
  count?: number;
  data_type: 'REALTIME' | 'AUTHORITATIVE' | 'SIMULATED' | 'SAMPLE';
}

export interface CityMetrics {
  traffic_congestion_index: number;
  air_quality_index: number;
  grid_load_mw: number;
  water_supply_flow_mld: number;
  active_incidents_count: number;
  transit_on_time_performance_pct: number;
}

export interface TemporalScenario {
  year: number;
  title: string;
  description: string;
  coastal_road_status: string;
  metro_line_3_status: string;
  avg_peak_commute_mins: number;
  air_quality_avg_aqi: number;
}
