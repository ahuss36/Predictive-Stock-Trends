@echo off

set "venv_path=.venv" REM Set the desired virtual environment path/name

if not exist %venv_path% (
    echo Creating virtual environment...
    python3.11 -m venv %venv_path%
    echo Virtual environment created at %venv_path%
) else (
    echo Virtual environment already exists at %venv_path%
)


.\.venv\Scripts\python.exe -m pip install -r requirements.txt

.\.venv\Scripts\python.exe .\Project\stocks\manage.py makemigrations stocks 
.\.venv\Scripts\python.exe .\Project\stocks\manage.py migrate

.\.venv\Scripts\python.exe .\Project\stocks\manage.py runserver

pause