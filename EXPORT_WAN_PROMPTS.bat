@echo off
title NISTAR — Export WAN Prompts
call "%~dp0.venv\Scripts\activate.bat" 2>nul
echo Exporting WAN 2.2 MAX prompts...
python "%~dp0scripts\export_wan_prompts.py"
echo.
echo Opening prompt folder...
explorer "%~dp0wan\prompts\episode_01"
pause
