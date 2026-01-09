from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services.rag_service import RAGService

router = APIRouter()

@router.post("/ask", response_model=schemas.ChatResponse)
def ask_question(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db)
):
    """Ask a question about news highlights using RAG"""
    try:
        rag_service = RAGService()
        
        # Get recent articles for context - don't require highlights
        query = db.query(models.Article)
        
        # Filter by category if question mentions a specific category
        question_lower = request.question.lower()
        if 'sport' in question_lower or 'sports' in question_lower:
            query = query.filter(models.Article.category == 'sports')
        elif 'finance' in question_lower or 'business' in question_lower or 'economic' in question_lower:
            query = query.filter(models.Article.category == 'finance')
        elif 'music' in question_lower:
            query = query.filter(models.Article.category == 'music')
        elif 'lifestyle' in question_lower:
            query = query.filter(models.Article.category == 'lifestyle')
        elif request.category:
            query = query.filter(models.Article.category == request.category)
        
        articles = query.order_by(
            models.Article.extracted_date.desc()
        ).limit(20).all()  # Reduced from 100 to 20 for faster processing
        
        # Convert to dict format - include content if summary is missing
        articles_data = []
        for art in articles:
            article_dict = {
                "id": art.id,
                "title": art.title,
                "summary": art.summary or art.content[:200] if art.content else "",
                "source": art.source,
                "author": art.author or "Unknown",
                "category": art.category
            }
            articles_data.append(article_dict)
        
        # Find relevant articles (limit to top 3 for speed)
        relevant_articles = rag_service.find_relevant_articles(
            request.question,
            articles_data,
            top_k=3  # Reduced from 5 to 3 for faster response
        )
        
        # Generate response
        response = rag_service.generate_response(
            request.question,
            relevant_articles,
            request.category
        )
        
        # Save chat history
        chat_history = models.ChatHistory(
            question=request.question,
            answer=response["answer"],
            context_articles=str(response["related_articles"])
        )
        db.add(chat_history)
        db.commit()
        
        return schemas.ChatResponse(
            answer=response["answer"],
            sources=response["sources"],
            related_articles=response["related_articles"]
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_chat_history(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get chat history"""
    history = db.query(models.ChatHistory).order_by(
        models.ChatHistory.created_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": h.id,
            "question": h.question,
            "answer": h.answer,
            "created_at": h.created_at
        }
        for h in history
    ]

