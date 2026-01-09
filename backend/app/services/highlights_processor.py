from typing import List, Dict
from collections import defaultdict
import re

class HighlightsProcessor:
    """Process articles into highlights based on frequency and keywords"""
    
    BREAKING_KEYWORDS = [
        "breaking", "urgent", "alert", "just in", "developing", 
        "live", "exclusive", "major", "significant", "critical"
    ]
    
    IMPORTANT_KEYWORDS = [
        "announcement", "decision", "reveals", "unveils", "launches",
        "wins", "victory", "defeats", "championship", "record", "historic"
    ]
    
    def calculate_priority_score(self, article: Dict, frequency: int) -> float:
        """Calculate priority score based on keywords and frequency"""
        text = (article.get("title", "") + " " + article.get("summary", "")).lower()
        
        score = 0.0
        
        # Frequency contributes to score
        score += frequency * 10
        
        # Breaking news keywords
        breaking_count = sum(1 for keyword in self.BREAKING_KEYWORDS if keyword in text)
        score += breaking_count * 50
        
        # Important keywords
        important_count = sum(1 for keyword in self.IMPORTANT_KEYWORDS if keyword in text)
        score += important_count * 20
        
        return score
    
    def is_breaking_news(self, article: Dict) -> bool:
        """Check if article is breaking news"""
        text = (article.get("title", "") + " " + article.get("summary", "")).lower()
        return any(keyword in text for keyword in self.BREAKING_KEYWORDS)
    
    def create_highlights(self, articles: List[Dict]) -> List[Dict]:
        """Create highlights from articles grouped by cluster"""
        # Group articles by cluster_id
        clusters = defaultdict(list)
        unclustered = []
        
        for article in articles:
            cluster_id = article.get("cluster_id")
            if cluster_id is not None:
                clusters[cluster_id].append(article)
            else:
                unclustered.append(article)
        
        highlights = []
        
        # Process clustered articles
        for cluster_id, cluster_articles in clusters.items():
            if not cluster_articles:
                continue
            
            # Use the first (primary) article as base
            primary_article = cluster_articles[0]
            
            # Collect all sources and authors
            sources = list(set([art.get("source", "Unknown") for art in cluster_articles]))
            authors = list(set([art.get("author", "Unknown") for art in cluster_articles if art.get("author")]))
            
            # Calculate frequency (number of sources)
            frequency = len(sources)
            
            # Calculate priority score
            priority_score = self.calculate_priority_score(primary_article, frequency)
            
            # Check if breaking news
            is_breaking = self.is_breaking_news(primary_article)
            
            highlight = {
                "article_id": primary_article.get("id"),
                "title": primary_article.get("title"),
                "summary": primary_article.get("summary", ""),
                "category": primary_article.get("category"),
                "frequency": frequency,
                "priority_score": priority_score,
                "sources": sources,
                "authors": authors,
                "is_breaking": is_breaking
            }
            
            highlights.append(highlight)
        
        # Process unclustered articles (single articles)
        for article in unclustered:
            sources = [article.get("source", "Unknown")]
            authors = [article.get("author", "Unknown")] if article.get("author") else []
            frequency = 1
            
            priority_score = self.calculate_priority_score(article, frequency)
            is_breaking = self.is_breaking_news(article)
            
            highlight = {
                "article_id": article.get("id"),
                "title": article.get("title"),
                "summary": article.get("summary", ""),
                "category": article.get("category"),
                "frequency": frequency,
                "priority_score": priority_score,
                "sources": sources,
                "authors": authors,
                "is_breaking": is_breaking
            }
            
            highlights.append(highlight)
        
        # Sort by priority score (descending)
        highlights.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return highlights

