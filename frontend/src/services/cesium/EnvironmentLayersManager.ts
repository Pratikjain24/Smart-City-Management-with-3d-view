import * as Cesium from 'cesium';
import { AQIStation, FloodRiskHotspot } from '../../types/digital_twin';

export class EnvironmentLayersManager {
  private viewer: Cesium.Viewer;
  private aqiEntities: Map<string, Cesium.Entity> = new Map();
  private floodEntities: Map<string, Cesium.Entity> = new Map();

  constructor(viewer: Cesium.Viewer) {
    this.viewer = viewer;
  }

  public renderEnvironment(aqiStations: AQIStation[], floodHotspots: FloodRiskHotspot[]) {
    this.clear();

    // 1. Render AQI Stations as heat cylinders
    aqiStations.forEach((station) => {
      const [lon, lat] = station.coordinates;
      const color = this.getAqiColor(station.aqi);

      const entity = this.viewer.entities.add({
        id: station.id,
        name: station.name,
        position: Cesium.Cartesian3.fromDegrees(lon, lat, 20),
        cylinder: {
          length: 50,
          topRadius: 300,
          bottomRadius: 300,
          material: color.withAlpha(0.35),
          outline: true,
          outlineColor: color
        },
        label: {
          text: `AQI ${station.aqi} • ${station.name.split(' ')[0]}`,
          font: 'bold 11px Inter, sans-serif',
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 3,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          pixelOffset: new Cesium.Cartesian2(0, -30),
          distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0, 45000)
        },
        properties: {
          category: 'ENVIRONMENT_AQI',
          aqiData: station
        }
      });

      this.aqiEntities.set(station.id, entity);
    });

    // 2. Render Flood Risk Hotspots
    floodHotspots.forEach((spot) => {
      const [lon, lat] = spot.coordinates;
      const entity = this.viewer.entities.add({
        id: spot.id,
        name: spot.name,
        position: Cesium.Cartesian3.fromDegrees(lon, lat, 5),
        ellipse: {
          semiMinorAxis: 180,
          semiMajorAxis: 180,
          material: Cesium.Color.fromCssColorString('#0284c7').withAlpha(0.4),
          outline: true,
          outlineColor: Cesium.Color.CYAN
        },
        label: {
          text: `🌊 Flood Sump: ${spot.name}`,
          font: '10px Inter, sans-serif',
          fillColor: Cesium.Color.fromCssColorString('#38bdf8'),
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 2,
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          pixelOffset: new Cesium.Cartesian2(0, -10)
        },
        properties: {
          category: 'ENVIRONMENT_FLOOD',
          floodData: spot
        }
      });

      this.floodEntities.set(spot.id, entity);
    });
  }

  public setVisibility(visible: boolean, layer?: 'aqi' | 'flood') {
    if (!layer || layer === 'aqi') this.aqiEntities.forEach((e) => { e.show = visible; });
    if (!layer || layer === 'flood') this.floodEntities.forEach((e) => { e.show = visible; });
  }

  private getAqiColor(aqi: number): Cesium.Color {
    if (aqi <= 50) return Cesium.Color.fromCssColorString('#10b981'); // Good
    if (aqi <= 100) return Cesium.Color.fromCssColorString('#84cc16'); // Satisfactory
    if (aqi <= 200) return Cesium.Color.fromCssColorString('#eab308'); // Moderate
    if (aqi <= 300) return Cesium.Color.fromCssColorString('#f97316'); // Poor
    return Cesium.Color.fromCssColorString('#ef4444'); // Very Poor / Severe
  }

  public clear() {
    this.aqiEntities.forEach((e) => this.viewer.entities.remove(e));
    this.aqiEntities.clear();
    this.floodEntities.forEach((e) => this.viewer.entities.remove(e));
    this.floodEntities.clear();
  }
}
