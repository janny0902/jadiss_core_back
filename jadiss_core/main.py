from fastapi import FastAPI
from database import models, engine
from routers import items

# 데이터베이스 초기화 (모델 -> 테이블 생성)
models.Base.metadata.create_all(bind=engine)

# FastAPI 인스턴스 생성
app = FastAPI()

# 라우터 등록
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}