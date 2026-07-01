[CmdletBinding()]
param(
  # 免费额度 smoke test 的默认模型；可通过 -ModelName 替换。
  [string]$ModelName = "llama-3.1-8b-instant",

  # 默认仍覆盖两类攻击，但每类只抽 1 条 prompt。
  [string]$ProbeSpec = "promptinject.HijackHateHumans,encoding.InjectBase64",

  [ValidateRange(1, 1024)]
  [int]$MaxTokens = 96
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$MainScript = Join-Path $ProjectRoot "scripts\run_stage3_groq_scan.ps1"
$SafeConfig = Join-Path $ProjectRoot "config\stage3_garak_safe.yaml"

# 安全版强制使用 GROQ_API_KEY，不接受 OPENAI_API_KEY 后备。
# YAML 将 parallel_attempts、parallel_requests、generations 都设为 1，
# 并把每个 Probe 的 prompt 上限设为 1，因此默认最多发出 2 个模型请求。
& $MainScript `
  -ModelName $ModelName `
  -ProbeSpec $ProbeSpec `
  -MaxTokens $MaxTokens `
  -ConfigPath $SafeConfig `
  -RunMode "safe" `
  -RequireGroqApiKey

exit $LASTEXITCODE
