import logging
from typing import List, Dict, Any
from datetime import datetime
from src.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

# Heuristic category/willingness tagger for real reviews
def tag_behavior_heuristics(content: str) -> Dict[str, Any]:
    text = content.lower()
    
    # Defaults
    primary = "Dairy, Bread & Eggs"
    willing = "Undecided"
    interest = []
    barrier = "No specific friction mentioned"
    
    # Tag primary category based on keyword matches
    if any(w in text for w in ["veggie", "vegetable", "onion", "tomato", "potato", "fruit", "mango", "apple"]):
        primary = "Fruits & Vegetables"
    elif any(w in text for w in ["shampoo", "soap", "brush", "beauty", "cream", "lotion", "serum", "lipstick"]):
        primary = "Personal Care"
    elif any(w in text for w in ["milk", "curd", "paneer", "cheese", "bread", "butter", "egg"]):
        primary = "Dairy, Bread & Eggs"
    elif any(w in text for w in ["dog", "cat", "pet", "pedigree", "whiskas"]):
        primary = "Pet Care"
    elif any(w in text for w in ["baby", "diaper", "formula", "pampers", "baby food"]):
        primary = "Baby Care"
    elif any(w in text for w in ["harpic", "surf", "cleaning", "lizol", "detergent", "vessel"]):
        primary = "Cleaning & Household"
    elif any(w in text for w in ["chicken", "meat", "mutton", "fish", "prawn"]):
        primary = "Meat & Fish"
    elif any(w in text for w in ["chips", "maggi", "kurkure", "snack", "biscuit", "cookie"]):
        primary = "Snacks & Munchies"
    elif any(w in text for w in ["coke", "sprite", "juice", "pepsi", "drink", "beverage", "water"]):
        primary = "Beverages"
        
    # Tag willingness and interest
    if "wish they had" in text or "should add" in text or "please stock" in text:
        willing = "Yes"
        if "dog" in text or "cat" in text or "pet" in text:
            interest.append("Pet Care")
        if "baby" in text or "diaper" in text:
            interest.append("Baby Care")
        if "skincare" in text or "makeup" in text:
            interest.append("Personal Care")
    elif any(w in text for w in ["only buy", "strictly buy", "never buy", "won't buy"]):
        willing = "No"
        
    # Tag barriers
    if "stock" in text or "not available" in text or "unavailable" in text:
        barrier = "Frequent out-of-stock issues"
    elif "price" in text or "costly" in text or "expensive" in text or "overpriced" in text:
        barrier = "High price margins compared to local markets"
    elif "delivery charge" in text or "surge" in text or "handling fee" in text or "extra charges" in text:
        barrier = "Surge fees and checkout charges on small orders"
    elif "bad quality" in text or "rotten" in text or "decayed" in text or "smelly" in text:
        barrier = "Quality concerns on fresh items"
    elif "search" in text or "find" in text or "hidden" in text:
        barrier = "Poor discoverability or category search layout"
        
    return {
        "primary_purchased_category": primary,
        "willing_to_try_new": willing,
        "new_categories_of_interest": interest,
        "barrier_reason": barrier
    }

class PlayStoreScraper(BaseScraper):
    """Scrapes customer reviews from Google Play Store for Swiggy (in.swiggy.android)."""
    
    def __init__(self, app_id: str = "in.swiggy.android", lang: str = "en", country: str = "in"):
        self.app_id = app_id
        self.lang = lang
        self.country = country
        
    def scrape(self, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            from google_play_scraper import reviews, Sort
        except ImportError:
            logger.warning("google-play-scraper package not installed. Skipping Play Store.")
            return []
            
        logger.info(f"Scraping Play Store for app {self.app_id} (limit={limit})...")
        
        all_reviews = []
        continuation_token = None
        batch_size = min(200, limit)
        
        try:
            while len(all_reviews) < limit:
                current_batch_size = min(batch_size, limit - len(all_reviews))
                batch, continuation_token = reviews(
                    self.app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.MOST_RELEVANT,
                    count=current_batch_size,
                    continuation_token=continuation_token
                )
                
                if not batch:
                    break
                    
                for r in batch:
                    content = r.get("content", "")
                    rating = r.get("score")
                    at_val = r.get("at")
                    created_at = at_val.isoformat() if isinstance(at_val, datetime) else str(at_val)
                    
                    behavior = tag_behavior_heuristics(content)
                    
                    all_reviews.append({
                        "id": f"gp_{r.get('reviewId')}",
                        "platform": "play_store",
                        "author": r.get("userName", "Anonymous"),
                        "raw_content": content,
                        "rating": rating,
                        "created_at": created_at,
                        "url": f"https://play.google.com/store/apps/details?id={self.app_id}&reviewId={r.get('reviewId')}",
                        "language": "en",
                        **behavior,
                        "is_spam": 0
                    })
                    
                if not continuation_token:
                    break
                    
            logger.info(f"Successfully scraped {len(all_reviews)} Play Store reviews.")
            return all_reviews[:limit]
        except Exception as e:
            logger.error(f"Error scraping Play Store: {e}")
            return []
