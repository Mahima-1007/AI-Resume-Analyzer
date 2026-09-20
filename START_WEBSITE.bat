@echo off
title AI Resume Pro - Starting...
echo ============================================
echo    Starting AI Resume & Job Matcher
echo ============================================
echo.

echo [1/2] Starting Backend (FastAPI)...
start "Backend - FastAPI" cmd /k "cd /d d:\AI_IOMP\backend && .\venv\Scripts\activate && python -m uvicorn main:app --reload --port 8001"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend (React)...
start "Frontend - React" cmd /k "cd /d d:\AI_IOMP\frontend && npm run dev"

timeout /t 5 /nobreak > nul

echo.
echo ============================================
echo  DONE! Opening website in browser...
echo ============================================
echo.
echo  Website:  http://localhost:5173
echo  API Docs: http://localhost:8000/docs
echo.
timeout /t 4 /nobreak > nul
start "" "http://localhost:5173"
