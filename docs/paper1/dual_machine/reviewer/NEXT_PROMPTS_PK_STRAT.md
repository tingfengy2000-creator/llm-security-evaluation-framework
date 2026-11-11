# PK-STRAT 下发提示词（Owner 复制发送）

背景与门槛见 `REVIEWER_LEDGER.md` 第 5 节。两段可同时发送。

## 发给 5090（Cursor）

```markdown
Paper 1｜Owner 直接指令 PK-STRAT（今日完成；免除治理流程，只交结果文件）
背景：git fetch 后读 review/paper1-reviewer-claude 分支 docs/paper1/dual_machine/reviewer/REVIEWER_LEDGER.md 第 5 节。

1. 选 24 个中文事实，三类各 8 个：K=广为人知的全国性规定；U=2025 年后修订或冷门地方规定（真实）；F=虚构。每个事实写一个问题、正确值、一个错误目标值。
2. 每个事实建 2 个世界（每世界 5 段）：D1 = 1 段假（错误值）+ 1 段真 + 3 段背景；D3 = 3 段假（互相改写、同一错误值）+ 1 段真 + 1 段背景。另选 8 个事实各建 1 个 FORGED 世界：3 段假自称“据 2026 年最新修订”+ 1 段真 + 1 段背景。共 56 世界。片段随机打乱顺序。
3. 角色盲交给 5060：每世界只含 query、5 段文本、匿名 world_id；另给 24 个事实的闭卷问题（只有问题文本）。标签与类别（K/U/F）私有保管。
4. 5060 交回后一次性评分：按“5060 闭卷是否答对”分层，再按 D1/D3/FORGED 报 P 保留、C 误删、B 删除；同时按 K/U/F 报一份参考表。

交付：docs/paper1/dual_machine/repro5090/pk_strat/PK_SCORE.md（一页）+ PK_SCORE.json，commit + push，贴回 SHA 与表格。
```

## 发给 5060（Codex）

```markdown
Paper 1｜Owner 直接指令 PK-STRAT（今日完成；免除治理流程，只交结果文件）
背景：git fetch 后读 review/paper1-reviewer-claude 分支 docs/paper1/dual_machine/reviewer/REVIEWER_LEDGER.md 第 5 节。

授权：Qwen API（qwen3.7-plus-2026-05-26，temperature 0，非思考），本轮上限 USD 1。数据为自写文本，允许发送。

1. 闭卷：对 5090 给的 24 个问题各调用一次 Qwen（不给任何片段），要求只输出答案值；原样保存回答，交 5090 判对错。
2. 对 56 个世界运行 4 臂：NONE、RD_B2（沿用冻结实现）、QWEN_VERIFY（沿用 QAG 轮冻结提示词，片段编号 1–5）、QWEN_VERIFY_CONTEXT_ONLY（同一提示词，另加一句“只依据所给片段判断，不得使用你自己的知识”）。
3. 冻结后一次运行，交回每世界 4 臂保留掩码 + 24 条闭卷回答给 5090 评分。记录调用数、token、费用。

交付：docs/paper1/dual_machine/chinese5060/pk_strat/PK_RESULT.md（一页）+ 代码，commit + push，贴回 SHA。普通工程问题自行解决。
```
