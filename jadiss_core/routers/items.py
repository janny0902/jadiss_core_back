from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from database.crud import create_item, get_items
from database.models import User
from database.models import Item

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

@router.get("/test")
def test(db: Session = Depends(get_db)):
    return create_item(db, name, description, price)

@router.post("/usersCreate")
def create_user(name: str, age: int, email: str, db: Session = Depends(get_db)):
    new_user = User(name=name, age=age, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # 삽입된 객체를 반환받음
    return {"message": "User created successfully", "user": new_user}

@router.get("/usersInsert")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/usersSelect/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    user = db.query(User).filter(User.id == user_id).first()  # WHERE id = user_id
    if not user:
        return {"message": "User not found"}
    return user

@router.get("/usersWhere/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()  # WHERE id = user_id
    if not user:
        return {"message": "User not found"}
    return user

@router.get("/usersWWhere/search")
def search_users(age: int, name: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.age > age, User.name.like(f"%{name}%")).all()
    # WHERE age > {age} AND name LIKE '%{name}%'
    return users

@router.put("/usersUpdate/{user_id}")
def update_user(user_id: int, name: str, age: int, email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    
    user.name = name
    user.age = age
    user.email = email
    
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}

@router.delete("/usersDelete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.get("/usersOrderby/sorted")
def get_users_sorted(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.age.desc()).all()  # ORDER BY age DESC
    return users

from sqlalchemy import func

@router.get("/usersGroupby/grouped")
def get_users_grouped_by_age(db: Session = Depends(get_db)):
    result = db.query(User.age, func.count(User.id).label("count")).group_by(User.age).all()
    # SELECT age, COUNT(id) AS count FROM users GROUP BY age
    return result


@router.get("/usersJoin/posts")
def get_users_with_posts(db: Session = Depends(get_db)):
    result = db.query(User.name, Post.title).join(Post, User.id == Post.user_id).all()
    # SELECT users.name, posts.title
    # FROM users
    # JOIN posts ON users.id = posts.user_id
    return result

@router.get("/usersLeftJoin/posts/all")
def get_users_with_or_without_posts(db: Session = Depends(get_db)):
    result = db.query(User.name, Post.title).outerjoin(Post, User.id == Post.user_id).all()
    # SELECT users.name, posts.title
    # FROM users
    # LEFT JOIN posts ON users.id = posts.user_id
    return result

