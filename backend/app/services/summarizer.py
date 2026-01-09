import os
from typing import Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class NewsSummarizer:
    """Summarize news articles using OpenAI"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            print("Warning: OPENAI_API_KEY not set. Summarization will use simple extraction.")
    
    def summarize(self, title: str, content: str) -> str:
        """Generate summary of article"""
        # If content already has a good summary (from RSS), use it
        if content and len(content) > 50 and len(content) < 500:
            return content[:300]  # Limit length
        
        # Use simple summary for speed (skip AI if not critical)
        simple = self._simple_summary(content)
        if len(simple) > 50:
            return simple
        
        # Only use AI if simple summary is too short
        if self.client:
            try:
                # Use shorter content for faster processing
                content_preview = (content[:500] if content else title)
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a news summarizer. Create concise summaries."},
                        {"role": "user", "content": f"Title: {title}\n\nContent: {content_preview}\n\nSummary:"}
                    ],
                    max_tokens=80,  # Very short for speed
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error in OpenAI summarization: {e}")
                return simple
        else:
            return simple
    
    def _simple_summary(self, content: str) -> str:
        """Fallback simple summary extraction"""
        sentences = content.split('.')
        if len(sentences) > 3:
            return '. '.join(sentences[:2]) + '.'
        return content[:200] + "..."

