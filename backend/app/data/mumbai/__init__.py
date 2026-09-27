"""Mumbai bundled dataset, split by domain.

Every module here contains plain literals with honesty labels baked in:
`data_provenance = "SAMPLE_BUNDLED_DATA"`, `freshness = "Bundled sample — not a live feed"`.
There is no import-time rewriting; what you read is what the API serves.
"""
from app.data.mumbai import (  # noqa: F401
    civic,
    environment,
    incidents,
    metadata,
    roads,
    temporal,
    transit,
    utilities,
)

__all__ = [
    "civic", "environment", "incidents", "metadata",
    "roads", "temporal", "transit", "utilities",
]
