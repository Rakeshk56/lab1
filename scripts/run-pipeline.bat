@echo off
REM =============================================================================
REM  GITHUB ACTIONS BASICS - LOCAL PIPELINE SIMULATOR (Windows)
REM =============================================================================
REM
REM  This script runs the same checks locally that GitHub Actions would run
REM  in the cloud. Use it to verify your code BEFORE pushing to GitHub.
REM
REM  The Pipeline Stages:
REM
REM   [1.FILES] --> [2.DEPS] --> [3.UNIT] --> [4.INTEG] --> [5.DONE]
REM
REM  KEY CONCEPT: If ANY stage fails, the pipeline STOPS immediately.
REM
REM  Usage: run-pipeline.bat  (from the lab-actions-basics folder)
REM
REM =============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0\.."

echo.
echo ============================================================
echo     GitHub Actions Basics - Local Pipeline Starting...
echo ============================================================
echo.
echo   Project:   %CD%
echo   Timestamp: %DATE% %TIME%
python --version 2>nul
echo.

REM ===========================================================================
REM STAGE 1: Verify Project Structure
REM ===========================================================================

echo.
echo ----------------------------------------------------------
echo   STAGE 1/5 - FILES (Verify Project Structure)
echo ----------------------------------------------------------
echo.
echo   Checking that all required files exist...

set "ALL_FOUND=1"

if exist "app\__init__.py" (echo     [OK] app\__init__.py) else (echo     [MISSING] app\__init__.py & set "ALL_FOUND=0")
if exist "app\greeter.py" (echo     [OK] app\greeter.py) else (echo     [MISSING] app\greeter.py & set "ALL_FOUND=0")
if exist "app\api.py" (echo     [OK] app\api.py) else (echo     [MISSING] app\api.py & set "ALL_FOUND=0")
if exist "tests\unit\test_greeter.py" (echo     [OK] tests\unit\test_greeter.py) else (echo     [MISSING] tests\unit\test_greeter.py & set "ALL_FOUND=0")
if exist "tests\integration\test_api.py" (echo     [OK] tests\integration\test_api.py) else (echo     [MISSING] tests\integration\test_api.py & set "ALL_FOUND=0")
if exist "requirements.txt" (echo     [OK] requirements.txt) else (echo     [MISSING] requirements.txt & set "ALL_FOUND=0")
if exist ".github\workflows\lab1-hello-world.yml" (echo     [OK] .github\workflows\lab1-hello-world.yml) else (echo     [MISSING] .github\workflows\lab1-hello-world.yml & set "ALL_FOUND=0")
if exist ".github\workflows\lab2-scheduled.yml" (echo     [OK] .github\workflows\lab2-scheduled.yml) else (echo     [MISSING] .github\workflows\lab2-scheduled.yml & set "ALL_FOUND=0")
if exist ".github\workflows\lab3-multi-trigger.yml" (echo     [OK] .github\workflows\lab3-multi-trigger.yml) else (echo     [MISSING] .github\workflows\lab3-multi-trigger.yml & set "ALL_FOUND=0")

if "%ALL_FOUND%"=="0" (
    echo.
    echo   [FAILED] Missing required files!
    echo   PIPELINE STOPPED at stage: FILES
    exit /b 1
)

echo.
echo   [PASSED] All source files present
echo.

REM ===========================================================================
REM STAGE 2: Install Dependencies
REM ===========================================================================

echo.
echo ----------------------------------------------------------
echo   STAGE 2/5 - DEPS (Install Dependencies)
echo ----------------------------------------------------------
echo.
echo   Installing Python dependencies from requirements.txt...
echo.

python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo   [FAILED] Could not install dependencies!
    echo   PIPELINE STOPPED at stage: DEPS
    exit /b 1
)

echo.
echo   [PASSED] Dependencies installed successfully
echo.

REM ===========================================================================
REM STAGE 3: Unit Tests
REM ===========================================================================

echo.
echo ----------------------------------------------------------
echo   STAGE 3/5 - UNIT TESTS (fast, isolated)
echo ----------------------------------------------------------
echo.
echo   Running unit tests against greeter.py...
echo   These test individual functions WITHOUT starting a server.
echo.

python -m pytest tests/unit/ -v --tb=short
if errorlevel 1 (
    echo.
    echo   [FAILED] Unit tests failed!
    echo   Hint: Look at the FAILED line above.
    echo         Check greeter.py -- did you change a function?
    echo   PIPELINE STOPPED at stage: UNIT TESTS
    exit /b 1
)

echo.
echo   [PASSED] Unit tests passed
echo.

REM ===========================================================================
REM STAGE 4: Integration Tests
REM ===========================================================================

echo.
echo ----------------------------------------------------------
echo   STAGE 4/5 - INTEGRATION TESTS (API endpoints)
echo ----------------------------------------------------------
echo.
echo   Running integration tests against the API endpoints...
echo   These test the full request/response cycle.
echo.

python -m pytest tests/integration/ -v --tb=short
if errorlevel 1 (
    echo.
    echo   [FAILED] Integration tests failed!
    echo   Hint: The API endpoint is broken.
    echo         Check api.py -- is the routing or response correct?
    echo   PIPELINE STOPPED at stage: INTEGRATION TESTS
    exit /b 1
)

echo.
echo   [PASSED] Integration tests passed
echo.

REM ===========================================================================
REM STAGE 5: Summary
REM ===========================================================================

echo.
echo ============================================================
echo.
echo        ALL CHECKS PASSED - READY TO PUSH!
echo.
echo ============================================================
echo.
echo   Pipeline Summary:
echo     [PASSED] Files       - Project structure verified
echo     [PASSED] Deps        - Dependencies installed
echo     [PASSED] Unit Tests  - All greeter functions working correctly
echo     [PASSED] Int. Tests  - All API endpoints responding correctly
echo.
echo   Next Steps:
echo     1. Push to GitHub:  git add . ^&^& git commit -m "feat: add greeter app" ^&^& git push
echo     2. Watch Actions:   Go to GitHub ^> Actions tab
echo     3. See workflows:   lab1-hello-world, lab2-scheduled, lab3-multi-trigger
echo.

endlocal
