import os
from typing import List
from dotenv import load_dotenv

# Load .env from backend root or system environment
ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "MoSPI Real-time Airfare Price Index (APIx) Engine")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server network settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_MAX_BYTES: int = int(os.getenv("LOG_MAX_BYTES", 5 * 1024 * 1024)) # 5MB default
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", 5))

    # CORS Allowed Origins (Comma-separated list or * in development)
    raw_cors = os.getenv("CORS_ORIGINS", "*")
    CORS_ORIGINS: List[str] = [origin.strip() for origin in raw_cors.split(",") if origin.strip()]

    # Database URI Setup (PostgreSQL support with fallback to SQLite for local development)
    raw_db_url = os.getenv("DATABASE_URL", "").strip()
    DB_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "apix_database.db")
    
    if raw_db_url:
        # Normalize Render/Heroku/Neon/Supabase 'postgres://' or standard 'postgresql://' to 'postgresql+psycopg2://'
        if raw_db_url.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URL: str = raw_db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif raw_db_url.startswith("postgresql://") and not raw_db_url.startswith("postgresql+"):
            SQLALCHEMY_DATABASE_URL: str = raw_db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        else:
            SQLALCHEMY_DATABASE_URL: str = raw_db_url
    else:
        # Local fallback SQLite database
        SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{DB_PATH}"

    # DGCA Primary City Pairs Basket
    CITY_PAIRS = [
        {"origin": "DEL", "destination": "BOM", "name": "Delhi - Mumbai", "weight": 0.18},
        {"origin": "DEL", "destination": "BLR", "name": "Delhi - Bengaluru", "weight": 0.14},
        {"origin": "BOM", "destination": "BLR", "name": "Mumbai - Bengaluru", "weight": 0.12},
        {"origin": "DEL", "destination": "CCU", "name": "Delhi - Kolkata", "weight": 0.09},
        {"origin": "BLR", "destination": "HYD", "name": "Bengaluru - Hyderabad", "weight": 0.08},
        {"origin": "MAA", "destination": "DEL", "name": "Chennai - Delhi", "weight": 0.08},
        {"origin": "CCU", "destination": "BLR", "name": "Kolkata - Bengaluru", "weight": 0.07},
        {"origin": "DEL", "destination": "HYD", "name": "Delhi - Hyderabad", "weight": 0.07},
        {"origin": "BOM", "destination": "GOI", "name": "Mumbai - Goa", "weight": 0.06},
        {"origin": "BLR", "destination": "MAA", "name": "Bengaluru - Chennai", "weight": 0.04},
        {"origin": "DEL", "destination": "PNQ", "name": "Delhi - Pune", "weight": 0.04},
        {"origin": "BOM", "destination": "AMD", "name": "Mumbai - Ahmedabad", "weight": 0.03},
    ]

    # Advance Purchase Lead Times (Days)
    ADVANCE_WINDOWS = [1, 7, 15, 30, 45]
    WINDOW_WEIGHTS = {1: 0.15, 7: 0.25, 15: 0.30, 30: 0.20, 45: 0.10}

    # Sources
    AIRLINES = ["IndiGo", "Air India", "Air India Express", "Akasa Air", "SpiceJet"]
    OTAS = ["MakeMyTrip", "Yatra", "EaseMyTrip", "Cleartrip", "Ixigo"]

settings = Settings()
