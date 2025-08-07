from fastapi import APIRouter
from database.postgres_query import PostgresQuery
from typing import List, Dict, Any
import logging

router = APIRouter(
    prefix="/industry-stock",
    tags=["industry-stock"],
    responses={404: {"description": "Not found"}},
)

@router.get("/getIndustryGrowth")
async def get_industry_growth(date: str, market: str = None) -> List[Dict[str, Any]]:
    """
    업종별 평균 증가율을 조회합니다.
    
    Args:
        date (str): 조회할 날짜 (YYYY-MM-DD 형식)
        market (str): 시장 구분 (KOSPI, KOSDAQ 등)
        
    Returns:
        List[Dict[str, Any]]: 업종별 평균 증가율 정보
    """
    logging.info(f"getIndustryGrowth API called with date: {date}, market: {market}")
    
    query = """
    SELECT
        ci.category_id, si.market,
        ROUND(AVG((sdd.close_price - sdd.open_price) * 100.0 / sdd.open_price), 2) AS avg_increase_rate
    FROM
        company_info ci 
        left join stock_daily_data sdd on ci.stock_code = sdd.stock_code
        left join stock_info si on ci.stock_code = si.stock_code
    where sdd.date = :date
    """
    
    params = {"date": date}
    
    if market:
        query += " AND si.market = :market"
        params["market"] = market
    
    query += " GROUP BY ci.category_id, si.market"
    
    result = PostgresQuery.execute_query(query, params)
    
    logging.info(f"getIndustryGrowth result: {result}")
    return result

@router.get("/getStocksDataSample")
async def get_stocks_data_sample(date: str) -> List[Dict[str, Any]]:
    """
    주식별 증가율을 조회합니다.
    
    Args:
        date (str): 조회할 날짜 (YYYY-MM-DD 형식)
        
    Returns:
        List[Dict[str, Any]]: 주식별 증가율 정보
    """
    query = """
    SELECT
        ci.stock_code,
        ROUND((sdd.close_price - sdd.open_price) * 100.0 / sdd.open_price, 2) AS increase_rate
    FROM
        company_info ci 
        left join stock_daily_data sdd on ci.stock_code = sdd.stock_code 
    where date = :date
    """
    params = {"date": date}
    result = PostgresQuery.execute_query(query, params)
    return result