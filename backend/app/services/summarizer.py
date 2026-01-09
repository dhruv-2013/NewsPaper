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
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a news summarizer. Create concise, informative summaries of news articles."},
                        {"role": "user", "content": f"Title: {title}\n\nContent: {content[:2000]}\n\nProvide a 2-3 sentence summary:"}
                    ],
                    max_tokens=150,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error in OpenAI summarization: {e}")
                return self._simple_summary(content)
        else:
            return self._simple_summary(content)
    
    def _simple_summary(self, content: str) -> str:
        """Fallback simple summary extraction"""
        sentences = content.split('.')
        if len(sentences) > 3:
            return '. '.join(sentences[:2]) + '.'
        return content[:200] + "..."

