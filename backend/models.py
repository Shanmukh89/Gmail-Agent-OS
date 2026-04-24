from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    notify = Column(Boolean, default=False)
    
    emails = relationship("Email", back_populates="category")

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True)
    thread_id = Column(String, index=True)
    sender = Column(String)
    subject = Column(String)
    snippet = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    confidence = Column(Integer, default=0) # 0-100
    needs_review = Column(Boolean, default=False)
    notified = Column(Boolean, default=False)

    category = relationship("Category", back_populates="emails")
