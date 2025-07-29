# PostgreSQL 직접 쿼리 사용 가이드

이 문서는 PostgreSQL 데이터베이스에 직접 SQL 쿼리를 실행하는 방법에 대한 가이드입니다.

## 연결 정보

- 데이터베이스 URL: `jdbc:postgresql://localhost:5432/core`
- 사용자 이름: `jadiss_core`

## 기본 사용법

### 1. PostgresQuery 클래스 임포트

```python
from database.postgres_query import PostgresQuery
```

### 2. 데이터 조회 (SELECT)

```python
# 기본 조회
result = PostgresQuery.execute_query("SELECT * FROM users")

# 파라미터를 사용한 조회
result = PostgresQuery.execute_query(
    "SELECT * FROM users WHERE age > :min_age",
    {"min_age": 18}
)

# 단일 값 조회
count = PostgresQuery.execute_scalar("SELECT COUNT(*) FROM users")
```

### 3. 데이터 수정 (INSERT, UPDATE, DELETE)

```python
# 데이터 삽입
affected_rows = PostgresQuery.execute_update(
    "INSERT INTO users (name, age, email) VALUES (:name, :age, :email)",
    {"name": "New User", "age": 25, "email": "user@example.com"}
)

# 데이터 수정
affected_rows = PostgresQuery.execute_update(
    "UPDATE users SET age = :age WHERE id = :id",
    {"age": 30, "id": 1}
)

# 데이터 삭제
affected_rows = PostgresQuery.execute_update(
    "DELETE FROM users WHERE id = :id",
    {"id": 1}
)
```

### 4. 트랜잭션 사용

여러 쿼리를 하나의 트랜잭션으로 실행할 수 있습니다:

```python
queries = [
    {
        'query': "INSERT INTO users (name, age, email) VALUES (:name, :age, :email)",
        'params': {'name': 'User 1', 'age': 25, 'email': 'user1@example.com'}
    },
    {
        'query': "INSERT INTO users (name, age, email) VALUES (:name, :age, :email)",
        'params': {'name': 'User 2', 'age': 30, 'email': 'user2@example.com'}
    }
]

success = PostgresQuery.execute_transaction(queries)
```

## FastAPI에서 사용 예제

```python
from fastapi import APIRouter, HTTPException
from database.postgres_query import PostgresQuery

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    result = PostgresQuery.execute_query(query, {"user_id": user_id})
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return result[0]
```

## 주의사항

1. SQL 인젝션 방지를 위해 항상 파라미터 바인딩을 사용하세요.
2. 복잡한 쿼리는 가독성을 위해 여러 줄로 작성하세요.
3. 트랜잭션이 필요한 경우 `execute_transaction` 메서드를 사용하세요.