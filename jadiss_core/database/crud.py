from sqlalchemy.orm import Session
from database.models import Item

# Create
def create_item(db: Session, name: str, description: str, price: int):
    item = Item(name=name, description=description, price=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# Read
def get_items(db: Session):
    return db.query(Item).all()
