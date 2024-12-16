from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 연결 URL (username, password, host, dbname은 환경에 맞게 변경)
##도커 실행
#DATABASE_URL = "mysql+pymysql://jadiss_core:jadiss_core##@172.17.0.1:3308/core"  
##로컬 실행
DATABASE_URL = "mysql+pymysql://jadiss_core:jadiss_core##@jadiss-core-mysql:3306/core"
# SQLAlchemy 엔진 및 세션 구성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()
