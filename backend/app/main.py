from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news, highlights, chat
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI News Aggregation API",
    description="AI-powered news aggregation and chatbot system",
    version="1.0.0"
)

# CORS middleware
import os
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(highlights.router, prefix="/api/highlights", tags=["highlights"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "AI News Aggregation API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

