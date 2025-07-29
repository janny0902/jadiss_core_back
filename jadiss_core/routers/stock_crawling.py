"""
주식 데이터 크롤링 라우터
"""
from fastapi import APIRouter, BackgroundTasks
from database.postgres_query import PostgresQuery
from services.stock_crawling_service import StockCrawlingService
from typing import Dict, Any

router = APIRouter(
    prefix="/db",
    tags=["database"],
    responses={404: {"description": "Not found"}},
)

@router.post("/crawling")
async def crawl_stock_data(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    코스피 주식 데이터를 크롤링하여 DB에 저장합니다.
    5년치 데이터를 가져옵니다.
    """
    try:
        # 백그라운드에서 크롤링 실행
        def run_crawling():
            return StockCrawlingService.crawl_all_stocks(5)
        background_tasks.add_task(run_crawling)
        
        return {
            "message": "주식 데이터 크롤링이 백그라운드에서 시작되었습니다.",
            "status": "started"
        }
        
    except Exception as e:
        return {
            "message": "크롤링 시작 중 오류가 발생했습니다.",
            "error": str(e)
        }

@router.post("/crawling-sync")
async def crawl_stock_data_sync() -> Dict[str, Any]:
    """
    코스피 주식 데이터를 동기식으로 크롤링합니다. (테스트용)
    """
    try:
        result = StockCrawlingService.crawl_all_stocks(years=1)  # 1년치만 테스트
        
        return {
            "message": "주식 데이터 크롤링이 완료되었습니다.",
            "result": result
        }
        
    except Exception as e:
        return {
            "message": "크롤링 중 오류가 발생했습니다.",
            "error": str(e)
        }

@router.get("/stock-count")
async def get_stock_count() -> Dict[str, Any]:
    """
    저장된 주식 데이터 개수를 조회합니다.
    """
    try:
        stock_info_count = PostgresQuery.execute_scalar("SELECT COUNT(*) FROM stock_info")
        daily_data_count = PostgresQuery.execute_scalar("SELECT COUNT(*) FROM stock_daily_data")
        
        return {
            "stock_info_count": stock_info_count or 0,
            "daily_data_count": daily_data_count or 0
        }
        
    except Exception as e:
        return {
            "error": str(e)
        }

@router.post("/company_crawling")
async def crawl_company_data() -> Dict[str, Any]:
    """
    OpenDartReader를 사용하여 기업 정보를 수집합니다.
    """
    try:
        result = StockCrawlingService.crawl_company_data()
        return result
        
    except Exception as e:
        return {
            "error": str(e)
        }