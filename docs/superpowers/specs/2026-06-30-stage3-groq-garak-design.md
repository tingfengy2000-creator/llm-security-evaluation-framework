# Stage 3 Groq Garak Design

## 1. 目标

在现有 Stage 2 本地 OpenAI-compatible Mock API 实验之上，增加一个真实模型评测阶段：

```text
garak
  -> garak.generators.groq.GroqChat
  -> OpenAI Python client
  -> https://api.groq.com/openai/v1/chat/completions
  -> Groq 托管的真实 LLM
  -> garak Detector
  -> JSONL / HTML / 聚合 JSON / 中文总结
```

Stage 3 不修改 Stage 1、Stage 2 的脚本和原始结果，只新增独立脚本、配置和交付目录。

## 2. 选型

采用 garak 0.15.1 自带的 `groq.GroqChat` Generator，而不是直接使用通用
`openai.OpenAICompatible`。

原因：

1. `GroqChat` 继承 `OpenAICompatible`，仍然展示 OpenAI-compatible 协议的复用价值。
2. 它已把 `base_url` 设为 `https://api.groq.com/openai/v1`。
3. 它已屏蔽 Groq 不支持或受限的 OpenAI 请求参数，例如 `n`、部分 penalty 和 logprob 参数。
4. 它使用 `GROQ_API_KEY`，与 Groq 官方命名一致。
5. garak 的 OpenAI-compatible 基类已对 429、超时、连接错误和部分 5xx 错误使用退避重试。

脚本优先读取 `GROQ_API_KEY`。为满足最初的通用接口要求，允许在
`GROQ_API_KEY` 缺失时显式使用 `OPENAI_API_KEY` 作为后备，并仅在当前 PowerShell
子进程中临时映射为 `GROQ_API_KEY`。本次真实实验必须使用 `GROQ_API_KEY`，不会使用
当前机器上的 `OPENAI_API_KEY` 代替。

## 3. 文件边界

新增：

```text
llm-security-stage1/
  config/
    stage3_garak.yaml
    stage3_garak_safe.yaml
  scripts/
    run_stage3_groq_scan.ps1
    run_stage3_groq_scan_safe.ps1

deliverables/stage3/
  00_stage3_overview.md
  01_groq_api_setup.md
  02_garak_groq_run_commands.md
  03_probe_explanation.md
  04_result_interpretation.md
  05_mock_vs_real_api.md
  06_troubleshooting.md
  07_interview_talking_points.md
  groq_scan_result.json
  groq_scan_summary.md
  screenshots/README.md
```

同时更新：

```text
deliverables/learning_notes.md
E:/CodeGuarder/docs/experiment_plan.md
```

`experiment_plan.md` 位于当前可写工作区之外，写入时需要单独授权。

## 4. 普通版与安全版

普通版：

- 默认模型：`llama-3.1-8b-instant`。
- probes：`promptinject.HijackHateHumans`、`encoding.InjectBase64`。
- 每个 prompt 生成 1 个回答。
- 每个 probe 最多抽样 8 个 prompt。
- 使用较低并发，不追求压满免费额度。

安全版：

- 同样覆盖两个 probes。
- 每个 probe 最多抽样 1 个 prompt。
- `parallel_attempts=1`、`parallel_requests=1`，完全串行。
- 每个 prompt 只生成 1 个回答。
- 适合作为 API Key、模型名、网络和报告链路的 smoke test。

garak 0.15.1 没有“每次请求后固定睡眠 N 秒”的 CLI 参数。安全版通过限制
`soft_probe_prompt_cap`、`generations` 和并发数控制请求量；遇到 429 时由
OpenAI-compatible Generator 的 Fibonacci backoff 处理。文档会明确说明退避重试不等于
主动限速。

## 5. 结果设计

garak 原生输出保留为：

- `*.report.jsonl`：逐事件、逐 Attempt 的审计证据。
- `*.report.html`：人工浏览报告。
- `*.hitlog.jsonl`：只在存在命中时生成的失败样本。
- `garak.log`：运行与异常日志。

脚本在两个 probe 都结束后，从 JSONL 中读取 `entry_type=eval` 的记录，生成：

- `groq_scan_result.json`：机器可读的运行元数据和每个 probe 的通过/失败计数。
- `groq_scan_summary.md`：中文结果摘要、ASR、解释边界和原始证据路径。

API Key 不进入参数 JSON、报告、日志、截图说明或聚合结果。

## 6. 错误处理

脚本在发送请求前检查：

1. garak 可执行文件是否存在。
2. `GROQ_API_KEY` 或后备变量是否存在。
3. 输出目录是否可写。
4. 模型名和 probe 参数是否为空。

Generator 参数写入本次运行目录中的 `generator_options.json`，再通过
`--generator_option_file` 交给 garak。这样可以避免 Windows PowerShell 5.1 在原生进程参数
边界破坏内联 JSON 引号。该文件只包含 base URL、temperature、max tokens 和随机性设置，
不包含 API Key。

任一 garak 子进程退出码非 0 时，脚本立即停止，不伪造成功结果。已经产生的原始日志保留，
用于判断是 401、403、404、429、超时还是参数不兼容。

## 7. 验证策略

不泄露 Key 的离线验证：

1. PowerShell 语法解析。
2. 缺少 Key 时应快速失败，且错误信息不包含任何凭据。
3. garak `--list_generators` / `--plugin_info` 验证 `groq.GroqChat` 存在。
4. 配置文件通过 garak `--list_config` 加载。
5. 文档、目录和必需字段完整性检查。
6. 对仓库执行敏感信息模式扫描。

真实验证：

1. 当前进程可见 `GROQ_API_KEY`。
2. 先运行安全版，共最多 2 次模型请求。
3. 检查两个原始 JSONL、HTML、聚合 JSON 和 summary。
4. 安全版成功后，用户再决定是否运行普通版。

## 8. 当前已知约束

- 当前 Codex 执行进程检测结果为 `GROQ_API_KEY_set=False`。
- 因此在变量可见之前不能诚实地声称真实 Groq 扫描已经完成。
- 当前目录不是 Git 仓库，设计文档无法按技能流程提交 commit；这不影响文件交付。
- Groq 模型和免费额度会变化，文档以 Groq 控制台中的实时 Limits 和 Models 页面为准。
