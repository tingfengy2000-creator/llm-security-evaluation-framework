# garak 运行命令记录

## 实验记录基准

- 参考实验计划：`E:\CodeGuarder\docs\experiment_plan.md`
- 本次实验阶段：Stage 1，garak 最小安全扫描链路验证
- 一键复跑脚本：`D:\llmProject\llm-security-stage1\scripts\run_stage1_scan.ps1`

## 通用环境变量

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:XDG_CONFIG_HOME='D:\llmProject\deliverables\stage1\xdg_config'
$env:XDG_DATA_HOME='D:\llmProject\deliverables\stage1\xdg_data'
$env:XDG_CACHE_HOME='D:\llmProject\deliverables\stage1\xdg_cache'
```

## 版本检查

```powershell
D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe --version
D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe --version
```

已验证：

- `Python 3.12.13`
- `garak LLM vulnerability scanner v0.15.1`

## 扫描 1：最小连通性扫描

目的：验证 garak 可以启动、加载 generator/probe/detector、执行扫描并生成报告。

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

输出：

- `D:\llmProject\deliverables\stage1\stage1_min_scan.report.jsonl`
- `D:\llmProject\deliverables\stage1\stage1_min_scan.report.html`

## 扫描 2：Prompt Injection mock 安全扫描

目的：用 echo 型 mock model 验证攻击 prompt、批量测试和 detector 判定流程。

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

输出：

- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.report.jsonl`
- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.report.html`
- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.hitlog.jsonl`

## 一键复跑

```powershell
powershell -ExecutionPolicy Bypass -File D:\llmProject\llm-security-stage1\scripts\run_stage1_scan.ps1
```
