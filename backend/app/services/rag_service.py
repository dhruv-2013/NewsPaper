import os
from typing import List, Dict, Optional
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    """Retrieval-Augmented Generation service for chatbot"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            print("Warning: OPENAI_API_KEY not set. RAG will use simple responses.")
        
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        return self.embedding_model.encode(text)
    
    def find_relevant_articles(self, query: str, articles: List[Dict], top_k: int = 5) -> List[Dict]:
        """Find most relevant articles for a query using semantic search"""
        if not articles:
            return []
        
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        # Calculate similarities
        similarities = []
        for article in articles:
            # Use title and summary for matching
            text = f"{article.get('title', '')} {article.get('summary', '')}"
            article_embedding = self.generate_embedding(text)
            
            similarity = cosine_similarity(
                query_embedding.reshape(1, -1),
                article_embedding.reshape(1, -1)
            )[0][0]
            
            similarities.append((similarity, article))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [article for _, article in similarities[:top_k]]
    
    def generate_response(self, question: str, context_articles: List[Dict], category: Optional[str] = None) -> Dict:
        """Generate chatbot response using RAG"""
        if not self.client:
            # Fallback response
            if context_articles:
                return {
                    "answer": f"Based on the news, {context_articles[0].get('summary', 'No information available.')}",
                    "sources": [art.get("source", "Unknown") for art in context_articles],
                    "related_articles": [art.get("id") for art in context_articles]
                }
            return {
                "answer": "I don't have enough information to answer that question. Please try asking about recent news highlights.",
                "sources": [],
                "related_articles": []
            }
        
        # Build context from articles
        context_text = ""
        for i, article in enumerate(context_articles[:3]):  # Use top 3 articles
            context_text += f"Article {i+1}:\n"
            context_text += f"Title: {article.get('title', '')}\n"
            context_text += f"Summary: {article.get('summary', '')}\n"
            context_text += f"Source: {article.get('source', '')}\n\n"
        
        try:
            # Generate response using OpenAI
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful news assistant. Answer questions based on the provided news articles. Be concise and informative. If the information isn't in the context, say so."
                },
                {
                    "role": "user",
                    "content": f"Context from recent news articles:\n\n{context_text}\n\nQuestion: {question}\n\nAnswer based on the context above:"
                }
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                "answer": answer,
                "sources": list(set([art.get("source", "Unknown") for art in context_articles])),
                "related_articles": [art.get("id") for art in context_articles]
            }
        except Exception as e:
            print(f"Error generating RAG response: {e}")
            return {
                "answer": "I encountered an error while processing your question. Please try again.",
                "sources": [],
                "related_articles": []
            }

