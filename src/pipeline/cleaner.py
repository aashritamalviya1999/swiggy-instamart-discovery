import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Hinglish normalizer maps common Hindi/Hinglish quick commerce slang to English
HINGLISH_MAP = {
    "accha": "good",
    "achha": "good",
    "bekaar": "useless",
    "kharab": "bad",
    "ghatiya": "very bad",
    "jaldi": "fast",
    "turant": "instantly",
    "late": "delayed",
    "mehanga": "expensive",
    "sasta": "cheap",
    "nahi": "not",
    "mil raha": "getting",
    "bahut": "very",
    "kaam": "less",
    "paisa": "money",
    "loot": "scam",
    "chahiye": "need",
}

class FeedbackCleaner:
    """Cleans and normalizes Swiggy Instamart customer feedback."""
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove links from review content."""
        return re.sub(r'https?://\S+|www\.\S+', '', text)
        
    @staticmethod
    def remove_emojis(text: str) -> str:
        """Strip non-ASCII emojis and symbols."""
        cleaned = text.encode('ascii', 'ignore').decode('ascii')
        return re.sub(r'\s+', ' ', cleaned).strip()
        
    @staticmethod
    def clean_spelling_and_hinglish(text: str) -> str:
        """Translate common Hinglish shopping words to English."""
        words = text.split()
        normalized_words = []
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word).lower()
            if clean_word in HINGLISH_MAP:
                replaced = HINGLISH_MAP[clean_word]
                normalized_words.append(word.lower().replace(clean_word, replaced))
            else:
                normalized_words.append(word)
        return " ".join(normalized_words)
        
    @staticmethod
    def is_spam(text: str) -> bool:
        """
        Check if review content is spam/referral code/promotional noise.
        """
        t = text.strip().lower()
        if len(t) < 8 or len(t.split()) < 3:
            return True
            
        # Referral patterns
        if re.search(r'\b(use code|referral|promo|discount code|earn money|free cash|share and earn)\b', t):
            return True
            
        # Repetitive keyword spam
        words = t.split()
        if len(set(words)) / len(words) < 0.4 and len(words) > 5:
            return True
            
        return False
        
    def clean_review(self, review: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a single review dict in place."""
        cleaned_review = dict(review)
        raw_text = cleaned_review.get("raw_content", "")
        
        # Spam check
        if self.is_spam(raw_text):
            cleaned_review["is_spam"] = 1
            cleaned_review["cleaned_content"] = ""
            return cleaned_review
            
        # Clean text pipeline
        text = raw_text
        text = self.remove_urls(text)
        text = self.remove_emojis(text)
        text = self.clean_spelling_and_hinglish(text)
        
        # Formatting
        text = text.replace("\n", " ").replace("\r", " ")
        text = re.sub(r'\s+', ' ', text).strip()
        
        cleaned_review["cleaned_content"] = text
        cleaned_review["is_spam"] = 0
        cleaned_review["language"] = "en"
        
        return cleaned_review
        
    def clean_batch(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean a batch of reviews, flagging duplicates as spam to avoid duplicates skewing results."""
        cleaned_list = []
        seen_contents = set()
        
        for rev in reviews:
            cleaned = self.clean_review(rev)
            content_key = cleaned["cleaned_content"].lower().strip()
            
            if not cleaned["is_spam"] and content_key:
                if content_key in seen_contents:
                    # Flag duplicates as spam
                    cleaned["is_spam"] = 1
                else:
                    seen_contents.add(content_key)
            cleaned_list.append(cleaned)
            
        return cleaned_list
