"""
PostgreSQL 데이터베이스에 직접 쿼리를 실행하기 위한 유틸리티 모듈
"""
from sqlalchemy import text
from typing import List, Dict, Any, Optional, Union
from . import engine, SessionLocal

class PostgresQuery:
    """PostgreSQL 데이터베이스에 직접 쿼리를 실행하기 위한 클래스
    
    이 클래스는 ORM을 사용하지 않고 직접 SQL 쿼리를 실행할 수 있는 메서드를 제공합니다.
    """
    
    @staticmethod
    def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """SQL 쿼리를 실행하고 결과를 반환합니다.
        
        Args:
            query (str): 실행할 SQL 쿼리 문자열
            params (Dict[str, Any], optional): 쿼리에 바인딩할 파라미터. 기본값은 None.
            
        Returns:
            List[Dict[str, Any]]: 쿼리 결과를 딕셔너리 리스트로 반환
            
        Example:
            >>> result = PostgresQuery.execute_query("SELECT * FROM users WHERE age > :age", {"age": 18})
        """
        with SessionLocal() as session:
            result = session.execute(text(query), params or {})
            return [dict(row._mapping) for row in result]
    
    @staticmethod
    def execute_update(query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """INSERT, UPDATE, DELETE 등의 변경 쿼리를 실행하고 영향받은 행 수를 반환합니다.
        
        Args:
            query (str): 실행할 SQL 쿼리 문자열
            params (Dict[str, Any], optional): 쿼리에 바인딩할 파라미터. 기본값은 None.
            
        Returns:
            int: 영향받은 행의 수
            
        Example:
            >>> affected_rows = PostgresQuery.execute_update(
            ...     "UPDATE users SET name = :name WHERE id = :id", 
            ...     {"name": "New Name", "id": 1}
            ... )
        """
        with SessionLocal() as session:
            result = session.execute(text(query), params or {})
            session.commit()
            return result.rowcount
    
    @staticmethod
    def execute_scalar(query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """단일 값을 반환하는 쿼리를 실행합니다.
        
        Args:
            query (str): 실행할 SQL 쿼리 문자열
            params (Dict[str, Any], optional): 쿼리에 바인딩할 파라미터. 기본값은 None.
            
        Returns:
            Any: 쿼리 결과의 첫 번째 행, 첫 번째 열 값
            
        Example:
            >>> count = PostgresQuery.execute_scalar("SELECT COUNT(*) FROM users")
        """
        with SessionLocal() as session:
            result = session.execute(text(query), params or {})
            first_row = result.first()
            return first_row[0] if first_row else None
    
    @staticmethod
    def execute_transaction(queries: List[Dict[str, Union[str, Dict[str, Any]]]]) -> bool:
        """여러 쿼리를 트랜잭션으로 실행합니다.
        
        Args:
            queries (List[Dict[str, Union[str, Dict[str, Any]]]]): 실행할 쿼리와 파라미터의 리스트
                각 항목은 {'query': 'SQL 쿼리', 'params': {파라미터 딕셔너리}} 형식이어야 함
                
        Returns:
            bool: 트랜잭션 성공 여부
            
        Example:
            >>> success = PostgresQuery.execute_transaction([
            ...     {
            ...         'query': "INSERT INTO users (name, age) VALUES (:name, :age)",
            ...         'params': {'name': 'John', 'age': 30}
            ...     },
            ...     {
            ...         'query': "UPDATE items SET price = :price WHERE id = :id",
            ...         'params': {'price': 1000, 'id': 1}
            ...     }
            ... ])
        """
        with SessionLocal() as session:
            try:
                for query_info in queries:
                    query = query_info.get('query', '')
                    params = query_info.get('params', {})
                    session.execute(text(query), params)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(f"트랜잭션 실행 중 오류 발생: {e}")
                return False