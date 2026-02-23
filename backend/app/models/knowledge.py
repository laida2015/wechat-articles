"""Knowledge base model."""
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from ..database import Base


class Knowledge(Base):
    """知识库模型."""
    
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False, index=True)  # paper, tool, news
    title = Column(String(500), nullable=False)
    content = Column(JSONB, nullable=False)  # Structured content based on type
    source_articles = Column(JSONB)  # [article_id1, article_id2, ...]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Knowledge(id={self.id}, type='{self.type}', title='{self.title[:30]}...')>"
