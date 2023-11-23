@echo off

.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\Project\stocks\manage.py runserver

pause