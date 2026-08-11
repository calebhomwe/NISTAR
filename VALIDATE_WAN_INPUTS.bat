@echo off
title NISTAR — Validate WAN Inputs
call "%~dp0.venv\Scripts\activate.bat" 2>nul
python "%~dp0scripts\validate_wan_inputs.py"
pause
