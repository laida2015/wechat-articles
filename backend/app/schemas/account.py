"""Account schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class AccountBase(BaseModel):
    """Base account schema."""
    name: str
    weread_id: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    feed_url: Optional[str] = None
    is_active: bool = True


class AccountCreate(AccountBase):
    """Schema for creating account."""
    pass


class AccountUpdate(BaseModel):
    """Schema for updating account."""
    name: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    feed_url: Optional[str] = None
    is_active: Optional[bool] = None


class Account(AccountBase):
    """Schema for account response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AccountList(BaseModel):
    """Schema for account list response."""
    total: int
    items: list[Account]
