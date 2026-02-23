"""Article API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models import Article, ArticleAnalysis
from ..schemas import article as schemas
from ..services.ai_service import AIService

router = APIRouter()


@router.get("/", response_model=schemas.ArticleList)
async def get_articles(
    account_id: Optional[int] = None,
    category: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get articles with filters."""
    query = db.query(Article)
    
    if account_id:
        query = query.filter(Article.account_id == account_id)
    if category:
        query = query.filter(Article.category == category)
    if is_favorite is not None:
        query = query.filter(Article.is_favorite == is_favorite)
    
    total = query.count()
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": articles}


@router.get("/{article_id}", response_model=schemas.ArticleDetail)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get article by ID with analysis."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/", response_model=schemas.Article)
async def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db)
):
    """Create new article."""
    db_article = Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.put("/{article_id}", response_model=schemas.Article)
async def update_article(
    article_id: int,
    article_update: schemas.ArticleUpdate,
    db: Session = Depends(get_db)
):
    """Update article."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    for key, value in article_update.model_dump(exclude_unset=True).items():
        setattr(article, key, value)
    
    db.commit()
    db.refresh(article)
    return article


@router.delete("/{article_id}")
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    """Delete article."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully"}


@router.post("/{article_id}/favorite", response_model=schemas.Article)
async def toggle_favorite(article_id: int, db: Session = Depends(get_db)):
    """Toggle article favorite status."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article.is_favorite = not article.is_favorite
    db.commit()
    db.refresh(article)
    return article


@router.post("/{article_id}/analyze")
async def analyze_article(article_id: int, db: Session = Depends(get_db)):
    """Analyze article with AI."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Check if analysis already exists
    existing_analysis = db.query(ArticleAnalysis).filter(
        ArticleAnalysis.article_id == article_id
    ).first()
    
    if existing_analysis:
        return {"message": "Analysis already exists", "analysis_id": existing_analysis.id}
    
    # Perform AI analysis
    ai_service = AIService()
    analysis_result = await ai_service.analyze_article(
        article.title,
        article.content_text or article.content or ""
    )
    
    # Save analysis
    db_analysis = ArticleAnalysis(
        article_id=article_id,
        summary=analysis_result.get("summary"),
        keywords=analysis_result.get("keywords"),
        entities=analysis_result.get("entities"),
        category_confidence=analysis_result.get("category_confidence"),
        paper_info=analysis_result.get("paper_info"),
        tool_info=analysis_result.get("tool_info"),
        news_info=analysis_result.get("news_info"),
    )
    
    # Update article category
    article.category = analysis_result.get("category", "other")
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return {"message": "Analysis completed", "analysis_id": db_analysis.id}


@router.get("/search/", response_model=schemas.ArticleList)
async def search_articles(
    q: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search articles by title or content."""
    query = db.query(Article).filter(
        (Article.title.ilike(f"%{q}%")) | (Article.content_text.ilike(f"%{q}%"))
    )
    
    total = query.count()
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": articles}
