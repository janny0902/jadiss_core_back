-- 주식 종목 정보 테이블
CREATE TABLE IF NOT EXISTS stock_info (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    market VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 주식 일별 데이터 테이블
CREATE TABLE IF NOT EXISTS stock_daily_data (
    id SERIAL PRIMARY KEY,
    stock_code VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open_price INTEGER NOT NULL,
    high_price INTEGER NOT NULL,
    low_price INTEGER NOT NULL,
    close_price INTEGER NOT NULL,
    volume BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_code, date),
    FOREIGN KEY (stock_code) REFERENCES stock_info(code)
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_stock_daily_data_code ON stock_daily_data(stock_code);
CREATE INDEX IF NOT EXISTS idx_stock_daily_data_date ON stock_daily_data(date);
CREATE INDEX IF NOT EXISTS idx_stock_daily_data_code_date ON stock_daily_data(stock_code, date);