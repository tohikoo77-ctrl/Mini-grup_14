@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Changing to src directory...
cd src

echo Starting Django development server...
python manage.py runserver

pause