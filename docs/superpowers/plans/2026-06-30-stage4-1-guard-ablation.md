# Stage 4.1 Guard 消融实验 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增独立 Stage 4.1 Proxy 与四组严格配对 runner，验证 Input Guard 和 Output Guard 的独立贡献，同时保持所有 Stage 4 历史产物不变。

**Architecture:** `guard_proxy_ablation.py` 导入现有 `GuardEngine` 规则，但使用独立服务和日志 schema。PowerShell runner 按 `passthrough / input-only / output-only / full-guard` 顺序运行同一组 garak Probe，验证日志契约、output-only 不变量和四组 prompt hash 后，生成独立聚合结果。

**Tech Stack:** Python 3.12、OpenAI Python SDK、标准库 HTTP server、garak 0.15.1、PowerShell 5.1、JSONL/Markdown。

**Repository note:** 当前 `D:\llmProject\.git` 不是有效 Git 仓库，计划中的阶段检查以测试输出代替 commit，不执行伪造的 Git 操作。

---

### Task 1: Stage 4.1 Proxy 日志与模式契约

**Files:**
- Create: `D:\llmProject\llm-security-stage1\tests\test_guard_proxy_ablation.py`
- Create: `D:\llmProject\llm-security-stage1\scripts\guard_proxy_ablation.py`
- Read only: `D:\llmProject\llm-security-stage1\scripts\guard_proxy.py`

- [ ] **Step 1: 写模式映射和日志字段失败测试**

测试必须断言：

```python
EXPECTED = {
    "passthrough": (False, False, "passthrough"),
    "input-only": (True, False, "input-only"),
    "output-only": (False, True, "output-only"),
    "full-guard": (True, True, "guarded"),
}

REQUIRED_LOG_FIELDS = {
    "input_guard_enabled",
    "output_guard_enabled",
    "upstream_called",
    "input_blocked",
    "output_blocked",
    "final_decision",
    "original_model_output_hash",
}
```

- [ ] **Step 2: 运行测试并确认因模块不存在而失败**

Run:

```powershell
& "D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe" -m unittest `
  "D:\llmProject\llm-security-stage1\tests\test_guard_proxy_ablation.py" -v
```

Expected: FAIL/ERROR，原因是 `guard_proxy_ablation` 尚不存在。

- [ ] **Step 3: 实现最小模式映射和基础记录**

新增：

```python
EXPERIMENT_MODES = {
    "passthrough": {
        "internal_mode": "passthrough",
        "input_guard_enabled": False,
        "output_guard_enabled": False,
    },
    "input-only": {
        "internal_mode": "input-only",
        "input_guard_enabled": True,
        "output_guard_enabled": False,
    },
    "output-only": {
        "internal_mode": "output-only",
        "input_guard_enabled": False,
        "output_guard_enabled": True,
    },
    "full-guard": {
        "internal_mode": "guarded",
        "input_guard_enabled": True,
        "output_guard_enabled": True,
    },
}
```

基础记录将九个必需字段初始化为明确的 bool/null 值，`final_decision` 初始为 `None`。

- [ ] **Step 4: 写 Output Guard 顺序失败测试**

使用 Fake Upstream 返回 `<script>alert(1)</script>`，断言：

```python
assert record["input_guard_enabled"] is False
assert record["upstream_called"] is True
assert record["input_blocked"] is False
assert record["original_model_output_hash"] is not None
assert record["output_blocked"] is True
assert record["final_decision"] == "output_block"
assert "<script>" not in response["choices"][0]["message"]["content"]
```

- [ ] **Step 5: 实现 Output Guard 先哈希后替换**

处理顺序固定为：

```python
upstream_response = client.chat.completions.create(**payload)
original_output = assistant_text(upstream_response)
record["original_model_output_hash"] = text_sha256(original_output)
record["original_model_output_length"] = len(original_output)
decision = engine.inspect_output(original_output)
if output_guard_enabled and decision.blocked:
    replace_with_refusal()
```

不把 `original_output` 或其 preview 写入日志。

- [ ] **Step 6: 补齐 input-only、full-guard、passthrough 和安全日志测试**

断言：

- input-only/full-guard 输入命中时 `upstream_called=false`
- passthrough 返回原始输出
- 日志不含 `api_key`、`authorization` 或完整危险输出
- 上游调用后的 `original_model_output_hash` 非空
- HTTP completion 契约可被 OpenAI-compatible 客户端解析

- [ ] **Step 7: 运行 Proxy 全部测试**

Run:

```powershell
& "D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe" -m unittest discover `
  -s "D:\llmProject\llm-security-stage1\tests" `
  -p "test_guard_proxy*.py" -v
```

Expected: Stage 4 与 Stage 4.1 Proxy 测试全部 PASS。

### Task 2: 四组消融主 runner

**Files:**
- Create: `D:\llmProject\llm-security-stage1\tests\test_stage4_ablation_scripts.ps1`
- Create: `D:\llmProject\llm-security-stage1\scripts\run_stage4_ablation.ps1`
- Read only: `D:\llmProject\llm-security-stage1\config\stage4_garak_safe.yaml`

- [ ] **Step 1: 写 PowerShell 契约失败测试**

测试解析脚本语法并要求包含：

```text
passthrough
input-only
output-only
full-guard
prompt_hash_parity
ablation_result.json
ablation_summary.md
original_model_output_hash
input_guard_enabled
output_guard_enabled
status = "invalid"
```

同时断言新 runner 不包含写入路径 `deliverables\stage4\`。

- [ ] **Step 2: 运行契约测试并确认脚本不存在**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  "D:\llmProject\llm-security-stage1\tests\test_stage4_ablation_scripts.ps1"
```

Expected: FAIL，提示缺少 `run_stage4_ablation.ps1`。

- [ ] **Step 3: 实现参数、路径和安全启动**

主脚本参数：

```powershell
param(
  [string]$ModelName = "llama-3.1-8b-instant",
  [string]$ProbeSpec = "promptinject.HijackHateHumans,encoding.InjectBase64",
  [int]$MaxTokens = 96,
  [int]$Port = 8011,
  [int]$DelaySeconds = 0
)
```

只读取 `GROQ_API_KEY`，所有输出写到
`D:\llmProject\deliverables\stage4_ablation`。使用 `.NET ProcessStartInfo`
隐藏启动独立 Proxy，Proxy 在原网络环境启动；`NO_PROXY` 只包裹 garak 子进程。

- [ ] **Step 4: 实现四组运行与独立日志**

固定顺序：

```powershell
$ExperimentNames = @(
  "passthrough",
  "input-only",
  "output-only",
  "full-guard"
)
```

每组写入：

```text
logs/<run_id>/<experiment_name>/
├── guard_logs.jsonl
├── generator_options.json
├── proxy_stdout.log
├── proxy_stderr.log
├── *.report.jsonl
└── *.report.html
```

- [ ] **Step 5: 实现 Attempt、Detector 和 Guard 指标提取**

每组聚合：

```text
attempt_count
passed_attempts
failed_attempts
attack_success_rate_percent
detector_evaluations
detector_failures
upstream_calls
input_blocks
output_blocks
observed_dangerous_outputs
```

- [ ] **Step 6: 实现四组 prompt hash parity**

每组生成排序后的：

```text
probe|prompt_sha256
```

以 passthrough 为基准比较其他三组。任何差异写：

```json
{
  "status": "invalid",
  "invalid_reasons": ["prompt_hash_parity=false"]
}
```

- [ ] **Step 7: 实现日志 schema 和 output-only 不变量**

逐条检查九个必需字段。对 output-only 额外检查：

```text
input_guard_enabled=false
output_guard_enabled=true
upstream_called=true
input_blocked=false
original_model_output_hash 非空
```

若 `output_matches` 非空，还检查 `output_blocked=true`、
`final_decision=output_block` 和最终 hash 不等于原始 hash。

- [ ] **Step 8: 实现完成、invalid 与 failed 结果**

- `completed`：报告、配对和不变量全部通过
- `invalid`：科学有效性检查失败
- `failed`：运行时或 API 失败

`ablation_summary.md` 输出四组 PASS、FAIL、ASR、上游调用、输入拦截、输出拦截和危险输出观察。

- [ ] **Step 9: 运行 PowerShell 契约测试**

Expected:

```text
stage4_ablation_script_contract_test=passed
```

### Task 3: safe 入口

**Files:**
- Modify: `D:\llmProject\llm-security-stage1\tests\test_stage4_ablation_scripts.ps1`
- Create: `D:\llmProject\llm-security-stage1\scripts\run_stage4_ablation_safe.ps1`

- [ ] **Step 1: 先扩展失败测试**

要求 safe 脚本：

- 调用主脚本
- 固定两个 Probe
- `DelaySeconds` 大于 0
- 不接受扩大 prompt cap 的参数
- 不包含 API Key 字面值

- [ ] **Step 2: 运行测试并确认缺少 safe 脚本**

Expected: FAIL，提示缺少 `run_stage4_ablation_safe.ps1`。

- [ ] **Step 3: 实现 safe wrapper**

safe wrapper 只暴露模型、端口和组间等待，默认调用：

```powershell
& $MainScript `
  -ModelName $ModelName `
  -ProbeSpec "promptinject.HijackHateHumans,encoding.InjectBase64" `
  -MaxTokens 96 `
  -Port $Port `
  -DelaySeconds $DelaySeconds
```

- [ ] **Step 4: 运行两个 PowerShell 契约测试**

Expected: 全部 PASS。

### Task 4: 中文教学交付物

**Files:**
- Create: `D:\llmProject\deliverables\stage4_ablation\00_ablation_overview.md`
- Create: `D:\llmProject\deliverables\stage4_ablation\01_experiment_design.md`
- Create: `D:\llmProject\deliverables\stage4_ablation\02_result_comparison.md`
- Create: `D:\llmProject\deliverables\stage4_ablation\03_output_guard_analysis.md`
- Create: `D:\llmProject\deliverables\stage4_ablation\04_limitations.md`
- Create: `D:\llmProject\deliverables\stage4_ablation\05_interview_talking_points.md`
- Create: `D:\llmProject\deliverables\stage4_ablation\ablation_summary.md`
- Create: `D:\llmProject\deliverables\stage4_ablation\ablation_result.json`

- [ ] **Step 1: 写运行前状态**

初始化 JSON：

```json
{
  "schema_version": "1.0",
  "status": "not_run",
  "stage": "4.1",
  "experiment_names": [
    "passthrough",
    "input-only",
    "output-only",
    "full-guard"
  ],
  "reason": "代码与教学文档已完成离线验证，真实 Groq 四组实验尚未运行。"
}
```

- [ ] **Step 2: 写六章中文学习文档**

文档必须解释：

- `full-guard` 与内部 `guarded` 的区别
- 四组控制变量
- Output Guard 为什么必须先调用模型
- 原始输出 hash 与最终输出 hash 的区别
- PASS/FAIL/ASR/上游调用如何联合解释
- output-only 和 full-guard 的结论边界
- rule-based baseline、误报和绕过风险
- 30 秒、1 分钟、3 分钟面试话术

- [ ] **Step 3: 写完整复跑命令和结果阅读顺序**

safe 命令作为首选：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  "D:\llmProject\llm-security-stage1\scripts\run_stage4_ablation_safe.ps1" `
  -ModelName "llama-3.1-8b-instant"
```

### Task 5: 离线集成验证与实验记录

**Files:**
- Modify: `D:\llmProject\deliverables\learning_notes.md`
- Modify: `E:\CodeGuarder\docs\experiment_plan.md`

- [ ] **Step 1: 编译和运行全部单元测试**

Run:

```powershell
& "D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe" -m py_compile `
  "D:\llmProject\llm-security-stage1\scripts\guard_proxy_ablation.py"

& "D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe" -m unittest discover `
  -s "D:\llmProject\llm-security-stage1\tests" -p "test_guard_proxy*.py" -v
```

- [ ] **Step 2: 运行 PowerShell 契约测试**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  "D:\llmProject\llm-security-stage1\tests\test_stage4_ablation_scripts.ps1"
```

- [ ] **Step 3: 使用 Fake Upstream 验证 output-only**

验证日志满足：

```text
upstream_called=true
input_blocked=false
output_blocked=true
original_model_output_hash 非空
final_decision=output_block
```

- [ ] **Step 4: 验证 Stage 4 产物没有变化**

对 Stage 4 关键脚本和聚合产物在实施前后的 SHA-256 做比较：

```text
guard_proxy.py
run_stage4_guard_proxy.ps1
run_stage4_guarded_scan.ps1
guarded_groq_scan_result.json
guarded_groq_scan_summary.md
```

- [ ] **Step 5: 扫描凭据泄露**

搜索 `deliverables/stage4_ablation` 与新脚本，不允许出现真实 `gsk_...` 模式。

- [ ] **Step 6: 更新实验记录**

记录：

- 为什么做 Stage 4.1
- 新增文件
- 离线测试结果
- 真实 API 状态为未运行
- 下一步只执行 safe 脚本，不进入 RAG

- [ ] **Step 7: 输出真实运行命令**

真实运行必须由持有 `GROQ_API_KEY` 的用户 PowerShell 执行。运行后再分析四组真实数据，
不能用 Fake Upstream 或预期结果替代。
