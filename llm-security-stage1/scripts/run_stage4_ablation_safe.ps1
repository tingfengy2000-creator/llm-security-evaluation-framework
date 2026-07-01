[CmdletBinding()]
param(
  [string]$ModelName = "llama-3.1-8b-instant",

  [ValidateRange(1024, 65535)]
  [int]$Port = 8011,

  [ValidateRange(1, 60)]
  [int]$DelaySeconds = 3
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$MainScript = Join-Path $ProjectRoot "scripts\run_stage4_ablation.ps1"

if (-not (Test-Path -LiteralPath $MainScript)) {
  throw "Missing Stage 4.1 main script: $MainScript"
}

# The safe entry point fixes the two smoke probes and one generation per prompt.
$ProbeSpec = (
  "promptinject.HijackHateHumans," +
  "encoding.InjectBase64"
)
$MaxTokens = 96

Write-Host "Stage 4.1 safe ablation"
Write-Host "Model: $ModelName"
Write-Host "Groups: passthrough, input-only, output-only, full-guard"
Write-Host "Probe cap: one prompt per probe (from the shared garak config)"
Write-Host "Parallelism: one (from the shared garak config)"
Write-Host "Delay between groups: $DelaySeconds seconds"

& $MainScript `
  -ModelName $ModelName `
  -ProbeSpec $ProbeSpec `
  -MaxTokens $MaxTokens `
  -Port $Port `
  -DelaySeconds $DelaySeconds

exit $LASTEXITCODE
