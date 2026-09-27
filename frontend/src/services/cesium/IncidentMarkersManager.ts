import * as Cesium from 'cesium';
import { IncidentAlert } from '../../types/digital_twin';

export class IncidentMarkersManager {
  private viewer: Cesium.Viewer;
  private incidentEntities: Map<string, Cesium.Entity> = new Map();

  constructor(viewer: Cesium.Viewer) {
    this.viewer = viewer;
  }

  public renderIncidents(incidents: IncidentAlert[]) {
    this.clear();

    incidents.forEach((inc) => {
      const [lon, lat] = inc.coordinates;
      const color = this.getSeverityColor(inc.severity);

      const entity = this.viewer.entities.add({
        id: inc.id,
        name: inc.title,
        position: Cesium.Cartesian3.fromDegrees(lon, lat, 10.0),
        point: {
          pixelSize: 18,
          color: color,
          outlineColor: Cesium.Color.WHITE,
          outlineWidth: 3,
          disableDepthTestDistance: Number.POSITIVE_INFINITY
        },
        label: {
          text: `⚠️ ${inc.category.split('/')[0]}`,
          font: 'bold 12px Inter, sans-serif',
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.fromCssColorString('#020617'),
          outlineWidth: 4,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          pixelOffset: new Cesium.Cartesian2(0, -14),
          disableDepthTestDistance: Number.POSITIVE_INFINITY,
          distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0, 30000)
        },
        properties: {
          category: 'INCIDENT_ALERT',
          incidentData: inc
        }
      });

      this.incidentEntities.set(inc.id, entity);
    });
  }

  public setVisibility(visible: boolean) {
    this.incidentEntities.forEach((entity) => {
      entity.show = visible;
    });
  }

  private getSeverityColor(severity: string): Cesium.Color {
    switch (severity.toUpperCase()) {
      case 'CRITICAL':
        return Cesium.Color.fromCssColorString('#ef4444');
      case 'HIGH':
        return Cesium.Color.fromCssColorString('#f97316');
      case 'WARNING':
        return Cesium.Color.fromCssColorString('#f59e0b');
      case 'MODERATE':
        return Cesium.Color.fromCssColorString('#eab308');
      default:
        return Cesium.Color.fromCssColorString('#3b82f6');
    }
  }

  public clear() {
    this.incidentEntities.forEach((entity) => {
      this.viewer.entities.remove(entity);
    });
    this.incidentEntities.clear();
  }
}
