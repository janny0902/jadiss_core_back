from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import FinanceDataReader as fdr
from database import models
from database.database import get_db  # get_db 불러오기
from datetime import datetime

router = APIRouter()

class StockRequest(BaseModel):
    start_date: str  # "YYYYMMDD"
    end_date: str
    codes: list[str]

@router.post("/api/save-stocks")
def save_stocks(req: StockRequest, db: Session = Depends(get_db)):
    try:
        for code in req.codes:
            df = fdr.DataReader(code, req.start_date, req.end_date)
            df.reset_index(inplace=True)

            for _, row in df.iterrows():
                stock = models.StockPrice(
                    code=code,
                    date=row['Date'].date() if isinstance(row['Date'], datetime) else row['Date'],
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=row['Volume']
                )
                db.add(stock)
            db.commit()
        return {"message": "✅ 모든 종목 저장 완료!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))