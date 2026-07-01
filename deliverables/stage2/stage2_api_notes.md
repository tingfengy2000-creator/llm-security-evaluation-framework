# Stage 2 OpenAI-compatible API 接入说明

## 实验记录基准

- 参考实验计划：`E:\CodeGuarder\docs\experiment_plan.md`
- 本阶段：Stage 2，OpenAI-compatible API 形态接入与安全扫描对比
- 记录原则：说明为什么做、改哪里、是否影响原始数据、怎么验证

## 为什么做

Stage 1 使用 garak 内置 mock generator，证明了安全评测链路能跑通。Stage 2 进一步把被测对象切换为 OpenAI-compatible API 形态，让 garak 通过 `/v1/chat/completions` 调用模型。这更接近真实项目中接入 OpenAI、OpenRouter、DeepSeek、Ollama、vLLM 等服务的方式。

由于当前没有提供真实 API key，本阶段使用本地 mock OpenAI-compatible 服务替代真实外部服务，避免网络、费用和密钥泄漏风险。

## 改了哪里

新增本地兼容 API：

- `D:\llmProject\llm-security-stage1\scripts\mock_openai_compatible_api.py`

新增 Stage 2 garak smoke test 配置：

- `D:\llmProject\llm-security-stage1\config\stage2_garak_smoke.yaml`

新增 Stage 2 复跑脚本：

- `D:\llmProject\llm-security-stage1\scripts\run_stage2_scan.ps1`

## API 设计

本地 API 监听：

- Base URL：`http://127.0.0.1:8000/v1/`
- Models endpoint：`/v1/models`
- Chat completions endpoint：`/v1/chat/completions`

支持两个模型名：

- `stage2-vulnerable`：故意脆弱的 echo 模型，会复述用户输入，用于构造不安全基线。
- `stage2-guarded`：带简单规则防护的 mock 模型，检测到 prompt injection 或编码绕过迹象时返回拒绝/忽略覆盖指令的响应。

API 请求日志：

- `D:\llmProject\deliverables\stage2\api_requests.jsonl`

## 是否影响原始数据

不影响。所有 Stage 2 文件都写入：

- `D:\llmProject\llm-security-stage1`
- `D:\llmProject\deliverables\stage2`

没有覆盖 `E:\CodeGuarder` 中的原始论文复现实验数据。

## 实验调整记录

第一次直接使用 garak 默认配置运行 `promptinject.HijackHateHumans` 时，默认样本上限为 256。OpenAI-compatible 客户端逐条请求，本地 smoke test 在 5 分钟内未完成。因此 Stage 2 明确改为 smoke test，并通过独立配置将每个 probe 限制为 8 条样本：

```yaml
run:
  generations: 1
  soft_probe_prompt_cap: 8
```

这个调整不改变实验目标：Stage 2 只验证 OpenAI-compatible 接入形态、防护前后对比和数据留存方式，不做全量模型评测。
