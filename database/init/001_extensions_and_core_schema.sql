-- MahaTwin Phase 1 database baseline.
-- Bundled Python fixtures remain explicitly SAMPLE until an approved importer
-- loads source-controlled municipal data into these tables.
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS infrastructure_assets (
    id TEXT PRIMARY KEY,
    asset_type TEXT NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'unknown',
    source_kind TEXT NOT NULL CHECK (source_kind IN ('sample', 'simulated', 'authoritative', 'live')),
    source_name TEXT NOT NULL,
    observed_at TIMESTAMPTZ,
    properties JSONB NOT NULL DEFAULT '{}'::jsonb,
    geometry geometry(GEOMETRY, 4326) NOT NULL,
    CONSTRAINT infrastructure_assets_geometry_srid CHECK (ST_SRID(geometry) = 4326)
);

CREATE INDEX IF NOT EXISTS infrastructure_assets_geometry_gix
    ON infrastructure_assets USING GIST (geometry);
CREATE INDEX IF NOT EXISTS infrastructure_assets_type_idx
    ON infrastructure_assets (asset_type);
CREATE INDEX IF NOT EXISTS infrastructure_assets_observed_at_idx
    ON infrastructure_assets (observed_at DESC);

CREATE TABLE IF NOT EXISTS road_connections (
    road_id TEXT NOT NULL REFERENCES infrastructure_assets(id) ON DELETE CASCADE,
    connected_road_id TEXT NOT NULL REFERENCES infrastructure_assets(id) ON DELETE CASCADE,
    PRIMARY KEY (road_id, connected_road_id),
    CONSTRAINT road_connections_not_self CHECK (road_id <> connected_road_id)
);

CREATE TABLE IF NOT EXISTS telemetry_observations (
    observed_at TIMESTAMPTZ NOT NULL,
    asset_id TEXT REFERENCES infrastructure_assets(id) ON DELETE SET NULL,
    metric_name TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit TEXT,
    source_kind TEXT NOT NULL CHECK (source_kind IN ('sample', 'simulated', 'authoritative', 'live')),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    PRIMARY KEY (observed_at, metric_name, asset_id)
);

SELECT create_hypertable('telemetry_observations', 'observed_at', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS telemetry_observations_asset_time_idx
    ON telemetry_observations (asset_id, observed_at DESC);
