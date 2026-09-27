from fastapi import APIRouter, HTTPException
from app.seed.mumbai_dataset import TEMPORAL_STATES

router = APIRouter()

@router.get("/scenarios")
def get_temporal_scenarios():
    return {
        "status": "success",
        "scenarios": TEMPORAL_STATES
    }

@router.get("/scenario/{scenario_id}")
def get_scenario_by_id(scenario_id: str):
    if scenario_id not in TEMPORAL_STATES:
        raise HTTPException(status_code=404, detail=f"Temporal scenario '{scenario_id}' not found. Valid: {list(TEMPORAL_STATES.keys())}")
    return {
        "status": "success",
        "data": TEMPORAL_STATES[scenario_id]
    }
