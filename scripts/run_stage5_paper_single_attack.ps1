[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("A1", "A2", "A3", "A4", "A5", "A6")]
    [string]$AttackId,
    [ValidateSet("groq", "mock")]
    [string]$Provider = "mock",
    [string]$ModelName = "llama-3.1-8b-instant",
    [int]$Seed = 42
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root "llm-security-stage1\.venv\Scripts\python.exe"
$env:PYTHONPATH = Join-Path $Root "src"
& $Python -m codeguarder.stage5_paper.evaluation.stage5_runner `
    --provider $Provider `
    --data-root (Join-Path $Root "data\stage5_paper") `
    --output-root (Join-Path $Root "deliverables\stage5_paper") `
    --attack-id $AttackId `
    --model $ModelName `
    --seed $Seed
if ($LASTEXITCODE -ne 0) { throw "Stage 5 Paper single-attack run failed." }
