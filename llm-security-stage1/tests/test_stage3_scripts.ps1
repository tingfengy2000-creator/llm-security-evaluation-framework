$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$ScriptPath = Join-Path $ProjectRoot "scripts\run_stage3_groq_scan.ps1"
$ScriptText = Get-Content -LiteralPath $ScriptPath -Raw -Encoding UTF8

if ($ScriptText -notmatch '"--generator_option_file"') {
  throw "Stage 3 脚本必须使用 --generator_option_file，避免 PowerShell 5.1 破坏内联 JSON。"
}

if ($ScriptText -match '"--generator_options"') {
  throw "Stage 3 脚本不应继续把 JSON 通过 --generator_options 传给原生 garak.exe。"
}

if ([regex]::Matches($ScriptText, [regex]::Escape('- 模型：``$ModelName``')).Count -lt 2) {
  throw "失败摘要必须保留 Markdown 反引号，同时插入实际 ModelName。"
}

if (-not $ScriptText.Contains('- 日志：``$ConsoleLog``')) {
  throw "失败摘要必须保留 Markdown 反引号，同时插入实际 ConsoleLog。"
}

if ([regex]::Matches($ScriptText, [regex]::Escape('- 模式：``$RunMode``')).Count -lt 2) {
  throw "失败摘要必须保留 Markdown 反引号，同时插入实际 RunMode。"
}

if (-not $ScriptText.Contains('$NativeErrorActionPreference = $ErrorActionPreference')) {
  throw "运行原生 garak 前必须保存 ErrorActionPreference。"
}

if (-not $ScriptText.Contains('$ErrorActionPreference = "Continue"')) {
  throw "运行原生 garak 时必须允许 PowerShell 5.1 的普通 stderr 通过。"
}

if (-not $ScriptText.Contains('$ErrorActionPreference = $NativeErrorActionPreference')) {
  throw "运行原生 garak 后必须恢复 ErrorActionPreference。"
}

if (-not $ScriptText.Contains('$_ -is [System.Management.Automation.ErrorRecord]')) {
  throw "必须把 PowerShell 5.1 的原生 stderr ErrorRecord 转回普通日志文本。"
}

if (-not $ScriptText.Contains('function Read-GarakAttemptMetrics')) {
  throw "聚合 ASR 必须按完成的 Attempt 去重，不能直接混合多个 Detector 记录。"
}

foreach ($Field in @(
  "attempt_count",
  "attack_successful_attempts",
  "detector_evaluations",
  "detector_hit_rate_percent"
)) {
  if (-not $ScriptText.Contains($Field)) {
    throw "聚合结果缺少口径字段：$Field"
  }
}

if (-not $ScriptText.Contains('groq = [ordered]@{')) {
  throw "Generator option file 必须使用 groq 命名空间。"
}

if (-not $ScriptText.Contains('GroqChat = [ordered]@{')) {
  throw "Generator option file 必须使用 GroqChat 类级配置。"
}

Write-Output "stage3_argument_transport_test=passed"
