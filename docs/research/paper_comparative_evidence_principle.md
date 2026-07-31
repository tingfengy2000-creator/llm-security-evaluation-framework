# 论文优先的外部对标与比较证据原则

*Paper-First Comparative Evidence Principle*

## 状态

- 决策状态：`ACCEPTED`。
- 生效日期：`2026-07-31`。
- 适用范围：Paper 1、Paper 2 以及以论文结论为目标的 Stage 6.1、Stage 6.2 研究任务。
- 优先级：论文研究方法中的最高优先级；安全、伦理、许可、Ground Truth/标签隔离、历史证据不可变等永久治理约束仍高于本文。
- 本次落地任务：`S6.1-LR1`。
- 正式实验状态：`FORMAL_EXPERIMENT = NOT STARTED`。

## 1. 原则

1. 先确认权威论文、官方源码和公开 Benchmark，再冻结内部实验协议。
2. 优先复现论文官方代码与公开数据；无官方源码的工作只能登记为 paper-guided reimplementation。
3. `Published Result`、`Reproduced Result` 与 `Our Method Result` 必须物理分栏、分别追溯，禁止混写。
4. 只有数据、attack budget、Retriever、Top-K、指标定义以及模型和配置尽可能一致时，才允许严格横向比较。
5. 自建数据集不能成为唯一实验依据；必须有 external benchmark track。
6. 每个核心创新必须同时回答：
   - Existing work 做了什么；
   - Existing work 缺什么；
   - 我们增加什么；
   - 哪个直接实验隔离并证明新增部分的效果。
7. 无源码论文不得冒充严格复现；必须标记 `PAPER_GUIDED_REIMPLEMENTATION`。
8. 复现失败必须登记 blocker。不同设置的数字不得被包装为超过 SOTA。
9. 论文实验必须同时报告 Safety、Utility、Efficiency、Reproducibility。
10. 自建 Benchmark 必须通过 external benchmark 验证泛化，降低“数据按方法设计”的偏差。

## 2. 证据状态

| 状态 | 含义 | 可否进入严格比较 |
| --- | --- | --- |
| `PUBLISHED_RESULT` | 来自正式论文或官方 artifact 的作者报告结果 | 仅作外部基准列 |
| `REPRODUCED_RESULT` | 我方按冻结协议独立运行并保存 manifest、日志和环境指纹 | 满足对齐门后可以 |
| `OUR_METHOD_RESULT` | 同一冻结协议下运行我方方法 | 满足对齐门后可以 |
| `ENGINEERING_SMOKE` | 只验证环境或代码链路可运行 | 不可以 |
| `UNKNOWN / TO_VERIFY` | 一手来源尚不能确认 | 不可以 |
| `BLOCKED` | 许可、数据、环境或协议条件未满足 | 不可以 |

任何表格都不得用空白表示未知；统一写 `UNKNOWN / TO_VERIFY`。

## 3. 严格比较资格门

一个结果只有同时满足以下条件，才能标记 `STRICT_COMPARISON_ELIGIBLE`：

- 数据集版本、split、预处理和许可记录一致；
- attack method、target selection、attack budget 和随机种子策略一致；
- Retriever、Embedding、相似度函数、索引和 Top-K 一致；
- Generator、prompt、temperature、decoding 和 API/model revision 尽可能一致；
- 指标公式、分母、聚合方式和人工/LLM judge 协议一致；
- 官方仓库 commit/tag、依赖锁和 compatibility patch 可追溯；
- 运行环境、GPU、RAM、disk、耗时和失败记录进入 Run Manifest；
- Published、Reproduced、Our Method 三类结果没有发生列替换或口径复用。

任一条件不满足时，只能标记 `NOT_ELIGIBLE` 或 `CONDITIONAL`，并列出差异。

## 4. 研究决策顺序

```text
authoritative paper
-> official repository and license
-> dataset and model terms
-> published protocol extraction
-> reproduction blocker review
-> frozen comparison protocol
-> engineering smoke
-> reproduced result
-> our method result
-> strict comparison eligibility review
```

任何一步的成功都不自动批准下一步。尤其是文献对齐、源码准备和 smoke test 不等于正式实验。

## 5. 与 LLMGuard 的关系

- S6-T5 提供已验收的透明检索与可追溯 Context 工程基线；它不是论文攻击、检测或结果基线。
- Paper 1 在外部对标后研究版本化知识库中的隐蔽事实污染检测。
- Paper 2 在 Paper 1 的威胁与证据基础上研究多证据可信检索、冲突感知和拒答。
- Ground Truth 只进入 Evaluator/GroundTruthVault，不得进入 Retriever、VectorStore、ContextBuilder、Detector inference feature 或公开 metadata。

## 6. 本轮边界

`S6.1-LR1` 只建立文献、Benchmark、源码、许可、硬件和复现对齐。它不运行 PoisonedRAG、GMTP 或 SafeRAG，
不生成数据，不训练 Detector，不创建结果表，不声称复现成功或优于任何论文。
