@echo off
title NISTAR — Build Animatic Package
call "%~dp0.venv\Scripts\activate.bat" 2>nul
echo ============================================================
echo  NISTAR — Build Animatic Assembly Package
echo ============================================================
echo.
python "%~dp0scripts\build_animatic_manifest.py"
echo.
echo Opening DaVinci export folder...
explorer "%~dp0davinci\episode_01"
pause
