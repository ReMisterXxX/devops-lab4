@echo off
chcp 65001 >nul
cd /d %~dp0
set APP_PORT=5080
if exist wyniki rmdir /s /q wyniki
mkdir wyniki
docker rm -f lab4_single >nul 2>&1
docker compose down -v >nul 2>&1
echo Uruchamianie Lab4...
echo [01_docker_build]
echo $ docker build -t lab4-app:1.0.0 . >> wyniki\01_docker_build.txt
docker build -t lab4-app:1.0.0 . >> wyniki\01_docker_build.txt 2>&1
echo.>> wyniki\01_docker_build.txt
echo [02_docker_run]
echo $ docker run -d --name lab4_single -p 5050:5000 -e APP_ENV=single-container lab4-app:1.0.0 >> wyniki\02_docker_run.txt
docker run -d --name lab4_single -p 5050:5000 -e APP_ENV=single-container lab4-app:1.0.0 >> wyniki\02_docker_run.txt 2>&1
echo.>> wyniki\02_docker_run.txt
timeout /t 5 /nobreak >nul
echo $ docker ps --filter name=lab4_single >> wyniki\02_docker_run.txt
docker ps --filter name=lab4_single >> wyniki\02_docker_run.txt 2>&1
echo.>> wyniki\02_docker_run.txt
echo $ curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5050/ >> wyniki\02_docker_run.txt
curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5050/ >> wyniki\02_docker_run.txt 2>&1
echo.>> wyniki\02_docker_run.txt
echo $ curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5050/health >> wyniki\02_docker_run.txt
curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5050/health >> wyniki\02_docker_run.txt 2>&1
echo.>> wyniki\02_docker_run.txt
echo $ docker rm -f lab4_single >> wyniki\02_docker_run.txt
docker rm -f lab4_single >> wyniki\02_docker_run.txt 2>&1
echo.>> wyniki\02_docker_run.txt
echo [03_compose_up]
echo $ docker compose up -d --build --wait >> wyniki\03_compose_up.txt
docker compose up -d --build --wait >> wyniki\03_compose_up.txt 2>&1
echo.>> wyniki\03_compose_up.txt
echo $ docker compose ps >> wyniki\03_compose_up.txt
docker compose ps >> wyniki\03_compose_up.txt 2>&1
echo.>> wyniki\03_compose_up.txt
echo [04_verify]
echo $ curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5080/ >> wyniki\04_verify.txt
curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5080/ >> wyniki\04_verify.txt 2>&1
echo.>> wyniki\04_verify.txt
echo $ curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5080/health >> wyniki\04_verify.txt
curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5080/health >> wyniki\04_verify.txt 2>&1
echo.>> wyniki\04_verify.txt
echo $ curl.exe -s -w "\nHTTP %%{http_code}\n" -X POST -H "Content-Type: application/json" -d "{\"title\":\"Przygotowac sprawozdanie\"}" http://localhost:5080/tasks >> wyniki\04_verify.txt
curl.exe -s -w "\nHTTP %%{http_code}\n" -X POST -H "Content-Type: application/json" -d "{\"title\":\"Przygotowac sprawozdanie\"}" http://localhost:5080/tasks >> wyniki\04_verify.txt 2>&1
echo.>> wyniki\04_verify.txt
echo $ curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5080/tasks >> wyniki\04_verify.txt
curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:5080/tasks >> wyniki\04_verify.txt 2>&1
echo.>> wyniki\04_verify.txt
echo [05_logs]
echo $ docker compose logs app >> wyniki\05_logs.txt
docker compose logs app >> wyniki\05_logs.txt 2>&1
echo.>> wyniki\05_logs.txt
echo Gotowe.
timeout /t 10
