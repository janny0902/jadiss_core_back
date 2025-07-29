-- 기업 정보 및 재무 데이터 테이블 생성 스크립트

-- 1. 기업 정보 테이블
DROP TABLE IF EXISTS company_info CASCADE;
CREATE TABLE company_info (
    id SERIAL PRIMARY KEY,
    corp_code VARCHAR(8) UNIQUE NOT NULL,
    corp_name VARCHAR(200),
    corp_name_eng VARCHAR(200),
    stock_name VARCHAR(200),
    stock_code VARCHAR(6),
    ceo_nm VARCHAR(100),
    corp_cls VARCHAR(2),
    jurir_no VARCHAR(13),
    bizr_no VARCHAR(10),
    adres TEXT,
    hm_url VARCHAR(500),
    ir_url VARCHAR(500),
    phn_no VARCHAR(20),
    fax_no VARCHAR(20),
    induty_code VARCHAR(6),
    est_dt VARCHAR(8),
    acc_mt VARCHAR(2),
    capital_stock BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 재무 데이터 테이블
DROP TABLE IF EXISTS financial_data CASCADE;
CREATE TABLE financial_data (
    id SERIAL PRIMARY KEY,
    corp_code VARCHAR(8) NOT NULL,
    bsns_year VARCHAR(4) NOT NULL,
    reprt_code VARCHAR(5) NOT NULL,
    account_nm VARCHAR(200) NOT NULL,
    fs_div VARCHAR(2),
    fs_nm VARCHAR(100),
    sj_div VARCHAR(2) NOT NULL,
    sj_nm VARCHAR(100),
    thstrm_nm VARCHAR(20),
    thstrm_amount BIGINT,
    thstrm_add_amount BIGINT,
    frmtrm_nm VARCHAR(20),
    frmtrm_amount BIGINT,
    frmtrm_q_nm VARCHAR(20),
    frmtrm_q_amount BIGINT,
    frmtrm_add_amount BIGINT,
    bfefrmtrm_nm VARCHAR(20),
    bfefrmtrm_amount BIGINT,
    ord INTEGER,
    currency VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(corp_code, bsns_year, reprt_code, account_nm, sj_div)
);

-- 3. 인덱스 생성
CREATE INDEX idx_company_info_stock_code ON company_info(stock_code);
CREATE INDEX idx_company_info_corp_name ON company_info(corp_name);
CREATE INDEX idx_company_info_induty_code ON company_info(induty_code);

CREATE INDEX idx_financial_data_corp_code ON financial_data(corp_code);
CREATE INDEX idx_financial_data_year ON financial_data(bsns_year);
CREATE INDEX idx_financial_data_account ON financial_data(account_nm);
CREATE INDEX idx_financial_data_corp_year ON financial_data(corp_code, bsns_year);

-- 4. 외래키 제약조건 (선택사항)
-- ALTER TABLE financial_data 
-- ADD CONSTRAINT fk_financial_company 
-- FOREIGN KEY (corp_code) REFERENCES company_info(corp_code) ON DELETE CASCADE;

-- 5. 유용한 뷰 생성
DROP VIEW IF EXISTS v_company_revenue;
CREATE VIEW v_company_revenue AS
SELECT 
    ci.corp_name,
    ci.stock_code,
    ci.induty_code,
    fd.bsns_year,
    fd.thstrm_amount as revenue,
    fd.frmtrm_amount as prev_revenue
FROM company_info ci
JOIN financial_data fd ON ci.corp_code = fd.corp_code
WHERE fd.account_nm LIKE '%매출%' 
   OR fd.account_nm LIKE '%수익%'
   OR fd.account_nm LIKE '%Revenue%'
ORDER BY ci.corp_name, fd.bsns_year DESC;

-- 6. 업종별 기업 수 뷰
DROP VIEW IF EXISTS v_industry_summary;
CREATE VIEW v_industry_summary AS
SELECT 
    induty_code,
    COUNT(*) as company_count,
    STRING_AGG(corp_name, ', ' ORDER BY corp_name) as companies
FROM company_info 
WHERE induty_code IS NOT NULL
GROUP BY induty_code
ORDER BY company_count DESC;

-- 7. 매출액/순이익 요약 뷰
DROP VIEW IF EXISTS v_company_financial_summary;
CREATE VIEW v_company_financial_summary AS
SELECT 
    ci.corp_name,
    ci.stock_code,
    ci.induty_code,
    ci.capital_stock,
    MAX(CASE WHEN fd.account_nm LIKE '%매출%' THEN fd.thstrm_amount END) as revenue,
    MAX(CASE WHEN fd.account_nm LIKE '%당기순이익%' THEN fd.thstrm_amount END) as net_income,
    fd.bsns_year
FROM company_info ci
JOIN financial_data fd ON ci.corp_code = fd.corp_code
GROUP BY ci.corp_name, ci.stock_code, ci.induty_code, ci.capital_stock, fd.bsns_year
ORDER BY ci.corp_name, fd.bsns_year DESC;