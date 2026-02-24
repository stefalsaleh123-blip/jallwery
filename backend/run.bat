@echo off
echo ========================================
echo Jewelry E-commerce Backend Setup
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    python -m pip install -r requirements.txt
)
echo.

echo Step 2: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file. Please edit it with your Gemini API key.
)
echo.

echo Step 3: Running database seeder...
python seeder.py
echo.

echo Step 4: Starting FastAPI server...
echo Server will run at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
