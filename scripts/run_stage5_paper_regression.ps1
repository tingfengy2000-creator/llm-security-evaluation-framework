[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root "llm-security-stage1\.venv\Scripts\python.exe"
$env:PYTHONPATH = Join-Path $Root "src"

& $Python -m unittest discover -s (Join-Path $Root "tests\stage5") -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Stage 5 regression failed." }
& $Python -m unittest discover -s (Join-Path $Root "tests\stage5_paper") -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Stage 5 Paper regression failed." }
& (Join-Path $PSScriptRoot "run_stage5_paper_smoke.ps1") -Provider mock
