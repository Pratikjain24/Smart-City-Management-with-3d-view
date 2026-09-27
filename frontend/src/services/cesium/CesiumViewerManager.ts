import * as Cesium from 'cesium';
import { ViewMode } from '../../types/digital_twin';

export interface CameraBookmark {
  name: string;
  destination: {
    longitude: number;
    latitude: number;
    height: number;
  };
  orientation: {
    heading: number;
    pitch: number;
    roll: number;
  };
}

export const MUMBAI_BOOKMARKS: Record<string, CameraBookmark> = {
  mumbai_overview: {
    name: "Mumbai Panoramic Skyview",
    destination: { longitude: 72.8400, latitude: 19.0300, height: 16000 },
    orientation: { heading: 0, pitch: -55, roll: 0 }
  },
  marine_drive: {
    name: "Marine Drive & Queen's Necklace",
    destination: { longitude: 72.8220, latitude: 18.9280, height: 950 },
    orientation: { heading: 25, pitch: -28, roll: 0 }
  },
  bandra_worli_sealink: {
    name: "Bandra-Worli Sea Link",
    destination: { longitude: 72.8280, latitude: 19.0150, height: 1200 },
    orientation: { heading: 335, pitch: -30, roll: 0 }
  },
  bkc_financial_district: {
    name: "Bandra Kurla Complex (BKC)",
    destination: { longitude: 72.8680, latitude: 19.0550, height: 1100 },
    orientation: { heading: 340, pitch: -35, roll: 0 }
  },
  coastal_road: {
    name: "Mumbai Coastal Road & Tunnels",
    destination: { longitude: 72.8050, latitude: 18.9700, height: 1400 },
    orientation: { heading: 15, pitch: -32, roll: 0 }
  },
  csmt_heritage: {
    name: "CSMT World Heritage Terminus",
    destination: { longitude: 72.8360, latitude: 18.9350, height: 650 },
    orientation: { heading: 45, pitch: -25, roll: 0 }
  }
};

export class CesiumViewerManager {
  public viewer: Cesium.Viewer | null = null;
  public google3DTileset: Cesium.Cesium3DTileset | null = null;
  public isGoogleTilesLoaded = false;
  public onTilesLoadedChange?: (isGoogle: boolean) => void;
  private onObjectSelectedCallback: ((objectId: string, entityType: string) => void) | null = null;

  public initialize(container: HTMLElement, onSelect: (id: string, type: string) => void): Cesium.Viewer {
    this.onObjectSelectedCallback = onSelect;

    // Set Cesium Ion default access token if provided in env
    const ionToken = (import.meta as any).env?.VITE_CESIUM_ION_TOKEN || '';
    if (ionToken) {
      Cesium.Ion.defaultAccessToken = ionToken;
    }

    // Initialize Viewer with high performance options
    const viewer = new Cesium.Viewer(container, {
      animation: false,
      baseLayerPicker: false,
      fullscreenButton: false,
      geocoder: false,
      homeButton: false,
      infoBox: false,
      sceneModePicker: false,
      selectionIndicator: false,
      timeline: false,
      navigationHelpButton: false,
      navigationInstructionsInitiallyVisible: false,
      scene3DOnly: true,
      shouldAnimate: true,
      terrainProvider: undefined,
    });

    this.viewer = viewer;

    // Set atmosphere and visual parameters
    const scene = viewer.scene;
    const globe = scene.globe;

    globe.depthTestAgainstTerrain = true;
    globe.enableLighting = true;
    globe.atmosphereBrightnessShift = 0.1;
    globe.atmosphereHueShift = 0.0;
    globe.atmosphereSaturationShift = 0.1;

    // Enhance sky atmosphere and fog
    if (scene.skyAtmosphere) {
      scene.skyAtmosphere.show = true;
    }
    if (scene.fog) {
      scene.fog.enabled = true;
      scene.fog.density = 0.00012;
    }

    // Setup input entity click picking
    const handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
    handler.setInputAction((click: any) => {
      const pickedFeature = scene.pick(click.position);
      if (Cesium.defined(pickedFeature) && pickedFeature.id) {
        const id = pickedFeature.id.id || pickedFeature.id.name || (typeof pickedFeature.id === 'string' ? pickedFeature.id : '');
        const entityType = pickedFeature.id.properties?.category?.getValue() || 'UNKNOWN';
        if (id && this.onObjectSelectedCallback) {
          this.onObjectSelectedCallback(id, entityType);
        }
      }
    }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

    // Initial camera position at space/globe level for cinematic intro
    viewer.camera.setView({
      destination: Cesium.Cartesian3.fromDegrees(72.8777, 19.0760, 4500000),
      orientation: {
        heading: Cesium.Math.toRadians(0),
        pitch: Cesium.Math.toRadians(-90),
        roll: 0.0
      }
    });

    // Load Google Photorealistic 3D Tiles (or graceful fallback)
    this.load3DTiles();

    return viewer;
  }

  public async load3DTiles() {
    if (!this.viewer) return;

    try {
      const googleApiKey = (import.meta as any).env?.VITE_GOOGLE_MAPS_API_KEY;
      if (googleApiKey && (Cesium as any).createGooglePhotorealistic3DTileset) {
        const tileset = await (Cesium as any).createGooglePhotorealistic3DTileset({
          key: googleApiKey
        });
        this.viewer.scene.primitives.add(tileset);
        this.google3DTileset = tileset;
        this.isGoogleTilesLoaded = true;
        this.onTilesLoadedChange?.(true);
        console.log('[MahaTwin 3D] Google Photorealistic 3D Tiles Loaded Successfully');
      } else {
        // Fallback to Cesium OSM Buildings if Ion token available
        try {
          const osmBuildings = await (Cesium as any).createOsmBuildingsAsync();
          this.viewer.scene.primitives.add(osmBuildings);
          this.google3DTileset = osmBuildings;
          this.isGoogleTilesLoaded = false;
          this.onTilesLoadedChange?.(false);
          console.log('[MahaTwin 3D] Fallback Cesium OSM 3D Buildings Loaded');
        } catch (e) {
          this.isGoogleTilesLoaded = false;
          this.onTilesLoadedChange?.(false);
          console.info('[MahaTwin 3D] Running in standard vector digital twin mode');
        }
      }
    } catch (err) {
      this.isGoogleTilesLoaded = false;
      this.onTilesLoadedChange?.(false);
      console.warn('[MahaTwin 3D] 3D Tiles fallback mode active:', err);
    }
  }

  public flyToMumbaiIntro() {
    if (!this.viewer) return;
    const bm = MUMBAI_BOOKMARKS.mumbai_overview;
    this.viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(
        bm.destination.longitude,
        bm.destination.latitude,
        bm.destination.height
      ),
      orientation: {
        heading: Cesium.Math.toRadians(bm.orientation.heading),
        pitch: Cesium.Math.toRadians(bm.orientation.pitch),
        roll: Cesium.Math.toRadians(bm.orientation.roll)
      },
      duration: 3.5
    });
  }

  public flyToBookmark(bookmarkKey: string) {
    if (!this.viewer) return;
    const bm = MUMBAI_BOOKMARKS[bookmarkKey] || MUMBAI_BOOKMARKS.mumbai_overview;
    this.viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(
        bm.destination.longitude,
        bm.destination.latitude,
        bm.destination.height
      ),
      orientation: {
        heading: Cesium.Math.toRadians(bm.orientation.heading),
        pitch: Cesium.Math.toRadians(bm.orientation.pitch),
        roll: Cesium.Math.toRadians(bm.orientation.roll)
      },
      duration: 2.2
    });
  }

  public flyToCoordinates(lon: number, lat: number, height = 800) {
    if (!this.viewer) return;
    this.viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(lon, lat, height),
      orientation: {
        heading: Cesium.Math.toRadians(0),
        pitch: Cesium.Math.toRadians(-45),
        roll: 0.0
      },
      duration: 2.0
    });
  }

  public setViewMode(mode: ViewMode, undergroundDepthMeters = 30) {
    if (!this.viewer) return;
    const scene = this.viewer.scene;
    const globe = scene.globe;

    if (mode === 'UNDERGROUND' || mode === 'UTILITY_ISOLATION') {
      // Enable globe translucency to reveal subsurface infrastructure with depth sensitivity
      globe.translucency.enabled = true;
      const frontAlpha = Math.max(0.08, 0.28 - (undergroundDepthMeters / 250));
      globe.translucency.frontFaceAlpha = frontAlpha;
      globe.translucency.backFaceAlpha = 0.12;
      globe.depthTestAgainstTerrain = false;

      // Dim surface tileset
      if (this.google3DTileset) {
        this.google3DTileset.style = new Cesium.Cesium3DTileStyle({
          color: "color('rgba(148, 163, 184, 0.12)')"
        });
      }
    } else {
      // Restore standard surface view
      globe.translucency.enabled = false;
      globe.depthTestAgainstTerrain = true;

      if (this.google3DTileset) {
        this.google3DTileset.style = new Cesium.Cesium3DTileStyle({
          color: "color('rgba(255, 255, 255, 1.0)')"
        });
      }
    }
  }

  public destroy() {
    if (this.viewer && !this.viewer.isDestroyed()) {
      this.viewer.destroy();
      this.viewer = null;
    }
  }
}
