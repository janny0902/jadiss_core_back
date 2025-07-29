# 주식 데이터 크롤링 가이드

## 개요

이 모듈은 코스피 주식 데이터를 크롤링하여 PostgreSQL 데이터베이스에 저장하는 기능을 제공합니다.

## 사용 라이브러리

### yfinance (현재 사용 중)
- **설명**: Yahoo Finance에서 주식 데이터를 가져오는 Python 라이브러리
- **장점**: 
  - 간단하고 사용하기 쉬움
  - 한국 주식 지원 (종목코드.KS 형식)
  - 무료
- **단점**: 
  - Yahoo Finance 서비스에 의존적
  - 실시간 데이터가 아님
  - 가끔 데이터 누락 가능

### 대안 라이브러리들

#### 1. FinanceDataReader
- **특징**: 한국 주식에 특화된 라이브러리
- **장점**: 한국 시장 데이터에 최적화, 다양한 한국 금융 데이터 제공
- **사용법**: `fdr.DataReader('005930', '2019-01-01', '2024-01-01')`

#### 2. pykrx
- **특징**: 한국거래소 공식 데이터 제공
- **장점**: 공식 데이터로 신뢰성 높음, 실시간에 가까운 데이터
- **사용법**: `stock.get_market_ohlcv_by_date()`

#### 3. pandas_datareader
- **특징**: 다양한 데이터 소스 지원
- **장점**: 여러 금융 데이터 소스 통합 지원
- **사용법**: `web.DataReader('005930.KS', 'yahoo')`

## 데이터베이스 구조

### stock_info 테이블
```sql
- id: 기본키 (SERIAL)
- code: 종목코드 (VARCHAR(10), UNIQUE)
- name: 종목명 (VARCHAR(100))
- market: 시장구분 (VARCHAR(20))
- created_at: 생성일시 (TIMESTAMP)
- updated_at: 수정일시 (TIMESTAMP)
```

### stock_daily_data 테이블
```sql
- id: 기본키 (SERIAL)
- stock_code: 종목코드 (VARCHAR(10), FK)
- date: 거래일 (DATE)
- open_price: 시가 (INTEGER)
- high_price: 고가 (INTEGER)
- low_price: 저가 (INTEGER)
- close_price: 종가 (INTEGER)
- volume: 거래량 (BIGINT)
- created_at: 생성일시 (TIMESTAMP)
```

## API 엔드포인트

### POST /db/crawling
- **기능**: 5년치 코스피 주식 데이터 크롤링 및 DB 저장
- **응답 예시**:
```json
{
  "message": "주식 데이터 크롤링이 완료되었습니다.",
  "result": {
    "processed_stocks": 10,
    "saved_stock_info": 10,
    "saved_daily_data": 12500,
    "period": "2019-01-01 ~ 2024-01-01"
  }
}
```

### GET /db/stock-count
- **기능**: 저장된 주식 데이터 개수 조회
- **응답 예시**:
```json
{
  "stock_info_count": 10,
  "daily_data_count": 12500
}
```

## 크롤링 대상 종목

현재 설정된 주요 코스피 종목들:
- 005930: 삼성전자
- 000660: SK하이닉스
- 035420: NAVER
- 051910: LG화학
- 006400: 삼성SDI
- 035720: 카카오
- 207940: 삼성바이오로직스
- 068270: 셀트리온
- 028260: 삼성물산
- 066570: LG전자

## 사용 방법

### 1. 크롤링 실행
```bash
curl -X POST http://localhost:8090/db/crawling
```

### 2. 데이터 개수 확인
```bash
curl -X GET http://localhost:8090/db/stock-count
```

### 3. Swagger UI에서 테스트
```
http://localhost:8090/docs
```

## 주의사항

1. **데이터 중복 처리**: ON CONFLICT를 사용하여 중복 데이터 자동 업데이트
2. **크롤링 시간**: 종목 수와 기간에 따라 시간이 오래 걸릴 수 있음
3. **네트워크 의존성**: 외부 API에 의존하므로 네트워크 상태에 영향받음
4. **데이터 정확성**: Yahoo Finance 데이터의 정확성에 의존

## 확장 가능성

- 더 많은 종목 추가
- 실시간 데이터 수집
- 다른 시장 데이터 추가 (코스닥, 해외 주식)
- 기술적 지표 계산 및 저장