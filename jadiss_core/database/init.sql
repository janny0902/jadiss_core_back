-- 테이블 생성 스크립트
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INTEGER,
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price INTEGER NOT NULL
);

-- 초기 데이터 삽입
INSERT INTO users (name, age, email) VALUES
    ('사용자1', 30, 'user1@example.com'),
    ('사용자2', 25, 'user2@example.com'),
    ('사용자3', 40, 'user3@example.com');

INSERT INTO items (name, description, price) VALUES
    ('상품1', '첫 번째 상품 설명', 10000),
    ('상품2', '두 번째 상품 설명', 20000),
    ('상품3', '세 번째 상품 설명', 30000);