from typing import List, Dict
import json

# Lazy import to avoid loading heavy models unless needed
_sentence_transformer = None
_numpy = None

def get_sentence_transformer():
    """Lazy load sentence transformer only when needed (for chat/RAG)"""
    global _sentence_transformer
    if _sentence_transformer is None:
        from sentence_transformers import SentenceTransformer
        _sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
    return _sentence_transformer

class NewsCategorizer:
    """Categorize and detect duplicate news articles - Memory optimized"""
    
    def __init__(self):
        # Don't load model here - only load when needed (saves memory)
        self.category_keywords = {
            "sports": ["sport", "game", "match", "player", "team", "championship", "league", "football", "cricket", "rugby", "tennis", "olympics"],
            "lifestyle": ["lifestyle", "health", "wellness", "food", "travel", "fashion", "beauty", "home", "garden", "recipe", "diet"],
            "music": ["music", "song", "album", "artist", "concert", "festival", "band", "singer", "musician", "chart", "billboard"],
            "finance": ["finance", "business", "economy", "stock", "market", "investment", "bank", "money", "financial", "trading", "dollar", "currency"]
        }
    
    def categorize_article(self, title: str, content: str) -> str:
        """Categorize article based on title and content"""
        text = (title + " " + content).lower()
        
        scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[category] = score
        
        # Return category with highest score, default to first category if tie
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return "lifestyle"  # Default category
    
    def generate_embedding(self, text: str):
        """Generate embedding for text - lazy load model only when needed"""
        global _numpy
        if _numpy is None:
            import numpy as np
            _numpy = np
        
        model = get_sentence_transformer()
        return model.encode(text)
    
    def detect_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Detect duplicate articles using simple URL-based matching (memory-efficient)"""
        if len(articles) < 2:
            for article in articles:
                article.setdefault('cluster_id', hash(article.get('title', '')) % 1000)
                article.setdefault('is_duplicate', False)
            return articles
        
        # Simple duplicate detection: group by similar titles (first 50 chars)
        seen_titles = {}
        processed_articles = []
        cluster_id_counter = 0
        
        for article in articles:
            title_key = article.get('title', '')[:50].lower().strip()
            
            if title_key in seen_titles:
                # Potential duplicate - same title start
                existing_cluster_id = seen_titles[title_key]
                article['cluster_id'] = existing_cluster_id
                article['is_duplicate'] = True
            else:
                # New article
                seen_titles[title_key] = cluster_id_counter
                article['cluster_id'] = cluster_id_counter
                article['is_duplicate'] = False
                cluster_id_counter += 1
            
            processed_articles.append(article)
        
        return processed_articles
    
    def embedding_to_json(self, embedding) -> str:
        """Convert numpy array to JSON string"""
        if hasattr(embedding, 'tolist'):
            return json.dumps(embedding.tolist())
        return json.dumps(list(embedding))
    
    def json_to_embedding(self, json_str: str):
        """Convert JSON string to numpy array"""
        global _numpy
        if _numpy is None:
            import numpy as np
            _numpy = np
        return _numpy.array(json.loads(json_str))

