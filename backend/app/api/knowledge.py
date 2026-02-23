"""Knowledge base API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models import Knowledge
from ..schemas import knowledge as schemas

router = APIRouter()


@router.get("/", response_model=schemas.KnowledgeList)
async def get_knowledge_list(
    type: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get knowledge list."""
    query = db.query(Knowledge)
    
    if type:
        query = query.filter(Knowledge.type == type)
    
    total = query.count()
    items = query.order_by(Knowledge.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": items}


@router.post("/", response_model=schemas.Knowledge)
async def create_knowledge(
    knowledge: schemas.KnowledgeCreate,
    db: Session = Depends(get_db)
):
    """Create new knowledge entry."""
    db_knowledge = Knowledge(**knowledge.model_dump())
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


@router.get("/{knowledge_id}", response_model=schemas.Knowledge)
async def get_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    """Get knowledge by ID."""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    return knowledge


@router.put("/{knowledge_id}", response_model=schemas.Knowledge)
async def update_knowledge(
    knowledge_id: int,
    knowledge_update: schemas.KnowledgeUpdate,
    db: Session = Depends(get_db)
):
    """Update knowledge."""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    
    for key, value in knowledge_update.model_dump(exclude_unset=True).items():
        setattr(knowledge, key, value)
    
    db.commit()
    db.refresh(knowledge)
    return knowledge


@router.delete("/{knowledge_id}")
async def delete_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    """Delete knowledge."""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    
    db.delete(knowledge)
    db.commit()
    return {"message": "Knowledge deleted successfully"}


@router.get("/search/", response_model=schemas.KnowledgeList)
async def search_knowledge(
    q: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search knowledge."""
    query = db.query(Knowledge).filter(Knowledge.title.ilike(f"%{q}%"))
    
    total = query.count()
    items = query.order_by(Knowledge.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": items}
