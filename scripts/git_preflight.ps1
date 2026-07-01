[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root "llm-security-stage1\.venv\Scripts\python.exe"
$env:PYTHONPATH = Join-Path $Root "src"

& $Python -m unittest discover -s (Join-Path $Root "tests\stage5") -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Stage 5 tests failed." }
& $Python -m unittest discover -s (Join-Path $Root "tests\stage5_paper") -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Stage 5 Paper tests failed." }

$secretPattern = "gsk_[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}"
$secretFiles = rg -l -i $secretPattern $Root `
    -g "!.git/**" -g "!**/.venv/**" -g "!**/xdg_*/**" 2>$null
if ($LASTEXITCODE -eq 0 -and $secretFiles) {
    throw "Credential-like values found in candidate files: $($secretFiles -join ', ')"
}

$large = Get-ChildItem -Recurse -File $Root |
    Where-Object {
        $_.Length -gt 10MB -and
        $_.FullName -notlike "*\.venv\*" -and
        $_.FullName -notlike "*\.git\*"
    }
Write-Output "large_file_count=$($large.Count)"
Write-Output "git_preflight=passed"
exit 0
