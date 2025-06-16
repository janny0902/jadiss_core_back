from fastapi import FastAPI
from database import models, engine
from routers import items, users, stocks
from jadiss_finance_lib.macd import macd
from jadiss_finance_lib.rsi import rsi
import pandas as pd

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 등록
app.include_router(items.router)
app.include_router(users.router)
app.include_router(stocks.router)

@app.get("/")
async def root():
    prices = [100, 101, 102, 101, 100, 98, 99, 100, 101, 102, 108, 103, 99, 90, 47]
    prices_series = pd.Series(prices)

    macd_line, signal_line = macd(prices_series)
    rsi_values = rsi(prices_series)

    return {
        "macd_line": macd_line.tolist(),
        "signal_line": signal_line.tolist(),
        "rsi_values": rsi_values.tolist()
    }