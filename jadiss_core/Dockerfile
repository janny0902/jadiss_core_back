# 1. Python 베이스 이미지 선택 (경량 Alpine 기반 이미지 사용 가능)
FROM python:3.10-slim

# 2. 컨테이너 내부 작업 디렉토리 생성 및 설정
WORKDIR /app

# 3. 기본 패키지 설치 및 git 설치
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. 환경 변수로 GitHub 토큰 설정
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN}

# 5. 종속성 설치를 위한 requirements.txt 복사
COPY requirements.txt .

# 6. 종속성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip uninstall -y jadiss-finance-lib && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir cryptography && \
    pip install pymysql

# 7. 애플리케이션 코드 복사
COPY . .

ENV DATABASE_URL="mysql+pymysql://jadiss_core:jadiss_core##@jadiss-core-mysql:3306/core"

# 8. FastAPI 앱 실행 (Uvicorn으로)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
