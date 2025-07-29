from fastapi import FastAPI
from database import models, engine
import pandas as pd

# 필요한 모듈 조건부 임포트
try:
    from database.postgres_query import PostgresQuery
except ImportError:
    print("PostgresQuery 모듈을 임포트할 수 없습니다.")

try:
    from routers import items, users, stocks
except ImportError:
    print("기본 라우터 모듈을 임포트할 수 없습니다.")

try:
    from routers import raw_query
except ImportError:
    print("raw_query 모듈을 임포트할 수 없습니다.")

try:
    from routers import stock_crawling
except ImportError:
    print("stock_crawling 모듈을 임포트할 수 없습니다.")



try:
    from jadiss_finance_lib.macd import macd
    from jadiss_finance_lib.rsi import rsi
except ImportError:
    print("jadiss_finance_lib 모듈을 임포트할 수 없습니다.")
    # 임시 함수 정의
    def macd(series):
        return series, series
    
    def rsi(series):
        return series


# DB 테이블 생성 (조건부)
try:
    if engine is not None:
        models.Base.metadata.create_all(bind=engine)
        print("데이터베이스 테이블이 생성되었습니다.")
    else:
        print("데이터베이스 연결이 없어 테이블을 생성할 수 없습니다.")
except Exception as e:
    print(f"테이블 생성 오류: {e}")

app = FastAPI()

# 라우터 등록 (조건부)
try:
    app.include_router(items.router)
    app.include_router(users.router)
    app.include_router(stocks.router)
except NameError:
    print("기본 라우터를 등록할 수 없습니다.")

try:
    app.include_router(raw_query.router)
except NameError:
    print("raw_query 라우터를 등록할 수 없습니다.")

try:
    app.include_router(stock_crawling.router)
except NameError:
    print("stock_crawling 라우터를 등록할 수 없습니다.")



@app.get("/")
async def root():
    return {"message": "FastAPI is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
@app.get("/dbtest")
async def dbtest():
    try:
        result = PostgresQuery.execute_query("SELECT * FROM users")
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}