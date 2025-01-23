from sqlalchemy import Column, Integer, String
from database import Base
##ORM 사용을 위해 생성해야함.


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)
    email = Column(String(100))