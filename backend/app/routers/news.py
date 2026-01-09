from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services.news_extractor import NewsExtractor
from app.services.categorizer import NewsCategorizer
from app.services.summarizer import NewsSummarizer
from app.services.highlights_processor import HighlightsProcessor
from datetime import datetime
import asyncio

router = APIRouter()

@router.post("/extract", response_model=schemas.ExtractionResponse)
async def extract_news(
    request: schemas.ExtractionRequest,
    db: Session = Depends(get_db)
):
    """Extract news articles from Australian news outlets - Optimized for speed"""
    try:
        extractor = NewsExtractor()
        categorizer = NewsCategorizer()
        summarizer = NewsSummarizer()
        highlights_processor = HighlightsProcessor()
        
        # Limit to 1 category only for fastest processing
        # Process sports first (most reliable RSS feeds)
        categories_to_extract = ["sports"]  # Always start with sports for speed
        
        async with extractor:
            articles_data = await extractor.extract_all_articles(categories_to_extract)
        
        if not articles_data:
            return schemas.ExtractionResponse(
                message="No articles extracted",
                articles_extracted=0,
                duplicates_found=0,
                highlights_created=0
            )
        
        # Limit to 10 articles for speed
        articles_data = articles_data[:10]
        
        # Simplified duplicate detection (faster)
        seen_urls = set()
        unique_articles = []
        for article in articles_data:
            url = article.get("source_url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        articles_data = unique_articles
        
        # Quick categorization without full clustering
        for article in articles_data:
            category = categorizer.categorize_article(article["title"], article.get("content", ""))
            article["category"] = category
            article["cluster_id"] = hash(article["title"]) % 1000  # Simple hash-based clustering
            article["is_duplicate"] = False
        
        # Process articles quickly (skip AI summarization, use RSS summaries)
        articles_created = 0
        duplicates_count = 0
        processed_articles = []
        
        for article_data in articles_data:
            # Check if article already exists
            existing = db.query(models.Article).filter(
                models.Article.source_url == article_data["source_url"]
            ).first()
            
            if existing and not request.force_refresh:
                processed_articles.append(existing)
                continue
            
            # Use RSS summary directly (skip AI for speed)
            summary = article_data.get("summary", "")
            if not summary or len(summary) < 30:
                summary = article_data.get("title", "") + " - News article from " + article_data.get("source", "")
            
            # Simple embedding (skip for now to save time)
            embedding_json = "[]"
            
            # Create or update article
            if existing:
                for key, value in article_data.items():
                    if key != "summary":
                        setattr(existing, key, value)
                existing.summary = summary
                existing.embedding = embedding_json
                existing.is_duplicate = False
                existing.cluster_id = article_data.get("cluster_id")
                article = existing
                processed_articles.append(article)
            else:
                article_dict = {k: v for k, v in article_data.items() if k != "summary"}
                article = models.Article(
                    **article_dict,
                    summary=summary,
                    embedding=embedding_json
                )
                db.add(article)
                articles_created += 1
                processed_articles.append(article)
        
        db.commit()
        
        # Refresh articles
        for article in processed_articles:
            db.refresh(article)
        
        # Create simple highlights (no complex clustering)
        highlights_created = 0
        db.query(models.Highlight).delete()
        
        for art in processed_articles[:10]:  # Max 10 highlights
            highlight = models.Highlight(
                article_id=art.id,
                title=art.title,
                summary=art.summary or art.title,
                category=art.category,
                frequency=1,
                priority_score=10.0,
                sources=art.source,
                authors=art.author or "Unknown",
                is_breaking=False
            )
            db.add(highlight)
            highlights_created += 1
        
        db.commit()
        
        return schemas.ExtractionResponse(
            message="News extraction completed successfully",
            articles_extracted=articles_created,
            duplicates_found=duplicates_count,
            highlights_created=highlights_created
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/articles", response_model=list[schemas.Article])
def get_articles(
    category: str = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get articles, optionally filtered by category"""
    query = db.query(models.Article)
    
    if category:
        query = query.filter(models.Article.category == category)
    
    articles = query.order_by(models.Article.extracted_date.desc()).limit(limit).all()
    return articles

