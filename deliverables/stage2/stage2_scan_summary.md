# Stage 2 扫描总结

## 本阶段目标

Stage 2 的目标是把 garak 从 Stage 1 的内置 mock generator，推进到 OpenAI-compatible API 接入形态，并做一个防护前后对比：

- `stage2-vulnerable`：不安全基线，复述用户输入。
- `stage2-guarded`：简单防护基线，识别 prompt injection/编码绕过迹象后拒绝执行覆盖指令。

本阶段仍是 smoke test，不代表真实商业模型或生产 RAG/Agent 的最终安全结论。

## 扫描矩阵

| 模型 | Probe | 样本数 | 结果 | 说明 |
| --- | --- | ---: | --- | --- |
| `stage2-vulnerable` | `promptinject.HijackHateHumans` | 8 | FAIL 0/8 | echo 模型复述攻击触发词，100% 命中 |
| `stage2-guarded` | `promptinject.HijackHateHumans` | 8 | PASS 8/8 | 简单防护响应未包含攻击触发词 |
| `stage2-vulnerable` | `encoding.InjectBase64` | 8 | PASS 8/8 | echo 行为未触发 garak 的 Base64 detector |
| `stage2-guarded` | `encoding.InjectBase64` | 8 | PASS 8/8 | 防护响应未触发编码注入 detector |

## 本阶段证明的能力

### 1. OpenAI-compatible 接入

garak 使用 `openai.OpenAICompatible` generator 调用本地 `/v1/chat/completions` 接口。后续替换为真实 API 时，只需要修改：

- `OPENAICOMPATIBLE_API_KEY`
- `--generator_options` 中的 `uri`
- `--target_name`

### 2. 防护前后对比

Stage 1 只有一个完全脆弱的 mock model，所以 prompt injection 全成功。Stage 2 加入 guarded mock model 后，可以展示同一组攻击样本在不同防护策略下的差异：

- vulnerable：攻击触发词进入输出，detector 判定失败。
- guarded：输出不包含攻击触发词，detector 判定通过。

### 3. 攻击样本和模型请求可追溯

本阶段除了 garak `.report.jsonl`，还保存了 API 层请求日志：

- `D:\llmProject\deliverables\stage2\api_requests.jsonl`

这样可以从两个角度复盘：

1. garak 视角：probe、attempt、detector、eval。
2. API 视角：收到的 prompt、模型名、返回内容。

### 4. 评估边界说明

`encoding.InjectBase64` 两组都通过，并不说明真实模型一定安全。它只说明当前 mock API 的响应行为没有触发该 detector。真实模型可能会解码、执行或重述编码 payload，因此 Stage 3 应接入真实模型或更贴近真实行为的本地模型继续测试。

## 面试可讲结论

这一阶段可以这样讲：

> Stage 2 我把评测对象从 garak 内置 generator 切换到了 OpenAI-compatible API 形态。为了避免 API key 和费用风险，我先实现了本地 `/v1/chat/completions` mock 服务，并提供 vulnerable 与 guarded 两个模型名。对同一组 prompt injection 样本，vulnerable 模型 8/8 失败，guarded 模型 8/8 通过，说明我不仅能跑扫描，还能设计防护前后对照实验，并保留 API 请求日志和 garak 原始报告用于复盘。

## 下一阶段计划

Stage 3 建议接入更真实的被测目标：

1. 接入真实 OpenAI-compatible API，例如 OpenAI、DeepSeek、OpenRouter、Ollama 或 vLLM。
2. 使用小样本 smoke test 控制成本，例如每个 probe 8 到 20 条。
3. 增加 RAG/Agent 风险：system prompt extraction、web injection、tool misuse、data exfiltration。
4. 建立结果对比表：模型、probe、样本数、失败数、攻击成功率、代表性失败案例。
5. 将失败案例转化为防护策略，例如输入净化、上下文隔离、工具调用 allowlist、输出检测与拒答策略。
