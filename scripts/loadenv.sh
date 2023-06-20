echo "Loading azd .env file from current environment"

while IFS='=' read -r key value; do
***REMOVED***value=$(echo "$value" | sed 's/^"//' | sed 's/"$//')
***REMOVED***export "$key=$value"
done <<EOF
$(azd env get-values)
EOF

echo 'Creating Python virtual environment ".venv" in root'
python3 -m venv .venv

echo 'Installing dependencies from "requirements.txt" into virtual environment'
./.venv/bin/python -m pip install -r requirements-dev.txt
