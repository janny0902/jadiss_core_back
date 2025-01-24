from fastapi import FastAPI
from database import models, engine
from routers import items
from routers import users
from jadiss_finance_lib.macd import macd
from jadiss_finance_lib.rsi import rsi
import pandas as pd 

#서버실행 명령어 : uvicorn main:app --reload
# 데이터베이스 초기화 (모델 -> 테이블 생성)
models.Base.metadata.create_all(bind=engine)

# FastAPI 인스턴스 생성
app = FastAPI()

# 라우터 등록
app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
async def root():
    prices = [100, 101, 102, 101, 100, 98, 99, 100, 101, 102]
    prices_series = pd.Series(prices)
    macd_line, signal_line = macd(prices_series)
    prices_series = pd.Series(prices)
    rsi_values = rsi(prices_series)
    return {
        "macd_line": macd_line.tolist(),
        "signal_line": signal_line.tolist(),
        "rsi_values": rsi_values.tolist()
    }
    #return {"message": "Hello, FastAPI!"}