"""One-off migration: bake the bundled Mumbai dataset into app/data/mumbai/.

Runs against the legacy app.seed.mumbai_dataset AFTER its import-time honesty
normalization pass, so the baked literals are exactly the values the API serves
today (SAMPLE_BUNDLED_DATA everywhere, AQI status SAMPLE, relabeled live_2026).
Delete this file after the migration is verified.
"""
import pathlib
from pprint import pformat

from app.seed import mumbai_dataset as legacy

BACKEND = pathlib.Path(__file__).resolve().parent
OUT = BACKEND / "app" / "data" / "mumbai"
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '"""Bundled Mumbai demonstration dataset — static fixtures, not a live feed.\n\nHonesty labels are baked as literals at the source of truth: every record here is\nSAMPLE_BUNDLED_DATA with freshness "Bundled sample — not a live feed". There is no\nimport-time normalization pass; what you read is what the API serves.\n"""\n\n'

MODULES = {
    "metadata.py": ("MUMBAI_METADATA", legacy.MUMBAI_METADATA),
    "roads.py": ("ROADS_DATA", legacy.ROADS_DATA),
    "utilities.py": ("UTILITIES_DATA", legacy.UTILITIES_DATA),
    "transit.py": ("TRANSIT_DATA", legacy.TRANSIT_DATA),
    "incidents.py": ("INCIDENTS_DATA", legacy.INCIDENTS_DATA),
    "environment.py": ("ENVIRONMENT_DATA", legacy.ENVIRONMENT_DATA),
    "civic.py": ("CIVIC_FACILITIES", legacy.CIVIC_FACILITIES),
    "temporal.py": ("TEMPORAL_STATES", legacy.TEMPORAL_STATES),
}

for filename, (constant, value) in MODULES.items():
    body = pformat(value, width=100, sort_dicts=False)
    (OUT / filename).write_text(HEADER + f"{constant} = {body}\n", encoding="utf-8")
    print("wrote", filename, f"({len(body)} chars)")
