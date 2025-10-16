@echo off
REM --- C:\analyzer 폴더로 직접 이동합니다 ---
cd /d C:\analyzer

echo Starting the analysis server in C:\analyzer...
REM --- 파이썬 웹 서버를 실행합니다 ---
python app.py

echo Starting web browser...
REM --- 웹 브라우저를 열어 분석기 페이지에 접속합니다 ---
start http://127.0.0.1:5001

