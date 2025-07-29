@echo off
echo FastAPI application container starting...
docker-compose down
docker-compose build --no-cache
docker-compose up -d
echo.
echo Container started successfully.
echo API is accessible at http://localhost:8090
echo Swagger documentation is available at http://localhost:8090/docs
echo.
echo To view container logs, run 'docker logs jadiss-core-api -f'
echo To stop the container, run 'docker-compose down'