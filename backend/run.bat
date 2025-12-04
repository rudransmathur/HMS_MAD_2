@echo off
echo ======================================================================
echo Welcome to the setup. This will enable the local virtual environment.
echo Then it will run the Python application.
echo You can rerun this without any issues.
echo ----------------------------------------------------------------------

REM Check if .env folder exists
if exist ".venv" (
    echo Enabling virtual environment...
) else (
    echo No virtual environment found. Please run setup_env.bat first.
    exit /b
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Set environment variable
set ENV=development

REM Run main.py
python app.py

REM Deactivate virtual environment
deactivate

echo ----------------------------------------------------------------------
echo Done! Virtual environment deactivated.
echo ======================================================================
pause