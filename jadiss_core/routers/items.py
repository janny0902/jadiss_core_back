from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from database.crud import create_item, get_items

router = APIRouter()

# Dependency: 요청마다 새로운 DB 세션을 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/items")
def read_items(db: Session = Depends(get_db)):
    items = get_items(db)
    return items

@router.post("/items")
def add_item(name: str, description: str = None, price: int = 0, db: Session = Depends(get_db)):
    return create_item(db, name, description, price)

# @app.get("/")
# def root():
#     return {"message": "home"}


