$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$ProxyRunner = Join-Path $ProjectRoot "scripts\run_stage4_guard_proxy.ps1"
$ScanRunner = Join-Path $ProjectRoot "scripts\run_stage4_guarded_scan.ps1"

foreach ($Path in @($ProxyRunner, $ScanRunner)) {
  if (-not (Test-Path -LiteralPath $Path)) {
    throw "缺少 Stage 4 脚本：$Path"
  }
  $Tokens = $null
  $Errors = $null
  [System.Management.Automation.Language.Parser]::ParseFile(
    $Path,
    [ref]$Tokens,
    [ref]$Errors
  ) | Out-Null
  if ($Errors.Count -ne 0) {
    throw "$Path 存在 PowerShell 语法错误：$($Errors[0].Message)"
  }
}

$ProxyText = Get-Content -LiteralPath $ProxyRunner -Raw -Encoding UTF8
$ScanText = Get-Content -LiteralPath $ScanRunner -Raw -Encoding UTF8

foreach ($Required in @(
  "GROQ_API_KEY",
  "guard_proxy.py",
  "passthrough",
  "input-only",
  "output-only",
  "guarded",
  "guard_logs.jsonl"
)) {
  if (-not $ProxyText.Contains($Required)) {
    throw "run_stage4_guard_proxy.ps1 缺少：$Required"
  }
}

foreach ($Required in @(
  "System.Diagnostics.ProcessStartInfo",
  "CreateNoWindow",
  "ProcessWindowStyle]::Hidden",
  "/health",
  "passthrough",
  "guarded",
  "OPENAICOMPATIBLE_API_KEY",
  "openai.OpenAICompatible",
  "promptinject.HijackHateHumans",
  "encoding.InjectBase64",
  "guarded_groq_scan_result.json",
  "guarded_groq_scan_summary.md",
  "guard_logs.jsonl",
  "prompt_hash_parity",
  "NO_PROXY",
  "127.0.0.1",
  "localhost",
  "OriginalNoProxy"
)) {
  if (-not $ScanText.Contains($Required)) {
    throw "run_stage4_guarded_scan.ps1 缺少：$Required"
  }
}

$InvokeGarakIndex = $ScanText.IndexOf("function Invoke-GarakProbe")
$KeyValidationIndex = $ScanText.IndexOf(
  'if ([string]::IsNullOrWhiteSpace($env:GROQ_API_KEY))'
)
$NoProxyScopeIndex = $ScanText.IndexOf('$OriginalNoProxy')
if (
  $InvokeGarakIndex -lt 0 -or
  $KeyValidationIndex -lt 0 -or
  $NoProxyScopeIndex -le $InvokeGarakIndex -or
  $NoProxyScopeIndex -ge $KeyValidationIndex
) {
  throw "NO_PROXY 必须只在 Invoke-GarakProbe 内设置，不能被 Guard Proxy 子进程继承。"
}

Write-Output "stage4_script_contract_test=passed"
