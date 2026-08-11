@echo off
title NISTAR — Validate
call "%~dp0.venv\Scripts\activate.bat" 2>nul
echo ============================================================
echo  NISTAR — Full Validation
echo ============================================================
echo.

echo --- WAN Input Validation ---
python "%~dp0scripts\validate_wan_inputs.py"
echo.

echo --- Audio Source Validation ---
python "%~dp0scripts\validate_audio_source.py"
echo.

echo --- Generation Load Estimate ---
python "%~dp0scripts\estimate_generation_load.py"
echo.

pause
