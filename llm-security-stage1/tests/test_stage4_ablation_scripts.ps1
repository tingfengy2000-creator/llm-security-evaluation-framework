$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$MainScript = Join-Path $ProjectRoot "scripts\run_stage4_ablation.ps1"
$SafeScript = Join-Path $ProjectRoot "scripts\run_stage4_ablation_safe.ps1"

if (-not (Test-Path -LiteralPath $MainScript)) {
  throw "Missing Stage 4.1 main script: $MainScript"
}

$Tokens = $null
$Errors = $null
[System.Management.Automation.Language.Parser]::ParseFile(
  $MainScript,
  [ref]$Tokens,
  [ref]$Errors
) | Out-Null
if ($Errors.Count -ne 0) {
  throw "Stage 4.1 main script syntax error: $($Errors[0].Message)"
}

$MainText = Get-Content -LiteralPath $MainScript -Raw -Encoding UTF8
foreach ($Required in @(
  "guard_proxy_ablation.py",
  "passthrough",
  "input-only",
  "output-only",
  "full-guard",
  "prompt_hash_parity",
  "ablation_result.json",
  "ablation_summary.md",
  "original_model_output_hash",
  "input_guard_enabled",
  "output_guard_enabled",
  "upstream_called",
  "input_blocked",
  "output_blocked",
  "final_decision",
  '"invalid"',
  "invalid_reasons",
  "System.Diagnostics.ProcessStartInfo",
  "NO_PROXY",
  "GROQ_API_KEY"
)) {
  if (-not $MainText.Contains($Required)) {
    throw "run_stage4_ablation.ps1 missing contract text: $Required"
  }
}

if ($MainText.Contains('deliverables\stage4\')) {
  throw "Stage 4.1 must not write to deliverables\stage4."
}

$ExpectedOrder = @(
  '"passthrough"',
  '"input-only"',
  '"output-only"',
  '"full-guard"'
)
$LastIndex = -1
foreach ($Name in $ExpectedOrder) {
  $Index = $MainText.IndexOf($Name)
  if ($Index -le $LastIndex) {
    throw "Experiment names missing or out of order: $Name"
  }
  $LastIndex = $Index
}

$InvalidBranchStart = $MainText.IndexOf('if ($Status -eq "invalid")')
$CatchStart = $MainText.IndexOf("catch {", $InvalidBranchStart)
if ($InvalidBranchStart -lt 0 -or $CatchStart -lt 0) {
  throw "Main script is missing the invalid-status exit branch."
}
$InvalidBranch = $MainText.Substring(
  $InvalidBranchStart,
  $CatchStart - $InvalidBranchStart
)
if ($InvalidBranch.Contains("Write-Error")) {
  throw "Invalid status must not be overwritten by the failed catch path."
}

Write-Output "stage4_ablation_main_contract_test=passed"

if (-not (Test-Path -LiteralPath $SafeScript)) {
  throw "Missing Stage 4.1 safe script: $SafeScript"
}

$SafeTokens = $null
$SafeErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile(
  $SafeScript,
  [ref]$SafeTokens,
  [ref]$SafeErrors
) | Out-Null
if ($SafeErrors.Count -ne 0) {
  throw "Stage 4.1 safe script syntax error: $($SafeErrors[0].Message)"
}

$SafeText = Get-Content -LiteralPath $SafeScript -Raw -Encoding UTF8
foreach ($Required in @(
  "run_stage4_ablation.ps1",
  "promptinject.HijackHateHumans",
  "encoding.InjectBase64",
  "DelaySeconds",
  "MaxTokens"
)) {
  if (-not $SafeText.Contains($Required)) {
    throw "run_stage4_ablation_safe.ps1 missing contract text: $Required"
  }
}
if ($SafeText.Contains("soft_probe_prompt_cap")) {
  throw "Safe script must not expose prompt-cap expansion."
}
if ($SafeText -match "gsk_[A-Za-z0-9_-]{12,}") {
  throw "Safe script contains a possible Groq API key."
}

Write-Output "stage4_ablation_safe_contract_test=passed"
