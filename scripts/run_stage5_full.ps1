[CmdletBinding()]
param(
    [string]$ModelName = "llama-3.1-8b-instant",
    [int]$Seed = 42,
    [double]$DelaySeconds = 3
)

$ErrorActionPreference = "Stop"
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
$AttackRoot = Join-Path $WorkspaceRoot "data\stage5\attacks"
$Categories = @(
    "prompt_injection",
    "role_confusion",
    "encoding_obfuscation",
    "context_injection",
    "data_exfiltration",
    "tool_injection"
)

# A full run is invalid until every category contains at least ten rows.
foreach ($Category in $Categories) {
    $Path = Join-Path $AttackRoot "$Category.jsonl"
    $Count = @(Get-Content -LiteralPath $Path | Where-Object { $_.Trim() }).Count
    if ($Count -lt 10) {
        throw "Full run refused: $Category has $Count rows; at least 10 required."
    }
}

$Python = Join-Path $WorkspaceRoot "llm-security-stage1\.venv\Scripts\python.exe"
if (-not $env:GROQ_API_KEY -and -not $env:OPENAI_API_KEY) {
    throw "Configure a supported credential environment variable first."
}

$env:PYTHONPATH = Join-Path $WorkspaceRoot "src"
& $Python -m codeguarder.evaluation.stage5_runner `
    --provider groq `
    --data-root (Join-Path $WorkspaceRoot "data\stage5") `
    --output-root (Join-Path $WorkspaceRoot "deliverables\stage5") `
    --per-category 10 `
    --include-benign `
    --delay-seconds $DelaySeconds `
    --model $ModelName `
    --seed $Seed

if ($LASTEXITCODE -ne 0) {
    throw "Stage 5 full run failed with exit code $LASTEXITCODE"
}
