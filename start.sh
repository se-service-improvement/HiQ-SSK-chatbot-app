#!/bin/bash

echo ""
echo "Restoring backend python packages"
echo ""
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
***REMOVED***echo "Failed to restore backend python packages"
***REMOVED***exit $?
fi

echo ""
echo "Restoring frontend npm packages"
echo ""
cd frontend
npm install
if [ $? -ne 0 ]; then
***REMOVED***echo "Failed to restore frontend npm packages"
***REMOVED***exit $?
fi

echo ""
echo "Building frontend"
echo ""
npm run build
if [ $? -ne 0 ]; then
***REMOVED***echo "Failed to build frontend"
***REMOVED***exit $?
fi

echo ""
echo "Starting backend"
echo ""
cd ..
python3 -m flask run --port=50505 --reload --debug
if [ $? -ne 0 ]; then
***REMOVED***echo "Failed to start backend"
***REMOVED***exit $?
fi