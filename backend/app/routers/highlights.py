from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas.Highlight])
def get_highlights(
    category: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get news highlights, optionally filtered by category"""
    query = db.query(models.Highlight)
    
    if category:
        query = query.filter(models.Highlight.category == category)
    
    highlights = query.order_by(
        models.Highlight.is_breaking.desc(),
        models.Highlight.priority_score.desc()
    ).limit(limit).all()
    
    # Convert sources and authors from strings to lists
    result = []
    for highlight in highlights:
        highlight_dict = {
            "id": highlight.id,
            "article_id": highlight.article_id,
            "title": highlight.title,
            "summary": highlight.summary,
            "category": highlight.category,
            "frequency": highlight.frequency,
            "priority_score": highlight.priority_score,
            "sources": highlight.sources.split(",") if highlight.sources else [],
            "authors": highlight.authors.split(",") if highlight.authors else [],
            "is_breaking": highlight.is_breaking,
            "created_date": highlight.created_date
        }
        result.append(highlight_dict)
    
    return result

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get available categories with counts"""
    categories = db.query(models.Highlight.category).distinct().all()
    result = {}
    
    for (category,) in categories:
        count = db.query(models.Highlight).filter(
            models.Highlight.category == category
        ).count()
        result[category] = count
    
    return result

@router.get("/breaking")
def get_breaking_news(db: Session = Depends(get_db)):
    """Get breaking news highlights"""
    highlights = db.query(models.Highlight).filter(
        models.Highlight.is_breaking == True
    ).order_by(
        models.Highlight.priority_score.desc()
    ).all()
    
    result = []
    for highlight in highlights:
        highlight_dict = {
            "id": highlight.id,
            "article_id": highlight.article_id,
            "title": highlight.title,
            "summary": highlight.summary,
            "category": highlight.category,
            "frequency": highlight.frequency,
            "priority_score": highlight.priority_score,
            "sources": highlight.sources.split(",") if highlight.sources else [],
            "authors": highlight.authors.split(",") if highlight.authors else [],
            "is_breaking": highlight.is_breaking,
            "created_date": highlight.created_date
        }
        result.append(highlight_dict)
    
    return result

