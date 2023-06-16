#!/bin/bash

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
python3 -m flask run --port=5000 --host=127.0.0.1 --reload --debug
if [ $? -ne 0 ]; then
***REMOVED***echo "Failed to start backend"
***REMOVED***exit $?
fi
