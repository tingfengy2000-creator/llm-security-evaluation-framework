[CmdletBinding()]
param(
    [ValidateSet("groq", "mock")]
    [string]$Provider = "groq",
    [string]$ModelName = "llama-3.1-8b-instant",
    [int]$Seed = 42
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root "llm-security-stage1\.venv\Scripts\python.exe"
if ($Provider -eq "groq" -and -not $env:GROQ_API_KEY -and -not $env:OPENAI_API_KEY) {
    throw "Configure a supported credential environment variable first."
}
$env:PYTHONPATH = Join-Path $Root "src"
& $Python -m codeguarder.stage5_paper.evaluation.stage5_runner `
    --provider $Provider `
    --data-root (Join-Path $Root "data\stage5_paper") `
    --output-root (Join-Path $Root "deliverables\stage5_paper") `
    --include-benign `
    --model $ModelName `
    --seed $Seed
if ($LASTEXITCODE -ne 0) { throw "Stage 5 Paper smoke failed." }
