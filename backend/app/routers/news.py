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
    """Extract news articles from Australian news outlets"""
    try:
        extractor = NewsExtractor()
        categorizer = NewsCategorizer()
        highlights_processor = HighlightsProcessor()
        
        # Use requested categories, but prioritize sports and music (most reliable)
        if request.categories:
            categories_to_extract = request.categories
        else:
            # Default to sports and music for faster, more reliable extraction
            categories_to_extract = ["sports", "music"]
        
        # Extract with shorter timeout (30 seconds) for faster response
        async with extractor:
            try:
                articles_data = await asyncio.wait_for(
                    extractor.extract_all_articles(categories_to_extract),
                    timeout=30.0  # 30 second timeout
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
        
        # Limit to reasonable number to avoid timeouts (max 10 articles)
        articles_data = articles_data[:10]
        
        # Detect duplicates using categorizer
        articles_data = categorizer.detect_duplicates(articles_data)
        
        # Process articles - use RSS summaries, skip AI for speed
        articles_created = 0
        duplicates_count = 0
        processed_articles = []
        
        for article_data in articles_data:
            # Check if article already exists
            existing = db.query(models.Article).filter(
                models.Article.source_url == article_data.get("source_url", "")
            ).first()
            
            if existing and not request.force_refresh:
                processed_articles.append(existing)
                continue
            
            # Use RSS summary if available, otherwise use title
            summary = article_data.get("summary", "")
            if not summary or len(summary) < 30:
                summary = article_data.get("title", "") + " - " + article_data.get("source", "Unknown")
            
            # Generate simple embedding for categorization
            text_for_embedding = f"{article_data.get('title', '')} {summary}"
            embedding = categorizer.generate_embedding(text_for_embedding)
            embedding_json = categorizer.embedding_to_json(embedding)
            
            # Create or update article
            if existing:
                for key, value in article_data.items():
                    if key != "summary":
                        setattr(existing, key, value)
                existing.summary = summary[:1000]
                existing.embedding = embedding_json
                existing.is_duplicate = article_data.get("is_duplicate", False)
                existing.cluster_id = article_data.get("cluster_id")
                existing.extracted_date = datetime.now()
                article = existing
                processed_articles.append(article)
            else:
                article_dict = {k: v for k, v in article_data.items() if k != "summary"}
                article = models.Article(
                    **article_dict,
                    summary=summary[:1000],
                    embedding=embedding_json,
                    extracted_date=datetime.now()
                )
                db.add(article)
                articles_created += 1
                processed_articles.append(article)
            
            if article_data.get("is_duplicate", False):
                duplicates_count += 1
        
        # Single commit for all articles
        db.commit()
        
        # Commit articles
        db.commit()
        
        # Refresh articles to get IDs
        for article in processed_articles:
            db.refresh(article)
        
        # Create highlights from processed articles
        articles_for_highlights = [
            {
                "id": art.id,
                "title": art.title,
                "summary": art.summary or "",
                "category": art.category,
                "source": art.source,
                "author": art.author or "Unknown",
                "cluster_id": art.cluster_id
            }
            for art in processed_articles if art.id
        ]
        
        highlights_data = highlights_processor.create_highlights(articles_for_highlights)
        
        # Clear old highlights and create new ones
        db.query(models.Highlight).delete()
        
        highlights_created = 0
        for highlight_data in highlights_data:
            highlight = models.Highlight(
                article_id=highlight_data["article_id"],
                title=highlight_data["title"],
                summary=highlight_data["summary"],
                category=highlight_data["category"],
                frequency=highlight_data["frequency"],
                priority_score=highlight_data["priority_score"],
                sources=",".join(highlight_data["sources"]),
                authors=",".join(highlight_data["authors"]),
                is_breaking=highlight_data["is_breaking"]
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

