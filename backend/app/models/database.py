from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class RawAirfareQuote(Base):
    __tablename__ = "raw_airfare_quotes"

    id = Column(Integer, primary_key=True, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)
    source = Column(String, index=True) # IndiGo, Air India, MakeMyTrip, etc.
    origin = Column(String, index=True) # DEL
    destination = Column(String, index=True) # BOM
    flight_number = Column(String)
    carrier = Column(String, index=True)
    departure_date = Column(DateTime, index=True)
    advance_days = Column(Integer, index=True) # 1, 7, 15, 30, 45
    raw_fare = Column(Float)
    currency = Column(String, default="INR")
    scraped_status = Column(String, default="SUCCESS") # SUCCESS, OUTLIER, FAILED

class CleanedAirfareQuote(Base):
    __tablename__ = "cleaned_airfare_quotes"

    id = Column(Integer, primary_key=True, index=True)
    raw_quote_id = Column(Integer, ForeignKey("raw_airfare_quotes.id"), nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)
    source = Column(String, index=True)
    carrier = Column(String, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    advance_days = Column(Integer, index=True)
    
    # Decomposed Components
    base_fare = Column(Float)
    taxes_fees = Column(Float) # Fuel surcharge, UDF, PSF
    convenience_fee = Column(Float)
    total_fare = Column(Float)

    fare_class = Column(String, default="Economy Standard")
    is_outlier = Column(Boolean, default=False)
    z_score = Column(Float, default=0.0)

class ApixDailyIndex(Base):
    __tablename__ = "apix_daily_indices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, index=True)
    
    # Composite Indices (Base = 100 on Baseline Date)
    apix_national = Column(Float)       # Fisher Ideal Price Index
    laspeyres_index = Column(Float)
    paasche_index = Column(Float)
    jevons_index = Column(Float)
    
    # Standard CPI Comparison Baseline
    cpi_transport_benchmark = Column(Float)

    pct_change_daily = Column(Float)
    pct_change_monthly = Column(Float)
    pct_change_annual = Column(Float)

class RouteWeight(Base):
    __tablename__ = "route_weights"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    route_name = Column(String)
    dgca_passenger_share = Column(Float) # e.g. 0.18
    weight_factor = Column(Float)

class DgcaBenchmark(Base):
    __tablename__ = "dgca_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    month_year = Column(String, index=True) # "2026-08"
    route = Column(String, index=True) # "DEL-BOM"
    dgca_published_avg_fare = Column(Float)
    apix_backtested_avg_fare = Column(Float)
    variance_pct = Column(Float)
