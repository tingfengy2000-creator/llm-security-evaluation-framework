# Groq API 配置学习笔记

## 1. 三个必须分清的量

### API Key：你是谁、是否有权调用

API Key 是凭据。客户端把它放进 HTTP `Authorization` 请求头，Groq 用它识别项目、权限和
额度。Key 不决定调用哪个模型，也不决定请求发到哪个网站。

### base_url：请求发到哪里

本实验固定为：

```text
https://api.groq.com/openai/v1
```

OpenAI client 会在此基础上调用 `/chat/completions`，最终地址相当于：

```text
https://api.groq.com/openai/v1/chat/completions
```

### model_name：让服务端选择哪个模型

本实验默认：

```text
llama-3.1-8b-instant
```

它会成为请求 JSON 中的 `model` 字段。Key 正确、URL 正确但模型名不存在时，仍会失败。

一句话记忆：

```text
API Key = 身份凭证
base_url = 服务地址
model_name = 服务端模型 ID
```

## 2. 为什么不能把 Key 写死

把 Key 写进 `.ps1`、Markdown 或 JSON 会造成：

- Git 历史永久保留凭据，即使后来删除。
- 截图、报告压缩包或聊天转发导致泄露。
- 多人共用同一 Key，无法追踪责任和撤销权限。
- 自动化日志可能打印完整命令。

企业通常把 Key 放进 Secret Manager、CI Secret 或运行时环境变量，并设置最小权限、轮换和
吊销机制。本项目使用环境变量，是本地实验里最小且合理的做法。

## 3. PowerShell 临时设置 `GROQ_API_KEY`

### 推荐：隐藏输入，避免进入命令历史

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

该变量只对当前 PowerShell 进程及其子进程有效。关闭窗口后通常消失。

### 简便写法

```powershell
$env:GROQ_API_KEY = "你的 Key"
```

这会把命令留在终端历史中，不适合截图或共享屏幕。不要把这行连同真实值写入脚本。

## 4. 验证变量是否生效，但不显示 Key

```powershell
if ([string]::IsNullOrWhiteSpace($env:GROQ_API_KEY)) {
  "GROQ_API_KEY 未设置"
}
else {
  "GROQ_API_KEY 已设置"
}
```

不要使用下面的命令截图：

```powershell
$env:GROQ_API_KEY
```

它会直接打印凭据。

## 5. 变量优先级

普通脚本满足通用需求：

1. 优先读取 `GROQ_API_KEY`。
2. 若缺失，可把 `OPENAI_API_KEY` 临时映射给当前子进程。
3. Key 从不进入 `--generator_options`。

安全版脚本增加 `-RequireGroqApiKey`，本次真实 Groq 实验只接受 `GROQ_API_KEY`，避免误用
另一个 Provider 的 Key。

## 6. 只验证鉴权和模型，不跑攻击

可以用 OpenAI-compatible 的模型列表接口做最小检查：

```powershell
$Headers = @{ Authorization = "Bearer $env:GROQ_API_KEY" }
$Models = Invoke-RestMethod `
  -Uri "https://api.groq.com/openai/v1/models" `
  -Headers $Headers `
  -Method Get
$Models.data.id | Sort-Object
```

这会消耗一次 API 请求，但不生成模型回答。不要打印 `$Headers`。

## 7. 企业里为什么分开配置三者

- Key 按环境和调用方轮换。
- base URL 按开发、测试、生产或供应商切换。
- model name 按成本、延迟、能力和安全基线切换。

三者分离后，同一评测脚本可在不同环境复用，而无需改攻击集和 Detector。

## 8. 和 Stage 2 的关系

Stage 2：

```text
Key = 本地假值
base_url = http://127.0.0.1:8000/v1/
model_name = stage2-vulnerable 或 stage2-guarded
```

Stage 3：

```text
Key = GROQ_API_KEY
base_url = https://api.groq.com/openai/v1
model_name = llama-3.1-8b-instant
```

改变的是连接参数和后端，garak 的 Probe、Detector 和 Report 流程没有改变。

## 9. 面试问答

**问：为什么只改 Key、base URL 和 model name 就能迁移？**

答：因为请求/响应契约保持为 OpenAI-compatible。Generator 仍然提交 `messages` 并读取
`choices[].message.content`，上层 Probe 和 Detector 不依赖供应商实现。

**问：环境变量绝对安全吗？**

答：不是。它比写入仓库更合适，但同一用户权限下的进程、崩溃转储或错误日志仍可能泄露。
企业应进一步使用密钥管理、短期凭据、权限隔离和日志脱敏。

## 10. 初学者误区

1. `OPENAI_API_KEY` 只是变量名，不会自动把请求发给 OpenAI。
2. `base_url` 不是模型名。
3. 模型网页显示名称不一定等于 API model ID。
4. 设置为“用户级永久环境变量”会扩大泄露面，本实验优先用会话级变量。

参考：

- [Groq OpenAI Compatibility](https://console.groq.com/docs/openai)
- [Groq Supported Models](https://console.groq.com/docs/models)

