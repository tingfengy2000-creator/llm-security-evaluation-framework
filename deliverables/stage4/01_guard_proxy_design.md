# Guard Proxy 设计详解

## 1. 组件职责

### HTTP Handler

负责 OpenAI-compatible HTTP 边界：

- 解析 JSON。
- 校验路径和请求大小。
- 返回 JSON 与 HTTP 状态码。
- 不包含具体安全规则。

### GuardEngine

负责纯规则判断：

```text
文本 -> 命中的规则名 -> blocked true/false
```

它不访问网络，因此可以快速单元测试。

### ProxyService

负责串联业务流程：

```text
Input Guard
  -> 是否调用上游
  -> Output Guard
  -> 构造最终响应
  -> 形成审计记录
```

### Upstream Client

使用已安装的 OpenAI Python client：

```python
openai.OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)
```

Key 只进入 client，不进入 Guard 日志。

## 2. OpenAI-compatible 接口

### Chat Completions

```text
POST /v1/chat/completions
```

请求至少包含：

```json
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    {"role": "user", "content": "hello"}
  ]
}
```

无论返回上游回答还是 Guard refusal，响应都保留：

```text
id
object=chat.completion
created
model
choices[0].message.role
choices[0].message.content
finish_reason
usage
```

### Health

```text
GET /health
```

PowerShell 编排不会固定睡眠两秒，而是轮询健康接口，确认进程真的已经监听且 mode 正确。

### Models

```text
GET /v1/models
```

返回当前配置的模型 ID，便于兼容客户端做最小发现。

## 3. 为什么复用标准库 HTTP Server

Stage 2 已使用 `ThreadingHTTPServer`，Stage 4 继续复用：

- 无需安装 FastAPI/Uvicorn。
- 依赖少，面试时容易讲清请求生命周期。
- 足够支持本地低并发实验。

生产环境不应直接使用这一实现，需要成熟 ASGI/WSGI 服务、鉴权、TLS、监控、进程管理和限流。

## 4. 上游参数兼容

garak 的通用 `openai.OpenAICompatible` 可能发送 Groq 不支持的可选参数。Proxy 在转发前移除：

```text
n
frequency_penalty
presence_penalty
logprobs
logit_bias
top_logprobs
```

两组 Proxy mode 都执行相同字段处理，因此不会成为 A/B 差异。

## 5. 日志结构

每个请求记录：

| 字段 | 用途 |
| --- | --- |
| `timestamp` | UTC 时间 |
| `request_id` | 本地请求关联 ID |
| `mode` | passthrough/guarded/消融模式 |
| `model` | 模型 ID |
| `prompt_sha256` | 验证样本一致性 |
| `prompt_preview` | 有界人工复盘 |
| `input_matches` | 输入规则名 |
| `input_action` | allow/block/error |
| `upstream_called` | 是否消耗真实模型请求 |
| `stripped_upstream_fields` | 兼容层移除字段 |
| `output_matches` | 输出规则名 |
| `final_action` | passthrough/input_block/output_block/allow/error |
| `latency_ms` | 代理处理耗时 |

不记录：

- API Key。
- Authorization header。
- 完整 HTTP headers。
- 无上限的 prompt 或 output。

## 6. 错误策略

| 问题 | 返回 |
| --- | --- |
| JSON 非法 | OpenAI-style 400 |
| messages 缺失 | OpenAI-style 400 |
| stream=true | 400，本 baseline 不支持流式检查 |
| Groq 401/429 等 | 对应 HTTP 状态 + 脱敏错误 |
| 网络/超时 | 502 |
| Guard 内部异常 | 500，并记录 error_type |

Guard 自身异常不会静默放行，因为安全边界出现未知错误时 fail-open 风险较高。

## 7. 测试边界

离线测试使用 Fake OpenAI Client：

- 验证输入拦截时上游调用次数为 0。
- 验证输出拦截会替换危险文本。
- 验证 passthrough 原样保留回答。
- 验证日志不含凭据。

本地 HTTP 测试使用随机端口，不访问 Groq。

