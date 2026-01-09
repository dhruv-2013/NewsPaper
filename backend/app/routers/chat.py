from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services.rag_service import RAGService

router = APIRouter()

@router.post("/ask", response_model=schemas.ChatResponse)
async def ask_question(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db)
):
    """Ask a question about news highlights using RAG - Fast mode"""
    try:
        rag_service = RAGService()
        import asyncio
        
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
        # Use simple keyword matching instead of embeddings for speed
        question_lower = request.question.lower()
        relevant_articles = articles_data[:3]  # Just take first 3 for speed
        
        # Simple keyword filtering
        if articles_data:
            keyword_matches = [
                art for art in articles_data
                if any(keyword in art.get("title", "").lower() or keyword in art.get("summary", "").lower() 
                      for keyword in question_lower.split() if len(keyword) > 3)
            ]
            if keyword_matches:
                relevant_articles = keyword_matches[:3]
        
        # Generate response with timeout (run in thread to prevent blocking)
        try:
            # Wrap the synchronous call in a thread with timeout
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,  # Use default executor
                    lambda: rag_service.generate_response(
                        request.question,
                        relevant_articles,
                        request.category
                    )
                ),
                timeout=20.0  # 20 second timeout for GPT response
            )
        except asyncio.TimeoutError:
            # Fallback response if GPT times out
            response = {
                "answer": f"Based on the recent news, here are some relevant articles: {', '.join([art.get('title', '')[:50] for art in relevant_articles[:2]])}",
                "sources": list(set([art.get("source", "Unknown") for art in relevant_articles])),
                "related_articles": [art.get("id") for art in relevant_articles if art.get("id")]
            }
        except Exception as e:
            # Fallback if GPT fails for any reason
            print(f"Error generating GPT response: {e}")
            response = {
                "answer": f"Here are some relevant articles: {', '.join([art.get('title', '')[:50] for art in relevant_articles[:2]])}",
                "sources": list(set([art.get("source", "Unknown") for art in relevant_articles])),
                "related_articles": [art.get("id") for art in relevant_articles if art.get("id")]
            }
        
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

