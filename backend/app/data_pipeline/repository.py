from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.models.database import RawAirfareQuote, CleanedAirfareQuote, ApixDailyIndex, RouteWeight, DgcaBenchmark
from app.core.config import settings

class DataRepository:
    """
    CRUD Data Repository for storing quotes, index records, and DGCA benchmarks.
    """

    @staticmethod
    def initialize_route_weights(db: Session):
        """Initializes primary DGCA route passenger traffic weights if empty."""
        existing = db.query(RouteWeight).count()
        if existing == 0:
            for pair in settings.CITY_PAIRS:
                rw = RouteWeight(
                    origin=pair["origin"],
                    destination=pair["destination"],
                    route_name=pair["name"],
                    dgca_passenger_share=pair["weight"],
                    weight_factor=pair["weight"]
                )
                db.add(rw)
            db.commit()

    @staticmethod
    def save_raw_quotes(db: Session, quotes: List[Dict[str, Any]]) -> List[RawAirfareQuote]:
        raw_models = []
        for q in quotes:
            raw_item = RawAirfareQuote(
                scraped_at=q.get("scraped_at", datetime.utcnow()),
                source=q.get("source"),
                origin=q.get("origin"),
                destination=q.get("destination"),
                flight_number=q.get("flight_number", "6E-101"),
                carrier=q.get("carrier"),
                departure_date=q.get("departure_date"),
                advance_days=q.get("advance_days"),
                raw_fare=q.get("total_fare"),
                currency=q.get("currency", "INR"),
                scraped_status="SUCCESS"
            )
            raw_models.append(raw_item)
        db.add_all(raw_models)
        db.commit()
        return raw_models

    @staticmethod
    def save_cleaned_quotes(db: Session, quotes: List[Dict[str, Any]]) -> int:
        cleaned_models = []
        for q in quotes:
            c_item = CleanedAirfareQuote(
                raw_quote_id=q.get("id"),
                scraped_at=q.get("scraped_at", datetime.utcnow()),
                source=q.get("source"),
                carrier=q.get("carrier"),
                origin=q.get("origin"),
                destination=q.get("destination"),
                advance_days=q.get("advance_days"),
                base_fare=q.get("base_fare"),
                taxes_fees=q.get("taxes_fees"),
                convenience_fee=q.get("convenience_fee"),
                total_fare=q.get("total_fare"),
                fare_class=q.get("fare_class", "Economy Standard"),
                is_outlier=q.get("is_outlier", False),
                z_score=q.get("z_score", 0.0)
            )
            cleaned_models.append(c_item)
        db.add_all(cleaned_models)
        db.commit()
        return len(cleaned_models)

    @staticmethod
    def get_cleaned_quotes_for_date(db: Session, date: datetime) -> List[CleanedAirfareQuote]:
        start = datetime(date.year, date.month, date.day, 0, 0, 0)
        end = datetime(date.year, date.month, date.day, 23, 59, 59)
        return db.query(CleanedAirfareQuote).filter(
            CleanedAirfareQuote.scraped_at >= start,
            CleanedAirfareQuote.scraped_at <= end,
            CleanedAirfareQuote.is_outlier == False
        ).all()

    @staticmethod
    def save_apix_index(db: Session, index_data: Dict[str, Any]) -> ApixDailyIndex:
        idx_date = index_data["date"]
        existing = db.query(ApixDailyIndex).filter(ApixDailyIndex.date == idx_date).first()
        if existing:
            existing.apix_national = index_data["apix_national"]
            existing.laspeyres_index = index_data["laspeyres_index"]
            existing.paasche_index = index_data["paasche_index"]
            existing.jevons_index = index_data["jevons_index"]
            existing.cpi_transport_benchmark = index_data["cpi_transport_benchmark"]
            existing.pct_change_daily = index_data["pct_change_daily"]
            existing.pct_change_monthly = index_data["pct_change_monthly"]
            db.commit()
            return existing
        else:
            new_idx = ApixDailyIndex(
                date=idx_date,
                apix_national=index_data["apix_national"],
                laspeyres_index=index_data["laspeyres_index"],
                paasche_index=index_data["paasche_index"],
                jevons_index=index_data["jevons_index"],
                cpi_transport_benchmark=index_data["cpi_transport_benchmark"],
                pct_change_daily=index_data["pct_change_daily"],
                pct_change_monthly=index_data["pct_change_monthly"],
                pct_change_annual=round(index_data["pct_change_monthly"] * 1.8, 2)
            )
            db.add(new_idx)
            db.commit()
            return new_idx

    @staticmethod
    def get_latest_index(db: Session) -> Optional[ApixDailyIndex]:
        return db.query(ApixDailyIndex).order_by(ApixDailyIndex.date.desc()).first()

    @staticmethod
    def get_index_history(db: Session, limit: int = 30) -> List[ApixDailyIndex]:
        return db.query(ApixDailyIndex).order_by(ApixDailyIndex.date.asc()).all()

data_repository = DataRepository()
