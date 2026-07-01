[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet(
        "prompt_injection",
        "role_confusion",
        "encoding_obfuscation",
        "context_injection",
        "data_exfiltration",
        "tool_injection"
    )]
    [string]$Category,
    [ValidateSet("groq", "mock")]
    [string]$Provider = "groq",
    [string]$ModelName = "llama-3.1-8b-instant",
    [int]$Seed = 42,
    [double]$DelaySeconds = 2,
    [switch]$IncludeBenign
)

$ErrorActionPreference = "Stop"
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $WorkspaceRoot "llm-security-stage1\.venv\Scripts\python.exe"
$Arguments = @(
    "-m", "codeguarder.evaluation.stage5_runner",
    "--provider", $Provider,
    "--data-root", (Join-Path $WorkspaceRoot "data\stage5"),
    "--output-root", (Join-Path $WorkspaceRoot "deliverables\stage5"),
    "--per-category", "2",
    "--category", $Category,
    "--delay-seconds", "$DelaySeconds",
    "--model", $ModelName,
    "--seed", "$Seed"
)

if ($Provider -eq "groq" -and
    -not $env:GROQ_API_KEY -and
    -not $env:OPENAI_API_KEY) {
    throw "Configure a supported credential environment variable first."
}
if ($IncludeBenign) {
    $Arguments += "--include-benign"
}

$env:PYTHONPATH = Join-Path $WorkspaceRoot "src"
& $Python @Arguments
if ($LASTEXITCODE -ne 0) {
    throw "Stage 5 category run failed with exit code $LASTEXITCODE"
}
