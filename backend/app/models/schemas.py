from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class AirfareQuoteBase(BaseModel):
    source: str
    carrier: str
    origin: str
    destination: str
    advance_days: int
    total_fare: float
    base_fare: float
    taxes_fees: float
    convenience_fee: float

class AirfareQuoteCreate(AirfareQuoteBase):
    flight_number: Optional[str] = "6E-204"

class AirfareQuoteOut(AirfareQuoteBase):
    id: int
    scraped_at: datetime
    is_outlier: bool

    class Config:
        from_attributes = True

class ApixIndexSummary(BaseModel):
    date: str
    apix_national: float
    laspeyres_index: float
    paasche_index: float
    jevons_index: float
    cpi_transport_benchmark: float
    pct_change_daily: float
    pct_change_monthly: float
    basket_count: int
    active_sources: List[str]

class RouteHeatmapItem(BaseModel):
    origin: str
    destination: str
    route_name: str
    weight: float
    avg_fare: float
    min_fare: float
    max_fare: float
    t1_fare: float
    t45_fare: float
    pressure_index: float # Fare relative to baseline

class ElasticityItem(BaseModel):
    advance_days: int
    avg_total_fare: float
    avg_base_fare: float
    avg_taxes: float
    discount_vs_t1_pct: float

class CarrierParityItem(BaseModel):
    carrier: str
    direct_avg_fare: float
    ota_avg_fare: float
    ota_markup_pct: float
    total_quotes: int

class DgcaBacktestItem(BaseModel):
    month_year: str
    route: str
    dgca_published_avg_fare: float
    apix_backtested_avg_fare: float
    variance_pct: float
    mape_pct: float
