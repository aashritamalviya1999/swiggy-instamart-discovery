import json
import logging
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.database.connection import get_db_connection, save_clusters
from src.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

# Predefined fallback labels for Swiggy Instamart KMeans clusters (Offline mode)
FALLBACK_CLUSTERS = [
    {
        "name": "Convenience Grocery & Repeat Habits",
        "subtheme": "High Frequency Routine Ordering Patterns",
        "description": "Users buying daily essentials (milk, eggs, curd, bread) who view Swiggy Instamart as a fast utility rather than a discovery or full-shopping platform."
    },
    {
        "name": "Catalog & Stock Limitations",
        "subtheme": "Out-of-Stock and Missing Premium Brands",
        "description": "Friction from unavailable items in niche sections (e.g. M-size diapers in Baby Care) or missing specialized brands in Beauty/Pet Care, causing users to shop elsewhere."
    },
    {
        "name": "Checkout Fees & Surge Friction",
        "subtheme": "Micro-order Surge Charges and Fees",
        "description": "User complaints regarding added delivery fees, surge pricing, handling fees, or Swiggy One minimum spend thresholds that make single category item trial too expensive."
    },
    {
        "name": "Perishables Quality & Freshness Fears",
        "subtheme": "Fruits, Vegetables & Meats Trust Deficit",
        "description": "Hesitancy to buy fresh produce or fresh meats due to concerns about receiving rotten, bruised, or non-hygienic products compared to local cart vendors."
    }
]

def run_theme_clustering(num_clusters: int = 4):
    """
    Load cleaned reviews, compute TF-IDF embeddings,
    cluster them using KMeans, label clusters via LLM or fallbacks,
    and save results to SQLite.
    """
    logger.info("Starting theme clustering pipeline...")
    
    with get_db_connection() as conn:
        reviews = conn.execute(
            "SELECT id, cleaned_content FROM reviews WHERE is_spam = 0 AND cleaned_content IS NOT NULL AND cleaned_content != ''"
        ).fetchall()
        
    if len(reviews) < num_clusters:
        logger.warning(f"Not enough reviews to perform KMeans clustering (found {len(reviews)}). Skipping.")
        return
        
    corpus = [r["cleaned_content"] for r in reviews]
    review_ids = [r["id"] for r in reviews]
    
    try:
        # 1. Compute TF-IDF matrix
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(corpus)
        
        # 2. Run KMeans clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto')
        kmeans.fit(X)
        
        labels = kmeans.labels_
        transform_dist = kmeans.transform(X)
        distances = [transform_dist[i, labels[i]] for i in range(len(corpus))]
        
        # Group reviews
        clustered_docs = {i: [] for i in range(num_clusters)}
        for doc_idx, label in enumerate(labels):
            clustered_docs[label].append({
                "id": review_ids[doc_idx],
                "content": corpus[doc_idx],
                "distance": float(distances[doc_idx])
            })
            
        # 3. Label Clusters
        clusters_list = []
        review_mappings = []
        
        agent = BaseAgent("") # Setup base agent to use LLM for cluster summary if key is present
        
        for cluster_idx in range(num_clusters):
            docs = clustered_docs[cluster_idx]
            docs_sample = [d["content"] for d in docs[:5]]
            sample_text = "\n".join([f"- {txt}" for txt in docs_sample])
            
            cluster_name = ""
            subtheme = ""
            description = ""
            
            if agent.use_gemini or agent.use_openai:
                prompt = f"""
                You are a Staff Product Manager. Analyze the following group of Swiggy Instamart customer feedback from the same cluster:
                
                {sample_text}
                
                Generate:
                1. A short, professional cluster name (3-5 words).
                2. A subtheme description (5-8 words).
                3. A detailed 1-2 sentence description of what these reviews complain about or discuss.
                
                Format your output as a valid JSON object:
                {{
                  "name": "Cluster Name",
                  "subtheme": "Subtheme summary",
                  "description": "Detailed description of the cluster theme."
                }}
                """
                raw_response = agent.call_llm(prompt)
                try:
                    res = json.loads(raw_response.strip())
                    cluster_name = res.get("name", FALLBACK_CLUSTERS[cluster_idx]["name"])
                    subtheme = res.get("subtheme", FALLBACK_CLUSTERS[cluster_idx]["subtheme"])
                    description = res.get("description", FALLBACK_CLUSTERS[cluster_idx]["description"])
                except Exception as e:
                    logger.error(f"Error parsing cluster labeling: {e}")
                    
            if not cluster_name:
                fallback = FALLBACK_CLUSTERS[cluster_idx % len(FALLBACK_CLUSTERS)]
                cluster_name = fallback["name"]
                subtheme = fallback["subtheme"]
                description = fallback["description"]
                
            clusters_list.append({
                "name": cluster_name,
                "subtheme": subtheme,
                "description": description,
                "size": len(docs)
            })
            
            # Map reviews
            for doc in docs:
                review_mappings.append({
                    "review_id": doc["id"],
                    "cluster_name": cluster_name,
                    "distance": doc["distance"]
                })
                
        # 4. Save to Database
        save_clusters(clusters_list, review_mappings)
        logger.info("Theme clustering pipeline run completed and results saved.")
        
    except Exception as e:
        logger.error(f"Error running theme clustering pipeline: {e}")
        logger.exception(e)
