[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $WorkspaceRoot "llm-security-stage1\.venv\Scripts\python.exe"
$env:PYTHONPATH = Join-Path $WorkspaceRoot "src"

& $Python -m unittest discover `
    -s (Join-Path $WorkspaceRoot "tests\stage5") `
    -p "test_*.py" `
    -v
if ($LASTEXITCODE -ne 0) {
    throw "Stage 5 unit tests failed."
}

# Offline end-to-end regression: no remote API is called.
& (Join-Path $PSScriptRoot "run_stage5_smoke.ps1") `
    -Provider mock `
    -DelaySeconds 0
if ($LASTEXITCODE -ne 0) {
    throw "Stage 5 offline regression failed."
}
