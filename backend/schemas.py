from pydantic import BaseModel
from typing import Optional, List
import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    notify: bool = False

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class EmailBase(BaseModel):
    message_id: str
    thread_id: Optional[str] = None
    sender: str
    subject: str
    snippet: str
    timestamp: datetime.datetime
    confidence: int = 0
    needs_review: bool = False
    notified: bool = False

class EmailCreate(EmailBase):
    category_id: Optional[int] = None

class Email(EmailBase):
    id: int
    category_id: Optional[int] = None
    category: Optional[Category] = None

    class Config:
        from_attributes = True
