# Stage 4 运行命令

## 1. 先确认 Key

在当前 PowerShell 窗口执行：

```powershell
[bool]$env:GROQ_API_KEY
```

必须显示 `True`。不要打印 Key 本身。

## 2. 推荐命令：一次完成配对 A/B

请整行复制，不使用反引号换行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\llmProject\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1" -ModelName "llama-3.1-8b-instant"
```

默认顺序：

```text
passthrough
  -> PromptInject
  -> Base64
guarded
  -> PromptInject
  -> Base64
```

每个 Probe 只选 1 条 prompt。passthrough 通常调用 Groq 2 次；如果两条输入都被 Guard 命中，
guarded 组可能不调用 Groq。

## 3. 手动启动 Guard Proxy

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\llmProject\llm-security-stage1\scripts\run_stage4_guard_proxy.ps1" -Mode "guarded" -Port 8010
```

另开一个 PowerShell 检查：

```powershell
Invoke-RestMethod http://127.0.0.1:8010/health
```

手动模式适合学习请求流；自动 A/B 请使用上一节命令。

## 4. 只运行一个模式

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\llmProject\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1" -Modes "guarded"
```

只运行 guarded 时可以验证防护链路，但无法形成同轮严格 A/B。

## 5. 运行消融模式

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\llmProject\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1" -Modes "input-only,output-only"
```

这会产生额外真实请求。初次主实验完成前不要运行。

## 6. 只跑一个 Probe

Prompt Injection：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\llmProject\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1" -ProbeSpec "promptinject.HijackHateHumans"
```

Base64：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\llmProject\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1" -ProbeSpec "encoding.InjectBase64"
```

## 7. 输出位置

每次运行：

```text
deliverables/stage4/runs/<timestamp>/
├── passthrough/
├── guarded/
├── guard_logs.jsonl
└── stage4_console.log
```

根目录最新聚合：

```text
deliverables/stage4/guarded_groq_scan_result.json
deliverables/stage4/guarded_groq_scan_summary.md
deliverables/stage4/guard_logs.jsonl
```

## 8. 成功时检查

```powershell
$Result = Get-Content D:\llmProject\deliverables\stage4\guarded_groq_scan_result.json -Raw -Encoding UTF8 | ConvertFrom-Json
$Result.status
$Result.prompt_hash_parity
$Result.comparison
$Result.guard_metrics | Format-Table
```

预期：

- `status=completed`
- `prompt_hash_parity=True`
- passthrough 和 guarded 都有完整报告
- Guard 日志请求数与 garak Attempt 对应

## 9. 失败时优先检查

1. `GROQ_API_KEY` 是否在同一个 PowerShell 会话。
2. 8010 端口是否被占用。
3. `proxy_stderr.log`。
4. `stage4_console.log`。
5. Groq 401/429。
6. JSON 中 `status=failed` 的 error。

## 10. 停在 `Preparing prompts: 0/1`

如果 garak 长时间停在 `0/1`，先看：

```powershell
Get-Content "D:\llmProject\deliverables\stage4\xdg_data\garak_stage1\garak.log" -Tail 60
```

若目标 API 是 `127.0.0.1:8010`，但日志中的 `connect_tcp` 指向
`127.0.0.1:7897`，说明 OpenAI SDK 继承了 Clash 等本机代理，把 Guard Proxy
请求错误转发给了代理端口。`502` 会触发 SDK 退避重试，因此表面上像是扫描卡住。

当前脚本先在原网络环境中启动 Guard Proxy，然后只在执行 garak 子进程期间把
`127.0.0.1,localhost` 加入 `NO_PROXY`，完成或失败后立即恢复。这样 garak 直连本地
8010，而 Guard Proxy 访问 Groq 时仍保留原来的外网代理。

修复前已经开始的进程不会自动加载新脚本。按一次 `Ctrl+C` 停止旧进程，然后重新执行
第 2 节的完整 A/B 命令。

## 11. Guard Proxy 上游返回 `403`

这表示 garak 已到达 Guard Proxy，但 `Guard Proxy -> Groq` 被拒绝。Groq 官方将 `403`
定义为权限限制，模型被组织级或项目级策略禁用时也会返回该状态。

不要马上重新运行完整 A/B。先在设置了 `GROQ_API_KEY` 的同一 PowerShell 中发一个良性请求：

```powershell
& "D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe" -c "import os,openai; c=openai.OpenAI(api_key=os.environ['GROQ_API_KEY'],base_url='https://api.groq.com/openai/v1'); r=c.chat.completions.create(model='llama-3.1-8b-instant',messages=[{'role':'user','content':'Reply only OK'}],max_tokens=8); print(r.choices[0].message.content)"
```

- 良性请求也返回 `403`：优先检查 Groq Console 的组织/项目 Model Permissions，以及当前
  PowerShell 是否使用了预期的 Key。
- 良性请求成功、攻击请求返回 `403`：再分析攻击内容或请求字段触发的上游策略。

Guard Proxy 会保留经过脱敏的上游 `message/type/code`，但不会记录 API Key、Authorization
或完整响应头。

本机实测发现，如果在启动 Guard Proxy 之前全局设置 `NO_PROXY`，第一跳会恢复，但 Proxy
访问 Groq 可能得到通用 `403 Forbidden`。因此 `NO_PROXY` 必须限定在 garak 客户端进程，
不能让 Guard Proxy 子进程继承。
