#!/bin/bash
echo "FastAPI 애플리케이션 컨테이너 시작 중..."
docker-compose up -d --build -no-cache
echo ""
echo "컨테이너가 시작되었습니다."
echo "API는 http://localhost:8090 에서 접근 가능합니다."
echo "Swagger 문서는 http://localhost:8090/docs 에서 확인할 수 있습니다."
echo ""
echo "컨테이너 로그를 보려면 'docker logs jadiss-core-api -f' 명령어를 실행하세요."
echo "컨테이너를 중지하려면 'docker-compose down' 명령어를 실행하세요."