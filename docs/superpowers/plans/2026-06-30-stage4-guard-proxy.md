# Stage 4 Guard Proxy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and evaluate a local OpenAI-compatible rule-based guard proxy in a paired passthrough-versus-guarded garak experiment.

**Architecture:** A testable Python guard engine is wrapped by a standard-library HTTP server. PowerShell starts each proxy mode, waits on `/health`, runs the same capped garak probes, verifies prompt parity, and aggregates Stage 3 historical plus Stage 4 paired results.

**Tech Stack:** Python 3.12, `http.server`, OpenAI Python 2.44, PowerShell 5.1, garak 0.15.1, JSONL, Markdown.

---

### Task 1: Guard Engine Red-Green Tests

**Files:**
- Create: `D:/llmProject/llm-security-stage1/tests/test_guard_proxy.py`
- Create: `D:/llmProject/llm-security-stage1/scripts/guard_proxy.py`

- [ ] **Step 1: Write failing rule tests**

Tests import `GuardEngine`, `ProxyService`, and `extract_text`; they assert that
instruction override, jailbreak, and decoded suspicious Base64 are detected,
while benign text and benign Base64 are allowed.

- [ ] **Step 2: Verify RED**

Run:

```powershell
& D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe `
  -m unittest D:\llmProject\llm-security-stage1\tests\test_guard_proxy.py -v
```

Expected: import failure because `guard_proxy.py` does not exist.

- [ ] **Step 3: Implement the guard engine**

Create named regex rules, bounded Base64 decoding, SHA-256 preview helpers,
OpenAI-compatible refusal completion generation, and mode enforcement.

- [ ] **Step 4: Verify GREEN**

Run the same unittest command. Expected: all rule tests pass.

### Task 2: Proxy Service and HTTP Contract

**Files:**
- Modify: `D:/llmProject/llm-security-stage1/scripts/guard_proxy.py`
- Modify: `D:/llmProject/llm-security-stage1/tests/test_guard_proxy.py`

- [ ] **Step 1: Add failing service tests**

Use a fake OpenAI client to prove:

- guarded input blocking does not call upstream
- output-only replaces a dangerous response
- passthrough preserves a safe response
- generated audit records omit key/header fields

- [ ] **Step 2: Implement `ProxyService`**

Forward non-streaming chat requests, strip Groq-incompatible optional fields,
apply input/output modes, return OpenAI-compatible errors, and append one
thread-safe JSONL audit record per request.

- [ ] **Step 3: Implement HTTP endpoints**

Add `/v1/chat/completions`, `/v1/models`, and `/health`. Read
`GROQ_API_KEY`; default upstream URL to `https://api.groq.com/openai/v1`.

- [ ] **Step 4: Run all proxy tests**

Expected: all tests pass and no network is used.

### Task 3: Stage 4 Runner

**Files:**
- Create: `D:/llmProject/llm-security-stage1/config/stage4_garak_safe.yaml`
- Create: `D:/llmProject/llm-security-stage1/scripts/run_stage4_guard_proxy.ps1`
- Create: `D:/llmProject/llm-security-stage1/scripts/run_stage4_guarded_scan.ps1`
- Create: `D:/llmProject/llm-security-stage1/tests/test_stage4_scripts.ps1`

- [ ] **Step 1: Write failing script contract checks**

Assert Key preflight, hidden proxy process, health polling, passthrough and
guarded modes, local OpenAI-compatible URI, identical probes, and result paths.

- [ ] **Step 2: Implement the manual proxy runner**

Validate the environment, create the Stage 4 directory, and launch the proxy
in the foreground with mode/model/port parameters.

- [ ] **Step 3: Implement the paired scan runner**

Start a hidden proxy for each requested mode, poll `/health`, run capped garak,
stop the server in `finally`, parse JSONL attempts/evals, verify prompt hashes,
aggregate metrics, and write guarded result/summary files.

- [ ] **Step 4: Validate scripts**

Run PowerShell parser checks, the static contract test, and garak
`--list_config`. Expected: zero failures.

### Task 4: Teaching Deliverables

**Files:**
- Create: `D:/llmProject/deliverables/stage4/00_stage4_overview.md`
- Create: `D:/llmProject/deliverables/stage4/01_guard_proxy_design.md`
- Create: `D:/llmProject/deliverables/stage4/02_input_output_guard_rules.md`
- Create: `D:/llmProject/deliverables/stage4/03_run_commands.md`
- Create: `D:/llmProject/deliverables/stage4/04_result_comparison.md`
- Create: `D:/llmProject/deliverables/stage4/05_ablation_study.md`
- Create: `D:/llmProject/deliverables/stage4/06_interview_talking_points.md`
- Create: `D:/llmProject/deliverables/stage4/guarded_groq_scan_result.json`
- Create: `D:/llmProject/deliverables/stage4/guarded_groq_scan_summary.md`
- Create: `D:/llmProject/deliverables/stage4/guard_logs.jsonl`
- Modify: `D:/llmProject/deliverables/learning_notes.md`
- Modify: `E:/CodeGuarder/docs/experiment_plan.md`

- [ ] **Step 1: Write the learning chapters**

Explain architecture, rules, exact commands, paired comparison, ablation,
limitations, enterprise rationale, interview questions, and beginner traps.

- [ ] **Step 2: Initialize not-run result artifacts**

Write valid JSON/Markdown that explicitly says the real paired scan has not
run. Create an empty JSONL audit file.

- [ ] **Step 3: Record the experiment plan**

Record purpose, changed files, original-data impact, verification evidence,
real-run status, and next command.

### Task 5: Offline and Real Verification

**Files:**
- Verify all Stage 4 files.

- [ ] **Step 1: Run offline tests**

Run Python unittests, PowerShell tests, syntax checks, configuration loading,
and a credential-pattern scan.

- [ ] **Step 2: Run local fake-upstream integration**

Start a local fake upstream and prove passthrough forwarding plus guarded
blocking without a real Groq key or network.

- [ ] **Step 3: Run real paired smoke test**

In the PowerShell session containing `GROQ_API_KEY`, run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  D:\llmProject\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1 `
  -ModelName llama-3.1-8b-instant
```

Expected: passthrough and guarded reports, prompt-hash parity, populated guard
logs, and a comparison result with `status=completed`.

