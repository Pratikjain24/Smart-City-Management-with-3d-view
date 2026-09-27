import React, { useState, useEffect, useRef } from 'react';
import { CesiumViewerManager } from './services/cesium/CesiumViewerManager';
import { RoadNetworkManager } from './services/cesium/RoadNetworkManager';
import { UtilityLayersManager } from './services/cesium/UtilityLayersManager';
import { TransitAnimator } from './services/cesium/TransitAnimator';
import { IncidentMarkersManager } from './services/cesium/IncidentMarkersManager';
import { EnvironmentLayersManager } from './services/cesium/EnvironmentLayersManager';
import { CivicFacilitiesManager } from './services/cesium/CivicFacilitiesManager';
import { TopNavBar } from './components/TopNavBar/TopNavBar';
import { LayerManager } from './components/LayerManager/LayerManager';
import { UniversalInspector } from './components/ObjectInspector/UniversalInspector';
import { TimeMachineBar } from './components/TimeMachine/TimeMachineBar';
import { ViewModeToolbar } from './components/ViewModeControls/ViewModeToolbar';
import { PerformanceHUD } from './components/Common/PerformanceHUD';
import { 
  TemporalMode, ViewMode, UtilityType, 
  LayerItem, CityMetrics, UniversalObjectInspection,
  TemporalScenario
} from './types/digital_twin';
import { api } from './services/api';
import { telemetryStream } from './services/websocket';
import type { ConnectionState } from './services/websocket';

export const App: React.FC = () => {
  const cesiumContainerRef = useRef<HTMLDivElement>(null);
  const viewerManagerRef = useRef<CesiumViewerManager | null>(null);
  const roadManagerRef = useRef<RoadNetworkManager | null>(null);
  const utilityManagerRef = useRef<UtilityLayersManager | null>(null);
  const transitManagerRef = useRef<TransitAnimator | null>(null);
  const incidentManagerRef = useRef<IncidentMarkersManager | null>(null);
  const envManagerRef = useRef<EnvironmentLayersManager | null>(null);
  const civicManagerRef = useRef<CivicFacilitiesManager | null>(null);

  // Application State
  const [temporalMode, setTemporalMode] = useState<TemporalMode>('LIVE');
  const [currentYear, setCurrentYear] = useState<number>(2026);
  const [viewMode, setViewMode] = useState<ViewMode>('SURFACE');
  const [undergroundDepth, setUndergroundDepth] = useState<number>(25);
  const [activeUtilityIsolation, setActiveUtilityIsolation] = useState<UtilityType | 'ALL' | null>(null);
  const [selectedInspection, setSelectedInspection] = useState<UniversalObjectInspection | null>(null);
  const [temporalScenarios, setTemporalScenarios] = useState<Record<string, TemporalScenario>>({});
  const [isGoogle3DLoaded, setIsGoogle3DLoaded] = useState<boolean>(false);
  const [connectionState, setConnectionState] = useState<ConnectionState>('disconnected');

  // Live Metrics
  const [cityMetrics, setCityMetrics] = useState<CityMetrics>({
    traffic_congestion_index: 68,
    air_quality_index: 142,
    grid_load_mw: 3420,
    water_supply_flow_mld: 3850,
    active_incidents_count: 5,
    transit_on_time_performance_pct: 96.4
  });

  // Layer Configuration
  const [layers, setLayers] = useState<LayerItem[]>([
    { id: 'layer_roads', name: 'Arterials & Highways', category: 'TRANSPORTATION', visible: true, opacity: 1.0, color: '#06b6d4', data_type: 'REALTIME' },
    { id: 'layer_metro', name: 'Mumbai Metro Lines', category: 'TRANSPORTATION', visible: true, opacity: 1.0, color: '#00A896', data_type: 'REALTIME' },
    { id: 'layer_rail', name: 'Suburban Railway Trunk', category: 'TRANSPORTATION', visible: true, opacity: 1.0, color: '#dc2626', data_type: 'REALTIME' },
    { id: 'layer_buses', name: 'BEST Electric Bus Fleet', category: 'TRANSPORTATION', visible: true, opacity: 1.0, color: '#f59e0b', data_type: 'REALTIME' },
    { id: 'layer_water', name: 'Bhandup Trunk Water Mains', category: 'WATER', visible: true, opacity: 1.0, color: '#38bdf8', data_type: 'AUTHORITATIVE' },
    { id: 'layer_sewer', name: 'MSDP Deep Sewer Tunnels', category: 'SEWERAGE', visible: true, opacity: 1.0, color: '#10b981', data_type: 'AUTHORITATIVE' },
    { id: 'layer_drainage', name: 'BRIMSTOWAD Storm SWD', category: 'DRAINAGE', visible: true, opacity: 1.0, color: '#818cf8', data_type: 'AUTHORITATIVE' },
    { id: 'layer_power', name: 'Tata 220kV Underground Grid', category: 'ELECTRICITY', visible: true, opacity: 1.0, color: '#f59e0b', data_type: 'REALTIME' },
    { id: 'layer_telecom', name: 'Core Dark Fiber Ring', category: 'TELECOM', visible: true, opacity: 1.0, color: '#ec4899', data_type: 'REALTIME' },
    { id: 'layer_civic', name: 'Hospitals & Emergency HQ', category: 'CIVIC', visible: true, opacity: 1.0, color: '#a855f7', data_type: 'AUTHORITATIVE' },
    { id: 'layer_incidents', name: 'Potholes & Road Incidents', category: 'INCIDENTS', visible: true, opacity: 1.0, color: '#ef4444', data_type: 'REALTIME' },
    { id: 'layer_aqi', name: 'SAFAR Air Quality Stations', category: 'ENVIRONMENT', visible: true, opacity: 1.0, color: '#14b8a6', data_type: 'REALTIME' },
    { id: 'layer_flood', name: 'Milan & Hindmata Flood Sumps', category: 'ENVIRONMENT', visible: true, opacity: 1.0, color: '#0284c7', data_type: 'REALTIME' }
  ]);

  // 1. Initialize Cesium 3D Engine & Managers
  useEffect(() => {
    if (!cesiumContainerRef.current) return;

    const viewerMgr = new CesiumViewerManager();
    const viewer = viewerMgr.initialize(cesiumContainerRef.current, (objectId, _entityType) => {
      handleInspectEntity(objectId);
    });

    viewerManagerRef.current = viewerMgr;
    viewerMgr.onTilesLoadedChange = (isGoogle) => setIsGoogle3DLoaded(isGoogle);
    roadManagerRef.current = new RoadNetworkManager(viewer);
    utilityManagerRef.current = new UtilityLayersManager(viewer);
    transitManagerRef.current = new TransitAnimator(viewer);
    incidentManagerRef.current = new IncidentMarkersManager(viewer);
    envManagerRef.current = new EnvironmentLayersManager(viewer);
    civicManagerRef.current = new CivicFacilitiesManager(viewer);

    // Initial cinematic zoom into Mumbai skyline
    setTimeout(() => {
      viewerMgr.flyToMumbaiIntro();
      setIsGoogle3DLoaded(viewerMgr.isGoogleTilesLoaded);
    }, 800);

    // 2. Fetch Initial Municipal Datasets
    const loadData = async () => {
      try {
        const [roadsRes, utilsRes, transitRes, incRes, envRes, tempRes, civicRes] = await Promise.all([
          api.getRoads(),
          api.getAllUtilities(),
          api.getTransitData(),
          api.getIncidents(),
          api.getEnvironmentSummary(),
          api.getTemporalScenarios(),
          api.getCivicFacilities()
        ]);

        if (roadManagerRef.current) roadManagerRef.current.renderRoads(roadsRes.data);
        if (utilityManagerRef.current) utilityManagerRef.current.renderUtilities(utilsRes.data);
        if (transitManagerRef.current) transitManagerRef.current.renderTransitNetwork(transitRes.data);
        if (incidentManagerRef.current) incidentManagerRef.current.renderIncidents(incRes.data);
        if (envManagerRef.current) envManagerRef.current.renderEnvironment(envRes.data.aqi_stations, envRes.data.flood_risk_hotspots);
        if (civicManagerRef.current) civicManagerRef.current.renderCivicFacilities(civicRes.data);
        if (tempRes.scenarios) setTemporalScenarios(tempRes.scenarios);
      } catch (err) {
        console.error('[MahaTwin] Data loading error:', err);
      }
    };

    loadData();

    // 3. Connect Live Telemetry WebSocket
    telemetryStream.connect();
    const unsubscribeConnection = telemetryStream.subscribeConnection(setConnectionState);
    const unsubscribe = telemetryStream.subscribe((payload) => {
      if (payload.type === 'MAHATWIN_TELEMETRY_PULSE') {
        if (payload.city_metrics) {
          setCityMetrics(payload.city_metrics);
        }
        if (payload.live_transit && transitManagerRef.current) {
          transitManagerRef.current.updateLiveVehicles(payload.live_transit);
        }
        if (payload.road_traffic_pulse && roadManagerRef.current) {
          roadManagerRef.current.updateTrafficPulse(payload.road_traffic_pulse);
        }
      }
    });

    return () => {
      unsubscribe();
      unsubscribeConnection();
      telemetryStream.disconnect();
      viewerMgr.destroy();
    };
  }, []);

  // Entity Inspection Handler
  const handleInspectEntity = async (objectId: string) => {
    try {
      const res = await api.inspectObject(objectId);
      setSelectedInspection(res.data);

      // If entity is a road, highlight connected roads
      if (roadManagerRef.current && res.data.category === 'ROAD_NETWORK') {
        const connIds = res.data.graph_connections.connected_roads?.map((r: any) => r.id) || [];
        roadManagerRef.current.highlightRoad(objectId, connIds);
      }
    } catch (e) {
      console.warn('Inspect entity failed:', e);
    }
  };

  // View Mode Switcher
  const handleSetViewMode = (mode: ViewMode) => {
    setViewMode(mode);
    if (viewerManagerRef.current) {
      viewerManagerRef.current.setViewMode(mode, undergroundDepth);
    }
    if (utilityManagerRef.current) {
      if (mode === 'UNDERGROUND') {
        utilityManagerRef.current.isolateUtility(null);
      }
    }
  };

  // Utility Isolation Handler
  const handleSelectUtilityIsolation = (type: UtilityType | 'ALL' | null) => {
    setActiveUtilityIsolation(type);
    if (type) {
      handleSetViewMode('UTILITY_ISOLATION');
      if (utilityManagerRef.current) {
        utilityManagerRef.current.isolateUtility(type);
      }
    } else {
      handleSetViewMode('SURFACE');
      if (utilityManagerRef.current) {
        utilityManagerRef.current.isolateUtility(null);
      }
    }
  };

  // Layer Toggles
  const setCesiumLayerVisibility = (layerId: string, visible: boolean) => {
    if (layerId === 'layer_roads') roadManagerRef.current?.setVisibility(visible);
    const utilityCategory: Record<string, UtilityType> = {
      layer_water: 'water', layer_sewer: 'sewer', layer_drainage: 'drainage',
      layer_power: 'electricity', layer_telecom: 'telecom'
    };
    if (utilityCategory[layerId]) utilityManagerRef.current?.setVisibility(visible, utilityCategory[layerId]);
    const transitKind: Record<string, 'metro' | 'rail' | 'buses'> = {
      layer_metro: 'metro', layer_rail: 'rail', layer_buses: 'buses'
    };
    if (transitKind[layerId]) transitManagerRef.current?.setVisibility(visible, transitKind[layerId]);
    if (layerId === 'layer_incidents') incidentManagerRef.current?.setVisibility(visible);
    if (layerId === 'layer_civic') civicManagerRef.current?.setVisibility(visible);
    if (layerId === 'layer_aqi') envManagerRef.current?.setVisibility(visible, 'aqi');
    if (layerId === 'layer_flood') envManagerRef.current?.setVisibility(visible, 'flood');
  };

  const handleToggleLayer = (layerId: string) => {
    const layer = layers.find((item) => item.id === layerId);
    if (!layer) return;
    const visible = !layer.visible;
    setLayers(prev => prev.map(l => l.id === layerId ? { ...l, visible } : l));
    setCesiumLayerVisibility(layerId, visible);
  };

  const handleIsolateLayer = (layerId: string) => {
    setLayers(prev => prev.map(l => ({ ...l, visible: l.id === layerId })));
    layers.forEach((layer) => setCesiumLayerVisibility(layer.id, layer.id === layerId));
  };

  // Search Selection Handler
  const handleSearchResultSelected = (item: any) => {
    if (item.coordinates && viewerManagerRef.current) {
      const [lon, lat] = item.coordinates;
      viewerManagerRef.current.flyToCoordinates(lon, lat, 750);
    }
    if (item.id) {
      handleInspectEntity(item.id);
    }
  };

  // Bookmark Fly-to
  const handleSelectBookmark = (key: string) => {
    if (viewerManagerRef.current) {
      viewerManagerRef.current.flyToBookmark(key);
    }
  };

  // Home Mumbai
  const handleResetHome = () => {
    if (viewerManagerRef.current) {
      viewerManagerRef.current.flyToMumbaiIntro();
      if (roadManagerRef.current) {
        roadManagerRef.current.highlightRoad(null);
      }
      setSelectedInspection(null);
    }
  };

  return (
    <div className="relative w-full h-full overflow-hidden bg-slate-950 font-sans">
      {/* 3D Cesium Viewport Container */}
      <div id="cesiumContainer" ref={cesiumContainerRef} className="w-full h-full" />

      {/* Top Navigation Bar */}
      <TopNavBar
        temporalMode={temporalMode}
        onSelectTemporalMode={(mode) => {
          setTemporalMode(mode);
          setCurrentYear(mode === 'HISTORICAL' ? 2020 : mode === 'LIVE' ? 2026 : 2028);
        }}
        cityMetrics={cityMetrics}
        onSearchResultSelected={handleSearchResultSelected}
      />

      {/* Performance & Coordinates HUD */}
      <PerformanceHUD isGoogle3DLoaded={isGoogle3DLoaded} connectionState={connectionState} />

      {/* Left Dock: Layer Manager */}
      <LayerManager
        layers={layers}
        onToggleLayer={handleToggleLayer}
        onIsolateLayer={handleIsolateLayer}
      />

      {/* Right Dock: Universal Object Inspector */}
      <UniversalInspector
        inspectionData={selectedInspection}
        onClose={() => {
          setSelectedInspection(null);
          if (roadManagerRef.current) roadManagerRef.current.highlightRoad(null);
        }}
        onSelectConnectedObject={(objId) => handleInspectEntity(objId)}
      />

      {/* Bottom Dock: 4D Time Machine */}
      <TimeMachineBar
        currentYear={currentYear}
        temporalMode={temporalMode}
        scenarios={temporalScenarios}
        onYearChange={(year) => {
          setCurrentYear(year);
          setTemporalMode(year < 2026 ? 'HISTORICAL' : year === 2026 ? 'LIVE' : 'FUTURE');
          roadManagerRef.current?.setTemporalFilter(year);
        }}
        onSelectScenario={(key) => {
          const scenario = temporalScenarios[key];
          if (scenario) {
            setCurrentYear(scenario.year);
            setTemporalMode(scenario.year < 2026 ? 'HISTORICAL' : scenario.year === 2026 ? 'LIVE' : 'FUTURE');
            roadManagerRef.current?.setTemporalFilter(scenario.year);
          }
        }}
      />

      {/* Floating Action Toolbar */}
      <ViewModeToolbar
        viewMode={viewMode}
        onSetViewMode={handleSetViewMode}
        undergroundDepth={undergroundDepth}
        onSetUndergroundDepth={(d) => {
          setUndergroundDepth(d);
          if (viewerManagerRef.current) viewerManagerRef.current.setViewMode(viewMode, d);
          if (utilityManagerRef.current) utilityManagerRef.current.setSubsurfaceDepth(d);
        }}
        activeUtilityIsolation={activeUtilityIsolation}
        onSelectUtilityIsolation={handleSelectUtilityIsolation}
        onSelectBookmark={handleSelectBookmark}
        onResetHome={handleResetHome}
      />
    </div>
  );
};

export default App;
