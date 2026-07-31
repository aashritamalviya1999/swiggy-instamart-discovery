# REST API Documentation

The Swiggy Instamart AI Product Discovery Engine exposes a REST API built with FastAPI. These endpoints allow external PM tools or engineering backends to trigger analysis runs, query processed reviews, and fetch synthesized opportunities.

Default Base URL: `http://127.0.0.1:8000`

---

## 🚦 Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health Check endpoint |
| `POST` | `/api/pipeline/run` | Trigger the 7-Agent Analysis Pipeline |
| `GET` | `/api/reviews` | Retrieve AI-analyzed review profiles |
| `GET` | `/api/insights` | Retrieve validated PM UX insights |
| `GET` | `/api/opportunities` | Retrieve ICE-prioritized product opportunities |
| `GET` | `/api/clusters` | Retrieve KMeans thematic clusters |

---

## 🔍 Endpoint Details

### 1. Health Check
*   **URL**: `/api/health`
*   **Method**: `GET`
*   **Response (`200 OK`)**:
    ```json
    {
      "status": "healthy",
      "service": "instamart-discovery-api"
    }
    ```

---

### 2. Trigger Pipeline Run
*   **URL**: `/api/pipeline/run`
*   **Method**: `POST`
*   **Parameters**:
    *   `target_count` (int, query, optional): Target count of items to collect. Default: `1000`.
*   **Response (`200 OK`)**:
    ```json
    {
      "status": "success",
      "reviews_collected": 1000,
      "reviews_cleaned": 1000,
      "reviews_analyzed": 260,
      "insights_generated": 9,
      "opportunities_generated": 4
    }
    ```
*   **cURL Example**:
    ```bash
    curl -X POST "http://127.0.0.1:8000/api/pipeline/run?target_count=1000"
    ```

---

### 3. Query Reviews
*   **URL**: `/api/reviews`
*   **Method**: `GET`
*   **Parameters**:
    *   `platform` (string, query, optional): Filter by platform (e.g. `play_store`).
    *   `sentiment` (string, query, optional): Filter by sentiment (`positive`, `neutral`, `negative`).
    *   `segment` (string, query, optional): Filter by user segment (e.g. `Pet Owner`).
    *   `category` (string, query, optional): Filter by category (e.g. `Pet Care`).
    *   `limit` (int, query, optional): Number of results to return. Default: `50`.
*   **Response (`200 OK`)**:
    ```json
    {
      "count": 1,
      "reviews": [
        {
          "id": "play_store_102",
          "platform": "play_store",
          "author": "Aman Sharma",
          "raw_content": "Whiskas cat food is always out of stock on Instamart. I have to buy from super market.",
          "cleaned_content": "whiskas cat food is always out of stock on instamart i have to buy from super market",
          "rating": 2,
          "created_at": "2026-07-27T12:00:00",
          "url": "",
          "language": "en",
          "primary_purchased_category": "Pet Care",
          "willing_to_try_new": "No",
          "new_categories_of_interest": [],
          "barrier_reason": "Niche items frequently out-of-stock",
          "is_spam": 0,
          "sentiment": "negative",
          "summary": "Customer complains about out-of-stock pet food items on Instamart.",
          "intent": "Order pet supplies quickly",
          "barriers": ["Niche items frequently out-of-stock"],
          "motivations": [],
          "pain_points": ["Niche items frequently out-of-stock"],
          "feature_requests": ["Restock niche items"],
          "shopping_behavior": "Routine Buyer",
          "user_segment": "Pet Owner",
          "detected_categories": ["Pet Care"]
        }
      ]
    }
    ```

---

### 4. Fetch PM Insights
*   **URL**: `/api/insights`
*   **Method**: `GET`
*   **Response (`200 OK`)**:
    ```json
    {
      "insights": [
        {
          "id": 1,
          "question": "Why do users repeatedly buy from the same categories?",
          "answer": "Users build strong operational habits around core convenience items like 'Dairy, Bread & Eggs'...",
          "confidence_score": 0.85,
          "supporting_reviews_count": 120,
          "supporting_quotes": ["...", "..."],
          "platforms": ["play_store"],
          "contradicting_opinions": ["..."],
          "confidence_explanation": "Validated against 120 reviews matching key search signals."
        }
      ]
    }
    ```

---

### 5. Fetch Opportunities
*   **URL**: `/api/opportunities`
*   **Method**: `GET`
*   **Response (`200 OK`)**:
    ```json
    {
      "opportunities": [
        {
          "id": 1,
          "title": "Smart Cart Cross-Category Bundler",
          "problem": "Users stick to routine categories (milk/bread) and fail to discover other sections...",
          "evidence": "Checkout fees and poor discoverability are identified as top barriers in 40% of reviews.",
          "representative_quotes": ["...", "..."],
          "frequency": "High",
          "impact": 8.5,
          "confidence": 9.0,
          "opportunity_score": 76.5,
          "business_value": "Increases Average Order Value (AOV) by 15-20%..."
        }
      ]
    }
    ```
