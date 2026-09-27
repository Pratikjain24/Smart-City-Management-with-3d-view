import { 
  RoadFeature, UtilityAsset, IncidentAlert, 
  AQIStation, FloodRiskHotspot, UniversalObjectInspection,
  TemporalScenario 
} from '../types/digital_twin';

const API_BASE = '/api/v1';

export const api = {
  // Cities & Boundaries
  async getMumbaiMetadata() {
    const res = await fetch(`${API_BASE}/cities/mumbai`);
    return res.json();
  },

  // Roads
  async getRoads(): Promise<{ data: RoadFeature[] }> {
    const res = await fetch(`${API_BASE}/roads`);
    return res.json();
  },

  async getRoadById(roadId: string): Promise<{ data: RoadFeature }> {
    const res = await fetch(`${API_BASE}/roads/${roadId}`);
    return res.json();
  },

  // Utilities
  async getAllUtilities(): Promise<{ data: Record<string, UtilityAsset[]> }> {
    const res = await fetch(`${API_BASE}/utilities/all`);
    return res.json();
  },

  async getUtilitiesByCategory(category: string): Promise<{ data: UtilityAsset[] }> {
    const res = await fetch(`${API_BASE}/utilities/${category}`);
    return res.json();
  },

  // Public Transit
  async getTransitData() {
    const res = await fetch(`${API_BASE}/transport/all`);
    return res.json();
  },

  // Incidents
  async getIncidents(): Promise<{ data: IncidentAlert[] }> {
    const res = await fetch(`${API_BASE}/incidents`);
    return res.json();
  },

  // Environment
  async getEnvironmentSummary(): Promise<{ 
    data: { 
      aqi_stations: AQIStation[]; 
      flood_risk_hotspots: FloodRiskHotspot[] 
    } 
  }> {
    const res = await fetch(`${API_BASE}/environment/summary`);
    return res.json();
  },

  // Civic Facilities (Hospitals, Emergency Command Centers, Police HQ)
  async getCivicFacilities(): Promise<{ data: any[] }> {
    const res = await fetch(`${API_BASE}/civic`);
    return res.json();
  },

  // Universal Inspector
  async inspectObject(objectId: string): Promise<{ data: UniversalObjectInspection }> {
    const res = await fetch(`${API_BASE}/objects/${objectId}`);
    return res.json();
  },

  // Search
  async search(query: string) {
    const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
    return res.json();
  },

  // Temporal
  async getTemporalScenarios(): Promise<{ scenarios: Record<string, TemporalScenario> }> {
    const res = await fetch(`${API_BASE}/temporal/scenarios`);
    return res.json();
  }
};
