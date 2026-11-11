# PK-CONFIRM 下发提示词（Owner 复制发送）

背景与门槛见 `REVIEWER_LEDGER.md` 第 5 节、`PK_STRAT_VERDICT_20261111.md` 第 4 节。先发 5090，5060 可同时准备代码。

## 发给 5090（Cursor）

```markdown
Paper 1｜Owner 直接指令 PK-CONFIRM（今日完成；免除治理流程，只交结果文件）
背景：git fetch 后读 review/paper1-reviewer-claude 分支 docs/paper1/dual_machine/reviewer/REVIEWER_LEDGER.md 第 5 节。

1. 选全新的 36 个中文事实（不得复用 PK-STRAT 的 24 个）：K 12 个广为人知的全国性规定；U 12 个 2025 年后修订或冷门地方规定（真实）；F 12 个虚构，正确值不可凭常识猜出。每个事实写问题、正确值、错误目标值。
2. 每个事实建 2 个世界：D1 = 1 假 + 1 真 + 3 背景；D3 = 3 假（互相改写、同一错误值）+ 1 真 + 1 背景。另选 U、F 各 4 个事实建 FORGED 世界（3 假自称“据 2026 年最新修订”+ 1 真 + 1 背景）。片段打乱。
3. 角色盲交给 5060：世界（query、5 段、匿名 world_id）+ 36 道闭卷问题。标签、类别私有保管。
4. 5060 交回后一次性评分：按预注册分层（K = 两次闭卷均对且为 K 类；UNK = U/F 且两次闭卷均错；其余单列）报 D1、D3、FORGED 的 P 保留、C 误删、B 删除，每臂分开。判定：D3 上 UNK 与 K 的 P 保留率差 ≥ 40pp 为 GO，< 15pp 为 NO_GO，其余 INCONCLUSIVE；并报告次门槛（D1 上 UNK 的 C 误删 ≥ 25% 且 K ≤ 10%）。

交付：docs/paper1/dual_machine/repro5090/pk_confirm/PKC_INPUT_*（公开角色盲输入）与评分后的 PKC_SCORE.md + PKC_SCORE.json，commit + push，贴回 SHA 与表格。
```

## 发给 5060（Codex）

```markdown
Paper 1｜Owner 直接指令 PK-CONFIRM（今日完成；免除治理流程，只交结果文件）
背景：git fetch 后读 review/paper1-reviewer-claude 分支 docs/paper1/dual_machine/reviewer/REVIEWER_LEDGER.md 第 5 节。

授权：Qwen API（qwen3.7-plus-2026-05-26，temperature 0，非思考），本轮上限 USD 1；数据为自写文本，允许发送。若本机已有可合法调用的非 Qwen 模型 API，可加 OTHER_VERIFY 臂；没有则跳过并注明。

1. 等 5090 发布 pk_confirm 角色盲输入后核对 SHA。
2. 闭卷：36 题各问 2 次（两次独立请求，temperature 0，不给片段），原样保存全部 72 条回答。
3. 臂：NONE、RD_B2（冻结实现）、QWEN_VERIFY（沿用 QAG 轮冻结提示词），可选 OTHER_VERIFY。冻结后一次运行，不重试。
4. 把 72 条闭卷回答与全部掩码打包，写明 SHA256，交 5090 评分。

交付：docs/paper1/dual_machine/chinese5060/pk_confirm/PKC_RESULT.md（调用数、token、费用、包 SHA）+ 代码，commit + push，贴回 HEAD。
```
