import * as Cesium from 'cesium';
import { UtilityAsset, UtilityType } from '../../types/digital_twin';

export class UtilityLayersManager {
  private viewer: Cesium.Viewer;
  private utilityEntities: Map<string, Cesium.Entity> = new Map();
  private activeCategoryFilter: string | null = null;
  private currentMaxDepth: number = 50;

  constructor(viewer: Cesium.Viewer) {
    this.viewer = viewer;
  }

  public renderUtilities(utilitiesByCategory: Record<string, UtilityAsset[]>) {
    this.clear();

    Object.entries(utilitiesByCategory).forEach(([category, assets]) => {
      const baseColor = this.getUtilityColor(category);

      assets.forEach((asset) => {
        if (asset.coordinates.length > 1) {
          // Render as 3D subsurface pipeline corridor
          const flatCoords: number[] = [];
          asset.coordinates.forEach((coord) => {
            const lon = coord[0];
            const lat = coord[1];
            const height = coord.length >= 3 ? coord[2] : (asset.depth_meters || -5);
            flatCoords.push(lon, lat, height);
          });

          const entity = this.viewer.entities.add({
            id: asset.id,
            name: asset.name,
            polyline: {
              positions: Cesium.Cartesian3.fromDegreesArrayHeights(flatCoords),
              width: 8,
              material: new Cesium.PolylineGlowMaterialProperty({
                glowPower: 0.35,
                color: baseColor,
                taperPower: 0.8
              }),
              clampToGround: false
            },
            properties: {
              category: `UTILITY_${asset.utility_type}`,
              utilityType: category,
              depthMeters: Math.abs(asset.depth_meters || 5),
              utilityData: asset
            }
          });

          this.utilityEntities.set(asset.id, entity);
        } else if (asset.coordinates.length === 1) {
          // Render as 3D node / plant / reservoir
          const [lon, lat, height = 0] = asset.coordinates[0];
          const entity = this.viewer.entities.add({
            id: asset.id,
            name: asset.name,
            position: Cesium.Cartesian3.fromDegrees(lon, lat, height),
            cylinder: {
              length: 25,
              topRadius: 18,
              bottomRadius: 18,
              material: baseColor.withAlpha(0.85),
              outline: true,
              outlineColor: Cesium.Color.WHITE
            },
            properties: {
              category: `UTILITY_${asset.utility_type}`,
              utilityType: category,
              depthMeters: Math.abs(asset.depth_meters || 0),
              utilityData: asset
            }
          });

          this.utilityEntities.set(asset.id, entity);
        }
      });
    });
  }

  public isolateUtility(category: UtilityType | 'ALL' | null) {
    this.activeCategoryFilter = category === 'ALL' ? null : category;
    this.applyFiltering();
  }

  public setSubsurfaceDepth(maxDepthMeters: number) {
    this.currentMaxDepth = maxDepthMeters;
    this.applyFiltering();
  }

  private applyFiltering() {
    this.utilityEntities.forEach((entity) => {
      const uType = entity.properties?.utilityType?.getValue();
      const depth = entity.properties?.depthMeters?.getValue() || 0;
      const baseColor = this.getUtilityColor(uType);

      const matchesCategory = !this.activeCategoryFilter || this.activeCategoryFilter === uType;
      const withinDepth = depth <= this.currentMaxDepth;

      if (matchesCategory && withinDepth) {
        // Active & Focused
        entity.show = true;
        if (entity.polyline) {
          entity.polyline.width = new Cesium.ConstantProperty(this.activeCategoryFilter ? 10 : 8);
          entity.polyline.material = new Cesium.PolylineGlowMaterialProperty({
            glowPower: this.activeCategoryFilter ? 0.45 : 0.35,
            color: baseColor,
            taperPower: 0.8
          });
        }
        if (entity.cylinder) {
          entity.cylinder.material = new Cesium.ColorMaterialProperty(baseColor.withAlpha(0.85));
        }
      } else if (!matchesCategory && withinDepth) {
        // Subdued / dimmed for other non-isolated categories
        entity.show = true;
        if (entity.polyline) {
          entity.polyline.width = new Cesium.ConstantProperty(3);
          entity.polyline.material = new Cesium.PolylineGlowMaterialProperty({
            glowPower: 0.1,
            color: baseColor.withAlpha(0.12),
            taperPower: 1.0
          });
        }
        if (entity.cylinder) {
          entity.cylinder.material = new Cesium.ColorMaterialProperty(baseColor.withAlpha(0.12));
        }
      } else {
        // Exceeds depth cutaway
        entity.show = false;
      }
    });
  }

  public setVisibility(visible: boolean, category?: UtilityType) {
    this.utilityEntities.forEach((entity) => {
      const utilityType = entity.properties?.utilityType?.getValue();
      if (!category || utilityType === category) entity.show = visible;
    });
  }

  public getUtilityColor(category: string): Cesium.Color {
    switch (category.toLowerCase()) {
      case 'water':
        return Cesium.Color.fromCssColorString('#38bdf8'); // Blue
      case 'sewer':
        return Cesium.Color.fromCssColorString('#10b981'); // Emerald
      case 'drainage':
        return Cesium.Color.fromCssColorString('#818cf8'); // Indigo
      case 'electricity':
        return Cesium.Color.fromCssColorString('#f59e0b'); // Amber
      case 'telecom':
        return Cesium.Color.fromCssColorString('#ec4899'); // Pink
      default:
        return Cesium.Color.fromCssColorString('#06b6d4');
    }
  }

  public clear() {
    this.utilityEntities.forEach((entity) => {
      this.viewer.entities.remove(entity);
    });
    this.utilityEntities.clear();
  }
}
