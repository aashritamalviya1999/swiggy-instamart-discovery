from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScraper(ABC):
    """Abstract base class for all Swiggy Instamart ingestion scrapers."""
    
    @abstractmethod
    def scrape(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Scrape reviews or discussions.
        Each dictionary should return:
        - id
        - platform
        - author
        - raw_content
        - rating (int/float or None)
        - created_at
        - url
        - language
        - primary_purchased_category
        - willing_to_try_new
        - new_categories_of_interest
        - barrier_reason
        - is_spam
        """
        pass
