@echo off
title NISTAR — Prepare WAN Shots
call "%~dp0.venv\Scripts\activate.bat" 2>nul
echo ============================================================
echo  NISTAR — Prepare WAN 2.2 MAX Shots
echo ============================================================
echo.

echo [1/4] Validating approved stills...
python "%~dp0scripts\validate_wan_inputs.py"
echo.

echo [2/4] Creating 832x480 input frames...
python "%~dp0scripts\prepare_wan_inputs.py"
echo.

echo [3/4] Exporting prompt files...
python "%~dp0scripts\export_wan_prompts.py"
echo.

echo [4/4] Opening WAN prompt folder...
explorer "%~dp0wan\prompts\episode_01"

echo.
echo ============================================================
echo  WAN SHOTS PREPARED
echo  Paste prompts from wan\prompts\episode_01\ into your WAN interface
echo  No paid generation started automatically.
echo ============================================================
pause
