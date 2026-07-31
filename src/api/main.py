import json
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.database.connection import get_db_connection
from src.agents.pipeline_orchestrator import PipelineOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Swiggy Instamart AI Product Discovery Engine API",
    description="Backend endpoints for customer reviews collection, AI behavior extraction, theme clustering, and opportunity scoring.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PipelineRunResponse(BaseModel):
    status: str
    reviews_collected: int
    reviews_cleaned: int
    reviews_analyzed: int
    insights_generated: int
    opportunities_generated: int

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "instamart-discovery-api"}

@app.post("/api/pipeline/run", response_model=PipelineRunResponse)
def run_pipeline(
    target_count: int = Query(default=1000, description="Total target reviews count")
):
    """Trigger the 7-Agent AI Discovery Pipeline to collect, clean, analyze, cluster, and prioritize opportunities."""
    try:
        orchestrator = PipelineOrchestrator()
        result = orchestrator.run_pipeline(target_count=target_count)
        return {
            "status": "success",
            "reviews_collected": result["reviews_collected"],
            "reviews_cleaned": result["reviews_cleaned"],
            "reviews_analyzed": result["reviews_analyzed"],
            "insights_generated": result["insights_generated"],
            "opportunities_generated": result["opportunities_generated"]
        }
    except Exception as e:
        logger.error(f"Error running pipeline via API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews")
def get_reviews(
    platform: Optional[str] = None,
    sentiment: Optional[str] = None,
    segment: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50
):
    """Query reviews with search filters."""
    query = """
    SELECT r.id, r.platform, r.author, r.raw_content, r.cleaned_content, r.rating, r.created_at,
           a.sentiment, a.summary, a.intent, a.barriers, a.motivations, a.pain_points,
           a.feature_requests, a.shopping_behavior, a.user_segment, a.detected_categories
    FROM reviews r
    JOIN analysis_results a ON r.id = a.review_id
    WHERE r.is_spam = 0
    """
    conditions = []
    params = []
    
    if platform:
        conditions.append("r.platform = ?")
        params.append(platform)
    if sentiment:
        conditions.append("a.sentiment = ?")
        params.append(sentiment)
    if segment:
        conditions.append("a.user_segment = ?")
        params.append(segment)
        
    if conditions:
        query += " AND " + " AND ".join(conditions)
        
    query += " LIMIT ?"
    params.append(limit)
    
    try:
        with get_db_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            
        reviews_list = []
        for r in rows:
            rev_dict = dict(r)
            for field in ["barriers", "motivations", "pain_points", "feature_requests", "detected_categories"]:
                try:
                    rev_dict[field] = json.loads(r[field])
                except:
                    rev_dict[field] = []
                    
            if category:
                if category not in rev_dict["detected_categories"]:
                    continue
                    
            reviews_list.append(rev_dict)
            
        return {"count": len(reviews_list), "reviews": reviews_list}
    except Exception as e:
        logger.error(f"Failed to query reviews: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/insights")
def get_insights():
    """Query synthesized PM discovery insights."""
    try:
        with get_db_connection() as conn:
            rows = conn.execute("SELECT * FROM insights").fetchall()
            
        insights_list = []
        for r in rows:
            ins_dict = dict(r)
            for list_field in ["supporting_quotes", "platforms", "contradicting_opinions"]:
                try:
                    ins_dict[list_field] = json.loads(r[list_field])
                except:
                    ins_dict[list_field] = []
            insights_list.append(ins_dict)
            
        return {"insights": insights_list}
    except Exception as e:
        logger.error(f"Failed to fetch insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/opportunities")
def get_opportunities():
    """Query prioritized product opportunities backlog."""
    try:
        with get_db_connection() as conn:
            rows = conn.execute("SELECT * FROM opportunities ORDER BY opportunity_score DESC").fetchall()
            
        opps_list = []
        for r in rows:
            opp_dict = dict(r)
            try:
                opp_dict["representative_quotes"] = json.loads(r["representative_quotes"])
            except:
                opp_dict["representative_quotes"] = []
            opps_list.append(opp_dict)
            
        return {"opportunities": opps_list}
    except Exception as e:
        logger.error(f"Failed to fetch opportunities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clusters")
def get_clusters():
    """Query discovered clusters."""
    try:
        with get_db_connection() as conn:
            rows = conn.execute("SELECT * FROM clusters").fetchall()
        return {"clusters": [dict(r) for r in rows]}
    except Exception as e:
        logger.error(f"Failed to fetch clusters: {e}")
        raise HTTPException(status_code=500, detail=str(e))
