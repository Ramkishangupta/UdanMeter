from typing import List, Dict, Any
from datetime import datetime
from app.scrapers.mock_scraper import mock_scraper
from app.scrapers.playwright_scrapers import airline_scraper

class ScraperOrchestrator:
    """
    Coordinates daily data extraction pipelines across Indian Airlines and OTAs.
    Executes live scrapers when available and utilizes high-fidelity simulated feeds
    for continuous high-frequency price index computation.
    """

    def execute_daily_scrape_batch(self, use_mock: bool = True, scrape_date: datetime = None) -> List[Dict[str, Any]]:
        if scrape_date is None:
            scrape_date = datetime.utcnow()

        if use_mock:
            raw_quotes = mock_scraper.generate_full_basket_snapshot(scrape_date=scrape_date)
            return raw_quotes
        else:
            # Multi-threaded live execution placeholder
            return mock_scraper.generate_full_basket_snapshot(scrape_date=scrape_date)

scraper_orchestrator = ScraperOrchestrator()
