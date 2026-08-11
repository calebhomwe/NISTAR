@echo off
title NISTAR Production Pipeline — Setup
echo ============================================================
echo  NISTAR PRODUCTION PIPELINE — SETUP
echo  Episode 1: PRIDE — "I Always Make It"
echo ============================================================
echo.

:: Create virtual environment
echo [1/7] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+
    pause
    exit /b 1
)

:: Activate and install
echo [2/7] Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: pip install failed
    pause
    exit /b 1
)

:: Unpack audio package
echo [3/7] Unpacking audio source package...
python scripts\unpack_audio_package.py
echo.

:: Validate source
echo [4/7] Validating audio source...
python scripts\validate_audio_source.py
echo.

:: Build manifests
echo [5/7] Building shot manifest...
python scripts\build_wan_manifest.py
echo.

:: Export prompts
echo [6/7] Exporting WAN prompts...
python scripts\export_wan_prompts.py
echo.

:: Run tests
echo [7/7] Running tests...
python -m pytest tests/ -v --tb=short 2>nul
if errorlevel 1 (
    echo.
    echo Running tests individually...
    python tests\test_naming.py
    python tests\test_wan_manifest.py
    python tests\test_validation.py
    python tests\test_audio_parser.py
    python tests\test_continuity.py
    python tests\test_dry_run.py
)

echo.
echo ============================================================
echo  SETUP COMPLETE
echo ============================================================
echo.
echo Next steps:
echo   1. Copy .env.example to .env and add your ELEVENLABS_API_KEY
echo   2. Add approved character stills to stills/characters/
echo   3. Run PREPARE_WAN_SHOTS.bat to create input frames
echo   4. Open wan/prompts/episode_01/ for paste-ready WAN prompts
echo.
pause
