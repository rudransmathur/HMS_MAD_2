@echo off
echo ======================================================================
echo Welcome to the setup. This will set up the local virtual environment.
echo It will then install all the required Python libraries.
echo You can rerun this without any issues.
echo ----------------------------------------------------------------------

REM Check if .env folder exists
if exist ".env" (
    echo .env folder exists. Installing using pip...
) else (
    echo Creating .env and installing using pip...
    python -m venv .env
)

REM Activate virtual environment
call .env\Scripts\activate

REM Install required packages
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found! Please make sure it exists.
)

REM Initalise Database
python -m scripts.seed

REM Deactivate virtual environment
deactivate

echo ----------------------------------------------------------------------
echo Setup complete!
echo ======================================================================
pause
