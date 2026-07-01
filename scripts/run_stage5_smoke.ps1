[CmdletBinding()]
param(
    [ValidateSet("groq", "mock")]
    [string]$Provider = "groq",
    [string]$ModelName = "llama-3.1-8b-instant",
    [int]$Seed = 42,
    [double]$DelaySeconds = 2
)

$ErrorActionPreference = "Stop"
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $WorkspaceRoot "llm-security-stage1\.venv\Scripts\python.exe"
$DataRoot = Join-Path $WorkspaceRoot "data\stage5"
$OutputRoot = Join-Path $WorkspaceRoot "deliverables\stage5"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python runtime not found: $Python"
}
if ($Provider -eq "groq" -and
    -not $env:GROQ_API_KEY -and
    -not $env:OPENAI_API_KEY) {
    throw "Configure a supported credential environment variable first."
}

# The runner is sequential: one request at a time, with a pause between samples.
$env:PYTHONPATH = Join-Path $WorkspaceRoot "src"
& $Python -m codeguarder.evaluation.stage5_runner `
    --provider $Provider `
    --data-root $DataRoot `
    --output-root $OutputRoot `
    --per-category 2 `
    --include-benign `
    --delay-seconds $DelaySeconds `
    --model $ModelName `
    --seed $Seed

if ($LASTEXITCODE -ne 0) {
    throw "Stage 5 smoke run failed with exit code $LASTEXITCODE"
}
