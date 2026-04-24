from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MailMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to MailMind API"}

@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.model_dump().items():
        setattr(db_category, key, value)
        
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    db.delete(db_category)
    db.commit()
    return {"ok": True}
@app.get("/emails/", response_model=List[schemas.Email])
def read_emails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emails = db.query(models.Email).offset(skip).limit(limit).all()
    return emails

@app.get("/stats/")
def get_stats(db: Session = Depends(get_db)):
    total_emails = db.query(models.Email).count()
    needs_review = db.query(models.Email).filter(models.Email.needs_review == True).count()
    return {"total_emails": total_emails, "needs_review": needs_review}

import email_service
from agent import process_email_pipeline
import datetime

@app.post("/sync/")
def sync_emails(db: Session = Depends(get_db)):
    # 1. Init Gmail service
    try:
        service = email_service.get_gmail_service()
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not service:
        raise HTTPException(status_code=500, detail="Failed to initialize Gmail API")
        
    # 2. Fetch categories
    categories = db.query(models.Category).all()
    if not categories:
        return {"message": "No categories defined. Please add routing rules first."}
        
    # 3. Fetch recent unread emails
    recent_emails = email_service.fetch_recent_emails(service, max_results=10)
    
    processed_count = 0
    notifications_fired = 0
    
    for email_data in recent_emails:
        # Check if already processed
        existing = db.query(models.Email).filter(models.Email.message_id == email_data['message_id']).first()
        if existing:
            continue
            
        # Run classification agent
        final_state = process_email_pipeline(email_data, categories)
        
        cat_name = final_state['classification_result'].get('category_name', 'Uncategorized')
        confidence = final_state['confidence']
        needs_review = final_state['needs_review']
        notified = final_state['notified']
        
        # Find category ID
        assigned_category = next((c for c in categories if c.name.lower() == cat_name.lower()), None)
        category_id = assigned_category.id if assigned_category else None
        
        # Save to DB
        new_email = models.Email(
            message_id=email_data['message_id'],
            thread_id=email_data['thread_id'],
            sender=email_data['sender'],
            subject=email_data['subject'],
            snippet=email_data['snippet'],
            timestamp=datetime.datetime.utcnow(),
            category_id=category_id,
            confidence=confidence,
            needs_review=needs_review,
            notified=notified
        )
        db.add(new_email)
        db.commit()
        
        processed_count += 1
        if notified:
            notifications_fired += 1
            # Here we could trigger a local system notification or webhook
            print(f"NOTIFICATION: New email in {cat_name} from {email_data['sender']} - {email_data['subject']}")
            
        # Apply label in Gmail if we are confident
        if not needs_review and assigned_category:
            email_service.apply_label_to_email(service, email_data['message_id'], assigned_category.name)
            
    return {
        "message": "Sync complete", 
        "processed": processed_count, 
        "notifications_fired": notifications_fired
    }
