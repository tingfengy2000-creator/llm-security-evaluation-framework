# Stage 5 Paper 学习记录

## 已掌握

- A1-A6 与 Training/Retrieval/Runtime 的关系；
- Dataset Runner 与 garak scheduler 的区别；
- 官方 garak Detector API 的直接调用；
- P/I/O/F 四模式和 output-only 顺序；
- canonical audit 与 measurement sidecar；
- ASR、DMR、GBR、Over-block 和 latency 的分母。

## 仍需完成

- 真实 Groq Stage 5 Paper smoke；
- 每类扩展到更大数据集；
- 语义分类器与 LLM-as-judge 校准；
- 真实业务 benign 分布。

## 结论边界

当前离线 mock 只验证框架。A1/A2 不代表真实训练攻击，A6 不执行工具。

## 2026-07-01 离线实验

- execution_id：`20260701T081320Z-c29f39`
- 状态：completed
- 22 个样本、88 个 Attempt
- canonical log 与测试中的第二次运行字节一致
- ASR 95.83%、GBR 94.44%、Detector Coverage 8.33%、Over-block 0%
- DMR 0% 只适用于有官方 detector coverage 的分母
- 真实 Groq：not run
