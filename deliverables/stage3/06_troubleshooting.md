# Stage 3 排障手册

## 1. 排障顺序

按从外到内的顺序：

```text
环境变量
  -> garak 与配置
  -> 网络 / DNS / TLS
  -> Groq 鉴权
  -> 模型权限和模型名
  -> 速率限制
  -> Probe / Detector / 报告
```

先看：

```text
deliverables/stage3/runs/<本次运行>/stage3_console.log
deliverables/stage3/xdg_data/garak_stage1/garak.log
```

## 2. 401 Unauthorized

### 常见原因

- `GROQ_API_KEY` 未设置、复制不完整或已撤销。
- 使用了其他 Provider 的 Key。
- Key 前后包含空格或引号。

### 安全检查

```powershell
if ([string]::IsNullOrWhiteSpace($env:GROQ_API_KEY)) {
  "未设置"
}
else {
  "已设置"
}
```

不要输出 Key 本身。

### 解决

重新从 Groq Console 创建或复制 Key，在当前 PowerShell 会话重新设置。若怀疑泄露，立即撤销旧
Key，不要只删除本地文件。

## 3. 403 Forbidden

### 常见原因

Key 有效，但组织或项目禁止访问目标模型。

### 排查

查看 Groq Console 的 Model Permissions，并尝试列出模型：

```powershell
$Headers = @{ Authorization = "Bearer $env:GROQ_API_KEY" }
(Invoke-RestMethod `
  -Uri "https://api.groq.com/openai/v1/models" `
  -Headers $Headers).data.id
```

### 解决

选择当前项目允许的模型，或由组织管理员调整权限。

## 4. 429 Rate Limit

### 原因

Groq 可能限制：

- RPM：每分钟请求数。
- RPD：每天请求数。
- TPM：每分钟 token。
- TPD：每天 token。

达到任意一项都可能 429。具体额度以账户 Limits 页面为准。

### 本项目如何处理

- 安全版：两个 probes 各 1 条，全串行。
- `generations=1`。
- `max_tokens` 默认 96。
- garak 0.15.1 的 OpenAI-compatible Generator 对 `RateLimitError` 使用 Fibonacci backoff，
  单次等待上限为 70 秒。

garak 0.15.1 没有固定“每次请求间隔 N 秒”的 CLI 参数。退避重试只在错误后等待，不等于主动
限速。

### 解决

1. 先等待 `retry-after` 指示的时间。
2. 使用安全版或只跑一个 probe。
3. 减少 `MaxTokens`。
4. 检查当天 RPD/TPD 是否已耗尽。
5. 不要通过立即高频重试扩大问题。

参考：[Groq Rate Limits](https://console.groq.com/docs/rate-limits)。

## 5. Model not found / 404

### 常见原因

- model ID 拼写错误。
- 模型已下线或改名。
- 使用了网页展示名，而不是 API ID。
- base URL 错误。

### 排查

```powershell
$Headers = @{ Authorization = "Bearer $env:GROQ_API_KEY" }
$Models = Invoke-RestMethod `
  -Uri "https://api.groq.com/openai/v1/models" `
  -Headers $Headers
$Models.data.id | Sort-Object
```

### 解决

从返回列表选择模型，并通过：

```powershell
-ModelName <准确的模型 ID>
```

重新运行。

## 6. Connection timeout / APIConnectionError

### 常见原因

- DNS、代理、防火墙或校园网限制。
- TLS 中间代理。
- Groq 服务暂时不可用。

### 排查

```powershell
Test-NetConnection api.groq.com -Port 443
Resolve-DnsName api.groq.com
```

不要使用携带 Key 的详细 HTTP 调试命令截图。

### 解决

确认代理和防火墙策略；短暂故障可稍后重试。不要为了绕过企业网络限制而关闭 TLS 校验。

## 7. garak 参数不兼容 / 400 Bad Request

### 原因

Groq 是 mostly OpenAI-compatible，并不支持全部 OpenAI 参数。例如 `n` 必须为 1，部分
logprob、penalty 参数可能不支持。

### 本项目的处理

使用 `groq.GroqChat`，它继承 `OpenAICompatible`，并屏蔽 Groq 不支持的参数。脚本还固定：

```text
generations = 1
vary_seed_each_call = false
vary_temp_each_call = false
```

### 排查

```powershell
$env:XDG_CONFIG_HOME = "D:\llmProject\deliverables\stage3\xdg_config"
$env:XDG_DATA_HOME = "D:\llmProject\deliverables\stage3\xdg_data"
$env:XDG_CACHE_HOME = "D:\llmProject\deliverables\stage3\xdg_cache"
& D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe `
  --plugin_info generators.groq.GroqChat
```

确认实际 garak 版本：

```powershell
& D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe --version
```

## 8. PowerShell 环境变量不生效

### 原因

- 在窗口 A 设置，却在窗口 B 运行。
- 使用 `set GROQ_API_KEY=...`，这是 cmd.exe 语法。
- 启动子进程前变量为空。

### 正确写法

```powershell
$env:GROQ_API_KEY = "..."
[bool]$env:GROQ_API_KEY
```

推荐使用 `01_groq_api_setup.md` 的隐藏输入方式。

## 9. garak 写用户目录失败

直接执行 garak 可能尝试写：

```text
C:\Users\<user>\.config
C:\Users\<user>\.cache
```

本项目脚本已把 XDG 目录重定向至 `deliverables/stage3`。如果手工运行 garak，也应先设置：

```powershell
$env:XDG_CONFIG_HOME = "D:\llmProject\deliverables\stage3\xdg_config"
$env:XDG_DATA_HOME = "D:\llmProject\deliverables\stage3\xdg_data"
$env:XDG_CACHE_HOME = "D:\llmProject\deliverables\stage3\xdg_cache"
```

## 10. API Key 泄露风险

### 可能泄露的位置

- `.ps1`、`.md`、JSON 和 `.env`。
- PowerShell 历史。
- 截图和录屏。
- Git 历史。
- 打印完整 request headers 的调试日志。

### 检查项目

```powershell
rg -n --hidden "gsk_[A-Za-z0-9_-]{10,}" `
  D:\llmProject\deliverables\stage3 `
  D:\llmProject\llm-security-stage1\scripts
```

### 发现泄露后

1. 立即在 Groq Console 撤销 Key。
2. 创建新 Key。
3. 删除工作区、日志、截图中的值。
4. 如果进入 Git，清理历史并通知所有协作者重新拉取。
5. 检查调用日志和额度是否异常。

“把文件删掉”不足以恢复已经泄露的 Key。

## 11. 脚本显示 failed，但没有安全结论

`groq_scan_result.json` 的 `status=failed` 表示运行链路未完成。此时不要计算 ASR，也不要把
已有的部分 PASS/FAIL 当成完整结果。先解决运行错误，再重新生成一个独立时间戳目录。

### Windows PowerShell 5.1 的 stderr 特例

如果日志停在 Probe 开始或 Request options，终端只显示包装脚本的 `WriteError`，但
`garak.log` 没有 401、429 或 OpenAI SDK 异常，可能是：

```text
$ErrorActionPreference = "Stop"
原生 garak.exe 2>&1 | Tee-Object
```

PowerShell 5.1 会把原生程序写到 stderr 的普通进度输出包装为 ErrorRecord，并提前终止管道。
当前 Stage 3 脚本已在 garak 调用期间临时使用 `Continue`，再通过 `$LASTEXITCODE` 判断真正
失败，最后恢复 `Stop`。

该问题属于脚本包装层，不属于模型安全 FAIL。

参考：[Groq API Error Codes](https://console.groq.com/docs/errors)。
