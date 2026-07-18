"""Web scraper utility for WHODIS."""

import random
import time
import requests
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
from .config import USER_AGENTS, REQUEST_TIMEOUT


class Scraper:
    """Utility class for web scraping with anti-bot features."""

    @staticmethod
    def get_random_user_agent() -> str:
        """Get a random user agent."""
        return random.choice(USER_AGENTS)

    @staticmethod
    def get_random_delay(min_sec: float = 0.5, max_sec: float = 2.0) -> None:
        """Add random delay."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    @staticmethod
    def fetch(url: str, timeout: int = REQUEST_TIMEOUT, retries: int = 3, 
              params: Optional[Dict] = None, json_response: bool = False) -> Optional[Any]:
        """
        Fetch URL with retry logic and anti-bot measures.
        
        Args:
            url: URL to fetch
            timeout: Timeout in seconds
            retries: Number of retries
            params: Query parameters
            json_response: If True, return JSON
            
        Returns:
            Response object or None if failed
        """
        headers = {
            "User-Agent": Scraper.get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/",
        }
        
        for attempt in range(retries):
            try:
                Scraper.get_random_delay(0.5, 1.5)
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    if json_response:
                        return response.json()
                    return response
                elif response.status_code == 429:  # Too many requests
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    return None
                    
            except requests.Timeout:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return None
            except requests.RequestException:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return None
        
        return None

    @staticmethod
    def parse_html(html_content: str) -> Optional[BeautifulSoup]:
        """Parse HTML content."""
        try:
            return BeautifulSoup(html_content, 'lxml')
        except Exception:
            try:
                return BeautifulSoup(html_content, 'html.parser')
            except Exception:
                return None

    @staticmethod
    def extract_text(soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract text from HTML using CSS selector."""
        try:
            element = soup.select_one(selector)
            return element.get_text(strip=True) if element else None
        except Exception:
            return None

    @staticmethod
    def extract_attr(soup: BeautifulSoup, selector: str, attribute: str) -> Optional[str]:
        """Extract attribute from HTML using CSS selector."""
        try:
            element = soup.select_one(selector)
            return element.get(attribute) if element else None
        except Exception:
            return None

    @staticmethod
    def extract_all_text(soup: BeautifulSoup, selector: str) -> list:
        """Extract all text elements matching selector."""
        try:
            elements = soup.select(selector)
            return [elem.get_text(strip=True) for elem in elements]
        except Exception:
            return []
