import os
import json
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base AI Agent that communicates with Google Gemini or OpenAI, or falls back to a rule-based parser."""
    
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        
        self.use_gemini = False
        self.use_openai = False
        
        if self.gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                self.use_gemini = True
                logger.info("BaseAgent: Configured Google Gemini client.")
            except ImportError:
                logger.warning("BaseAgent: google-generativeai package missing but GEMINI_API_KEY found.")
                
        elif self.openai_key and not self.use_gemini:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_key)
                self.use_openai = True
                logger.info("BaseAgent: Configured OpenAI client.")
            except ImportError:
                logger.warning("BaseAgent: openai package missing but OPENAI_API_KEY found.")
                
        if not self.use_gemini and not self.use_openai:
            logger.info("BaseAgent: Running in MOCK/HEURISTIC offline mode (no LLM keys configured).")
            
    def call_llm(self, prompt: str, retries: int = 3, delay: float = 1.0) -> str:
        """Call LLM with retries."""
        if self.use_gemini:
            import google.generativeai as genai
            for attempt in range(retries):
                try:
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction=self.system_prompt
                    )
                    response = model.generate_content(prompt)
                    return response.text.strip()
                except Exception as e:
                    logger.error(f"Gemini API attempt {attempt+1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay * (2 ** attempt))
            
        elif self.use_openai:
            for attempt in range(retries):
                try:
                    response = self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.2
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    logger.error(f"OpenAI API attempt {attempt+1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay * (2 ** attempt))
                        
        return self._heuristic_mock_parse(prompt)
        
    def _heuristic_mock_parse(self, prompt: str) -> str:
        """Heuristics engine to analyze Instamart reviews offline."""
        content = prompt.lower()
        
        # Sentiment
        sentiment = "neutral"
        if any(w in content for w in ["love", "amazing", "great", "excellent", "superb", "best", "saving"]):
            sentiment = "positive"
        elif any(w in content for w in ["bad", "smell", "decay", "overprice", "waste", "scam", "annoy", "frustrat", "worst", "hate", "rotten"]):
            sentiment = "negative"
            
        # User Segment
        segment = "Routine Buyer"
        if "dog" in content or "cat" in content or "pet" in content or "whiskas" in content or "pedigree" in content:
            segment = "Pet Owner"
        elif "baby" in content or "diaper" in content or "formula" in content or "pampers" in content:
            segment = "Baby Product Buyer"
        elif "price" in content or "fee" in content or "charge" in content or "expensive" in content or "overpriced" in content or "dmart" in content:
            segment = "Price-Sensitive Shopper"
        elif "health" in content or "organic" in content or "seed" in content or "olive oil" in content:
            segment = "Health-Conscious Buyer"
        elif "student" in content or "pg" in content or "hostel" in content:
            segment = "Student"
        elif "working" in content or "office" in content or "job" in content or "busy" in content:
            segment = "Working Professional"
        elif "family" in content or "kids" in content or "wife" in content:
            segment = "Family Planner"
        elif "try" in content or "recommend" in content or "explore" in content:
            segment = "Experiment Seeker"
            
        # Categories
        categories = []
        if "milk" in content or "bread" in content or "curd" in content or "egg" in content or "butter" in content:
            categories.append("Dairy, Bread & Eggs")
        if "vegetable" in content or "fruit" in content or "tomato" in content or "onion" in content or "fresh" in content:
            categories.append("Fruits & Vegetables")
        if "shampoo" in content or "face wash" in content or "soap" in content or "beauty" in content or "cosmetics" in content or "makeup" in content:
            categories.append("Personal Care")
        if "dog" in content or "cat" in content or "pet" in content or "whiskas" in content:
            categories.append("Pet Care")
        if "baby" in content or "diaper" in content or "formula" in content:
            categories.append("Baby Care")
        if "cleaner" in content or "floor" in content or "detergent" in content or "handwash" in content or "soap" in content:
            categories.append("Cleaning & Household")
        if "chicken" in content or "meat" in content or "fish" in content or "seafood" in content:
            categories.append("Meat & Fish")
        if "chips" in content or "snack" in content or "biscuit" in content or "cookie" in content or "nachos" in content:
            categories.append("Snacks & Munchies")
        if "sprite" in content or "pepsi" in content or "drink" in content or "beverage" in content or "juice" in content:
            categories.append("Beverages")
        if "knife" in content or "charging" in content or "kitchen" in content or "home" in content:
            categories.append("Kitchen & Home Essentials")
        if "organic" in content or "olive oil" in content or "seeds" in content:
            categories.append("Gourmet & Organic")
            
        if not categories:
            categories = ["Dairy, Bread & Eggs"]
            
        # Barriers
        barriers = []
        if "stock" in content or "notify" in content:
            barriers.append("Niche items frequently out-of-stock")
        if "brand" in content or "choice" in content or "variety" in content or "limited" in content or "nykaa" in content or "heads up" in content:
            barriers.append("Prefers specialized apps (FirstCry, Nykaa, Heads Up For Tails)")
        if "price" in content or "expensive" in content or "overprice" in content or "dmart" in content:
            barriers.append("Pricing is higher compared to local supermarkets (DMart)")
        if "fee" in content or "charge" in content or "surge" in content or "handling" in content:
            barriers.append("High delivery/surge fees on small value items")
        if "quality" in content or "smell" in content or "decay" in content or "rotten" in content or "freshness" in content:
            barriers.append("Fears about quality of fresh produce or meats")
        if "search" in content or "suggest" in content or "find" in content or "discover" in content or "hidden" in content:
            barriers.append("Difficulty discovering category menu or poor search matching")
        if "pass" in content or "one" in content or "membership" in content or "threshold" in content:
            barriers.append("Loyalty/Instamart Pass discounts do not apply to other categories")
            
        # Motivations
        motivations = []
        if "discount" in content or "off" in content or "coupon" in content or "deals" in content:
            motivations.append("Custom discounts on new categories")
        if "search" in content or "suggest" in content or "recommend" in content:
            motivations.append("Smart basket suggestions")
        if "pass" in content or "one" in content:
            motivations.append("Swiggy One cross-vertical rewards")
            
        # Pain points
        pain_points = []
        if barriers:
            pain_points.extend(barriers)
        if "delivery" in content or "time" in content:
            pain_points.append("Delivery delays")
            
        # Intent
        intent = "Purchase daily groceries and items in 10 minutes"
        if "dog" in content or "cat" in content:
            intent = "Order pet supplies quickly"
        elif "baby" in content:
            intent = "Order emergency baby products"
            
        # Determine willing
        willing = "Undecided"
        if "try" in content or "recommend" in content or "explore" in content:
            willing = "Yes"
        elif "never" in content or "strictly" in content or "only buy" in content or "dmart" in content:
            willing = "No"
            
        response = {
            "sentiment": sentiment,
            "summary": f"Customer expresses {sentiment} experience with Instamart category items.",
            "intent": intent,
            "barriers": barriers,
            "motivations": motivations,
            "pain_points": pain_points,
            "feature_requests": ["Restock niche items" if "stock" in content else "Reduce surge fees"],
            "shopping_behavior": "Routine Buyer" if willing == "No" else ("Experiment Seeker" if willing == "Yes" else "Occasional Buyer"),
            "user_segment": segment,
            "detected_categories": categories
        }
        
        return json.dumps(response)
        
    def parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse JSON response from LLM."""
        try:
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Failed to parse JSON response: {e}. Raw response: {text}")
            return {
                "sentiment": "neutral",
                "summary": "Failed to parse analysis.",
                "intent": "Unknown",
                "barriers": [],
                "motivations": [],
                "pain_points": [],
                "feature_requests": [],
                "shopping_behavior": "Routine Buyer",
                "user_segment": "Routine Buyer",
                "detected_categories": []
            }
