"""
Database Initialization & Seeding Script for MoSPI APIx Engine
Usage:
    python init_db.py
Works with both PostgreSQL (via DATABASE_URL in .env) and SQLite fallback.
"""
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("init_db")

try:
    from app.core.config import settings
    from app.core.database import engine, Base, SessionLocal, IS_SQLITE
    from app.data_pipeline.repository import data_repository
    from app.scrapers.mock_scraper import mock_scraper
    from app.data_pipeline.cleaner import data_cleaner
    from app.index_engine.apix_calculator import apix_engine
except ImportError as e:
    logger.error(f"Failed to import project modules: {e}")
    sys.exit(1)

def setup_database(seed_initial_quotes: bool = True):
    db_type = "SQLite" if IS_SQLITE else "PostgreSQL"
    logger.info(f"Connecting to database [{db_type}]: {settings.SQLALCHEMY_DATABASE_URL.split('@')[-1] if '@' in settings.SQLALCHEMY_DATABASE_URL else settings.SQLALCHEMY_DATABASE_URL}")

    # 1. Create Tables
    logger.info("Creating database tables if not present...")
    Base.metadata.create_all(bind=engine)
    logger.info("All tables successfully verified/created.")

    db = SessionLocal()
    try:
        # 2. Seed DGCA Route Weights
        logger.info("Seeding DGCA primary route weights...")
        data_repository.initialize_route_weights(db)
        logger.info("Route weights verified.")

        # 3. Seed Initial Basket Snapshot (if database has 0 quotes)
        if seed_initial_quotes:
            from app.models.database import RawAirfareQuote, ApixDailyIndex
            existing_count = db.query(RawAirfareQuote).count()
            if existing_count == 0:
                logger.info("Database is empty. Generating initial high-fidelity airfare quotes basket (~1,500+ quotes)...")
                raw_quotes = mock_scraper.generate_full_basket_snapshot()
                data_repository.save_raw_quotes(db, raw_quotes)
                logger.info(f"Saved {len(raw_quotes)} raw airfare quotes.")

                # Clean & Deduplicate
                cleaned_records, outlier_count = data_cleaner.clean_and_deduplicate_batch(raw_quotes)
                data_repository.save_cleaned_quotes(db, cleaned_records)
                logger.info(f"Saved {len(cleaned_records)} cleaned quotes (Flagged {outlier_count} anomalous outliers).")

                # Calculate Initial APIx Daily Index
                today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                index_payload = apix_engine.compute_daily_index(cleaned_records, cleaned_records)
                index_payload["date"] = today
                data_repository.save_apix_index(db, index_payload)
                logger.info(f"Initial APIx Index computed: National APIx = {index_payload['apix_national']} (Base = 100.0)")
            else:
                logger.info(f"Database already contains {existing_count} raw quotes. Skipping synthetic seeding.")

        logger.info(f"Database setup complete! [{db_type}] is ready for production use.")

    except Exception as err:
        logger.error(f"Error during database initialization: {err}")
        db.rollback()
        raise err
    finally:
        db.close()

if __name__ == "__main__":
    setup_database(seed_initial_quotes=True)
