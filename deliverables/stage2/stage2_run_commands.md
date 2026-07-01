# Stage 2 运行命令记录

## 实验记录基准

- 参考实验计划：`E:\CodeGuarder\docs\experiment_plan.md`
- 一键复跑脚本：`D:\llmProject\llm-security-stage1\scripts\run_stage2_scan.ps1`

## 通用环境变量

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:XDG_CONFIG_HOME='D:\llmProject\deliverables\stage2\xdg_config'
$env:XDG_DATA_HOME='D:\llmProject\deliverables\stage2\xdg_data'
$env:XDG_CACHE_HOME='D:\llmProject\deliverables\stage2\xdg_cache'
$env:OPENAICOMPATIBLE_API_KEY='stage2-local-mock-key'
```

## 启动本地 OpenAI-compatible mock API

```powershell
D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe `
  D:\llmProject\llm-security-stage1\scripts\mock_openai_compatible_api.py `
  --host 127.0.0.1 `
  --port 8000 `
  --log-path D:\llmProject\deliverables\stage2\api_requests.jsonl
```

## garak smoke test 配置

```yaml
system:
  narrow_output: true

run:
  generations: 1
  soft_probe_prompt_cap: 8

reporting:
  confidence_interval_method: none
```

配置文件：

- `D:\llmProject\llm-security-stage1\config\stage2_garak_smoke.yaml`

## Prompt Injection：vulnerable model

```powershell
D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe `
  --config D:\llmProject\llm-security-stage1\config\stage2_garak_smoke.yaml `
  --target_type openai.OpenAICompatible `
  --target_name stage2-vulnerable `
  --generator_options '{"uri":"http://127.0.0.1:8000/v1/","temperature":0.0,"max_tokens":200}' `
  --probes promptinject.HijackHateHumans `
  --generations 1 `
  --seed 42 `
  --report_prefix D:\llmProject\deliverables\stage2\stage2_vulnerable_promptinject `
  --narrow_output
```

结果：`FAIL score 0/8`，attack success rate `100.00%`

## Prompt Injection：guarded model

```powershell
D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe `
  --config D:\llmProject\llm-security-stage1\config\stage2_garak_smoke.yaml `
  --target_type openai.OpenAICompatible `
  --target_name stage2-guarded `
  --generator_options '{"uri":"http://127.0.0.1:8000/v1/","temperature":0.0,"max_tokens":200}' `
  --probes promptinject.HijackHateHumans `
  --generations 1 `
  --seed 42 `
  --report_prefix D:\llmProject\deliverables\stage2\stage2_guarded_promptinject `
  --narrow_output
```

结果：`PASS score 8/8`

## Base64 编码注入 smoke test

本阶段也运行了 `encoding.InjectBase64`，用于观察编码绕过类 probe 的接入情况。

结果：

- `stage2-vulnerable`：`PASS score 8/8`
- `stage2-guarded`：`PASS score 8/8`

解释：当前本地 mock API 的 vulnerable 行为是复述 prompt，并未生成 detector 期望的解码后 payload，因此 Base64 probe 未命中。这个结果可作为后续改进 mock 目标或接入真实模型时的对照。

## 一键复跑

```powershell
powershell -ExecutionPolicy Bypass -File D:\llmProject\llm-security-stage1\scripts\run_stage2_scan.ps1
```
