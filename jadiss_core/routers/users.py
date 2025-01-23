from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from database.models import User
from typing import Optional

class UserCreate(BaseModel):
    name: str
    age: int
    email: str

class UserSearch(BaseModel):
    id :  Optional[int] = None
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None

router = APIRouter()

@router.get("/users")
def read_items(db: Session = Depends(get_db)):
     return db.query(User).all()

@router.post("/usersCreate")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, age=user.age, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # 삽입된 객체를 반환받음
    return {"message": "User created successfully", "user": new_user}

@router.post("/usersWhere")
def read_users_with_conditions(user_search: UserSearch, db: Session = Depends(get_db)):
    query = db.query(User)

    if user_search.id:
        query = query.filter(User.id == user_search.id)
    if user_search.name:
        query = query.filter(User.name == user_search.name)
    if user_search.age:
        query = query.filter(User.age == user_search.age)
    if user_search.email:
        query = query.filter(User.email == user_search.email)
        
    users = query.all()
    return users
