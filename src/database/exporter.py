import csv
import logging
import json
from pathlib import Path
from src.config import CSV_PATH
from src.database.connection import get_db_connection

logger = logging.getLogger(__name__)

def export_reviews_to_csv(reviews_list, output_path=CSV_PATH):
    """
    Legacy exporter, replaced by full database exporter but kept for compatibility.
    """
    return export_full_database_to_csv(output_path=output_path)

def export_full_database_to_csv(output_path=CSV_PATH):
    """
    Export the full merged reviews and AI analysis results to a structured CSV file.
    Includes all AI tags, sentiment, barriers, and segments.
    """
    logger.info(f"Exporting full database to CSV at {output_path}...")
    
    # Ensure parent folder exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    query = """
    SELECT r.id, r.platform, r.author, r.raw_content, r.cleaned_content, r.rating, r.created_at, r.url,
           r.primary_purchased_category, r.willing_to_try_new, r.new_categories_of_interest, r.barrier_reason, r.is_spam,
           a.sentiment, a.summary, a.intent, a.barriers, a.motivations, a.pain_points, a.feature_requests, 
           a.shopping_behavior, a.user_segment, a.detected_categories
    FROM reviews r
    LEFT JOIN analysis_results a ON r.id = a.review_id
    """
    
    try:
        with get_db_connection() as conn:
            rows = conn.execute(query).fetchall()
            
        if not rows:
            logger.warning("No database records found to export.")
            return False
            
        fieldnames = list(rows[0].keys())
        
        with open(output_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for row_data in rows:
                row = {}
                for field in fieldnames:
                    val = row_data[field]
                    # Format lists/JSON arrays nicely for CSV
                    if val is not None and str(val).startswith("[") and str(val).endswith("]"):
                        try:
                            parsed_list = json.loads(val)
                            if isinstance(parsed_list, list):
                                row[field] = ", ".join(map(str, parsed_list))
                            else:
                                row[field] = str(val)
                        except:
                            row[field] = str(val)
                    elif val is None:
                        row[field] = ""
                    else:
                        row[field] = str(val)
                writer.writerow(row)
                
        logger.info(f"CSV export succeeded. File size: {Path(output_path).stat().st_size} bytes.")
        return True
    except Exception as e:
        logger.error(f"Failed to export CSV: {e}")
        return False
