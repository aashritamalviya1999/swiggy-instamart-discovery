import logging
from typing import List, Dict, Any
from datetime import datetime
from src.scrapers.base import BaseScraper
from src.scrapers.play_store import tag_behavior_heuristics
from src.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

logger = logging.getLogger(__name__)

class RedditScraper(BaseScraper):
    """Scrapes social posts about Swiggy Instamart from Reddit using PRAW."""
    
    def __init__(self):
        self.client_id = REDDIT_CLIENT_ID
        self.client_secret = REDDIT_CLIENT_SECRET
        self.user_agent = REDDIT_USER_AGENT
        
    def scrape(self, limit: int = 50) -> List[Dict[str, Any]]:
        if not self.client_id or not self.client_secret:
            logger.warning("Reddit API keys missing in environment. Skipping Reddit scraper.")
            return []
            
        try:
            import praw
        except ImportError:
            logger.warning("praw package not installed. Skipping Reddit scraper.")
            return []
            
        logger.info("Initializing PRAW Reddit client...")
        try:
            reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
            
            search_query = "Instamart OR (Swiggy Instamart)"
            logger.info(f"Searching Reddit for query: '{search_query}' (limit={limit})...")
            
            results = []
            submissions = reddit.subreddit("all").search(search_query, sort="relevance", time_filter="year", limit=limit)
            
            for submission in submissions:
                created_utc = datetime.utcfromtimestamp(submission.created_utc).isoformat()
                content = f"Title: {submission.title}\nBody: {submission.selftext}"
                
                behavior = tag_behavior_heuristics(content)
                
                results.append({
                    "id": f"rd_{submission.id}",
                    "platform": "reddit",
                    "author": str(submission.author) if submission.author else "Anonymous",
                    "raw_content": content,
                    "rating": None,
                    "created_at": created_utc,
                    "url": f"https://www.reddit.com{submission.permalink}",
                    "language": "en",
                    **behavior,
                    "is_spam": 0
                })
                
            logger.info(f"Successfully scraped {len(results)} posts from Reddit.")
            return results
        except Exception as e:
            logger.error(f"Error scraping Reddit: {e}")
            return []
