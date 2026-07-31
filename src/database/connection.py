import sqlite3
import json
import logging
from pathlib import Path
from src.config import DB_PATH, PROJECT_ROOT

logger = logging.getLogger(__name__)

def get_db_connection():
    """Establish a connection to the SQLite database with dictionary row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initialize the database using the schema.sql file if tables don't exist."""
    schema_path = PROJECT_ROOT / "schema.sql"
    if not schema_path.exists():
        logger.error(f"schema.sql not found at {schema_path}")
        return False
    
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
            
        with get_db_connection() as conn:
            conn.executescript(schema_sql)
            conn.commit()
        logger.info("Database initialized successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False

def save_reviews(reviews_list):
    """
    Save list of reviews to database.
    Each review should be a dict matching the reviews table fields.
    """
    query = """
    INSERT OR REPLACE INTO reviews (
        id, platform, author, raw_content, cleaned_content, rating, created_at, url, language, 
        primary_purchased_category, willing_to_try_new, new_categories_of_interest, barrier_reason, is_spam
    )
    VALUES (
        :id, :platform, :author, :raw_content, :cleaned_content, :rating, :created_at, :url, :language, 
        :primary_purchased_category, :willing_to_try_new, :new_categories_of_interest, :barrier_reason, :is_spam
    )
    """
    try:
        with get_db_connection() as conn:
            processed_list = []
            for r in reviews_list:
                item = dict(r)
                # Default all keys in reviews schema to None if missing
                for k in ["cleaned_content", "rating", "url", "language", "primary_purchased_category", 
                          "willing_to_try_new", "new_categories_of_interest", "barrier_reason", "is_spam"]:
                    if k not in item:
                        item[k] = None
                
                if isinstance(item.get("new_categories_of_interest"), (list, dict)):
                    item["new_categories_of_interest"] = json.dumps(item["new_categories_of_interest"])
                elif "new_categories_of_interest" not in item or item["new_categories_of_interest"] is None:
                    item["new_categories_of_interest"] = "[]"
                processed_list.append(item)
                
            conn.executemany(query, processed_list)
            conn.commit()
        logger.info(f"Saved/Updated {len(reviews_list)} reviews in the database.")
        return True
    except Exception as e:
        logger.error(f"Error saving reviews to DB: {e}")
        return False

def get_all_reviews():
    """Retrieve all non-spam reviews from the database."""
    query = "SELECT * FROM reviews WHERE is_spam = 0"
    try:
        with get_db_connection() as conn:
            rows = conn.execute(query).fetchall()
            
        reviews_list = []
        for r in rows:
            item = dict(r)
            try:
                item["new_categories_of_interest"] = json.loads(r["new_categories_of_interest"])
            except:
                item["new_categories_of_interest"] = []
            reviews_list.append(item)
        return reviews_list
    except Exception as e:
        logger.error(f"Error reading reviews: {e}")
        return []

def save_analysis_result(analysis):
    """
    Save single AI analysis result.
    """
    query = """
    INSERT OR REPLACE INTO analysis_results (
        review_id, sentiment, summary, intent, barriers, motivations, 
        pain_points, feature_requests, shopping_behavior, user_segment, detected_categories
    ) VALUES (
        :review_id, :sentiment, :summary, :intent, :barriers, :motivations,
        :pain_points, :feature_requests, :shopping_behavior, :user_segment, :detected_categories
    )
    """
    data = dict(analysis)
    for field in ['barriers', 'motivations', 'pain_points', 'feature_requests', 'detected_categories']:
        if field in data and isinstance(data[field], (list, dict)):
            data[field] = json.dumps(data[field])
        elif field not in data:
            data[field] = "[]"
            
    try:
        with get_db_connection() as conn:
            conn.execute(query, data)
            conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error saving analysis result for review {analysis.get('review_id')}: {e}")
        return False

def save_clusters(clusters_list, review_cluster_mappings):
    """
    Save clusters and maps reviews to them.
    """
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM review_clusters;")
            conn.execute("DELETE FROM clusters;")
            
            cluster_id_map = {}
            for cluster in clusters_list:
                cursor = conn.execute(
                    "INSERT INTO clusters (name, subtheme, description, size) VALUES (?, ?, ?, ?)",
                    (cluster['name'], cluster['subtheme'], cluster['description'], cluster['size'])
                )
                generated_id = cursor.lastrowid
                cluster_id_map[cluster['name']] = generated_id
            
            insert_mapping_query = """
            INSERT OR REPLACE INTO review_clusters (review_id, cluster_id, distance)
            VALUES (?, ?, ?)
            """
            mappings_to_insert = []
            for mapping in review_cluster_mappings:
                c_id = cluster_id_map.get(mapping['cluster_name'])
                if c_id:
                    mappings_to_insert.append((mapping['review_id'], c_id, mapping['distance']))
            
            conn.executemany(insert_mapping_query, mappings_to_insert)
            conn.commit()
        logger.info("Saved clusters and mappings successfully.")
        return True
    except Exception as e:
        logger.error(f"Error saving clusters to DB: {e}")
        return False

def save_insights(insights_list):
    """Save synthesized PM insights."""
    query = """
    INSERT INTO insights (
        question, answer, confidence_score, supporting_reviews_count, 
        supporting_quotes, platforms, contradicting_opinions, confidence_explanation
    ) VALUES (
        :question, :answer, :confidence_score, :supporting_reviews_count, 
        :supporting_quotes, :platforms, :contradicting_opinions, :confidence_explanation
    )
    """
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM insights;")
            for insight in insights_list:
                data = dict(insight)
                for list_field in ['supporting_quotes', 'platforms', 'contradicting_opinions']:
                    if list_field in data and isinstance(data[list_field], (list, dict)):
                        data[list_field] = json.dumps(data[list_field])
                    elif list_field not in data:
                        data[list_field] = "[]"
                conn.execute(query, data)
            conn.commit()
        logger.info(f"Saved {len(insights_list)} insights.")
        return True
    except Exception as e:
        logger.error(f"Error saving insights: {e}")
        return False

def save_opportunities(opportunities_list):
    """Save prioritized product opportunities."""
    query = """
    INSERT INTO opportunities (
        title, problem, evidence, representative_quotes, frequency, 
        impact, confidence, opportunity_score, business_value
    ) VALUES (
        :title, :problem, :evidence, :representative_quotes, :frequency, 
        :impact, :confidence, :opportunity_score, :business_value
    )
    """
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM opportunities;")
            for opp in opportunities_list:
                data = dict(opp)
                if 'representative_quotes' in data and isinstance(data['representative_quotes'], (list, dict)):
                    data['representative_quotes'] = json.dumps(data['representative_quotes'])
                elif 'representative_quotes' not in data:
                    data['representative_quotes'] = "[]"
                conn.execute(query, data)
            conn.commit()
        logger.info(f"Saved {len(opportunities_list)} opportunities.")
        return True
    except Exception as e:
        logger.error(f"Error saving opportunities: {e}")
        return False
