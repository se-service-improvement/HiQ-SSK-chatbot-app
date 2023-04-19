@echo off

echo.
echo Restoring backend python packages
echo.
call python -m pip install -r requirements.txt
if "%errorlevel%" neq "0" (
***REMOVED***echo Failed to restore backend python packages
***REMOVED***exit /B %errorlevel%
)

echo.
echo Restoring frontend npm packages
echo.
cd frontend
call npm install
if "%errorlevel%" neq "0" (
***REMOVED***echo Failed to restore frontend npm packages
***REMOVED***exit /B %errorlevel%
)

echo.
echo Building frontend
echo.
call npm run build
if "%errorlevel%" neq "0" (
***REMOVED***echo Failed to build frontend
***REMOVED***exit /B %errorlevel%
)

echo.
echo Starting backend
echo.
cd ..
start http://127.0.0.1:5000
call python ./app.py
if "%errorlevel%" neq "0" (
***REMOVED***echo Failed to start backend
***REMOVED***exit /B %errorlevel%
)
