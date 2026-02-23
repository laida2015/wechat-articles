"""RSS service for fetching articles from wewe-rss."""
import httpx
import feedparser
from typing import List, Dict, Optional
from datetime import datetime
from bs4 import BeautifulSoup
import html2text
from ..config import settings


class RSSService:
    """Service for interacting with wewe-rss."""
    
    def __init__(self):
        self.base_url = settings.WEWE_RSS_URL
        self.auth_code = settings.WEWE_RSS_AUTH_CODE
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
    
    async def get_feeds(self) -> List[Dict]:
        """Get all RSS feeds from wewe-rss."""
        async with httpx.AsyncClient() as client:
            headers = {}
            if self.auth_code:
                headers["Authorization"] = f"Bearer {self.auth_code}"
            
            response = await client.get(
                f"{self.base_url}/api/feeds",
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_feed_articles(self, feed_id: str, limit: int = 20) -> List[Dict]:
        """Get articles from a specific feed."""
        feed_url = f"{self.base_url}/feeds/{feed_id}.json"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(feed_url, timeout=30.0)
            response.raise_for_status()
            feed_data = response.json()
        
        articles = []
        for item in feed_data.get("items", [])[:limit]:
            article = {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content_html": item.get("content_html", ""),
                "content_text": item.get("content_text", ""),
                "published_at": self._parse_date(item.get("date_published")),
                "author": item.get("author", {}).get("name", ""),
            }
            articles.append(article)
        
        return articles
    
    async def fetch_article_content(self, url: str) -> Dict[str, str]:
        """Fetch full article content from URL."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0, follow_redirects=True)
            response.raise_for_status()
            html_content = response.text
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text_content = self.html_converter.handle(str(soup))
        
        return {
            "html": html_content,
            "text": text_content.strip()
        }
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None
        
        try:
            # Try ISO format first
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    async def sync_feed(self, feed_id: str, account_id: int) -> List[Dict]:
        """Sync articles from a feed."""
        articles = await self.get_feed_articles(feed_id, settings.ARTICLES_PER_SYNC)
        
        # Add account_id to each article
        for article in articles:
            article["account_id"] = account_id
        
        return articles
