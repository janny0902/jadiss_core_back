# 1. Python 베이스 이미지 선택 (경량 Alpine 기반 이미지 사용 가능)
FROM python:3.10-slim



# 2. 컨테이너 내부 작업 디렉토리 생성 및 설정
WORKDIR /app

# 3. 종속성 설치를 위한 requirements.txt 복사
COPY requirements.txt .

# 4. 종속성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir cryptography && \
    pip install pymysql

# 5. 애플리케이션 코드 복사
COPY . .

ENV DATABASE_URL="mysql+pymysql://jadiss_core:jadiss_core##@jadiss-core-mysql:3306/core"

# 6. FastAPI 앱 실행 (Uvicorn으로)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]







