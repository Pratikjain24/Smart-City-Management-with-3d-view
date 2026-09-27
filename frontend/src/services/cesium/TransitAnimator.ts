import * as Cesium from 'cesium';

export class TransitAnimator {
  private viewer: Cesium.Viewer;
  private lineEntities: Map<string, Cesium.Entity> = new Map();
  private stationEntities: Map<string, Cesium.Entity> = new Map();
  private liveVehicleEntities: Map<string, Cesium.Entity> = new Map();
  private isVisible = true;

  constructor(viewer: Cesium.Viewer) {
    this.viewer = viewer;
  }

  public renderTransitNetwork(transitData: any) {
    this.clearLines();
    this.clearStations();

    // 1. Render Metro Lines & Underground Stations
    transitData.metro_lines?.forEach((line: any) => {
      const flatCoords: number[] = [];
      line.coordinates.forEach(([lon, lat, height = 15]: number[]) => {
        flatCoords.push(lon, lat, height);
      });

      const color = Cesium.Color.fromCssColorString(line.color || '#00A896');

      const entity = this.viewer.entities.add({
        id: line.id,
        name: line.name,
        polyline: {
          positions: Cesium.Cartesian3.fromDegreesArrayHeights(flatCoords),
          width: 6,
          material: new Cesium.PolylineGlowMaterialProperty({
            glowPower: 0.3,
            color: color,
            taperPower: 1.0
          }),
          clampToGround: false
        },
        properties: {
          category: 'TRANSIT_METRO',
          layerKind: 'metro',
          transitData: line
        }
      });

      this.lineEntities.set(line.id, entity);

      // Render Metro Stations
      line.stations?.forEach((st: any) => {
        const [lon, lat, height = -15] = st.coords;
        const stId = `${line.id}_${st.name.toLowerCase().replace(/\s+/g, '_')}`;

        const stEntity = this.viewer.entities.add({
          id: stId,
          name: `Station: ${st.name}`,
          position: Cesium.Cartesian3.fromDegrees(lon, lat, height),
          point: {
            pixelSize: 10,
            color: Cesium.Color.WHITE,
            outlineColor: color,
            outlineWidth: 3,
            disableDepthTestDistance: Number.POSITIVE_INFINITY
          },
          label: {
            text: `Ⓜ️ ${st.name}`,
            font: '10px Inter, sans-serif',
            fillColor: Cesium.Color.WHITE,
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 2,
            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            pixelOffset: new Cesium.Cartesian2(0, -8),
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
            distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0, 20000)
          },
          properties: {
            category: 'TRANSIT_STATION',
            layerKind: 'metro',
            stationData: st
          }
        });

        this.stationEntities.set(stId, stEntity);
      });
    });

    // 2. Render Suburban Railways & Stations
    transitData.suburban_railway?.forEach((rail: any) => {
      const flatCoords: number[] = [];
      rail.coordinates.forEach(([lon, lat]: number[]) => {
        flatCoords.push(lon, lat, 6.0);
      });

      const color = Cesium.Color.fromCssColorString(rail.color || '#dc2626');

      const entity = this.viewer.entities.add({
        id: rail.id,
        name: rail.name,
        polyline: {
          positions: Cesium.Cartesian3.fromDegreesArrayHeights(flatCoords),
          width: 7,
          material: new Cesium.PolylineOutlineMaterialProperty({
            color: color,
            outlineColor: Cesium.Color.WHITE,
            outlineWidth: 2
          }),
          clampToGround: false
        },
        properties: {
          category: 'TRANSIT_RAIL',
          layerKind: 'rail',
          transitData: rail
        }
      });

      this.lineEntities.set(rail.id, entity);

      // Render Rail Stations
      rail.stations?.forEach((st: any) => {
        const [lon, lat, height = 6.0] = st.coords;
        const stId = `${rail.id}_${st.name.toLowerCase().replace(/\s+/g, '_')}`;

        const stEntity = this.viewer.entities.add({
          id: stId,
          name: `Station: ${st.name}`,
          position: Cesium.Cartesian3.fromDegrees(lon, lat, height),
          point: {
            pixelSize: 11,
            color: Cesium.Color.WHITE,
            outlineColor: color,
            outlineWidth: 3,
            disableDepthTestDistance: Number.POSITIVE_INFINITY
          },
          label: {
            text: `🚉 ${st.name}`,
            font: '10px Inter, sans-serif',
            fillColor: Cesium.Color.WHITE,
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 2,
            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            pixelOffset: new Cesium.Cartesian2(0, -8),
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
            distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0, 22000)
          },
          properties: {
            category: 'TRANSIT_STATION',
            layerKind: 'rail',
            stationData: st
          }
        });

        this.stationEntities.set(stId, stEntity);
      });
    });
  }

  public updateLiveVehicles(liveData: { metro_trains?: any[]; suburban_trains?: any[]; best_buses?: any[] }) {
    if (!this.isVisible) return;

    // 1. Update Metro Trains
    liveData.metro_trains?.forEach((train) => {
      const [lon, lat, height = -20] = train.coordinates;
      this.upsertVehicleMarker(
        `veh_${train.train_id}`,
        train.train_id,
        lon, lat, height,
        '#00A896',
        `🚇 ${train.train_id} (${train.speed_kmh} km/h)`,
        'TRANSIT_METRO_TRAIN',
        train
      );
    });

    // 2. Update Suburban Rail Fast/Slow Trains
    liveData.suburban_trains?.forEach((train) => {
      const [lon, lat, height = 6] = train.coordinates;
      this.upsertVehicleMarker(
        `veh_${train.train_id}`,
        train.train_id,
        lon, lat, height,
        '#dc2626',
        `🚆 ${train.train_id} (${train.speed_kmh} km/h)`,
        'TRANSIT_RAIL_TRAIN',
        train
      );
    });

    // 3. Update BEST Electric Buses
    liveData.best_buses?.forEach((bus) => {
      const [lon, lat, height = 4] = bus.coordinates;
      this.upsertVehicleMarker(
        `veh_${bus.bus_id}`,
        bus.bus_id,
        lon, lat, height,
        '#f59e0b',
        `🚌 ${bus.route_no} (${bus.speed_kmh} km/h)`,
        'TRANSIT_BUS',
        bus
      );
    });
  }

  private upsertVehicleMarker(
    id: string,
    label: string,
    lon: number,
    lat: number,
    height: number,
    colorHex: string,
    labelText: string,
    category: string,
    vehicleData: any
  ) {
    const position = Cesium.Cartesian3.fromDegrees(lon, lat, height);
    const color = Cesium.Color.fromCssColorString(colorHex);

    if (this.liveVehicleEntities.has(id)) {
      const entity = this.liveVehicleEntities.get(id)!;
      entity.position = new Cesium.ConstantPositionProperty(position);
    } else {
      const entity = this.viewer.entities.add({
        id: id,
        name: label,
        position: position,
        point: {
          pixelSize: 14,
          color: color,
          outlineColor: Cesium.Color.WHITE,
          outlineWidth: 2,
          disableDepthTestDistance: Number.POSITIVE_INFINITY
        },
        label: {
          text: labelText,
          font: '11px Outfit, sans-serif',
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 3,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          pixelOffset: new Cesium.Cartesian2(0, -10),
          disableDepthTestDistance: Number.POSITIVE_INFINITY,
          distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0, 15000)
        },
        properties: {
          category: category,
          layerKind: category === 'TRANSIT_BUS' ? 'buses' : category === 'TRANSIT_METRO_TRAIN' ? 'metro' : 'rail',
          vehicleData: vehicleData
        }
      });

      this.liveVehicleEntities.set(id, entity);
    }
  }

  public setVisibility(visible: boolean, layer?: 'metro' | 'rail' | 'buses') {
    if (!layer) this.isVisible = visible;
    this.lineEntities.forEach((entity) => {
      if (!layer || entity.properties?.layerKind?.getValue() === layer) entity.show = visible;
    });
    this.stationEntities.forEach((entity) => {
      if (!layer || entity.properties?.layerKind?.getValue() === layer) entity.show = visible;
    });
    this.liveVehicleEntities.forEach((entity) => {
      if (!layer || entity.properties?.layerKind?.getValue() === layer) entity.show = visible;
    });
  }

  public clearLines() {
    this.lineEntities.forEach((entity) => {
      this.viewer.entities.remove(entity);
    });
    this.lineEntities.clear();
  }

  public clearStations() {
    this.stationEntities.forEach((entity) => {
      this.viewer.entities.remove(entity);
    });
    this.stationEntities.clear();
  }

  public clearVehicles() {
    this.liveVehicleEntities.forEach((entity) => {
      this.viewer.entities.remove(entity);
    });
    this.liveVehicleEntities.clear();
  }

  public clear() {
    this.clearLines();
    this.clearStations();
    this.clearVehicles();
  }
}
