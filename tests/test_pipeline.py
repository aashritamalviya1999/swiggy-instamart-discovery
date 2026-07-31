import pytest
import sqlite3
import json
from src.pipeline.cleaner import FeedbackCleaner
from src.database.connection import init_db, get_db_connection, save_reviews, get_all_reviews
from src.agents.base_agent import BaseAgent
from src.pipeline.clusterer import run_theme_clustering

def test_cleaner_is_spam():
    # Valid customer reviews
    assert not FeedbackCleaner.is_spam("Ordered curd and bread from Swiggy Instamart, they delivered in 9 minutes.")
    assert not FeedbackCleaner.is_spam("diapers for my baby are completely out of stock on Instamart. Disappointing.")
    
    # Referral spam codes
    assert FeedbackCleaner.is_spam("Use code EXTRA50 to get massive discounts on vegetables. Try now!")
    
    # Noise/too short
    assert FeedbackCleaner.is_spam("great")
    assert FeedbackCleaner.is_spam("bad app")

def test_cleaner_removes_urls_and_emojis():
    raw_text = "Check out Instamart at http://swiggy.com/instamart 🍊⚡ Very fast!"
    # remove_urls leaves double spaces
    url_removed = FeedbackCleaner.remove_urls(raw_text)
    assert "http://swiggy.com/instamart" not in url_removed
    
    emoji_removed = FeedbackCleaner.remove_emojis(url_removed)
    assert "🍊" not in emoji_removed
    assert "⚡" not in emoji_removed
    
    # Final cleanup assertion
    clean_pipeline = FeedbackCleaner()
    res = clean_pipeline.clean_review({"raw_content": raw_text})
    assert res["cleaned_content"] == "Check out Instamart at Very fast!"

def test_cleaner_hinglish_translation():
    text = "Instamart ka service bahut accha hai aur vegetables sasta mil raha hai"
    # "bahut" -> "very", "accha" -> "good", "sasta" -> "cheap"
    cleaned = FeedbackCleaner.clean_spelling_and_hinglish(text)
    assert "very" in cleaned
    assert "good" in cleaned
    assert "cheap" in cleaned

def test_database_operations():
    # Init
    assert init_db() is True
    
    # Mock review list
    test_reviews = [
        {
            "id": "test_rev_1",
            "platform": "play_store",
            "author": "Tester One",
            "raw_content": "I strictly buy milk and bread daily.",
            "rating": 4,
            "created_at": "2026-07-27T12:00:00",
            "url": "http://mock.com/1",
            "language": "en",
            "primary_purchased_category": "Dairy, Bread & Eggs",
            "willing_to_try_new": "No",
            "new_categories_of_interest": [],
            "barrier_reason": "Pricing premium",
            "is_spam": 0
        }
    ]
    
    # Save & retrieve
    assert save_reviews(test_reviews) is True
    retrieved = get_all_reviews()
    assert len(retrieved) >= 1
    assert any(r["id"] == "test_rev_1" for r in retrieved)
    assert isinstance(retrieved[0]["new_categories_of_interest"], list)

def test_base_agent_heuristics():
    agent = BaseAgent("System Instruction")
    # Prompt matching pet parent segment
    raw_res = agent.call_llm("I need cat food and whiskas wet treats for my kitten.")
    analysis = agent.parse_json_response(raw_res)
    
    assert analysis["sentiment"] in ["positive", "neutral", "negative"]
    assert "Pet Care" in analysis["detected_categories"]
    assert analysis["user_segment"] == "Pet Owner"
    assert isinstance(analysis["barriers"], list)
