import logging
from typing import List, Dict, Any
from src.scrapers.play_store import PlayStoreScraper
from src.scrapers.app_store import AppStoreScraper
from src.scrapers.reddit import RedditScraper
from src.scrapers.mock_generator import MockDataGenerator

logger = logging.getLogger(__name__)

def collect_all_sources(target_count: int = 1000) -> List[Dict[str, Any]]:
    """
    Collect reviews from Play Store, App Store, Reddit, and fill the rest 
    using the high-fidelity mock generator to achieve the exact target distribution.
    Enforces exact platform counts (Reddit: 200, Play Store: 300, etc. for 1000 target).
    """
    # Scale targets based on requested count (default 1000)
    scale = target_count / 1000.0
    targets = {
        "play_store": int(300 * scale),
        "reddit": int(200 * scale),
        "app_store": int(150 * scale),
        "youtube": int(150 * scale),
        "twitter": int(100 * scale),
        "quora": int(100 * scale)
    }
    
    # Adjust for rounding to ensure sum is exactly target_count
    diff = target_count - sum(targets.values())
    if diff != 0:
        targets["play_store"] += diff
        
    collected_by_platform = {p: [] for p in targets}
    
    # 1. Play Store
    try:
        ps = PlayStoreScraper()
        ps_data = ps.scrape(limit=targets["play_store"])
        collected_by_platform["play_store"].extend(ps_data)
        logger.info(f"Collected {len(ps_data)} reviews from Play Store.")
    except Exception as e:
        logger.error(f"Play Store scraper failed: {e}")
        
    # 2. App Store
    try:
        as_scraper = AppStoreScraper()
        as_data = as_scraper.scrape(limit=targets["app_store"])
        collected_by_platform["app_store"].extend(as_data)
        logger.info(f"Collected {len(as_data)} reviews from App Store.")
    except Exception as e:
        logger.error(f"App Store scraper failed: {e}")
        
    # 3. Reddit
    try:
        rs = RedditScraper()
        rs_data = rs.scrape(limit=targets["reddit"])
        collected_by_platform["reddit"].extend(rs_data)
        logger.info(f"Collected {len(rs_data)} posts from Reddit.")
    except Exception as e:
        logger.error(f"Reddit scraper failed: {e}")
        
    mg = MockDataGenerator()
    final_data = []
    
    for platform, target in targets.items():
        scraped = collected_by_platform[platform]
        unique_scraped = {item["id"]: item for item in scraped}
        scraped_list = list(unique_scraped.values())
        scraped_count = len(scraped_list)
        
        if scraped_count < target:
            remainder = target - scraped_count
            logger.info(f"Generating {remainder} mock entries for {platform} to reach target {target}.")
            mock_list = mg.generate_for_platforms({platform: remainder})
            scraped_list.extend(mock_list)
            
        final_data.extend(scraped_list[:target])
        
    logger.info(f"Successfully compiled baseline dataset with {len(final_data)} entries.")
    return final_data
