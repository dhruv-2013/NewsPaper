from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ArticleBase(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    source: str
    source_url: str
    category: str
    published_date: Optional[datetime] = None

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    summary: Optional[str] = None
    extracted_date: datetime
    is_duplicate: bool
    cluster_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class HighlightBase(BaseModel):
    title: str
    summary: str
    category: str
    frequency: int
    priority_score: float
    sources: List[str]
    authors: List[str]
    is_breaking: bool

class Highlight(HighlightBase):
    id: int
    article_id: int
    created_date: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    question: str
    category: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    related_articles: List[int]

class ExtractionRequest(BaseModel):
    categories: List[str] = ["sports", "lifestyle", "music", "finance"]
    force_refresh: bool = False

class ExtractionResponse(BaseModel):
    message: str
    articles_extracted: int
    duplicates_found: int
    highlights_created: int

