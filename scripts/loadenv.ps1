Write-Host "Loading azd .env file from current environment"

$output = azd env get-values

foreach ($line in $output) {
  if (!$line.Contains('=')) {
***REMOVED***continue
  }

  $name, $value = $line.Split("=")
  $value = $value -replace '^\"|\"$'
  [Environment]::SetEnvironmentVariable($name, $value)
}
