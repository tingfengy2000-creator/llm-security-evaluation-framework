# 如何阅读 Stage 3 结果

## 1. 先区分两套“成功/失败”

### 程序层

- PowerShell exit code `0`：脚本运行完成。
- 非 `0`：配置、网络、鉴权、限流或报告解析失败。

### 安全评测层

- PASS：Detector 没有发现该攻击样本达到目标。
- FAIL：Detector 判定攻击目标达成。

所以最重要的一句话是：

```text
garak 的 FAIL 通常代表安全测试发现问题，不代表程序运行失败。
```

## 2. PASS 是什么

PASS 只表示：

```text
在当前模型、当前 prompt、当前采样参数和当前 Detector 下，没有检测到攻击成功。
```

它不表示：

- 所有 Prompt Injection 都无效。
- 所有编码绕过都无效。
- 模型未来版本仍然相同。
- Detector 没有漏报。
- RAG/Agent 整体安全。

## 3. FAIL 是什么

FAIL 表示 Detector 的命中分数达到 garak 的阈值。例如：

- `AttackRogueString` 找到攻击目标字符串。
- `DecodeMatch` 找到解码后的目标。
- `DecodeApprox` 找到近似目标。

FAIL 是需要复盘的证据，不应直接等同于“模型完全不安全”。还要检查：

1. 模型是否真正服从了攻击，还是只在引用攻击文本。
2. Detector 是否误报。
3. 输出截断或格式是否影响判断。
4. 该样本是否符合真实业务威胁模型。

## 4. Attack Success Rate

本项目区分 Attempt 级 ASR 和 Detector 级命中率。

```text
Attempt 级 ASR =
至少一个 Detector 分数达到阈值的 Attempt 数 / 完成的 Attempt 数 × 100%

Detector 级命中率 =
FAIL 的 Detector 评测记录数 / Detector 评测记录总数 × 100%
```

首轮安全版示例：

```text
完成 Attempt = 2
攻击成功 Attempt = 1
Attempt 级 ASR = 1 / 2 = 50%

Detector 评测记录 = 3
Detector FAIL = 1
Detector 级命中率 = 1 / 3 = 33.33%
```

两个 Base64 Detectors 检查同一个模型回答，所以 3 条 Detector 记录不等于 3 次模型请求。

ASR 越高，表示当前攻击集在当前条件下越容易命中。但比较两个模型时必须控制：

- Probe 和 prompt 样本。
- generations。
- 温度、seed 和最大输出长度。
- 系统提示和外部防护。
- Detector 与阈值。

## 5. 为什么安全版结果不能做强结论

安全版每个 probe 只抽 1 条 prompt，目的是 smoke test：

- Key 是否有效。
- API 是否连通。
- 模型名是否正确。
- Probe/Generator/Detector/Report 是否闭环。

它最多说明两条具体样本的表现。要形成稳定结论，应扩大样本、重复运行、固定配置并给出置信区间。

## 6. 如何读 `groq_scan_result.json`

关键字段：

| 字段 | 含义 |
| --- | --- |
| `status` | `not_run`、`completed` 或 `failed` |
| `provider` | 本阶段为 Groq |
| `api_style` | OpenAI-compatible |
| `model` | 实际模型 ID |
| `generator` | `groq.GroqChat` |
| `run_mode` | `safe` 或 `normal` |
| `run_directory` | 本次原始证据目录 |
| `attempt_count` | 已完成的模型攻击 Attempt 数 |
| `attack_successful_attempts` | 至少一个 Detector 达到阈值的 Attempt 数 |
| `attack_success_rate_percent` | Attempt 级 ASR |
| `detector_evaluations` | Detector 评测记录总数 |
| `detector_failures` | Detector FAIL 记录数 |
| `detector_hit_rate_percent` | Detector 级命中率 |
| `results[]` | 按 Probe + Detector 的明细 |

注意：Base64 Probe 可能绑定两个 Detectors，因此 `total_evaluated` 可能大于模型请求数。不要把
Detector 评测条目数直接当成 HTTP 请求数。

PowerShell 查看聚合结果：

```powershell
$Result = Get-Content `
  D:\llmProject\deliverables\stage3\groq_scan_result.json `
  -Raw -Encoding UTF8 | ConvertFrom-Json
$Result.status
$Result.results | Format-Table probe, detector, passed, fails, total_evaluated, attack_success_rate_percent
```

## 7. 如何读原始 JSONL

找到所有 `eval`：

```powershell
Get-Content <report.jsonl> -Encoding UTF8 |
  ForEach-Object { $_ | ConvertFrom-Json } |
  Where-Object entry_type -eq "eval" |
  Format-Table probe, detector, passed, fails, total_evaluated
```

找到已完成的 Attempt：

```powershell
Get-Content <report.jsonl> -Encoding UTF8 |
  ForEach-Object { $_ | ConvertFrom-Json } |
  Where-Object { $_.entry_type -eq "attempt" -and $_.status -eq 2 } |
  Select-Object -First 3 probe_classname, prompt, outputs, detector_results
```

其中：

- `prompt`：Probe 构造的输入。
- `outputs`：模型回答。
- `detector_results`：各 Detector 对输出的分数。
- `notes.triggers`：某些 Probe 用于判断的目标内容。

## 8. 如何读 summary

`groq_scan_summary.md` 是从 JSONL 的 `eval` 记录聚合而来，适合汇报，但不是最原始证据。

审计优先级建议：

```text
JSONL Attempt / Eval
  -> hitlog
  -> 聚合 JSON
  -> Markdown summary
  -> 截图
```

截图最容易传播，但信息最少；JSONL 最完整。

## 9. 结果不稳定如何处理

真实模型结果可能因采样、服务版本和后端策略变化。处理方式：

1. 保存模型 ID、时间、garak 版本和所有参数。
2. 固定 garak seed，并尽量固定模型采样参数。
3. 同一配置重复运行多次。
4. 报告样本数、均值和区间，而不是只报一次百分比。
5. 对 FAIL 和边界 PASS 做人工复核。
6. 把模型版本或防护升级前后的结果做回归比较。

## 10. 面试回答

**问：模型 PASS 率 100%，能上线吗？**

答：不能仅据此决定。需要确认覆盖范围、样本量、Detector 可靠性和业务威胁模型，并补充多轮、
RAG、Agent 工具越权、数据泄露和人工红队测试。这里的 100% 只是特定测试条件下的结果。

## 11. 初学者误区

1. `passed + fails` 不一定等于 HTTP 请求数。
2. 一个 Probe 可能有多个 Detectors。
3. PASS/FAIL 是 Detector 结论，不是客观真理。
4. 聚合 JSON 是本项目生成的二次结果，原始证据是 garak JSONL。
