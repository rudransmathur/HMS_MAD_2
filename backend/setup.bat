@echo off
echo ======================================================================
echo Welcome to the setup. This will set up the local virtual environment.
echo It will then install all the required Python libraries.
echo You can rerun this without any issues.
echo ----------------------------------------------------------------------

REM Check if .env folder exists
if exist ".venv" (
    echo .venv folder exists. Installing using pip...
) else (
    echo Creating .venv and installing using pip...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Install required packages
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found! Please make sure it exists.
)

REM Initalise Database
python -m scripts.seed

REM Deactivate virtual environment
call .venv\Scripts\deactivate

echo ----------------------------------------------------------------------
echo Setup complete!
echo ======================================================================
pause
