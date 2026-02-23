"""Article model."""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from ..database import Base


class Article(Base):
    """文章模型."""
    
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    content_text = Column(Text)
    url = Column(Text, unique=True)
    published_at = Column(DateTime(timezone=True))
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    is_favorite = Column(Boolean, default=False, index=True)
    category = Column(String(50), index=True)  # paper, tool, news, other
    tags = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    account = relationship("Account", back_populates="articles")
    analysis = relationship("ArticleAnalysis", back_populates="article", uselist=False, cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_articles_published_at', published_at.desc()),
    )
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:30]}...')>"
