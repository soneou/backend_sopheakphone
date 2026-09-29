@echo off
cd /d %~dp0
set FLASK_APP=wsgi.py
venv\Scripts\python.exe -m flask run
