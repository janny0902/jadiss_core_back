import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLAlchemy 엔진 및 세션 구성
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

# Dependency: 요청마다 새로운 DB 세션을 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
