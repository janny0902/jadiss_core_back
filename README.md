# jadiss_core_back

## 프로젝트 개요
- jadiss(자디스) 서비스의 핵심 백엔드 모듈
- FastAPI 기반의 Python 백엔드 구조

## 주요 폴더 및 파일
- jadiss_core/: 핵심 백엔드 소스 코드
- _Fast API_가이드.pptx: FastAPI 사용 가이드 문서

## 실행 방법
1. Python 3.x 설치
2. 의존성 설치: `pip install -r requirements.txt` (requirements.txt 필요시)
3. 서버 실행: `uvicorn jadiss_core.main:app --reload` (main.py 기준)

## 특징
- FastAPI 기반의 RESTful API 서버
- 서비스의 핵심 로직 담당

## 참고
- 실제 서비스 환경에서는 환경 변수 및 보안 설정 필요
