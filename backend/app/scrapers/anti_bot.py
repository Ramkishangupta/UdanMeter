import random
import time
import urllib.robotparser
from typing import Dict, Optional

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
]

class AntiBotManager:
    """
    Handles Ethical Rate-Limiting, User-Agent Rotation, Session Management,
    and Robots.txt compliance checks for Indian airline and OTA portals.
    """
    def __init__(self, requests_per_minute: int = 30):
        self.delay_range = (60.0 / requests_per_minute, 60.0 / requests_per_minute + 1.5)
        self.robot_parsers: Dict[str, urllib.robotparser.RobotFileParser] = {}

    def get_random_user_agent(self) -> str:
        return random.choice(USER_AGENTS)

    def get_stealth_headers(self, source_domain: str) -> Dict[str, str]:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"https://{source_domain}/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
        }

    def enforce_rate_limit(self):
        """Sleep for a randomized jitter duration to prevent IP banning."""
        sleep_dur = random.uniform(*self.delay_range)
        time.sleep(sleep_dur)

    def is_allowed_by_robots(self, url: str, user_agent: str = "*") -> bool:
        """Check source robots.txt compliance prior to scraping."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            robots_url = f"{base_url}/robots.txt"

            if base_url not in self.robot_parsers:
                rp = urllib.robotparser.RobotFileParser()
                rp.set_url(robots_url)
                rp.read()
                self.robot_parsers[base_url] = rp

            return self.robot_parsers[base_url].can_fetch(user_agent, url)
        except Exception:
            return True

anti_bot_manager = AntiBotManager()
