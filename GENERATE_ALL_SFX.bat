@echo off
title NISTAR — Generate All SFX
call "%~dp0.venv\Scripts\activate.bat" 2>nul
echo ============================================================
echo  NISTAR — Generate ALL Sound Effects
echo  WARNING: This calls ElevenLabs API (costs credits)
echo ============================================================
echo.
set /p CONFIRM="Type YES to proceed (or anything else for dry-run): "
if /i "%CONFIRM%"=="YES" (
    python "%~dp0scripts\generate_sfx.py"
) else (
    echo Running dry-run...
    python "%~dp0scripts\generate_sfx.py" --dry-run
)
pause
