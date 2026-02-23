"""Knowledge base schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List, Any
from datetime import datetime


class KnowledgeBase(BaseModel):
    """Base knowledge schema."""
    type: str  # paper, tool, news
    title: str
    content: Dict[str, Any]
    source_articles: Optional[List[int]] = None


class KnowledgeCreate(KnowledgeBase):
    """Schema for creating knowledge."""
    pass


class KnowledgeUpdate(BaseModel):
    """Schema for updating knowledge."""
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    source_articles: Optional[List[int]] = None


class Knowledge(KnowledgeBase):
    """Schema for knowledge response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class KnowledgeList(BaseModel):
    """Schema for knowledge list response."""
    total: int
    items: list[Knowledge]
