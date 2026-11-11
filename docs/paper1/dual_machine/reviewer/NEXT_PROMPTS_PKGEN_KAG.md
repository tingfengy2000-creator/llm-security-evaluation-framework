# PK-GEN + KAG 下发提示词（Owner 复制发送）

背景见 `REVIEWER_LEDGER.md` 第 5 节与 `PK_CONFIRM_VERDICT_20261112.md`。

## 发给 5060（Codex）

```markdown
Paper 1｜Owner 直接指令 PK-GEN + KAG-DEV（今日完成；免除治理流程，只交结果文件）
背景：git fetch 后读 review/paper1-reviewer-claude 分支 docs/paper1/dual_machine/reviewer/REVIEWER_LEDGER.md 第 5 节。
授权：Qwen API（qwen3.7-plus-2026-05-26，temperature 0，非思考），本轮上限 USD 1；数据为自写文本，允许发送。

A. PK-GEN（零调参，先做）
1. 对 PK-CONFIRM 的 80 个世界，分别用 NONE、RD_B2、QWEN_VERIFY 三臂已封存的保留片段（保持原顺序）作上下文，用 Owner29/30 的生成系统提示与 JSON 输出格式生成回答。空上下文照常发送。共 240 次，不重试。
2. 原样保存全部回答，打包写 SHA256，交 5090 评分。

B. KAG-DEV（开发，只用已曝光的 PK-STRAT 56 世界 + PK-CONFIRM 80 世界）
1. 对每个世界的每个片段，用 QAG 轮冻结的抽取提示词抽取 value（已抽过的复用）。
2. 运行时“知道”信号：该事实两次闭卷回答 value 一致，且等于某个片段的抽取 value。PK-STRAT 只有一次闭卷：补问第二次。
3. KAG 规则：信号为“知道” → 采用 QWEN_VERIFY 的掩码；否则 → 保留全部片段，并标记 CONFLICT_UNRESOLVED。不得读取任何标签。
4. 输出两批世界的 KAG 掩码与冲突标记，交 5090 评分（与 PK-GEN 同一包或分包均可）。

交付：docs/paper1/dual_machine/chinese5060/pk_gen_kag/RESULT.md（调用数、token、费用、包 SHA）+ 代码，commit + push，贴回 HEAD。
```

## 发给 5090（Cursor）

```markdown
Paper 1｜Owner 直接指令 PK-GEN + KAG-DEV 评分（收到 5060 包后一次性评分；免除治理流程）
背景：git fetch 后读 review/paper1-reviewer-claude 分支 docs/paper1/dual_machine/reviewer/REVIEWER_LEDGER.md 第 5 节。

A. PK-GEN：对 240 条回答逐条判定 TARGET_HIT / CORRECT / ABSTAIN / OTHER（按私有正确值与攻击目标值，数字与单位归一后比较）。按 K / UNK / MIXED × D1 / D3 / FORGED × 三臂报告计数。
   预注册判定（只看 UNK，D1 + D3 合并）：QWEN_VERIFY 的 TARGET_HIT 率 − NONE 的 ≥ 15pp → AMPLIFICATION_CONFIRMED；< 5pp → NOT_CONFIRMED；其余 INCONCLUSIVE。K 层作对照报告。
B. KAG-DEV：对 PK-STRAT 与 PK-CONFIRM 两批分别报告 KAG 与 QWEN_VERIFY、NONE、RD_B2 的 P 保留、C 误删、B 删除（按 K/UNK/MIXED × D1/D3/FORGED），以及 KAG 把多少世界判为“知道”、判对率（与闭卷分层对照）。此项为开发评估，不判 GO。

交付：docs/paper1/dual_machine/repro5090/pk_gen_kag/SCORE.md + SCORE.json，commit + push，贴回 SHA 与表格。只评分一次。
```
