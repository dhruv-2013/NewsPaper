import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import re
from typing import List, Dict
import aiohttp
import asyncio
from urllib.parse import urljoin, urlparse

class NewsExtractor:
    """Extract news from Australian news outlets"""
    
    # Australian news sources with RSS feeds and categories
    NEWS_SOURCES = {
        "sports": [
            {
                "name": "ABC Sport",
                "rss": "https://www.abc.net.au/news/feed/51120/rss.xml",
                "base_url": "https://www.abc.net.au"
            },
            {
                "name": "The Guardian Australia Sport",
                "rss": "https://www.theguardian.com/australia-news/sport/rss",
                "base_url": "https://www.theguardian.com"
            },
            {
                "name": "SBS Sport",
                "rss": "https://www.sbs.com.au/news/feed/sport",
                "base_url": "https://www.sbs.com.au"
            }
        ],
        "lifestyle": [
            {
                "name": "ABC Lifestyle",
                "rss": "https://www.abc.net.au/news/feed/51120/rss.xml",
                "base_url": "https://www.abc.net.au",
                "filter_keywords": ["lifestyle", "health", "wellness", "food", "travel"]
            },
            {
                "name": "The Guardian Australia Lifestyle",
                "rss": "https://www.theguardian.com/australia-news/lifeandstyle/rss",
                "base_url": "https://www.theguardian.com"
            }
        ],
        "music": [
            {
                "name": "ABC Music",
                "rss": "https://www.abc.net.au/triplej/feed/",
                "base_url": "https://www.abc.net.au"
            },
            {
                "name": "The Guardian Australia Music",
                "rss": "https://www.theguardian.com/music/rss",
                "base_url": "https://www.theguardian.com"
            }
        ],
        "finance": [
            {
                "name": "ABC Business",
                "rss": "https://www.abc.net.au/news/feed/51892/rss.xml",
                "base_url": "https://www.abc.net.au"
            },
            {
                "name": "The Guardian Australia Business",
                "rss": "https://www.theguardian.com/australia-news/business/rss",
                "base_url": "https://www.theguardian.com"
            },
            {
                "name": "AFR",
                "rss": "https://www.afr.com/rss",
                "base_url": "https://www.afr.com"
            }
        ]
    }
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def parse_date(self, date_str: str) -> datetime:
        """Parse various date formats"""
        try:
            from dateparser import parse
            parsed = parse(date_str)
            return parsed if parsed else datetime.now()
        except:
            return datetime.now()
    
    async def fetch_rss_feed(self, rss_url: str) -> List[Dict]:
        """Fetch and parse RSS feed - optimized for speed"""
        try:
            timeout = aiohttp.ClientTimeout(total=8)
            
            if self.session:
                async with self.session.get(rss_url, timeout=timeout) as response:
                    if response.status != 200:
                        print(f"RSS feed returned status {response.status}")
                        return []
                    content = await response.text()
            else:
                # Fallback for sync requests
                response = requests.get(rss_url, timeout=8)
                if response.status_code != 200:
                    print(f"RSS feed returned status {response.status_code}")
                    return []
                content = response.text
            
            # Parse feed
            feed = feedparser.parse(content)
            
            # Get only first 1 article from feed (for speed)
            articles = []
            if feed.entries:
                entry = feed.entries[0]  # Just first entry
                article = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", "") or entry.get("description", ""),
                    "author": entry.get("author", "") or entry.get("dc:creator", "") or "Unknown",
                }
                articles.append(article)
            
            return articles
        except asyncio.TimeoutError:
            print(f"RSS feed timeout: {rss_url}")
            return []
        except Exception as e:
            print(f"Error fetching RSS feed {rss_url}: {e}")
            return []
    
    async def extract_article_content(self, url: str, base_url: str) -> str:
        """Extract full article content from URL"""
        try:
            if self.session:
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    html = await response.text()
            else:
                response = requests.get(url, timeout=10)
                html = response.text
            
            soup = BeautifulSoup(html, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Try to find main content
            content_selectors = [
                'article',
                '.article-body',
                '.content',
                '.post-content',
                'main',
                '[role="main"]'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = ' '.join([elem.get_text() for elem in elements])
                    break
            
            # Fallback to body text
            if not content:
                content = soup.get_text()
            
            # Clean up text
            content = re.sub(r'\s+', ' ', content)
            content = content.strip()
            
            return content[:5000]  # Limit content length
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return ""
    
    async def extract_articles_by_category(self, category: str) -> List[Dict]:
        """Extract articles for a specific category - 1 article per source for speed"""
        sources = self.NEWS_SOURCES.get(category, [])
        all_articles = []
        
        # Process only first 2 sources per category for speed (faster than all sources)
        for source in sources[:2]:
            try:
                rss_articles = await asyncio.wait_for(
                    self.fetch_rss_feed(source["rss"]),
                    timeout=8.0  # 8 second timeout per RSS feed
                )
                
                # Get only 1 article per source (faster, avoids timeout)
                if rss_articles:
                    rss_article = rss_articles[0]  # Just first article
                    
                    # Use RSS data - no web scraping for speed
                    summary = rss_article.get("summary", "") or rss_article.get("title", "")
                    content = summary  # Use summary as content (faster than scraping)
                    
                    article = {
                        "title": rss_article.get("title", "Untitled"),
                        "content": content[:1000],  # Limit content length
                        "summary": summary[:300],  # Limit summary length
                        "author": rss_article.get("author", "Unknown"),
                        "source": source["name"],
                        "source_url": rss_article.get("link", ""),
                        "category": category,
                        "published_date": self.parse_date(rss_article.get("published", ""))
                    }
                    all_articles.append(article)
                
                # Small delay between sources
                await asyncio.sleep(0.2)
            except asyncio.TimeoutError:
                print(f"RSS feed timeout for {source['name']}")
                continue
            except Exception as e:
                print(f"Error processing source {source['name']}: {e}")
                continue
        
        return all_articles
    
    async def extract_all_articles(self, categories: List[str]) -> List[Dict]:
        """Extract articles from all specified categories"""
        all_articles = []
        
        for category in categories:
            articles = await self.extract_articles_by_category(category)
            all_articles.extend(articles)
        
        return all_articles

