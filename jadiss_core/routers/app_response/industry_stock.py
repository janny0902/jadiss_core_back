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

@router.get("/getStocksData")
async def get_stocks_data(date: str, market: str = None) -> List[Dict[str, Any]]:
    """
    카테고리별 주식 종목과 증가율을 조회합니다.
    
    Args:
        date (str): 조회할 날짜 (YYYY-MM-DD 형식)
        market (str): 시장 구분 (KOSPI, KOSDAQ 등)
        
    Returns:
        List[Dict[str, Any]]: 카테고리별 주식 종목 정보
    """
    logging.info(f"getStocksData API called with date: {date}, market: {market}")
    
    query = """
    SELECT
        ci.category_id,
        ci.stock_code,
        ci.corp_name as company_name,
        si.market,
        sdd.close_price,
        sdd.open_price,
        ROUND((sdd.close_price - sdd.open_price) * 100.0 / sdd.open_price, 2) AS increase_rate
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
    
    query += " ORDER BY ci.category_id, ci.stock_code"
    
    result = PostgresQuery.execute_query(query, params)
    
    logging.info(f"getStocksData result count: {len(result) if result else 0}")
    return result

@router.get("/getStockChartData")
async def get_stock_chart_data(stock_code: str) -> List[Dict[str, Any]]:
    """
    특정 종목의 차트 데이터를 조회합니다.
    
    Args:
        stock_code (str): 주식 코드
        
    Returns:
        List[Dict[str, Any]]: 해당 종목의 모든 차트 데이터
    """
    logging.info(f"getStockChartData API called with stock_code: {stock_code}")
    
    query = """
    SELECT
        sdd.date,
        sdd.stock_code,
        sdd.open_price,
        sdd.close_price,
        sdd.high_price,
        sdd.low_price
    FROM
        stock_daily_data sdd
    WHERE sdd.stock_code = :stock_code
    ORDER BY sdd.date ASC
    """
    
    params = {"stock_code": stock_code}
    result = PostgresQuery.execute_query(query, params)
    
    logging.info(f"getStockChartData result count: {len(result) if result else 0}")
    return result

@router.get("/getStockInfo")
async def get_stock_info(stock_code: str, market: str = None) -> List[Dict[str, Any]]:
    """
    특정 종목의 기본 정보를 조회합니다.
    
    Args:
        stock_code (str): 주식 코드
        market (str): 시장 구분 (KOSPI, KOSDAQ 등)
        
    Returns:
        List[Dict[str, Any]]: 해당 종목의 기본 정보
    """
    logging.info(f"getStockInfo API called with stock_code: {stock_code}, market: {market}")
    
    query = """
    SELECT
        ci.category_id,
        ci.stock_code,
        ci.corp_name as company_name,
        si.market
    FROM
        company_info ci 
        left join stock_info si on ci.stock_code = si.stock_code
    WHERE ci.stock_code = :stock_code
    """
    
    params = {"stock_code": stock_code}
    
    if market:
        query += " AND si.market = :market"
        params["market"] = market
    
    result = PostgresQuery.execute_query(query, params)
    
    logging.info(f"getStockInfo result count: {len(result) if result else 0}")
    return result