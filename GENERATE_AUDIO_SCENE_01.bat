@echo off
title NISTAR — Generate Audio Scene 01
call "%~dp0.venv\Scripts\activate.bat" 2>nul
echo ============================================================
echo  NISTAR — Generate Dialogue (Scene 01)
echo  WARNING: This calls ElevenLabs API (costs credits)
echo ============================================================
echo.
set /p CONFIRM="Type YES to proceed (or anything else for dry-run): "
if /i "%CONFIRM%"=="YES" (
    python "%~dp0scripts\generate_dialogue.py" --scene SC01
) else (
    echo Running dry-run...
    python "%~dp0scripts\generate_dialogue.py" --scene SC01 --dry-run
)
pause
