# Stage 1 运行命令记录

## 目录创建

```powershell
New-Item -ItemType Directory -Force -Path D:\llmProject\llm-security-stage1
New-Item -ItemType Directory -Force -Path D:\llmProject\llm-security-stage1\scripts
New-Item -ItemType Directory -Force -Path D:\llmProject\llm-security-stage1\results
New-Item -ItemType Directory -Force -Path D:\llmProject\llm-security-stage1\docs
New-Item -ItemType Directory -Force -Path D:\llmProject\deliverables\stage1
```

## Python 环境

```powershell
C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m venv D:\llmProject\llm-security-stage1\.venv
D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe --version
D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe -m pip install --upgrade pip garak
```

最终验证版本：

```powershell
D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe --version
D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe --version
```

## garak 本地运行环境变量

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:XDG_CONFIG_HOME='D:\llmProject\deliverables\stage1\xdg_config'
$env:XDG_DATA_HOME='D:\llmProject\deliverables\stage1\xdg_data'
$env:XDG_CACHE_HOME='D:\llmProject\deliverables\stage1\xdg_cache'
```

说明：当前沙箱限制了默认用户目录下的配置/缓存写入，因此 Stage 1 将 garak 的 XDG 配置、数据、缓存目录固定到本工作区交付目录。

## 最小连通性扫描

```powershell
D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe `
  --target_type test.Blank `
  --target_name blank `
  --probes test.Blank `
  --generations 1 `
  --seed 42 `
  --report_prefix D:\llmProject\deliverables\stage1\stage1_min_scan `
  --narrow_output
```

输出结果：

- `D:\llmProject\deliverables\stage1\stage1_min_scan.report.jsonl`
- `D:\llmProject\deliverables\stage1\stage1_min_scan.report.html`

## Prompt Injection mock 安全扫描

```powershell
D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe `
  --target_type test.Repeat `
  --target_name repeat `
  --probes promptinject.HijackHateHumans `
  --generations 1 `
  --seed 42 `
  --report_prefix D:\llmProject\deliverables\stage1\stage1_promptinject_scan `
  --narrow_output
```

输出结果：

- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.report.jsonl`
- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.report.html`
- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.hitlog.jsonl`

## 一键复跑

```powershell
powershell -ExecutionPolicy Bypass -File D:\llmProject\llm-security-stage1\scripts\run_stage1_scan.ps1
```
