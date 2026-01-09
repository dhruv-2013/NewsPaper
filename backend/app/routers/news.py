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
        summarizer = NewsSummarizer()
        highlights_processor = HighlightsProcessor()
        
        # Extract articles (limit to 2 categories max for faster processing)
        categories_to_extract = request.categories[:2] if len(request.categories) > 2 else request.categories
        async with extractor:
            articles_data = await extractor.extract_all_articles(categories_to_extract)
        
        if not articles_data:
            return schemas.ExtractionResponse(
                message="No articles extracted",
                articles_extracted=0,
                duplicates_found=0,
                highlights_created=0
            )
        
        # Categorize and detect duplicates
        articles_data = categorizer.detect_duplicates(articles_data)
        
        # Process each article (limit to first 20 for faster processing)
        articles_to_process = articles_data[:20]
        articles_created = 0
        duplicates_count = 0
        processed_articles = []
        
        for article_data in articles_to_process:
            # Check if article already exists
            existing = db.query(models.Article).filter(
                models.Article.source_url == article_data["source_url"]
            ).first()
            
            if existing and not request.force_refresh:
                processed_articles.append(existing)
                continue
            
            # Use RSS summary if available, otherwise generate (faster)
            if article_data.get("summary") and len(article_data["summary"]) > 50:
                summary = article_data["summary"]
            else:
                # Only generate AI summary if RSS summary is poor
                summary = summarizer.summarize(
                    article_data["title"],
                    article_data.get("content", article_data.get("summary", ""))
                )
            
            # Generate embedding (only for new articles)
            text_for_embedding = f"{article_data['title']} {summary}"
            embedding = categorizer.generate_embedding(text_for_embedding)
            embedding_json = categorizer.embedding_to_json(embedding)
            
            # Create or update article
            if existing:
                for key, value in article_data.items():
                    if key != "summary":  # Don't overwrite summary from article_data
                        setattr(existing, key, value)
                existing.summary = summary
                existing.embedding = embedding_json
                existing.is_duplicate = article_data.get("is_duplicate", False)
                existing.cluster_id = article_data.get("cluster_id")
                article = existing
                processed_articles.append(article)
            else:
                # Remove summary from article_data if it exists to avoid duplicate
                article_dict = {k: v for k, v in article_data.items() if k != "summary"}
                article = models.Article(
                    **article_dict,
                    summary=summary,
                    embedding=embedding_json
                )
                db.add(article)
                articles_created += 1
                processed_articles.append(article)
            
            if article_data.get("is_duplicate", False):
                duplicates_count += 1
        
        db.commit()
        
        # Refresh all articles to get IDs
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

