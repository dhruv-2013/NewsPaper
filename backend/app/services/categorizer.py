from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import json

class NewsCategorizer:
    """Categorize and detect duplicate news articles"""
    
    def __init__(self):
        # Load pre-trained model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
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
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        return self.model.encode(text)
    
    def detect_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Detect duplicate or similar articles using clustering"""
        if len(articles) < 2:
            return articles
        
        # Generate embeddings for all articles
        texts = [f"{art['title']} {art['summary']}" for art in articles]
        embeddings = self.model.encode(texts)
        
        # Use DBSCAN clustering to find similar articles
        # eps controls the distance threshold for clustering
        clustering = DBSCAN(eps=0.3, min_samples=1, metric='cosine')
        cluster_labels = clustering.fit_predict(embeddings)
        
        # Group articles by cluster
        clusters = {}
        for idx, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(idx)
        
        # Mark duplicates and assign cluster IDs
        processed_articles = []
        cluster_id_counter = 0
        
        for cluster_id, article_indices in clusters.items():
            if len(article_indices) > 1:
                # Multiple articles in cluster - mark as potential duplicates
                # Keep the first one as primary, mark others as duplicates
                primary_idx = article_indices[0]
                articles[primary_idx]['cluster_id'] = cluster_id_counter
                articles[primary_idx]['is_duplicate'] = False
                processed_articles.append(articles[primary_idx])
                
                for idx in article_indices[1:]:
                    articles[idx]['cluster_id'] = cluster_id_counter
                    articles[idx]['is_duplicate'] = True
                    processed_articles.append(articles[idx])
                
                cluster_id_counter += 1
            else:
                # Single article in cluster
                idx = article_indices[0]
                articles[idx]['cluster_id'] = cluster_id_counter
                articles[idx]['is_duplicate'] = False
                processed_articles.append(articles[idx])
                cluster_id_counter += 1
        
        return processed_articles
    
    def embedding_to_json(self, embedding: np.ndarray) -> str:
        """Convert numpy array to JSON string"""
        return json.dumps(embedding.tolist())
    
    def json_to_embedding(self, json_str: str) -> np.ndarray:
        """Convert JSON string to numpy array"""
        return np.array(json.loads(json_str))

