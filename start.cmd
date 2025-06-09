@echo off

echo.
echo Restoring backend python packages
echo.
call py -m pip install -r requirements.txt
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

echo.***REMOVED***
echo Starting backend***REMOVED***
echo.***REMOVED***
cd ..  
start http://127.0.0.1:10505
call py -m uvicorn app:app  --port 10505 --reload
if "%errorlevel%" neq "0" (***REMOVED***
***REMOVED***echo Failed to start backend***REMOVED***
***REMOVED***exit /B %errorlevel%***REMOVED***
) 
