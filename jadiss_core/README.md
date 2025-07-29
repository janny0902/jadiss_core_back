# Jadiss Core Back

외부 PostgreSQL 데이터베이스를 사용하는 FastAPI 애플리케이션입니다.

## 시작하기

### 필수 조건

- Docker 및 Docker Compose가 설치되어 있어야 합니다.
- PostgreSQL 데이터베이스가 이미 실행 중이어야 합니다.
- Windows 또는 Linux/Mac 환경에서 실행 가능합니다.

### 실행 방법

#### Windows

```bash
start.bat
```

#### Linux/Mac

```bash
chmod +x start.sh
./start.sh
```

## 접속 정보

- API 서버: http://localhost:8090
- Swagger 문서: http://localhost:8090/docs
- PostgreSQL 데이터베이스 연결 정보:
  - URL: jdbc:postgresql://localhost:5432/core
  - 사용자: jadiss_core

## 직접 SQL 쿼리 사용하기

API 서버에는 직접 SQL 쿼리를 실행할 수 있는 엔드포인트가 포함되어 있습니다.
자세한 내용은 Swagger 문서를 참조하세요.

### 예제 엔드포인트

- `GET /raw-query/users`: 모든 사용자 조회
- `GET /raw-query/users/{user_id}`: 특정 ID의 사용자 조회
- `POST /raw-query/users`: 새 사용자 생성
- `PUT /raw-query/users/{user_id}`: 사용자 정보 업데이트
- `DELETE /raw-query/users/{user_id}`: 사용자 삭제

## 컨테이너 관리

- 컨테이너 로그 보기: `docker logs jadiss-core-api -f`
- 컨테이너 중지: `docker-compose down`
- 컨테이너 재시작: `docker-compose restart`