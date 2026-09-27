"""Single owner of data-honesty policy.

Every entity the API serves carries `data_provenance` + `freshness`. Bundled
static fixtures must never be presented as operational feeds, so the only
provenance value that may reach a response for bundled data is defined here
and applied at the source of truth in app/data/ — not scattered as string
literals across the codebase.
"""

# Bundled static fixture, shipped in app/data/. Not a live feed.
SAMPLE_BUNDLED_DATA = "SAMPLE_BUNDLED_DATA"
SAMPLE_FRESHNESS = "Bundled sample — not a live feed"

# Emitted by the telemetry simulator for its derived, animated values.
SIMULATED_TELEMETRY = "SIMULATED_TELEMETRY"
SIMULATED_FRESHNESS = "Simulated animation derived from bundled data"


def bundled_provenance(record: dict) -> str:
    """Provenance of a bundled record; defaults honestly if the literal is missing."""
    return record.get("data_provenance", SAMPLE_BUNDLED_DATA)


def bundled_freshness(record: dict) -> str:
    """Freshness of a bundled record; defaults honestly if the literal is missing."""
    return record.get("freshness", SAMPLE_FRESHNESS)
