import * as Cesium from 'cesium';
import { RoadFeature } from '../../types/digital_twin';

export class RoadNetworkManager {
  private viewer: Cesium.Viewer;
  private roadEntities: Map<string, Cesium.Entity> = new Map();
  private selectedRoadId: string | null = null;
  private currentConnectedIds: string[] = [];

  constructor(viewer: Cesium.Viewer) {
    this.viewer = viewer;
  }

  public renderRoads(roads: RoadFeature[]) {
    this.clear();

    roads.forEach((road) => {
      const flatCoords: number[] = [];
      road.coordinates.forEach(([lon, lat]) => {
        flatCoords.push(lon, lat, 4.0); // 4 meters above ground
      });

      const color = this.getTrafficColor(road.traffic_level);

      const entity = this.viewer.entities.add({
        id: road.id,
        name: road.name,
        polyline: {
          positions: Cesium.Cartesian3.fromDegreesArrayHeights(flatCoords),
          width: 5,
          material: new Cesium.PolylineGlowMaterialProperty({
            glowPower: 0.25,
            color: color,
            taperPower: 1.0
          }),
          clampToGround: false
        },
        properties: {
          category: 'ROAD_NETWORK',
          roadData: road
        }
      });

      this.roadEntities.set(road.id, entity);
    });
  }

  public highlightRoad(roadId: string | null, connectedRoadIds: string[] = []) {
    this.selectedRoadId = roadId;
    this.currentConnectedIds = connectedRoadIds;

    this.roadEntities.forEach((entity, id) => {
      if (!entity.polyline) return;

      const roadData: RoadFeature = entity.properties?.roadData?.getValue();
      const baseColor = roadData ? this.getTrafficColor(roadData.traffic_level) : Cesium.Color.CYAN;

      if (id === roadId) {
        // Selected road: thick vibrant cyan glow
        entity.polyline.width = new Cesium.ConstantProperty(10);
        entity.polyline.material = new Cesium.PolylineGlowMaterialProperty({
          glowPower: 0.45,
          color: Cesium.Color.fromCssColorString('#38bdf8'),
          taperPower: 1.0
        });
      } else if (connectedRoadIds.includes(id)) {
        // Connected road: pulsing purple/violet glow
        entity.polyline.width = new Cesium.ConstantProperty(7);
        entity.polyline.material = new Cesium.PolylineGlowMaterialProperty({
          glowPower: 0.35,
          color: Cesium.Color.fromCssColorString('#c084fc'),
          taperPower: 1.0
        });
      } else {
        // Unselected normal road
        entity.polyline.width = new Cesium.ConstantProperty(5);
        entity.polyline.material = new Cesium.PolylineGlowMaterialProperty({
          glowPower: 0.2,
          color: baseColor.withAlpha(this.selectedRoadId ? 0.4 : 1.0),
          taperPower: 1.0
        });
      }
    });
  }

  public updateTrafficPulse(pulseData: { road_id: string; current_speed_kmh: number; traffic_level: string }[]) {
    if (!pulseData || pulseData.length === 0) return;

    pulseData.forEach((pulse) => {
      const entity = this.roadEntities.get(pulse.road_id);
      if (!entity || !entity.polyline) return;

      // Don't override highlight styling on selected / connected roads
      if (this.selectedRoadId === pulse.road_id || this.currentConnectedIds.includes(pulse.road_id)) {
        return;
      }

      const color = this.getTrafficColor(pulse.traffic_level);
      entity.polyline.material = new Cesium.PolylineGlowMaterialProperty({
        glowPower: 0.25,
        color: color.withAlpha(this.selectedRoadId ? 0.4 : 1.0),
        taperPower: 1.0
      });
    });
  }

  public setTemporalFilter(year: number) {
    this.roadEntities.forEach((entity, id) => {
      // Historical Coastal Road pre-reclamation state (2020)
      if (id === 'road_coastal_01') {
        if (year <= 2021) {
          // Pre-reclamation: Dimmed / Under Sea Wall Construction
          if (entity.polyline) {
            entity.polyline.width = new Cesium.ConstantProperty(3);
            entity.polyline.material = new Cesium.PolylineGlowMaterialProperty({
              glowPower: 0.2,
              color: Cesium.Color.fromCssColorString('#f59e0b').withAlpha(0.5), // Construction Amber
              taperPower: 0.5
            });
          }
        } else {
          // Post-2024 / 2026: Fully operational Coastal Highway
          if (entity.polyline && id !== this.selectedRoadId) {
            entity.polyline.width = new Cesium.ConstantProperty(5);
            entity.polyline.material = new Cesium.PolylineGlowMaterialProperty({
              glowPower: 0.3,
              color: Cesium.Color.fromCssColorString('#10b981'),
              taperPower: 1.0
            });
          }
        }
      }
    });
  }

  public setVisibility(visible: boolean) {
    this.roadEntities.forEach((entity) => {
      entity.show = visible;
    });
  }

  private getTrafficColor(level: string): Cesium.Color {
    switch (level) {
      case 'GREEN':
        return Cesium.Color.fromCssColorString('#10b981');
      case 'YELLOW':
        return Cesium.Color.fromCssColorString('#eab308');
      case 'ORANGE':
        return Cesium.Color.fromCssColorString('#f97316');
      case 'RED':
        return Cesium.Color.fromCssColorString('#ef4444');
      default:
        return Cesium.Color.fromCssColorString('#06b6d4');
    }
  }

  public clear() {
    this.roadEntities.forEach((entity) => {
      this.viewer.entities.remove(entity);
    });
    this.roadEntities.clear();
  }
}
