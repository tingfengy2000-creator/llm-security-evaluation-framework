# Stage 3 完整复跑命令

## 1. 运行前检查

```powershell
Test-Path D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe
& D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe --version
& D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe --version
```

如果直接运行 garak 遇到用户目录写权限问题，使用项目脚本即可；脚本会把 XDG 目录重定向到
`deliverables/stage3`。

## 2. 设置 Key

推荐隐藏输入：

```powershell
$SecureKey = Read-Host "请输入 GROQ_API_KEY" -AsSecureString
$Pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureKey)
try {
  $env:GROQ_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($Pointer)
}
finally {
  [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($Pointer)
}
```

只检查状态，不打印值：

```powershell
[bool]$env:GROQ_API_KEY
```

## 3. 第一条应该执行的命令：安全版

```powershell
powershell -ExecutionPolicy Bypass -File `
  D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan_safe.ps1 `
  -ModelName llama-3.1-8b-instant
```

安全版默认测试：

```text
promptinject.HijackHateHumans
encoding.InjectBase64
```

每个 probe 最多 1 个 prompt，全串行，每个 prompt 只生成 1 次。

## 4. 安全版成功后运行普通版

```powershell
powershell -ExecutionPolicy Bypass -File `
  D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan.ps1 `
  -ModelName llama-3.1-8b-instant
```

普通版每个 probe 最多抽 8 条 prompt，最多约 16 次模型请求；实际请求数以报告为准。

## 5. 如何切换模型

```powershell
powershell -ExecutionPolicy Bypass -File `
  D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan_safe.ps1 `
  -ModelName llama-3.3-70b-versatile
```

模型是否可用、免费额度是多少，以 Groq Console 的 Models 和 Limits 页面为准。不要把网页产品名
想当然地写成 API model ID。

## 6. 如何只跑一个 probe

只跑 Prompt Injection：

```powershell
powershell -ExecutionPolicy Bypass -File `
  D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan_safe.ps1 `
  -ProbeSpec promptinject.HijackHateHumans
```

只跑 Base64 Encoding：

```powershell
powershell -ExecutionPolicy Bypass -File `
  D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan_safe.ps1 `
  -ProbeSpec encoding.InjectBase64
```

## 7. 如何限制输出长度

```powershell
powershell -ExecutionPolicy Bypass -File `
  D:\llmProject\llm-security-stage1\scripts\run_stage3_groq_scan_safe.ps1 `
  -MaxTokens 64
```

`MaxTokens` 限制模型输出，不限制输入 prompt 的 token。Groq 可能同时按 RPM、RPD、TPM 和
TPD 限流，所以仅降低输出长度不能解决所有 429。

## 8. 脚本实际执行的 garak 参数

核心命令等价于：

```powershell
garak `
  --config stage3_garak_safe.yaml `
  --target_type groq.GroqChat `
  --target_name llama-3.1-8b-instant `
  --generator_option_file <本次运行目录>\generator_options.json `
  --probes promptinject.HijackHateHumans `
  --generations 1 `
  --seed 42 `
  --report_prefix <本次运行目录> `
  --narrow_output
```

参数含义：

| 参数 | 作用 |
| --- | --- |
| `--target_type` | 选择如何调用模型，即 Generator |
| `--target_name` | Groq 请求里的 `model` |
| `--generator_option_file` | 从 JSON 文件读取 base URL、温度、输出上限等，不含 Key |
| `--probes` | 选择攻击方法 |
| `--generations 1` | 每个 prompt 只取一个回答 |
| `--seed 42` | 固定 garak 的抽样随机源 |
| `--report_prefix` | 指定报告文件前缀 |
| `--narrow_output` | 精简终端输出，不影响原始报告 |

## 9. 日志保存在哪里

每次运行创建独立目录：

```text
deliverables/stage3/runs/<时间戳>-safe/
deliverables/stage3/runs/<时间戳>-normal/
```

其中包括：

- `stage3_console.log`
- `generator_options.json`：实际模型参数，不含 Key
- `*.report.jsonl`
- `*.report.html`
- 有攻击命中时可能出现 `*.hitlog.jsonl`

garak 全局运行日志位于：

```text
deliverables/stage3/xdg_data/garak_stage1/garak.log
```

根目录以下两个文件表示最近一次运行：

```text
deliverables/stage3/groq_scan_result.json
deliverables/stage3/groq_scan_summary.md
```

这里使用 option file 而不是内联 `--generator_options`，因为 Windows PowerShell 5.1 在调用
原生 `.exe` 时可能剥离 JSON 内部引号。文件方式更容易复现和审计。

实际 `generator_options.json` 必须按插件命名空间嵌套：

```json
{
  "groq": {
    "GroqChat": {
      "uri": "https://api.groq.com/openai/v1",
      "temperature": 0.1,
      "max_tokens": 96,
      "vary_seed_each_call": false,
      "vary_temp_each_call": false
    }
  }
}
```

只把这些字段放在 JSON 根层，garak 会读取文件但 `GroqChat` 实例不会应用它们。

此外，Probe 可以为具体攻击指定生成参数。例如 `promptinject.HijackHateHumans` 会把
`max_tokens` 设为 60。此时 Probe 的单次攻击参数优先于 Generator 默认值，真实请求参数应以
`garak.log` 中的 `Request options` 为准。

## 10. 如何截图留证

建议截图：

1. 运行命令和 garak 版本，不包含 Key 设置过程。
2. 终端中的模型、probe 和 PASS/FAIL 汇总。
3. `groq_scan_summary.md`。
4. 两个 HTML 报告的概览和代表性样本。

不要截图：

- `$env:GROQ_API_KEY` 的输出。
- Groq Console 的 Key 页面。
- 含 Authorization header 的网络调试窗口。

截图命名建议：

```text
01_safe_run_terminal.png
02_promptinject_report.png
03_base64_report.png
04_summary.png
```

## 11. 初学者最容易误解

- PowerShell 反引号必须是行尾最后一个字符，后面不能有空格。
- `-ProbeSpec` 是本项目脚本参数，`--probes` 才是 garak 原生参数。
- 把终端输出重定向到文件不等于生成了 garak JSONL 报告。
- 不要同时开启高并发和大 prompt cap 来“测试限流”，那不是本阶段目标。
