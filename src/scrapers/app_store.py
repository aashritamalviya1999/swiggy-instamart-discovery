import logging
import requests
import uuid
from typing import List, Dict, Any
from datetime import datetime
from src.scrapers.base import BaseScraper
from src.scrapers.play_store import tag_behavior_heuristics

logger = logging.getLogger(__name__)

class AppStoreScraper(BaseScraper):
    """Scrapes customer reviews from Apple App Store for Swiggy using the iTunes RSS JSON feed."""
    
    def __init__(self, app_id: int = 989540920, country: str = "in"):
        self.app_id = app_id
        self.country = country
        
    def scrape(self, limit: int = 100) -> List[Dict[str, Any]]:
        logger.info(f"Scraping App Store via iTunes RSS for App ID {self.app_id} (limit={limit})...")
        
        # iTunes customer reviews feed URL
        url = f"https://itunes.apple.com/{self.country}/rss/customerreviews/id={self.app_id}/mostrecent/json"
        
        all_reviews = []
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if response.status_code != 200:
                logger.warning(f"App Store RSS returned status code {response.status_code}")
                return []
                
            data = response.json()
            feed = data.get("feed", {})
            entries = feed.get("entry", [])
            
            # If there's only one entry, it might be a dict instead of a list
            if isinstance(entries, dict):
                entries = [entries]
                
            # The first entry in the RSS feed is often the app metadata itself, skip if it doesn't have an author
            for entry in entries:
                if "author" not in entry:
                    continue
                    
                author = entry.get("author", {}).get("name", {}).get("label", "Anonymous")
                title = entry.get("title", {}).get("label", "")
                content = entry.get("content", {}).get("label", "")
                rating_str = entry.get("im:rating", {}).get("label", "0")
                rating = int(rating_str) if rating_str.isdigit() else 0
                
                review_id = entry.get("id", {}).get("label", f"as_{self.app_id}_{uuid.uuid4().hex[:6]}")
                
                full_content = f"{title} - {content}" if title else content
                behavior = tag_behavior_heuristics(full_content)
                
                # Default created_at if not present
                created_at = datetime.now().isoformat()
                
                all_reviews.append({
                    "id": f"as_{review_id}",
                    "platform": "app_store",
                    "author": author,
                    "raw_content": full_content,
                    "rating": rating,
                    "created_at": created_at,
                    "url": f"https://apps.apple.com/in/app/swiggy/id{self.app_id}",
                    "language": "en",
                    **behavior,
                    "is_spam": 0
                })
                
                if len(all_reviews) >= limit:
                    break
                    
            logger.info(f"Successfully fetched {len(all_reviews)} App Store reviews.")
            return all_reviews
        except Exception as e:
            logger.error(f"Error scraping App Store RSS feed: {e}")
            return []
