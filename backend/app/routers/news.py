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
    """Extract news articles - MINIMAL mode: Fastest possible extraction"""
    try:
        extractor = NewsExtractor()
        
        # MINIMAL: Only 1 category, 1 source, 1 article
        categories_to_extract = ["sports"]  # Most reliable
        
        # Extract with very short timeout (15 seconds max)
        async with extractor:
            try:
                articles_data = await asyncio.wait_for(
                    extractor.extract_all_articles(categories_to_extract),
                    timeout=15.0  # 15 second timeout - must be fast
                )
            except asyncio.TimeoutError:
                return schemas.ExtractionResponse(
                    message="Extraction timed out - Backend may be slow. Try again in 30 seconds.",
                    articles_extracted=0,
                    duplicates_found=0,
                    highlights_created=0
                )
            except Exception as e:
                print(f"Extraction error: {e}")
                return schemas.ExtractionResponse(
                    message=f"Extraction error: {str(e)[:100]}",
                    articles_extracted=0,
                    duplicates_found=0,
                    highlights_created=0
                )
        
        if not articles_data:
            return schemas.ExtractionResponse(
                message="No articles extracted - RSS feeds may be unavailable",
                articles_extracted=0,
                duplicates_found=0,
                highlights_created=0
            )
        
        # MINIMAL: Only process first 3 articles maximum
        articles_data = articles_data[:3]
        
        # Quick duplicate check (URL only)
        seen_urls = set()
        unique_articles = []
        for article in articles_data:
            url = article.get("source_url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        articles_data = unique_articles
        
        # Minimal processing - no clustering, no AI
        articles_created = 0
        processed_article_ids = []
        
        # Single transaction - process all articles at once
        for article_data in articles_data:
            # Check existence
            existing = db.query(models.Article).filter(
                models.Article.source_url == article_data.get("source_url", "")
            ).first()
            
            if existing and not request.force_refresh:
                processed_article_ids.append(existing.id)
                continue
            
            # Minimal summary (RSS only, no AI)
            summary = article_data.get("summary", "") or article_data.get("title", "")
            if len(summary) < 20:
                summary = article_data.get("title", "") + " - " + article_data.get("source", "")
            
            # Create article (minimal fields)
            if existing:
                existing.title = article_data.get("title", "")
                existing.summary = summary[:500]  # Limit length
                existing.category = article_data.get("category", "sports")
                existing.extracted_date = datetime.now()
                article = existing
            else:
                article = models.Article(
                    title=article_data.get("title", ""),
                    content=article_data.get("content", summary)[:1000],  # Limit content
                    summary=summary[:500],
                    author=article_data.get("author", "Unknown"),
                    source=article_data.get("source", "Unknown"),
                    source_url=article_data.get("source_url", ""),
                    category=article_data.get("category", "sports"),
                    published_date=article_data.get("published_date", datetime.now()),
                    extracted_date=datetime.now(),
                    embedding="[]",
                    is_duplicate=False,
                    cluster_id=None
                )
                db.add(article)
                articles_created += 1
        
        # Single commit for all articles
        db.commit()
        
        # Refresh to get IDs
        if articles_created > 0:
            db.query(models.Article).filter(
                models.Article.extracted_date >= datetime.now().replace(second=0, microsecond=0)
            ).all()
        
        # MINIMAL highlights - only if we have articles and time permits
        highlights_created = 0
        if articles_created > 0:
            try:
                # Get recently created articles
                recent_articles = db.query(models.Article).filter(
                    models.Article.extracted_date >= datetime.now().replace(second=0, microsecond=0)
                ).limit(5).all()
                
                if recent_articles:
                    # Delete old highlights only if we have new ones
                    db.query(models.Highlight).delete()
                    
                    for art in recent_articles[:3]:  # Max 3 highlights for speed
                        highlight = models.Highlight(
                            article_id=art.id,
                            title=art.title,
                            summary=art.summary or art.title,
                            category=art.category or "sports",
                            frequency=1,
                            priority_score=10.0,
                            sources=art.source or "Unknown",
                            authors=art.author or "Unknown",
                            is_breaking=False
                        )
                        db.add(highlight)
                        highlights_created += 1
                    
                    db.commit()
            except Exception as e:
                print(f"Error creating highlights: {e}")
                db.rollback()
                # Continue without highlights - better than failing
        
        return schemas.ExtractionResponse(
            message=f"Extraction completed - {articles_created} articles processed",
            articles_extracted=articles_created,
            duplicates_found=len(articles_data) - articles_created,
            highlights_created=highlights_created
        )
    
    except Exception as e:
        db.rollback()
        error_msg = str(e)[:200]  # Limit error message length
        print(f"Extraction exception: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {error_msg}")

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

