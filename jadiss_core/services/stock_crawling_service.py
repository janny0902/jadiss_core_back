"""
주식 데이터 크롤링 서비스
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
from database.postgres_query import PostgresQuery
try:
    import FinanceDataReader as fdr
except ImportError:
    fdr = None
    print("FinanceDataReader가 설치되지 않았습니다. pip install finance-datareader")



class StockCrawlingService:
    """코스피 주식 데이터 크롤링 서비스"""
    
    @staticmethod
    def get_kospi_stock_list() -> List[Dict[str, str]]:
        """코스피 종목 리스트를 가져옵니다."""
        try:
            # 간단한 예시 종목들
            sample_stocks = [
                {"code": "005930", "name": "삼성전자"},
                {"code": "000660", "name": "SK하이닉스"},
                {"code": "035420", "name": "NAVER"},
                {"code": "051910", "name": "LG화학"},
                {"code": "006400", "name": "삼성SDI"},
                {"code": "035720", "name": "카카오"},
                {"code": "207940", "name": "삼성바이오로직스"},
                {"code": "068270", "name": "셀트리온"},
                {"code": "028260", "name": "삼성물산"},
                {"code": "066570", "name": "LG전자"}
            ]
            
            return sample_stocks
            
        except Exception as e:
            print(f"종목 리스트 가져오기 오류: {e}")
            return []
    
    @staticmethod
    def get_stock_data(stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """특정 종목의 주식 데이터를 FinanceDataReader에서 가져옵니다."""
        try:
            if fdr is None:
                print(f"{stock_code}: FinanceDataReader가 설치되지 않았습니다.")
                return pd.DataFrame()
            
            data = fdr.DataReader(stock_code, start_date, end_date)
            
            if data.empty:
                print(f"{stock_code}: FinanceDataReader에서 데이터를 가져올 수 없습니다.")
                return pd.DataFrame()
            
            data = data.reset_index()
            data['stock_code'] = stock_code
            data['date'] = data['Date'].dt.date
            data['open_price'] = (data['Open']).astype(int)
            data['high_price'] = (data['High']).astype(int)
            data['low_price'] = (data['Low']).astype(int)
            data['close_price'] = (data['Close']).astype(int)
            data['volume'] = data['Volume'].astype(int)
            
            result = data[['stock_code', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']]
            
            return result
            
        except Exception as e:
            print(f"주식 데이터 가져오기 오류 ({stock_code}): {e}")
            return pd.DataFrame()
    
    @staticmethod
    def save_stock_info(stocks: List[Dict[str, str]]) -> int:
        """종목 정보를 DB에 저장합니다."""
        try:
            saved_count = 0
            
            for stock in stocks:
                # 먼저 존재 여부 확인
                check_query = "SELECT COUNT(*) FROM stock_info WHERE code = :code"
                exists = PostgresQuery.execute_scalar(check_query, {"code": stock["code"]})
                
                if exists == 0:
                    # 새로 삽입
                    query = """
                    INSERT INTO stock_info (code, name, market, created_at, updated_at) 
                    VALUES (:code, :name, :market, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """
                else:
                    # 업데이트
                    query = """
                    UPDATE stock_info SET 
                        name = :name,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE code = :code
                    """
                params = {
                    "code": stock["code"],
                    "name": stock["name"],
                    "market": "KOSPI"
                }
                
                print(f"종목 정보 저장 시도: {stock['name']} ({stock['code']})")
                affected_rows = PostgresQuery.execute_update(query, params)
                print(f"영향받은 행 수: {affected_rows}")
                saved_count += 1  # ON CONFLICT로 인해 항상 1개씩 처리됨
            
            return saved_count
            
        except Exception as e:
            print(f"종목 정보 저장 오류: {e}")
            return 0
    
    @staticmethod
    def save_stock_daily_data(df: pd.DataFrame) -> int:
        """일별 주식 데이터를 DB에 저장합니다."""
        try:
            if df.empty:
                return 0
            
            saved_count = 0
            
            for _, row in df.iterrows():
                # 먼저 존재 여부 확인
                check_query = "SELECT COUNT(*) FROM stock_daily_data WHERE stock_code = :stock_code AND date = :date"
                exists = PostgresQuery.execute_scalar(check_query, {"stock_code": row['stock_code'], "date": row['date']})
                
                if exists == 0:
                    # 새로 삽입
                    query = """
                    INSERT INTO stock_daily_data (stock_code, date, open_price, high_price, low_price, close_price, volume, created_at)
                    VALUES (:stock_code, :date, :open_price, :high_price, :low_price, :close_price, :volume, CURRENT_TIMESTAMP)
                    """
                else:
                    # 업데이트
                    query = """
                    UPDATE stock_daily_data SET 
                        open_price = :open_price,
                        high_price = :high_price,
                        low_price = :low_price,
                        close_price = :close_price,
                        volume = :volume
                    WHERE stock_code = :stock_code AND date = :date
                    """
                params = {
                    "stock_code": row['stock_code'],
                    "date": row['date'],
                    "open_price": row['open_price'],
                    "high_price": row['high_price'],
                    "low_price": row['low_price'],
                    "close_price": row['close_price'],
                    "volume": row['volume']
                }
                
                affected_rows = PostgresQuery.execute_update(query, params)
                saved_count += 1  # ON CONFLICT로 인해 항상 처리됨
            
            return saved_count
            
        except Exception as e:
            print(f"일별 데이터 저장 오류: {e}")
            return 0
    

    
    @staticmethod
    def crawl_all_stocks(years: int = 5) -> Dict[str, int]:
        """모든 코스피 종목의 데이터를 크롤링합니다."""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years * 365)
            
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            stocks = StockCrawlingService.get_kospi_stock_list()
            
            if not stocks:
                return {"error": "종목 리스트를 가져올 수 없습니다."}
            
            stock_info_count = StockCrawlingService.save_stock_info(stocks)
            
            total_data_count = 0
            processed_stocks = 0
            
            for stock in stocks:
                stock_code = stock["code"]
                stock_name = stock["name"]
                
                print(f"처리 중: {stock_name} ({stock_code})")
                
                df = StockCrawlingService.get_stock_data(stock_code, start_date_str, end_date_str)
                
                print(f"가져온 데이터 행 수: {len(df)}")
                
                if not df.empty:
                    data_count = StockCrawlingService.save_stock_daily_data(df)
                    total_data_count += data_count
                    print(f"{stock_name}: {data_count}개 데이터 저장")
                else:
                    print(f"{stock_name}: 데이터가 비어있음")
                
                processed_stocks += 1
            
            return {
                "processed_stocks": processed_stocks,
                "saved_stock_info": stock_info_count,
                "saved_daily_data": total_data_count,
                "period": f"{start_date_str} ~ {end_date_str}"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def crawl_company_data() -> Dict[str, any]:
        """OpenDartReader를 사용하여 기업 정보를 수집합니다."""
        try:
            from OpenDartReader.dart import OpenDartReader

            # 발급받은 API 키 입력
            api_key = ''
            dart = OpenDartReader(api_key)

            
            # stock_crawling과 동일한 기업 리스트 사용
            stock_codes = ['005930', '000660', '035420', '051910', '006400', 
                          '035720', '207940', '068270', '028260', '066570']
            
            saved_companies = 0
            saved_financial = 0
            
            for stock_code in stock_codes:
                try:
                    # 각 종목의 기업 정보 가져오기
                    company_info = dart.company(stock_code)
                    
                    if company_info is not None:
                        print(f"Company info for {stock_code}: {company_info}")
                        
                        # 기업 정보 저장
                        saved_companies += StockCrawlingService._save_company_info_dict(company_info)
                        
                        # corp_code 가져오기
                        corp_code = company_info.get('corp_code')
                        
                        if corp_code:
                            print(f"{stock_code} corp_code: {corp_code}")
                            
                            # 모든 종목 재무데이터 수집
                            try:
                                print(f"=== {stock_code} 재무데이터 수집 ===")
                                
                                # finstate_all 방식 사용 (가장 많은 데이터 반환)
                                for year in ['2023', '2022']:
                                    try:
                                        print(f"{stock_code} {year}년 데이터 수집...")
                                        result = dart.finstate_all(corp_code, year)
                                        
                                        if result is not None and hasattr(result, 'empty') and not result.empty:
                                            print(f"{stock_code} {year}년 데이터 발견: {result.shape}")
                                            
                                            saved_count = StockCrawlingService._save_financial_data(corp_code, year, result)
                                            saved_financial += saved_count
                                            print(f"{stock_code} {year}년 {saved_count}개 데이터 저장 완료")
                                        else:
                                            print(f"{stock_code} {year}년 데이터 없음")
                                            
                                    except Exception as year_error:
                                        print(f"{stock_code} {year}년 오류: {year_error}")
                                        
                            except Exception as e:
                                print(f"{stock_code} 재무데이터 수집 오류: {e}")
                    else:
                        print(f"{stock_code} 기업 정보를 찾을 수 없습니다.")
                        
                except Exception as e:
                    print(f"{stock_code} 처리 중 오류: {e}")
            
            return {
                "message": "기업 정보 수집 완료",
                "saved_companies": saved_companies,
                "saved_financial_data": saved_financial
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def _save_company_info_dict(company_dict) -> int:
        """딕셔너리 형태의 기업 정보를 DB에 저장합니다."""
        try:
            query = """
            INSERT INTO company_info (
                corp_code, corp_name, corp_name_eng, stock_name, stock_code,
                ceo_nm, corp_cls, jurir_no, bizr_no, adres, hm_url,
                ir_url, phn_no, fax_no, induty_code, est_dt, acc_mt,
                created_at, updated_at
            ) VALUES (
                :corp_code, :corp_name, :corp_name_eng, :stock_name, :stock_code,
                :ceo_nm, :corp_cls, :jurir_no, :bizr_no, :adres, :hm_url,
                :ir_url, :phn_no, :fax_no, :induty_code, :est_dt, :acc_mt,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
            ON CONFLICT (corp_code) DO UPDATE SET
                corp_name = EXCLUDED.corp_name,
                stock_name = EXCLUDED.stock_name,
                ceo_nm = EXCLUDED.ceo_nm,
                induty_code = EXCLUDED.induty_code,
                updated_at = CURRENT_TIMESTAMP
            """
            
            params = {
                "corp_code": company_dict.get('corp_code'),
                "corp_name": company_dict.get('corp_name'),
                "corp_name_eng": company_dict.get('corp_name_eng'),
                "stock_name": company_dict.get('stock_name'),
                "stock_code": company_dict.get('stock_code'),
                "ceo_nm": company_dict.get('ceo_nm'),
                "corp_cls": company_dict.get('corp_cls'),
                "jurir_no": company_dict.get('jurir_no'),
                "bizr_no": company_dict.get('bizr_no'),
                "adres": company_dict.get('adres'),
                "hm_url": company_dict.get('hm_url'),
                "ir_url": company_dict.get('ir_url'),
                "phn_no": company_dict.get('phn_no'),
                "fax_no": company_dict.get('fax_no'),
                "induty_code": company_dict.get('induty_code'),
                "est_dt": company_dict.get('est_dt'),
                "acc_mt": company_dict.get('acc_mt')
            }
            
            PostgresQuery.execute_update(query, params)
            return 1
            
        except Exception as e:
            print(f"기업 정보 저장 오류: {e}")
            return 0
    
    @staticmethod
    def _save_company_info(company) -> int:
        """기업 정보를 DB에 저장합니다."""
        try:
            query = """
            INSERT INTO company_info (
                corp_code, corp_name, corp_name_eng, stock_name, stock_code,
                ceo_nm, corp_cls, jurir_no, bizr_no, adres, hm_url,
                ir_url, phn_no, fax_no, induty_code, est_dt, acc_mt,
                created_at, updated_at
            ) VALUES (
                :corp_code, :corp_name, :corp_name_eng, :stock_name, :stock_code,
                :ceo_nm, :corp_cls, :jurir_no, :bizr_no, :adres, :hm_url,
                :ir_url, :phn_no, :fax_no, :induty_code, :est_dt, :acc_mt,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
            ON CONFLICT (corp_code) DO UPDATE SET
                corp_name = EXCLUDED.corp_name,
                stock_name = EXCLUDED.stock_name,
                ceo_nm = EXCLUDED.ceo_nm,
                induty_code = EXCLUDED.induty_code,
                updated_at = CURRENT_TIMESTAMP
            """
            
            params = {
                "corp_code": company.get('corp_code'),
                "corp_name": company.get('corp_name'),
                "corp_name_eng": company.get('corp_name_eng'),
                "stock_name": company.get('stock_name'),
                "stock_code": company.get('stock_code'),
                "ceo_nm": company.get('ceo_nm'),
                "corp_cls": company.get('corp_cls'),
                "jurir_no": company.get('jurir_no'),
                "bizr_no": company.get('bizr_no'),
                "adres": company.get('adres'),
                "hm_url": company.get('hm_url'),
                "ir_url": company.get('ir_url'),
                "phn_no": company.get('phn_no'),
                "fax_no": company.get('fax_no'),
                "induty_code": company.get('induty_code'),
                "est_dt": company.get('est_dt'),
                "acc_mt": company.get('acc_mt')
            }
            
            PostgresQuery.execute_update(query, params)
            return 1
            
        except Exception as e:
            print(f"기업 정보 저장 오류: {e}")
            return 0
    
    @staticmethod
    def _save_financial_data(corp_code: str, year: str, fs_data) -> int:
        """재무 데이터를 DB에 저장합니다."""
        try:
            saved_count = 0
            print(f"\n=== 재무데이터 저장 시작: {corp_code} {year}년 ({len(fs_data)}건) ===")
            
            for idx, row in fs_data.iterrows():
                try:
                    # 데이터 타입 변환
                    thstrm_amount = None
                    frmtrm_amount = None
                    
                    if row.get('thstrm_amount'):
                        try:
                            thstrm_amount = int(str(row.get('thstrm_amount')).replace(',', '').replace('-', '0'))
                        except:
                            thstrm_amount = None
                    
                    if row.get('frmtrm_amount'):
                        try:
                            frmtrm_amount = int(str(row.get('frmtrm_amount')).replace(',', '').replace('-', '0'))
                        except:
                            frmtrm_amount = None
                    
                    query = """
                    INSERT INTO financial_data (
                        corp_code, bsns_year, reprt_code, account_nm, fs_div,
                        fs_nm, sj_div, sj_nm, thstrm_nm, thstrm_amount,
                        frmtrm_nm, frmtrm_amount, ord, currency, created_at
                    ) VALUES (
                        :corp_code, :bsns_year, :reprt_code, :account_nm, :fs_div,
                        :fs_nm, :sj_div, :sj_nm, :thstrm_nm, :thstrm_amount,
                        :frmtrm_nm, :frmtrm_amount, :ord, :currency, CURRENT_TIMESTAMP
                    )
                    ON CONFLICT (corp_code, bsns_year, reprt_code, account_nm, sj_div) 
                    DO UPDATE SET
                        thstrm_amount = EXCLUDED.thstrm_amount,
                        frmtrm_amount = EXCLUDED.frmtrm_amount,
                        updated_at = CURRENT_TIMESTAMP
                    """
                    
                    # VARCHAR 길이 제한 처리
                    def truncate_string(value, max_length):
                        if value is None:
                            return None
                        return str(value)[:max_length] if len(str(value)) > max_length else str(value)
                    
                    params = {
                        "corp_code": corp_code,
                        "bsns_year": year,
                        "reprt_code": truncate_string(row.get('reprt_code'), 5),
                        "account_nm": truncate_string(row.get('account_nm'), 200),
                        "fs_div": truncate_string(row.get('fs_div'), 2),
                        "fs_nm": truncate_string(row.get('fs_nm'), 100),
                        "sj_div": truncate_string(row.get('sj_div'), 2),
                        "sj_nm": truncate_string(row.get('sj_nm'), 100),
                        "thstrm_nm": truncate_string(row.get('thstrm_nm'), 20),
                        "thstrm_amount": thstrm_amount,
                        "frmtrm_nm": truncate_string(row.get('frmtrm_nm'), 20),
                        "frmtrm_amount": frmtrm_amount,
                        "ord": row.get('ord'),
                        "currency": truncate_string(row.get('currency'), 10)
                    }
                    
                    PostgresQuery.execute_update(query, params)
                    saved_count += 1
                    
                    if saved_count == 1:  # 첫 번째만 로그 출력
                        print(f"[1] 저장: {row.get('account_nm')} | 당기: {thstrm_amount}")
                        
                except Exception as row_error:
                    if "too long" in str(row_error):
                        print(f"!!! 길이 초과 오류 ({idx}): {str(row_error)[:100]}...")
                    else:
                        print(f"!!! 행 저장 오류 ({idx}): {row_error}")
                    continue  # 오류 발생시 다음 행으로 계속
            
            print(f"재무데이터 저장 완료: {saved_count}개")
            return saved_count
            
        except Exception as e:
            print(f"재무 데이터 저장 오류: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return 0