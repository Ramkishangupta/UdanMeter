import os

class Settings:
    PROJECT_NAME: str = "MoSPI Real-time Airfare Price Index (APIx) Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # SQLite Database URI
    DB_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "apix_database.db")
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
