from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")
    PROJECT_NAME: str = "MahaTwin Mumbai"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Database (PostgreSQL / PostGIS)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/mahatwin_mumbai"
    )
    
    # Redis for live events
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Google Photorealistic 3D Tiles Key (Loaded securely from env)
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    CESIUM_ION_TOKEN: str = os.getenv("CESIUM_ION_TOKEN", "")
    
    # Mumbai Bounding Box [min_lon, min_lat, max_lon, max_lat]
    MUMBAI_BBOX: List[float] = [72.7500, 18.8800, 73.0500, 19.3200]
    MUMBAI_CENTER: List[float] = [72.8777, 19.0760, 150.0]  # lon, lat, height

settings = Settings()
