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
        
        # Get recent articles/highlights for context
        query = db.query(models.Article).join(models.Highlight)
        
        if request.category:
            query = query.filter(models.Article.category == request.category)
        
        articles = query.order_by(
            models.Article.extracted_date.desc()
        ).limit(100).all()
        
        # Convert to dict format
        articles_data = [
            {
                "id": art.id,
                "title": art.title,
                "summary": art.summary or "",
                "source": art.source,
                "author": art.author,
                "category": art.category
            }
            for art in articles
        ]
        
        # Find relevant articles
        relevant_articles = rag_service.find_relevant_articles(
            request.question,
            articles_data,
            top_k=5
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

