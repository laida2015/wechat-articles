"""Article analysis model."""
from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from ..database import Base


class ArticleAnalysis(Base):
    """文章分析结果模型."""
    
    __tablename__ = "article_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    summary = Column(Text)
    keywords = Column(JSONB)  # ["keyword1", "keyword2", ...]
    entities = Column(JSONB)  # {"persons": [], "organizations": [], "tools": [], ...}
    category_confidence = Column(Float)
    paper_info = Column(JSONB)  # {"title": "", "authors": [], "journal": "", "doi": "", ...}
    tool_info = Column(JSONB)  # {"name": "", "description": "", "url": "", "features": [], ...}
    news_info = Column(JSONB)  # {"event": "", "date": "", "impact": "", ...}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    article = relationship("Article", back_populates="analysis")
    
    def __repr__(self):
        return f"<ArticleAnalysis(id={self.id}, article_id={self.article_id})>"
