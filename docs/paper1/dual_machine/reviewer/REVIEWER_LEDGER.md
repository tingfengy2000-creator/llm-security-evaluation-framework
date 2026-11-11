# Paper 1｜评审与临时负责人台账（Reviewer Ledger）

本文件是 Paper 1 当前研究判断的**单一接手入口**。任何接手者（GPT 网页版、Claude、5060 Codex、5090 Cursor）先读本文件，再按文末链接读原始报告。只记录结论、证据位置与下一步，不复制原始数据。

- 分支：`review/paper1-reviewer-claude`（只放 `docs/paper1/dual_machine/reviewer/`，不改其他分支文件，避免与 5060/5090 冲突）
- 维护者：Claude（独立技术评审，2026-11-11 起受 Owner 委托临时指挥 5060/5090）
- Owner 指令（2026-11-11）：本轮免除授权、登记、台账同步等治理流程；保留本台账，保证 GPT 可随时无缝接管；机器间只用 Git 交互，Owner 负责下发提示词。

## 1. 角色

| 角色 | 职责 |
| --- | --- |
| Owner（用户） | 最终决策；把提示词发给 5060/5090；转发结果 |
| 评审/临时负责人（Claude） | 读 Git、裁决、写下一步提示词、维护本台账 |
| GPT 网页版 | 原主控；可随时按本台账接管 |
| 5060 Codex | 中文方法实现、本地运行、Qwen 调用 |
| 5090 Cursor | 独立选题/盲评输入、私有标签保管、一次性评分；RAGDefender 原论文复现（Claims 1–3 仍 NOT_RUN） |

## 2. 当前状态（2026-11-12 01:00 JST）

- **RQ3：PK-CONFIRM 预注册 GO。** LLM 核验的裁决来自参数知识；对模型不知道的事实，核验站在多数一边并删掉正确证据（UNK D3：P 保留 58/63，C 误删 20/21；K D3：6/36、2/12）。见 `PK_CONFIRM_VERDICT_20261112.md`。
- **论文主线（评审建议）：** 中文版本敏感污染基准 + RAGDefender 中文失效 + “LLM 核验继承知识边界并放大攻击” + 知识感知门控防御（KAG，开发中）。
- **下一步：** 第 5 节 NEXT_ACTION = PK-GEN（回答层确认）+ KAG 开发。
- **不可宣称：** 正式 ASR、答案准确率、统计显著性、“优于 RAGDefender 原论文”、跨模型普适（只测了 Qwen）。所有数字为 AGENT_PROVISIONAL 候选级。

## 3. 关键事实（只记录已封存、可复核的数字）

| 轮次 | 结论 | 关键数字 | 证据（分支@提交 · 文件） |
| --- | --- | --- | --- |
| G0–G2 基线 | B2 大量误删 | D1 36 世界：B2 删 81/180，Clean 误删 4/10 | 5060 · `REVIEWER_S0_S4_SUMMARY.md` |
| S0 诊断 | 英文 TF-IDF 未适配中文 | 12/36 世界误入“多数是假页”分支；W1/W2/W4 确认 | 5060 · 同上 |
| VESA v0.1/v0.2 | 0 变化 | 0/36、0/36 | 5060 · `vesa_guard_v01/`、`vesa_guard_v02/` |
| 规则抽取 | NO_GO | 新数据命中 5/70，严格绑定 0/320 | 5060 · `vesa_guard_reviewer_replan/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_RESULT.md` |
| Owner25 合成收据 | 收益来自收据，版本模块 0 | HN 误删两臂均 12/28 | 5060 · `OWNER25_SCIENCE_FIRST_RESULT.md` |
| Owner26 Qwen 七臂 | BLOCKED（治理门） | Qwen 调用 0 | 5060 · `OWNER26_D1_QWEN7_RESULT.md` |
| Owner27 联合门控 | 与简单收据规则相同 | Clean 误删均 29/63 | 5060 · `OWNER27_OFFLINE_FASTTRACK_RESULT.md` |
| Owner30 回答层 | 无防御攻击不成功；RD_ZH 诱发命中 | 目标命中 NONE 0/22、B2 0/22、RD_ZH 5/22 | 5060 · `OWNER30_FEASIBILITY_CLOSURE_SUPERVISOR_REVIEW_20261111.md` |
| Owner31 Q-CER | NO_GO | 与 B2 掩码 32/32 相同 | 5060 · `OWNER31_QCER_DEV_RESULT.md` |
| Owner33 V-CARE | 独立评估 NO_GO | 意图识别 0/32，掩码变化 0/32 | 5060 · `OWNER33_FRESH_EVAL_SUPERVISOR_VERDICT_20261111.md` |
| **QAG（本轮）** | **QAG NO_GO；QWEN_VERIFY 全面胜 RD_B2** | 测试 P 保留 QAG 53/62、VERIFY 23/62、B2 27/62；C 误删 7/118、2/118、73/118；抽取 175/179 | 5060@`30eb9d6` · `chinese5060/qag/QAG_RESULT.md`；5090@`22ae2b1` · `repro5090/qag_eval/QAG_SCORE.md` |
| QAG 面板拆分 | VERIFY 多数污染收益仅在真实法规面板 | 3/5：真实 0/9 vs 虚构 14/15；1/5：两面板均 0 | 本分支 · `QAG_VERDICT_20261111.md` |
| PK-STRAT | INCONCLUSIVE（预注册）；方向支持 | 3/5 合并：闭卷错 30/36 vs 闭卷对 30/60；D3 按类别 K 3/24 vs U/F 24/24；“只看片段”指令仅改 3/56 世界 | 5090@`c69adc5` · `repro5090/pk_strat/PK_SCORE.md`；本分支 · `PK_STRAT_VERDICT_20261111.md` |
| **PK-CONFIRM** | **GO（预注册）** | D3 P 保留 UNK 58/63 vs K 6/36（差 75pp）；D1 C 误删 UNK 18/21 vs K 0/12；UNK D3 核验误删正确片段 20/21 | 5090@`60a1727` · `repro5090/pk_confirm/PKC_SCORE.md`；本分支 · `PK_CONFIRM_VERDICT_20261112.md` |

## 4. 决策记录

| 日期 | 决策 | 理由 |
| --- | --- | --- |
| 11-05 | 受限恢复（v0.2 Rescue）降级为对照 | 恢复条件恰好是隐蔽污染满足的条件 |
| 11-06 | 增加 RD-zh 公平基线；S0 先行 | 区分中文迁移问题与方法贡献 |
| 11-11 | 停止 Q-CER、V-CARE、候选 A | 均未胜过同预算基线；候选 A 新颖性不足 |
| 11-11 | 给“Qwen 抽取 + 答案分组”最后一次机会 | Owner 决定；免除治理流程 |
| 11-11 | **QAG NO_GO；转向“LLM 核验在未知事实上的失效”** | 见 `QAG_VERDICT_20261111.md` |
| 11-11 | PK-STRAT INCONCLUSIVE → 做 PK-CONFIRM，不改写本批口径 | 预注册门未达，最强信号来自事后切片 |
| 11-12 | PK-CONFIRM GO → RQ3 成立；下一步回答层确认（PK-GEN）与知识感知门控防御（KAG） | 主门 75pp、次门满足 |

## 5. NEXT_ACTION：PK-GEN + KAG

### 5a. PK-GEN：回答层确认（零调参，复用 PK-CONFIRM 已封存掩码）

- 对 PK-CONFIRM 的 80 个世界，用 NONE、RD_B2、QWEN_VERIFY 三臂已封存的保留片段作上下文，Qwen 生成回答（沿用 Owner29/30 的系统提示与 JSON 格式，temperature 0）。约 240 次调用。
- 5090 按私有正确值与攻击目标值判定：TARGET_HIT（答出攻击目标值）、CORRECT（答出正确值）、ABSTAIN、OTHER。
- 预注册门槛（只看 UNK，D1 + D3 合并）：QWEN_VERIFY 的 TARGET_HIT 率 − NONE 的 ≥ 15pp → “核验放大攻击”在回答层成立；< 5pp → 不成立；其余 INCONCLUSIVE。K 层报告作对照（预期 QWEN_VERIFY ≤ NONE）。

### 5b. KAG：知识感知门控（防御开发，DEV 使用已曝光的 PK-STRAT + PK-CONFIRM）

- 思路：核验只在模型“知道”时才允许删除；模型不知道时，不删除，改为输出“证据冲突”标记（交给可信版本来源或拒答）。
- 运行时信号（不得使用标签）：两次闭卷回答是否一致，且闭卷答案是否与某个片段的抽取值相符（用 QAG 已验证的抽取器，准确率 97.8%）。两者都满足 → 视为“知道”，执行 QWEN_VERIFY；否则 → 保留全部片段并标记冲突。
- DEV 目标（在已曝光数据上，仅作开发）：UNK 的 C 误删大幅下降（D3 从 20/21），K 的 P 保留不上升。
- 之后必须在**全新**事实批次（PK-TEST）上预注册测试一次，并做回答层评估。

提示词：`NEXT_PROMPTS_PKGEN_KAG.md`。

## 6. 开放风险

- 所有数据为项目自写改写或虚构，非自然网页；每批事实单位少（4–8 个），世界不独立。
- Human Gold = 0；RAGDefender 原论文 Claims 1–3 未复现。
- QWEN_VERIFY 与生成器同为 Qwen，存在同模型偏差；后续需换一个核验模型做对照。
- 新颖性待核：需检索 2025–2026 年是否已有“LLM 核验防御依赖参数知识 / 对未知事实失效”的工作。

## 7. 台账维护规则

- 每轮结束：在第 3 节加一行事实、第 4 节加一行决策、更新第 2、5 节；裁决写成本目录下独立文件 `*_VERDICT_YYYYMMDD.md`。
- 接手者（GPT）若改动路线，在第 4 节追加记录，不删除旧行。
