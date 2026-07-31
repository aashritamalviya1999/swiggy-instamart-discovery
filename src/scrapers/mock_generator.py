import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Target categories for Swiggy Instamart
INSTAMART_CATEGORIES = [
    "Fruits & Vegetables",
    "Dairy, Bread & Eggs",
    "Snacks & Munchies",
    "Beverages",
    "Personal Care",
    "Cleaning & Household",
    "Baby Care",
    "Pet Care",
    "Meat & Fish",
    "Kitchen & Home Essentials",
    "Gourmet & Organic"
]

class MockDataGenerator:
    """Generates high-fidelity, unique Swiggy Instamart customer feedback records dynamically."""

    def __init__(self):
        # Grocery items for slot filling
        self.groceries = {
            "Dairy, Bread & Eggs": ["milk", "curd", "bread", "eggs", "butter", "paneer", "cheese"],
            "Fruits & Vegetables": ["tomatoes", "onions", "potatoes", "fresh bananas", "apples", "coriander", "lemons"],
            "Snacks & Munchies": ["chips", "nachos", "biscuits", "cookies", "maggi noodles", "salted peanuts"],
            "Beverages": ["coca-cola", "sprite", "coconut water", "orange juice", "soda bottles", "cold coffee"]
        }
        
        self.time_phrases = ["every single morning", "almost daily", "every evening", "2-3 times a week", "on weekends"]
        self.delivery_adjs = ["super fast", "extremely quick", "incredibly reliable", "always on time", "amazing"]
        self.comp_stores = ["DMart", "local supermarket", "BigBasket", "local grocery store"]

        # User segment definitions
        self.segments = {
            "Pet Owner": {
                "cats": ["Pet Care"],
                "items": ["dog food", "cat food", "wet treats", "dog chew sticks", "litter powder"],
                "stores": ["Heads Up For Tails", "supermarket"],
                "barriers": ["Prefers specialized apps (Heads Up For Tails)", "Niche items frequently out-of-stock"],
                "templates": [
                    "I noticed a pet care section in the menu. I would love to order {item} from Instamart since it saves me a trip. However, they only have 1-2 local brands. If they stock Pedigree or Royal Canin, I will buy every month.",
                    "Why is the pet care section on Swiggy Instamart always empty? Whenever I want to order {item}, they are out of stock. I buy groceries here but order all my pet needs from {store}."
                ]
            },
            "Baby Product Buyer": {
                "cats": ["Baby Care"],
                "items": ["Pampers diapers", "baby wipes", "baby formula", "baby bottle cleaner", "baby shampoo"],
                "stores": ["FirstCry", "pharmacy"],
                "barriers": ["Prefers specialized apps (FirstCry, Nykaa, Heads Up For Tails)", "Niche items frequently out-of-stock"],
                "templates": [
                    "Why is the baby care section on Swiggy Instamart always empty? Whenever I want to order {item}, it is out of stock. I've stopped checking. I buy groceries here but order all my baby needs from {store} now.",
                    "Instamart is great for routine orders, but the baby section has no range. I try to order {item} in emergencies, but they never have the right size or brand. I end up ordering from {store}."
                ]
            },
            "Price-Sensitive Shopper": {
                "cats": ["Personal Care", "Cleaning & Household"],
                "items": ["face wash", "body soap", "shampoo", "floor cleaner", "dishwashing liquid"],
                "stores": ["DMart", "local wholesale market"],
                "barriers": ["Pricing is higher compared to local supermarkets (DMart)", "High delivery/surge fees on small value items"],
                "templates": [
                    "I buy groceries from Instamart, but I never order {item} or household cleaners here. They are far cheaper at {store}, and Instamart prices have a high premium.",
                    "I use Swiggy Instamart for urgent snacks. But the checkout page adds so many fees! Handling fee + delivery charge + surge fee. It doesn't make sense to add a single {item} because the fees double the price compared to {store}."
                ]
            },
            "Experiment Seeker": {
                "cats": ["Gourmet & Organic", "Kitchen & Home Essentials"],
                "items": ["organic chia seeds", "extra virgin olive oil", "kitchen knife", "charging cable", "scented candles"],
                "stores": ["Amazon", "specialty gourmet store"],
                "barriers": ["Difficulty discovering category menu or poor search matching", "Fears about quality of fresh produce or meats"],
                "templates": [
                    "I buy my regular items from Instamart. I saw they launched a gourmet and organic section and wanted to order {item}. But the search didn't show them properly. Will try if they recommend them on my cart page.",
                    "Instamart is fast, and I recently ordered a {item} which arrived in 9 minutes! That was great. I'd love to try ordering premium organic food, but it is very hard to discover in the app's search."
                ]
            },
            "Routine Buyer": {
                "cats": ["Fruits & Vegetables", "Meat & Fish"],
                "items": ["fresh tomatoes", "onions", "coriander leaves", "fresh chicken", "fish fillets"],
                "stores": ["local vendor", "Licious", "Safal"],
                "barriers": ["Fears about quality of fresh produce or meats"],
                "templates": [
                    "Instamart is great for snacks and beverages when friends come over. But I will never buy {item} here. Last time I ordered, they were not fresh. I'd rather buy from my {store}.",
                    "I want to try ordering {item} from Instamart, but I am hesitant about how they package it and if it's fresh. If they guarantee high quality and hygiene like {store}, I am willing to try."
                ]
            }
        }

        # Extra sentences to add random variation
        self.extra_sentences = [
            " Swiggy support is helpful though.",
            " Delivery partner was polite.",
            " It's getting better day by day.",
            " Strongly recommend this app.",
            " Hope they resolve this stock issue soon.",
            " Instamart is saving me so much time.",
            " Placed order from Bangalore.",
            " The delivery speed is unmatched.",
            " Overall good experience with daily items.",
            " I use it almost every day."
        ]

    def generate_single_review(self, platform: str) -> Dict[str, Any]:
        """Generate a single high-fidelity, unique review."""
        # Pick a segment
        segment_name = random.choice(list(self.segments.keys()))
        segment_info = self.segments[segment_name]
        
        # Pick grocery category for the core behavior opener
        grocery_cat = random.choice(list(self.groceries.keys()))
        grocery_items = random.sample(self.groceries[grocery_cat], 2)
        
        opener = f"I order {grocery_items[0]} and {grocery_items[1]} from Swiggy Instamart {random.choice(self.time_phrases)}. It is {random.choice(self.delivery_adjs)}."
        
        # Fill template for target segment
        template = random.choice(segment_info["templates"])
        item = random.choice(segment_info["items"])
        store = random.choice(segment_info["stores"])
        
        body = template.format(item=item, store=store)
        
        # Combine opener and body
        raw_content = f"{opener} {body}"
        if random.random() > 0.5:
            raw_content += " " + random.choice(self.extra_sentences)
            
        # Determine willingness and barriers based on segment
        willing = "Undecided"
        if segment_name in ["Experiment Seeker"]:
            willing = "Yes"
        elif segment_name in ["Routine Buyer", "Price-Sensitive Shopper"]:
            willing = "No"
            
        barrier = random.choice(segment_info["barriers"])
        
        # Rating logic (1-5 stars)
        rating = None
        if platform in ["play_store", "app_store"]:
            if willing == "Yes":
                rating = random.choice([4, 5])
            elif willing == "No":
                rating = random.choice([1, 2, 3])
            else:
                rating = random.choice([2, 3, 4])
                
        # Author details
        first_names = ["Arjun", "Priya", "Rahul", "Sneha", "Karan", "Anjali", "Vikram", "Deepa", "Amit", "Neha", "Rohan", "Meera", "Sanjay", "Kavita", "Ravi", "Divya"]
        last_names = ["Sharma", "Nair", "Patel", "Rao", "Gupta", "Sen", "Mehta", "Verma", "Malhotra", "Singh", "Joshi", "Bose", "Kulkarni", "Reddy", "Pillai", "Choudhury"]
        author = f"{random.choice(first_names)} {random.choice(last_names)}"
        if platform in ["reddit", "twitter"]:
            author = f"u/{author.lower().replace(' ', '_')}" if platform == "reddit" else f"@{author.lower().replace(' ', '_')}"
            
        # Compile categories
        detected_categories = [grocery_cat] + segment_info["cats"]
        detected_categories = list(set(detected_categories))
        
        review_id = f"mock_{platform[:3]}_{uuid.uuid4().hex[:12]}"
        days_ago = random.randint(1, 150)
        created_at = (datetime.now() - timedelta(days=days_ago)).isoformat()
        
        return {
            "id": review_id,
            "platform": platform,
            "author": author,
            "raw_content": raw_content,
            "rating": rating,
            "created_at": created_at,
            "url": f"https://www.mockplatform.com/swiggy/{review_id}",
            "language": "en",
            "primary_purchased_category": grocery_cat,
            "willing_to_try_new": willing,
            "new_categories_of_interest": segment_info["cats"],
            "barrier_reason": barrier,
            "is_spam": 0
        }

    def generate(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate reviews using the default platform distribution."""
        # Proportions: Reddit 20%, Play Store 30%, App Store 15%, YouTube 15%, Twitter 10%, Quora 10%
        target_counts = {
            "play_store": int(0.30 * count),
            "reddit": int(0.20 * count),
            "app_store": int(0.15 * count),
            "youtube": int(0.15 * count),
            "twitter": int(0.10 * count),
            "quora": int(0.10 * count)
        }
        
        # Adjust for rounding to ensure sum is exactly count
        diff = count - sum(target_counts.values())
        if diff != 0:
            target_counts["play_store"] += diff
            
        return self.generate_for_platforms(target_counts)

    def generate_for_platforms(self, platform_counts: Dict[str, int]) -> List[Dict[str, Any]]:
        """Generate reviews with specific platform counts."""
        results = []
        for platform, count in platform_counts.items():
            for _ in range(count):
                results.append(self.generate_single_review(platform))
        return results
