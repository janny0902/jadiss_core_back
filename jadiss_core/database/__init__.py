import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL 연결 정보 설정
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://jadiss_core:jadiss_core##@host.docker.internal:5432/core")

# Base 클래스 생성
Base = declarative_base()

# SQLAlchemy 엔진 및 세션 구성 (조건부)
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"데이터베이스 연결 오류: {e}")
    engine = None
    SessionLocal = None

# Dependency: 요청마다 새로운 DB 세션을 생성
def get_db():
    """FastAPI 의존성 주입을 위한 데이터베이스 세션 제공 함수
    
    Yields:
        Session: SQLAlchemy 세션 객체
    """
    if SessionLocal is None:
        raise Exception("데이터베이스 연결이 설정되지 않았습니다.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
