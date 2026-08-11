@echo off
title NISTAR — Export for DaVinci Resolve
call "%~dp0.venv\Scripts\activate.bat" 2>nul
echo ============================================================
echo  NISTAR — Export for DaVinci Resolve
echo ============================================================
echo.
python "%~dp0scripts\export_resolve.py"
echo.
echo Opening DaVinci folder...
explorer "%~dp0davinci\episode_01"
pause
