"""
주식 데이터 모델
"""
from sqlalchemy import Column, Integer, String, Date, BigInteger, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class StockInfo(Base):
    """주식 종목 정보 테이블"""
    __tablename__ = "stock_info"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    market = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class StockDailyData(Base):
    """주식 일별 데이터 테이블"""
    __tablename__ = "stock_daily_data"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_code = Column(String(10), ForeignKey("stock_info.code"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    open_price = Column(Integer, nullable=False)
    high_price = Column(Integer, nullable=False)
    low_price = Column(Integer, nullable=False)
    close_price = Column(Integer, nullable=False)
    volume = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, server_default=func.now())