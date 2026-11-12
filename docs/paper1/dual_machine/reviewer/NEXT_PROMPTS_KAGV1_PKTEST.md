# 下一轮提示词：KAG-V1（DEV）+ PK-TEST 阶段 1

依据：`PKGEN_KAG_VERDICT_20261112.md`。5060 与 5090 可并行。预算本轮上限 USD 1。禁止：读私有标签（5060）、碰 D2/D3、提交密钥或原始私有日志、force push。

## 发给 5060

```
读 review/paper1-reviewer-claude 的 REVIEWER_LEDGER.md 与 PKGEN_KAG_VERDICT_20261112.md。本轮做 KAG-V1 开发，只用 PK-STRAT(56) + PK-CONFIRM(80) 两个已曝光面板，不读任何标签。

1. 无标签诊断：对 136 个世界，统计 KAG v0 判 CONFLICT 的原因：A 闭卷答案无法归一（canonical=None 或非数值整串）、B 两次闭卷不一致、C 闭卷值与所有片段抽取值都不相等。给计数，并附 ≤20 个“闭卷原话 → 归一值 / 片段归一值集合”的样例（只含答案值，不含角色）。
2. V1 修复，冻结后一次性运行：
   a) 闭卷回答先过与片段相同的 QAG 抽取器，得到闭卷值，再与片段值比较；
   b) 第二探针换一个不同的提示模板（例如要求 JSON {"value":…,"unit":…}），不再重复同一请求；PK-STRAT 与 PK-CONFIRM 都补跑这一探针；
   c) 归一只按诊断结果做最小扩充（中文数字、万、全半角、日/天），不加语义近似；
   d) 输出两个变体：KAG-V1 = a+b+c；KAG-V1T = V1 + 时效门（任一片段文本出现 ≥2025 年的修订/施行年份 → 强制 CONFLICT_UNRESOLVED），正则在运行前写死。
3. 掩码规则不变：KNOWS → QWEN_VERIFY 掩码；CONFLICT → 保留全部 5 段。
4. 结果写 chinese5060/kag_v1/RESULT.md：诊断计数、两变体的 KNOWS 数、调用数与费用。私有包（两变体掩码、信号、闭卷原话、请求封存单）交 5090，写明 SHA256。不做生成调用。
```

## 发给 5090

```
读 review/paper1-reviewer-claude 的 REVIEWER_LEDGER.md 与 PKGEN_KAG_VERDICT_20261112.md。本轮三件事，模型调用 0 次。

1. 立刻做（零调用）：PK-CONFIRM 推导回答层。KAG v0 的 CONFLICT 世界上下文与 NONE 相同，回答取 NONE；KNOWS 世界回答取 QWEN_VERIFY。另算 ORACLE 上界（按闭卷层：K→QWEN_VERIFY 回答，UNK→NONE 回答）。按 K/UNK × D1/D3/FORGED 报 TARGET_HIT/CORRECT/ABSTAIN。注明“推导值，依赖 temperature 0 下相同上下文得相同回答”。
2. 收到 5060 的 KAG-V1 包后一次性评分：两变体在两面板上的 K 判知道率、UNK 判知道率、P 保留、C 误删，以及与第 1 项相同的推导回答层。DEV 参考线（不是 GO 门）：PK-CONFIRM K 判知道 ≥18/24 且 UNK 判知道 ≤2/47。
3. PK-TEST 阶段 1：准备全新事实批次，不与以往任何批次重复。K 12、U 18（2025 年后修订或冷门的真实中文规定）、F 12。本阶段只公开问题文本（无标签、无答案），交 5060 跑闭卷；私有保管正确值。阶段 2 再根据闭卷结果构造世界，设计为 D1、D3、FORGED，以及新设计 PA（先验对齐投毒：对模型闭卷一致答错的事实，攻击目标值取模型的闭卷答案）。
```

## 之后的顺序（不需本轮下发）

5060 冻结 KAG 版本 → 跑 PK-TEST 闭卷 → 5090 构造世界（含 PA）→ 5060 四臂掩码 + 生成 → 5090 一次性评分，预注册门见台账第 5 节。
