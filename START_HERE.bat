@echo off
title NISTAR — Start Here
echo ============================================================
echo  NISTAR PRODUCTION PIPELINE
echo  Opening project files...
echo ============================================================

:: Open README
start "" notepad "%~dp0README.md"

:: Open WAN settings
start "" notepad "%~dp0config\wan22_max.yaml"

:: Open voice settings
start "" notepad "%~dp0config\voices.yaml"

:: Open shot manifest (if built)
if exist "%~dp0wan\manifests\episode_01_shots.md" (
    start "" notepad "%~dp0wan\manifests\episode_01_shots.md"
) else (
    echo Shot manifest not built yet. Run SETUP.bat first.
)

:: Open project folder
explorer "%~dp0"

echo.
echo Opened: README, WAN config, voices, shot manifest, project folder
pause
