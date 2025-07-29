"""
PostgreSQL 직접 쿼리 사용 예제
"""
from fastapi import APIRouter, Depends, HTTPException
from database.postgres_query import PostgresQuery
from typing import List, Dict, Any

router = APIRouter(
    prefix="/raw-query",
    tags=["raw-query"],
    responses={404: {"description": "Not found"}},
)

@router.get("/users")
async def get_all_users() -> List[Dict[str, Any]]:
    """
    모든 사용자 정보를 조회합니다.
    
    Returns:
        List[Dict[str, Any]]: 사용자 정보 목록
    """
    # 직접 SQL 쿼리 실행
    query = "SELECT * FROM users"
    result = PostgresQuery.execute_query(query)
    return result

@router.get("/users/{user_id}")
async def get_user_by_id(user_id: int) -> Dict[str, Any]:
    """
    특정 ID의 사용자 정보를 조회합니다.
    
    Args:
        user_id (int): 조회할 사용자 ID
        
    Returns:
        Dict[str, Any]: 사용자 정보
    """
    query = "SELECT * FROM users WHERE id = :user_id"
    params = {"user_id": user_id}
    result = PostgresQuery.execute_query(query, params)
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return result[0]

@router.post("/users")
async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    새로운 사용자를 생성합니다.
    
    Args:
        user_data (Dict[str, Any]): 생성할 사용자 정보
        
    Returns:
        Dict[str, Any]: 생성된 사용자 정보
    """
    query = """
    INSERT INTO users (name, age, email) 
    VALUES (:name, :age, :email) 
    RETURNING id, name, age, email
    """
    params = {
        "name": user_data.get("name"),
        "age": user_data.get("age"),
        "email": user_data.get("email")
    }
    
    result = PostgresQuery.execute_query(query, params)
    return result[0] if result else {"message": "Failed to create user"}

@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    특정 ID의 사용자 정보를 업데이트합니다.
    
    Args:
        user_id (int): 업데이트할 사용자 ID
        user_data (Dict[str, Any]): 업데이트할 사용자 정보
        
    Returns:
        Dict[str, Any]: 업데이트 결과
    """
    # 먼저 사용자가 존재하는지 확인
    check_query = "SELECT id FROM users WHERE id = :user_id"
    check_result = PostgresQuery.execute_query(check_query, {"user_id": user_id})
    
    if not check_result:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 사용자 정보 업데이트
    update_query = """
    UPDATE users 
    SET name = :name, age = :age, email = :email 
    WHERE id = :user_id
    """
    params = {
        "user_id": user_id,
        "name": user_data.get("name"),
        "age": user_data.get("age"),
        "email": user_data.get("email")
    }
    
    affected_rows = PostgresQuery.execute_update(update_query, params)
    
    if affected_rows > 0:
        return {"message": f"User {user_id} updated successfully"}
    else:
        return {"message": "No changes made"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int) -> Dict[str, Any]:
    """
    특정 ID의 사용자를 삭제합니다.
    
    Args:
        user_id (int): 삭제할 사용자 ID
        
    Returns:
        Dict[str, Any]: 삭제 결과
    """
    query = "DELETE FROM users WHERE id = :user_id"
    params = {"user_id": user_id}
    
    affected_rows = PostgresQuery.execute_update(query, params)
    
    if affected_rows > 0:
        return {"message": f"User {user_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/complex-query")
async def execute_complex_query() -> Dict[str, Any]:
    """
    복잡한 쿼리 실행 예제
    
    Returns:
        Dict[str, Any]: 쿼리 결과
    """
    # 여러 테이블 조인 예제
    query = """
    SELECT u.id, u.name, u.email, COUNT(i.id) as item_count
    FROM users u
    LEFT JOIN items i ON i.id % 10 = u.id % 10  -- 예시를 위한 임의의 조인 조건
    GROUP BY u.id, u.name, u.email
    ORDER BY item_count DESC
    """
    
    result = PostgresQuery.execute_query(query)
    return {"users_with_items": result}

@router.post("/transaction-example")
async def transaction_example() -> Dict[str, Any]:
    """
    트랜잭션 실행 예제
    
    Returns:
        Dict[str, Any]: 트랜잭션 실행 결과
    """
    # 여러 쿼리를 하나의 트랜잭션으로 실행
    queries = [
        {
            'query': "INSERT INTO users (name, age, email) VALUES (:name, :age, :email)",
            'params': {'name': 'Transaction User', 'age': 25, 'email': 'transaction@example.com'}
        },
        {
            'query': "UPDATE items SET price = price * 1.1 WHERE price < 1000",
            'params': {}
        }
    ]
    
    success = PostgresQuery.execute_transaction(queries)
    
    if success:
        return {"message": "Transaction completed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Transaction failed")