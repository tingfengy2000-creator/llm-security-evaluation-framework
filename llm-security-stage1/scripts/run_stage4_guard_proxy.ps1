[CmdletBinding()]
param(
  [ValidateSet("passthrough", "input-only", "output-only", "guarded")]
  [string]$Mode = "guarded",

  [ValidateRange(1024, 65535)]
  [int]$Port = 8010,

  [string]$ModelName = "llama-3.1-8b-instant",

  [string]$LogPath = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$WorkspaceRoot = Split-Path -Parent $ProjectRoot
$DeliverableRoot = Join-Path $WorkspaceRoot "deliverables\stage4"
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$ProxyScript = Join-Path $ProjectRoot "scripts\guard_proxy.py"

if ([string]::IsNullOrWhiteSpace($LogPath)) {
  $LogPath = Join-Path $DeliverableRoot "guard_logs.jsonl"
}

if ([string]::IsNullOrWhiteSpace($env:GROQ_API_KEY)) {
  throw "未检测到 GROQ_API_KEY。Guard Proxy 不会从文件读取或保存 API Key。"
}
if (-not (Test-Path -LiteralPath $Python)) {
  throw "未找到虚拟环境 Python：$Python"
}
if (-not (Test-Path -LiteralPath $ProxyScript)) {
  throw "未找到 Guard Proxy：$ProxyScript"
}

New-Item -ItemType Directory -Force -Path $DeliverableRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null

$env:PYTHONIOENCODING = "utf-8"

Write-Host "Stage 4 Guard Proxy"
Write-Host "模式：$Mode"
Write-Host "本地地址：http://127.0.0.1:$Port/v1"
Write-Host "上游：https://api.groq.com/openai/v1"
Write-Host "模型：$ModelName"
Write-Host "审计日志：$LogPath"
Write-Host "API Key：仅从 GROQ_API_KEY 读取，值不会输出"

& $Python `
  $ProxyScript `
  --host "127.0.0.1" `
  --port $Port `
  --mode $Mode `
  --log-path $LogPath `
  --model $ModelName

exit $LASTEXITCODE
