# Only load env from azd if azd command and azd environment exist
if (-not (Get-Command azd -ErrorAction SilentlyContinue)) {
  Write-Host "azd command not found, skipping .env file load"
} else {
  $output = azd env list
  if (!($output -like "*true*")) {
***REMOVED***Write-Output "No azd environments found, skipping .env file load"
  } else {
***REMOVED***Write-Host "Loading azd .env file from current environment"
***REMOVED***$output = azd env get-values
***REMOVED***foreach ($line in $output) {
***REMOVED***  if (!$line.Contains('=')) {
***REMOVED***continue
  ***REMOVED***

***REMOVED***  $name, $value = $line.Split("=")
***REMOVED***  $value = $value -replace '^\"|\"$'
***REMOVED***  [Environment]::SetEnvironmentVariable($name, $value)
***REMOVED***
  }
}

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
  # fallback to python3 if python not found
  $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

Write-Host 'Creating Python virtual environment ".venv" in root'
Start-Process -FilePath ($pythonCmd).Source -ArgumentList "-m venv ./.venv" -Wait -NoNewWindow

$venvPythonPath = "./.venv/scripts/python.exe"
if (Test-Path -Path "/usr") {
  # fallback to Linux venv path
  $venvPythonPath = "./.venv/bin/python"
}

Write-Host 'Installing dependencies from "requirements.txt" into virtual environment'
Start-Process -FilePath $venvPythonPath -ArgumentList "-m pip install -r ./requirements-dev.txt" -Wait -NoNewWindow
