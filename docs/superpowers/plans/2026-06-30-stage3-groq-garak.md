# Stage 3 Groq Garak Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有 garak 项目中增加使用 Groq OpenAI-compatible API 的真实模型安全评测，并提供可复跑脚本、结构化结果和中文教学资料。

**Architecture:** 使用 garak 0.15.1 自带的 `groq.GroqChat` Generator，通过 OpenAI Python client 调用 Groq。两个配置分别控制普通扫描和免费额度 smoke test；PowerShell 脚本负责 Key 检查、调用 garak、解析 JSONL `eval` 记录并生成聚合结果。

**Tech Stack:** PowerShell 5.1、Python 3.12、garak 0.15.1、OpenAI-compatible Chat Completions、YAML、JSONL、Markdown。

---

### Task 1: 创建 Stage 3 garak 配置

**Files:**
- Create: `D:/llmProject/llm-security-stage1/config/stage3_garak.yaml`
- Create: `D:/llmProject/llm-security-stage1/config/stage3_garak_safe.yaml`

- [ ] **Step 1: 创建普通配置**

写入 `narrow_output: true`、`generations: 1`、`soft_probe_prompt_cap: 8` 和禁用 bootstrap 的报告设置。

- [ ] **Step 2: 创建安全配置**

写入 `parallel_requests: 1`、`parallel_attempts: 1`、`generations: 1`、`soft_probe_prompt_cap: 1` 和禁用 bootstrap 的报告设置。

- [ ] **Step 3: 用 garak 加载配置**

Run:

```powershell
$env:XDG_CONFIG_HOME='D:\llmProject\deliverables\_verify\xdg_config'
$env:XDG_DATA_HOME='D:\llmProject\deliverables\_verify\xdg_data'
$env:XDG_CACHE_HOME='D:\llmProject\deliverables\_verify\xdg_cache'
.\llm-security-stage1\.venv\Scripts\garak.exe --config .\llm-security-stage1\config\stage3_garak_safe.yaml --list_config
```

Expected: exit code 0，并显示 `soft_probe_prompt_cap: 1`。

### Task 2: 创建扫描脚本

**Files:**
- Create: `D:/llmProject/llm-security-stage1/scripts/run_stage3_groq_scan.ps1`
- Create: `D:/llmProject/llm-security-stage1/scripts/run_stage3_groq_scan_safe.ps1`

- [ ] **Step 1: 实现普通扫描**

脚本参数为 `ModelName`、`ProbeSpec`、`MaxTokens`。Key 优先级为
`GROQ_API_KEY`，其次为 `OPENAI_API_KEY`；后备值只映射到当前进程的
`GROQ_API_KEY`。分别运行两个 probe，并检查 `$LASTEXITCODE`。

- [ ] **Step 2: 聚合结果**

读取每个 `*.report.jsonl` 的 `entry_type=eval`，写出 UTF-8
`groq_scan_result.json` 和 `groq_scan_summary.md`。结果包含模型、base URL、garak
版本、probe、detector、passed、fails、total、ASR 和原始报告路径，不包含 Key。

- [ ] **Step 3: 实现免费额度脚本**

安全脚本复用普通脚本并传入安全配置，限制 prompt cap 和并发；默认只产生两个模型请求。

- [ ] **Step 4: PowerShell 语法验证**

Run:

```powershell
$errors=@()
[System.Management.Automation.Language.Parser]::ParseFile(
  'D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan.ps1',
  [ref]$null,
  [ref]$errors
) | Out-Null
if ($errors.Count) { $errors; exit 1 }
```

Expected: exit code 0、无解析错误。对安全脚本重复执行。

### Task 3: 编写教学型交付文档

**Files:**
- Create: `D:/llmProject/deliverables/stage3/00_stage3_overview.md`
- Create: `D:/llmProject/deliverables/stage3/01_groq_api_setup.md`
- Create: `D:/llmProject/deliverables/stage3/02_garak_groq_run_commands.md`
- Create: `D:/llmProject/deliverables/stage3/03_probe_explanation.md`
- Create: `D:/llmProject/deliverables/stage3/04_result_interpretation.md`
- Create: `D:/llmProject/deliverables/stage3/05_mock_vs_real_api.md`
- Create: `D:/llmProject/deliverables/stage3/06_troubleshooting.md`
- Create: `D:/llmProject/deliverables/stage3/07_interview_talking_points.md`
- Create: `D:/llmProject/deliverables/stage3/screenshots/README.md`

- [ ] **Step 1: 写调用链和 API 设置**

解释 Stage 1/2/3 递进、OpenAI-compatible、Key/base URL/model 的职责、企业原因、
上一阶段关系、面试追问和初学者误区。

- [ ] **Step 2: 写复跑命令和 probe 原理**

提供普通版、安全版、切换模型、单 probe、日志保存和截图命令；解释两个 probe 及
mock/真实模型差异。

- [ ] **Step 3: 写结果与排障**

解释 PASS/FAIL/ASR、JSONL 与聚合 JSON；覆盖 401、403、404、429、超时、参数不兼容、
环境变量失效和泄露风险。

- [ ] **Step 4: 写面试话术**

提供 30 秒、1 分钟、3 分钟版本及用户指定的八个追问回答。

### Task 4: 初始化结果占位和学习记录

**Files:**
- Create: `D:/llmProject/deliverables/stage3/groq_scan_result.json`
- Create: `D:/llmProject/deliverables/stage3/groq_scan_summary.md`
- Modify: `D:/llmProject/deliverables/learning_notes.md`

- [ ] **Step 1: 初始化未运行状态**

在尚未真实请求时写入 `status: not_run`，明确这不是安全评测结论。

- [ ] **Step 2: 更新学习记录**

追加 Stage 3 的已掌握、待验证和下一步内容，不覆盖已有笔记。

### Task 5: 离线验证与真实 smoke test

**Files:**
- Verify: `D:/llmProject/deliverables/stage3/**`
- Verify: `D:/llmProject/llm-security-stage1/scripts/run_stage3_groq_scan*.ps1`

- [ ] **Step 1: 验证 Generator**

Run:

```powershell
.\llm-security-stage1\.venv\Scripts\garak.exe --plugin_info generators.groq.GroqChat
```

Expected: exit code 0，并显示 GroqChat 使用 `GROQ_API_KEY`。

- [ ] **Step 2: 验证缺 Key 路径**

在清空当前子进程两个候选变量后运行安全脚本。

Expected: 非 0 退出，错误仅提示设置环境变量，不包含凭据。

- [ ] **Step 3: 扫描敏感信息**

Run:

```powershell
rg -n --hidden "(gsk_[A-Za-z0-9_-]{10,}|api[_-]?key\s*[:=]\s*['\"][^$])" `
  D:\llmProject\deliverables\stage3 `
  D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan*.ps1
```

Expected: 不出现真实 Key。

- [ ] **Step 4: 运行真实安全版**

仅当 `GROQ_API_KEY` 在当前执行进程中可见时运行：

```powershell
powershell -ExecutionPolicy Bypass -File `
  D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan_safe.ps1 `
  -ModelName llama-3.1-8b-instant
```

Expected: 两个 probe 均生成 JSONL/HTML，聚合 JSON 的 `status` 为 `completed`。

### Task 6: 记录外部实验计划

**Files:**
- Modify: `E:/CodeGuarder/docs/experiment_plan.md`

- [ ] **Step 1: 追加 Stage 3 记录**

记录目的、改动、对原数据影响、验证命令、当前运行状态和阻塞项。写入 UTF-8，不覆盖原内容。

- [ ] **Step 2: 最终文件完整性检查**

Run:

```powershell
Get-ChildItem D:\llmProject\deliverables\stage3 -Recurse |
  Select-Object FullName,Length
```

Expected: 用户要求的所有文件均存在且教学文档非空。

