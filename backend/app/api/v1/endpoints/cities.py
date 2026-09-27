from fastapi import APIRouter
from app.seed.mumbai_dataset import MUMBAI_METADATA

router = APIRouter()

@router.get("/mumbai")
def get_mumbai_metadata():
    return {
        "status": "success",
        "data": MUMBAI_METADATA
    }

@router.get("/wards")
def get_wards():
    return {
        "status": "success",
        "total": len(MUMBAI_METADATA["admin_wards"]),
        "data": MUMBAI_METADATA["admin_wards"]
    }
