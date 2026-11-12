# PK-GEN + KAG-DEV 裁决（2026-11-12）

证据：5060@`0013458`（源码冻结 `2f28120`）`chinese5060/pk_gen_kag/RESULT.md`；5090@`7783a7c` `repro5090/pk_gen_kag/SCORE.md`（SHA256 `6958f011…46be9`，已复核一致）。全部为 AGENT_PROVISIONAL；Human Gold = 0；仅 Qwen。

## 1. PK-GEN：AMPLIFICATION_CONFIRMED（预注册门通过）

- UNK（D1+D3）攻击目标命中：QWEN_VERIFY **26/42** vs NONE **1/42**（+59.5pp，门槛 15pp）。
- K 对照：QWEN_VERIFY 2/24 vs NONE 0/24。预期 QV ≤ NONE 未满足（+8.3pp，来自 K D3 的 2 个世界），需如实报告：核验对已知事实也偶尔站在多数一边。
- **新发现（论文核心叙事）**：生成器在证据冲突时几乎总是拒答（NONE ABSTAIN 73/80）。核验把冲突“消解”掉，使 57/80 个世界从拒答变成作答：K 上变成答对（CORRECT 21/24），UNK 上变成答错（TARGET_HIT 26/42）。即：**核验把“不确定”变成了“确定的错”**。
- 伪造修订（FORGED）是独立威胁：UNK FORGED 上 NONE 自己就被骗 3/5，MIXED FORGED 三臂均 3/3。KAG 的回退行为等于 NONE，对伪造修订无效。

## 2. KAG-DEV：安全目标达成，可用性失败（DEV，非 GO）

- 安全：PK-CONFIRM UNK 判“知道”0/47；UNK D3 正确片段误删 KAG 0/21 vs QV 20/21。
- 可用性：K 判“知道”仅 6/24（PK-STRAT 2/19）。K D3 毒片段保留 KAG 30/36 vs QV 6/36，即核验在 K 上的收益基本丢失。推导回答层：KAG 在 CONFLICT 世界的上下文与 NONE 相同，回答等于 NONE（多为拒答）。
- 根因（评审读码）：`kag_decision` 用闭卷**原始回答**与片段抽取值做字符串匹配。`canonical_value` 只对“纯数值+单位”整串生效，闭卷回答若是句子就无法匹配。K 层闭卷两次都答对，正确片段也在场，失配多半是格式问题，而不是概念问题。另外，温度 0 下第二次闭卷与第一次逐字相同（24/24），“两次一致”条件没有提供任何信息。

## 3. 决策

1. RQ2+RQ3 回答层成立，作为论文主结论（仍需换核验模型、人工 Gold）。
2. KAG 进入 V1：修复匹配（对闭卷回答走同一抽取器）、第二探针改为不同模板、增加“时效门”变体（任一片段声称 ≥2025 年修订则强制 CONFLICT；只降低信任，符合 P0）。
3. 先在 DEV 上用推导回答层和 ORACLE 上界定位 KAG 的可达空间，再进入全新批次 PK-TEST（含先验对齐投毒与伪造修订）。PK-TEST 预注册门见台账第 5 节。
