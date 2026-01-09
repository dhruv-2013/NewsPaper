from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    summary = Column(Text)
    author = Column(String)
    source = Column(String, index=True)
    source_url = Column(String, unique=True)
    category = Column(String, index=True)  # sports, lifestyle, music, finance
    published_date = Column(DateTime)
    extracted_date = Column(DateTime, server_default=func.now())
    is_duplicate = Column(Boolean, default=False)
    cluster_id = Column(Integer, nullable=True)  # For grouping similar articles
    embedding = Column(Text, nullable=True)  # JSON string of embedding vector
    
    # Relationships
    highlights = relationship("Highlight", back_populates="article")

class Highlight(Base):
    __tablename__ = "highlights"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    title = Column(String, index=True)
    summary = Column(Text)
    category = Column(String, index=True)
    frequency = Column(Integer, default=1)  # Number of sources reporting this
    priority_score = Column(Float, default=0.0)  # Based on keywords and frequency
    sources = Column(Text)  # JSON string of source names
    authors = Column(Text)  # JSON string of author names
    created_date = Column(DateTime, server_default=func.now())
    is_breaking = Column(Boolean, default=False)
    
    # Relationships
    article = relationship("Article", back_populates="highlights")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    context_articles = Column(Text)  # JSON string of article IDs used
    created_at = Column(DateTime, server_default=func.now())

