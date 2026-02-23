"""Article analysis schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List, Any
from datetime import datetime


class ArticleAnalysisBase(BaseModel):
    """Base article analysis schema."""
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    entities: Optional[Dict[str, Any]] = None
    category_confidence: Optional[float] = None
    paper_info: Optional[Dict[str, Any]] = None
    tool_info: Optional[Dict[str, Any]] = None
    news_info: Optional[Dict[str, Any]] = None


class ArticleAnalysisCreate(ArticleAnalysisBase):
    """Schema for creating article analysis."""
    article_id: int


class ArticleAnalysis(ArticleAnalysisBase):
    """Schema for article analysis response."""
    id: int
    article_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
