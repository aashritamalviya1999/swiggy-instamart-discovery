import argparse
import logging
import pandas as pd
from src.database.connection import init_db, save_reviews, get_all_reviews
from src.scrapers import collect_all_sources
from src.database.exporter import export_reviews_to_csv
from src.config import CSV_PATH

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_ingestion(count: int):
    logger.info(f"Initializing database and starting Swiggy Instamart Ingestion (Target: {count} reviews)...")
    
    # 1. Initialize Database Schema
    if not init_db():
        logger.error("Failed to initialize database. Exiting.")
        return
        
    # 2. Run Data Collection
    reviews_list = collect_all_sources(target_count=count)
    
    # 3. Save to Database
    save_reviews(reviews_list)
    
    # 4. Save to CSV
    export_reviews_to_csv(reviews_list, output_path=CSV_PATH)
    
    # 5. Baseline PM Aggregate Analysis
    print_pm_baseline_report(reviews_list)

def print_pm_baseline_report(reviews):
    """Analyze the collected data and print the baseline metrics requested by the Product Manager."""
    df = pd.DataFrame(reviews)
    
    total_records = len(df)
    print("\n" + "="*60)
    print("      SWIGGY INSTAMART PRODUCT DISCOVERY BASELINE REPORT")
    print("="*60)
    print(f"Total Feedback Records Ingested: {total_records}")
    print(f"Data Sources Covered: {df['platform'].nunique()} sources")
    print(" - " + ", ".join(df['platform'].unique()))
    print("-"*60)
    
    # 1. Mostly Purchased Categories
    print("\n[1] MOSTLY PURCHASED / ACTIVE CATEGORIES:")
    cat_counts = df['primary_purchased_category'].value_counts()
    cat_pcts = (cat_counts / total_records * 100).round(1)
    
    for cat, count in cat_counts.items():
        pct = cat_pcts[cat]
        print(f"  * {cat:<30}: {count:>4} orders ({pct:>4}%)")
        
    # 2. Willingness to Explore New Categories
    print("\n[2] CROSS-CATEGORY EXPLORATION WILLINGNESS:")
    will_counts = df['willing_to_try_new'].value_counts()
    will_pcts = (will_counts / total_records * 100).round(1)
    
    print(f"  * Willing to Explore (Yes)    : {will_counts.get('Yes', 0):>4} customers ({will_pcts.get('Yes', 0.0):>4}%)")
    print(f"  * Hesitant / Unwilling (No)   : {will_counts.get('No', 0):>4} customers ({will_pcts.get('No', 0.0):>4}%)")
    print(f"  * Undecided / Neutral         : {will_counts.get('Undecided', 0):>4} customers ({will_pcts.get('Undecided', 0.0):>4}%)")
    
    # 3. Key Target Categories of Interest (For willing users)
    print("\n[3] CATEGORIES TARGET CUSTOMERS ARE WILLING TO TRY:")
    interested_cats = []
    for item in df['new_categories_of_interest']:
        if isinstance(item, list):
            interested_cats.extend(item)
            
    if interested_cats:
        interest_counts = pd.Series(interested_cats).value_counts()
        for cat, count in interest_counts.items():
            print(f"  * {cat:<30}: {count:>4} customers interested")
    else:
        print("  * No target categories listed.")
        
    # 4. Primary Friction/Barrier Reasons
    print("\n[4] PRIMARY ADOPTION BARRIERS (WHY USERS DO NOT EXPLORE):")
    barrier_counts = df['barrier_reason'].value_counts()
    barrier_pcts = (barrier_counts / total_records * 100).round(1)
    
    for barrier, count in barrier_counts.items():
        pct = barrier_pcts[barrier]
        print(f"  * {barrier:<55}: {count:>4} reports ({pct:>4}%)")
        
    print("="*60 + "\n")
    print("[+] SQLite DB Location: data/database.db")
    print(f"[+] Consolidated CSV Location: {CSV_PATH}")
    print("="*60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest customer feedback and generate PM baseline insights.")
    parser.add_argument("-n", "--count", type=int, default=1000, help="Number of records to collect (default: 1000)")
    
    args = parser.parse_args()
    run_ingestion(args.count)
