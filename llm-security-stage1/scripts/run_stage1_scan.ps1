$ErrorActionPreference = "Stop"

$ProjectRoot = "D:\llmProject\llm-security-stage1"
$DeliverableRoot = "D:\llmProject\deliverables\stage1"
$Garak = Join-Path $ProjectRoot ".venv\Scripts\garak.exe"

$env:PYTHONIOENCODING = "utf-8"
$env:XDG_CONFIG_HOME = Join-Path $DeliverableRoot "xdg_config"
$env:XDG_DATA_HOME = Join-Path $DeliverableRoot "xdg_data"
$env:XDG_CACHE_HOME = Join-Path $DeliverableRoot "xdg_cache"

& $Garak --version

& $Garak `
  --target_type test.Blank `
  --target_name blank `
  --probes test.Blank `
  --generations 1 `
  --seed 42 `
  --report_prefix (Join-Path $DeliverableRoot "stage1_min_scan") `
  --narrow_output

& $Garak `
  --target_type test.Repeat `
  --target_name repeat `
  --probes promptinject.HijackHateHumans `
  --generations 1 `
  --seed 42 `
  --report_prefix (Join-Path $DeliverableRoot "stage1_promptinject_scan") `
  --narrow_output
