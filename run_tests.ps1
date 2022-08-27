# pass with "./run_tests.ps1 -build"
param(
    [switch]$build = $null
)

# exit on failure
$ErrorActionPreference = "Stop"

# print lines
Set-PSDebug -Trace 1

if (-Not (Test-Path -Path virtualenv)) {
    python -m venv virtualenv
}

./virtualenv/scripts/activate

pip install nox
nox --verbose
if ($LASTEXITCODE -ne 0){
    exit $LASTEXITCODE
}

if ($build) {
    python setup.py sdist
    pip install .
}