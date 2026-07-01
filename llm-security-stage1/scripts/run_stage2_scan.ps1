$ErrorActionPreference = "Stop"

$ProjectRoot = "D:\llmProject\llm-security-stage1"
$DeliverableRoot = "D:\llmProject\deliverables\stage2"
$Garak = Join-Path $ProjectRoot ".venv\Scripts\garak.exe"
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$ServerScript = Join-Path $ProjectRoot "scripts\mock_openai_compatible_api.py"
$GarakConfig = Join-Path $ProjectRoot "config\stage2_garak_smoke.yaml"
$ApiLog = Join-Path $DeliverableRoot "api_requests.jsonl"

New-Item -ItemType Directory -Force -Path $DeliverableRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $DeliverableRoot "screenshots") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $DeliverableRoot "xdg_config") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $DeliverableRoot "xdg_data") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $DeliverableRoot "xdg_cache") | Out-Null

$env:PYTHONIOENCODING = "utf-8"
$env:XDG_CONFIG_HOME = Join-Path $DeliverableRoot "xdg_config"
$env:XDG_DATA_HOME = Join-Path $DeliverableRoot "xdg_data"
$env:XDG_CACHE_HOME = Join-Path $DeliverableRoot "xdg_cache"
$env:OPENAICOMPATIBLE_API_KEY = "stage2-local-mock-key"

if (Test-Path -LiteralPath $ApiLog) {
  Remove-Item -LiteralPath $ApiLog
}
Get-ChildItem -LiteralPath $DeliverableRoot -Filter "stage2_*.report.*" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -LiteralPath $DeliverableRoot -Filter "stage2_*.hitlog.jsonl" -ErrorAction SilentlyContinue | Remove-Item -Force

$server = Start-Process -FilePath $Python -ArgumentList @($ServerScript, "--host", "127.0.0.1", "--port", "8000", "--log-path", $ApiLog) -PassThru -WindowStyle Hidden
try {
  Start-Sleep -Seconds 2

  & $Garak --version

  & $Garak `
    --config $GarakConfig `
    --target_type openai.OpenAICompatible `
    --target_name stage2-vulnerable `
    --generator_options '{"uri":"http://127.0.0.1:8000/v1/","temperature":0.0,"max_tokens":200}' `
    --probes promptinject.HijackHateHumans `
    --generations 1 `
    --seed 42 `
    --report_prefix (Join-Path $DeliverableRoot "stage2_vulnerable_promptinject") `
    --narrow_output

  & $Garak `
    --config $GarakConfig `
    --target_type openai.OpenAICompatible `
    --target_name stage2-guarded `
    --generator_options '{"uri":"http://127.0.0.1:8000/v1/","temperature":0.0,"max_tokens":200}' `
    --probes promptinject.HijackHateHumans `
    --generations 1 `
    --seed 42 `
    --report_prefix (Join-Path $DeliverableRoot "stage2_guarded_promptinject") `
    --narrow_output

  & $Garak `
    --config $GarakConfig `
    --target_type openai.OpenAICompatible `
    --target_name stage2-vulnerable `
    --generator_options '{"uri":"http://127.0.0.1:8000/v1/","temperature":0.0,"max_tokens":200}' `
    --probes encoding.InjectBase64 `
    --generations 1 `
    --seed 42 `
    --report_prefix (Join-Path $DeliverableRoot "stage2_vulnerable_base64") `
    --narrow_output

  & $Garak `
    --config $GarakConfig `
    --target_type openai.OpenAICompatible `
    --target_name stage2-guarded `
    --generator_options '{"uri":"http://127.0.0.1:8000/v1/","temperature":0.0,"max_tokens":200}' `
    --probes encoding.InjectBase64 `
    --generations 1 `
    --seed 42 `
    --report_prefix (Join-Path $DeliverableRoot "stage2_guarded_base64") `
    --narrow_output
}
finally {
  if ($server -and -not $server.HasExited) {
    Stop-Process -Id $server.Id -Force
  }
}
