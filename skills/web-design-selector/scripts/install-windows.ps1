$ErrorActionPreference = "Stop"

$bootstrap = Join-Path $PSScriptRoot "bootstrap.py"
$python = Get-Command python -ErrorAction SilentlyContinue

if ($python) {
    & $python.Source $bootstrap @args
    exit $LASTEXITCODE
}

$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($pyLauncher) {
    & $pyLauncher.Source -3 $bootstrap @args
    exit $LASTEXITCODE
}

throw "Python 3 is required. Run this script from the Codex integrated terminal where the bundled Python runtime is available."
