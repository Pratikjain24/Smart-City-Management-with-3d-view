# MAHATWIN MUMBAI
### High-Fidelity 4D Digital Twin of Mumbai City (Phase 1 Foundation)

![MahaTwin Mumbai](https://img.shields.io/badge/MahaTwin-Mumbai%204D-06b6d4?style=for-the-badge&logo=cesium)
![CesiumJS](https://img.shields.io/badge/CesiumJS-1.121-3b82f6?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-10b981?style=for-the-badge&logo=fastapi)
![PostGIS](https://img.shields.io/badge/PostGIS-16-0284c7?style=for-the-badge&logo=postgresql)
![WebSockets](https://img.shields.io/badge/WebSockets-Live%20Stream-8b5cf6?style=for-the-badge)

---

## 🌟 Overview

**MahaTwin Mumbai** is an enterprise-grade, photorealistic 4D Digital Twin of Mumbai. Combining **Google Photorealistic 3D Tiles**, **CesiumJS**, **PostGIS**, **FastAPI**, and real-time **WebSockets**, MahaTwin enables urban command center operators, civil engineers, municipal authorities, and citizens to inspect and interact with Mumbai across surface, underground, and temporal dimensions.

---

## 🚀 Key Features

### 1. Photorealistic 3D Foundation & Camera Engine
- **Google Photorealistic 3D Tiles & CesiumJS**: High-fidelity 3D buildings, dynamic atmospheric lighting, fog depth, and terrain awareness covering the entire Mumbai metropolitan region.
- **Cinematic Navigation**: Smooth globe-to-city camera transitions, 6 landmark bookmarks (*Marine Drive, Bandra-Worli Sea Link, BKC Financial District, Mumbai Coastal Road & Tunnels, CSMT Heritage Terminus*), coordinate HUD, and FPS performance monitor.
- **Graceful Fallback**: Automatically switches to Cesium World Terrain + OSM 3D vector buildings when Google API keys are not supplied.

### 2. Connected Mumbai GIS Road Network
- **Graph-Connected Corridors**: Western Express Highway (WEH), Eastern Express Highway (EEH), Mumbai Coastal Road, Bandra-Worli Sea Link (BWSL), Eastern Freeway, S.V. Road, LBS Marg, JVLR, and SCLR.
- **Traffic Intelligence**: Real-time traffic condition colors (`GREEN`, `YELLOW`, `ORANGE`, `RED`), speed limits, and average speeds.
- **Interactive Connectivity**: Clicking any road highlights the primary polyline in vibrant cyan, highlights connected intersecting roads in pulsing violet, and displays the **Road Intelligence Panel**.

### 3. Subsurface & Utility Isolation View
- **Underground Mode**: Globe translucency activates, 3D surface buildings fade to 15% opacity, and subterranean networks emerge with accurate negative altitude offsets (-2m to -25m).
- **Utility Layers**:
  - 💧 **Water Distribution**: Bhandup Master Trunk Mains (3000mm), Vihar/Tulsi conduits, balancing reservoirs.
  - 🚰 **Sewerage**: MSDP deep sewerage tunnel (-24m), Dadar/Worli shafts, 3.5km marine outfall.
  - 🌧️ **Storm Drainage**: BRIMSTOWAD storm box drains, Mithi River training channel, Milan Subway 20ML retention sump.
  - ⚡ **Power Grid**: Tata Power 220kV underground transmission, Adani BKC smart ring main.
  - 📡 **Telecom**: Subsea landing station core dark fiber loop connecting Prabhadevi, BKC, and SEEPZ.
- **Utility Isolation**: Single-click isolation of any utility domain (e.g. `WATER`) glows the target pipes while dimming all other infrastructure.

### 4. 4D Time Machine Engine
- **Historical (2020 - 2024)**: Pre-coastal road reclamation baseline, Metro 3 tunneling phase.
- **LIVE (2026)**: Real-time telemetry, active transit GPS tracks, live traffic fluctuations.
- **Simulated Future (2028 - 2030)**: Multi-modal Metro expansion (Lines 4, 6, 11), Bullet Train underground BKC terminal, zero-emission transit, and tidal flood resilience gates.
- **Interactive Scrubber**: Scrub, play/pause, and adjust speed (1x, 5x, 20x).

### 5. Multimodal Transit & Active Incident Layer
- **Live Transit Trackers**: Animated GPS markers for Metro Line 3 (Aqua Line), Metro Line 1, Western & Central Railway fast/slow locals, and BEST Electric AC buses.
- **Incident & Damage Management**: Interactive 3D pins for potholes, waterlogging risk sumps (Milan Subway, Hindmata), construction lane diversions, and signal faults with work order tracking.
- **SAFAR AQI & Weather Stations**: Continuous air quality monitoring stations (Colaba, BKC, Andheri, Borivali, Chembur, Worli) with heat rings.

### 6. Universal Object Intelligence & Graph Inspector
- Click any entity (Road, Pipeline, Reservoir, Metro train, Station, Hospital, Incident, Police HQ) to open the deep inspection sidebar with:
  - Data Honesty Badge (`LIVE`, `HISTORICAL`, `SIMULATED`, `SAMPLE`).
  - Operational metrics and specifications.
  - Upstream/Downstream supply chain links.
  - Connected infrastructure graph tree.

---

## 🛠️ Architecture & Tech Stack

| Component | Technology | Description |
|---|---|---|
| **3D Engine** | CesiumJS 1.121 + Google Photorealistic 3D Tiles | 3D WebGL rendering, camera animation, subsurface clipping |
| **Frontend** | React 18, TypeScript, Vite, Tailwind/Modern CSS | Command center UI, glassmorphism docks, HUDs |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, WebSockets | Asynchronous REST APIs and live 1-second telemetry hub |
| **GIS & Math** | Shapely, GeoJSON | Spatial graph traversal and geometric indexing |
| **Database** | PostgreSQL 16 + PostGIS 3.4 | Geospatial relational store |
| **Streaming** | Native WebSockets + Redis Pub/Sub | Real-time vehicle positions & sensor pulses |
| **DevOps** | Docker, Docker Compose, Nginx | Multi-container orchestration |

---

## ⚡ Quick Start

### Option 1: Run with Docker Compose (Recommended)

```bash
# 1. Clone repository & configure environment
cp .env.example .env

# 2. Build and start all services (PostGIS, Redis, Backend, Frontend)
docker-compose up --build -d

# 3. Access MahaTwin Mumbai
# Frontend Command Center: http://localhost:3000
# Backend API Documentation: http://localhost:8000/docs
```

---

### Option 2: Run Locally for Development

#### 1. Backend Setup
```bash
cd backend

# Create & activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run pytest verification suite
pytest tests/ -v

# Start FastAPI dev server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup
```bash
cd frontend

# Install npm packages
npm install

# Start Vite development server with proxying
npm run dev
```

Open your browser at `http://localhost:5173`.

---

## 📡 API Reference Summary

- `GET /api/v1/cities/mumbai` - Mumbai metadata and administrative wards
- `GET /api/v1/roads` - Connected Mumbai roads network
- `GET /api/v1/roads/geojson` - GeoJSON representation of road polylines
- `GET /api/v1/roads/{id}/connected` - Graph traversal of connected roads & nearby assets
- `GET /api/v1/utilities/all` - All subsurface water, sewer, drainage, power, telecom layers
- `GET /api/v1/utilities/geojson/{category}` - GeoJSON utility pipelines and junction nodes
- `GET /api/v1/transport/all` - Metro, Suburban Railway, and BEST bus routes
- `GET /api/v1/incidents` - Active potholes, waterlogging sumps, and construction diversions
- `GET /api/v1/environment/summary` - SAFAR AQI stations and flood risk hotspots
- `GET /api/v1/temporal/scenarios` - 4D Time Machine temporal states (2020-2030)
- `GET /api/v1/objects/{id}` - Universal Object Inspector query
- `GET /api/v1/search?q={query}` - Global fuzzy spatial and lexical search
- `WS /api/v1/ws/live-stream` - Real-time synchronized telemetry WebSocket stream

---

## 🔮 Future-Ready Architecture (Phases 2-5)
- **Phase 2**: Machine Learning road damage AI and real-time SCADA pressure predictive models.
- **Phase 3**: SUMO (Simulation of Urban MObility) microscopic traffic flow simulation.
- **Phase 4**: Autonomous AI Agentic Urban Mayor & LLM municipal query copilot.
- **Phase 5**: Climate sea-level rise inundation simulation & emergency evacuation optimizer.
