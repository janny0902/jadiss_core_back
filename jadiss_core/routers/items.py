from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from database.models import Item
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    description: str
    price: int

class ItemSearch(BaseModel):
    id :  Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

router = APIRouter()

@router.get("/items")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
    

@router.post("/itemCreate")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    new_item = Item(name=item.name, description=item.description, price=item.price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)  # 삽입된 객체를 반환받음1
    return {"message": "Item created successfully", "item": new_item}

@router.post("/itemsWhere")
def read_items_with_conditions(item_search: ItemSearch, db: Session = Depends(get_db)):
    query = db.query(Item)

    if item_search.id:
        query = query.filter(Item.id == item_search.id)
    if item_search.name:
        query = query.filter(Item.name == item_search.name)
    if item_search.description:
        query = query.filter(Item.description == item_search.description)
    if item_search.price:
        query = query.filter(Item.price == item_search.price)
        
    items = query.all()
    return items