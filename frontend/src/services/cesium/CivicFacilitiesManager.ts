import * as Cesium from 'cesium';

export interface CivicFacility {
  id: string;
  name: string;
  category: string;
  type: string;
  beds?: number;
  emergency_trauma_level?: string;
  coordinates: [number, number];
  data_provenance?: string;
  freshness?: string;
}

export class CivicFacilitiesManager {
  private viewer: Cesium.Viewer;
  private facilityEntities: Map<string, Cesium.Entity> = new Map();

  constructor(viewer: Cesium.Viewer) {
    this.viewer = viewer;
  }

  public renderCivicFacilities(facilities: CivicFacility[]) {
    this.clear();

    facilities.forEach((fac) => {
      const [lon, lat] = fac.coordinates;
      const isHospital = fac.type === 'HOSPITAL';
      const isPolice = fac.type === 'POLICE_HQ';
      const color = isHospital
        ? Cesium.Color.fromCssColorString('#a855f7') // Purple for Hospital
        : isPolice
        ? Cesium.Color.fromCssColorString('#3b82f6') // Blue for Police
        : Cesium.Color.fromCssColorString('#f59e0b'); // Amber for Command Center

      const iconPrefix = isHospital ? '🏥' : isPolice ? '👮' : '🚨';

      const entity = this.viewer.entities.add({
        id: fac.id,
        name: fac.name,
        position: Cesium.Cartesian3.fromDegrees(lon, lat, 15.0),
        point: {
          pixelSize: 16,
          color: color,
          outlineColor: Cesium.Color.WHITE,
          outlineWidth: 3,
          disableDepthTestDistance: Number.POSITIVE_INFINITY
        },
        label: {
          text: `${iconPrefix} ${fac.name.split(' ')[0]}`,
          font: 'bold 11px Inter, sans-serif',
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.fromCssColorString('#020617'),
          outlineWidth: 3,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          pixelOffset: new Cesium.Cartesian2(0, -12),
          disableDepthTestDistance: Number.POSITIVE_INFINITY,
          distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0, 35000)
        },
        properties: {
          category: `CIVIC_${fac.type}`,
          facilityData: fac
        }
      });

      this.facilityEntities.set(fac.id, entity);
    });
  }

  public setVisibility(visible: boolean) {
    this.facilityEntities.forEach((entity) => {
      entity.show = visible;
    });
  }

  public clear() {
    this.facilityEntities.forEach((entity) => {
      this.viewer.entities.remove(entity);
    });
    this.facilityEntities.clear();
  }
}
