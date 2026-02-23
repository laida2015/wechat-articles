"""Article schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class ArticleBase(BaseModel):
    """Base article schema."""
    title: str
    content: Optional[str] = None
    content_text: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None


class ArticleCreate(ArticleBase):
    """Schema for creating article."""
    account_id: int


class ArticleUpdate(BaseModel):
    """Schema for updating article."""
    title: Optional[str] = None
    content: Optional[str] = None
    content_text: Optional[str] = None
    is_favorite: Optional[bool] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None


class Article(ArticleBase):
    """Schema for article response."""
    id: int
    account_id: int
    is_favorite: bool
    fetched_at: datetime
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ArticleDetail(Article):
    """Schema for article detail with analysis."""
    analysis: Optional[Any] = None  # Will be ArticleAnalysis
    
    model_config = ConfigDict(from_attributes=True)


class ArticleList(BaseModel):
    """Schema for article list response."""
    total: int
    items: list[Article]
