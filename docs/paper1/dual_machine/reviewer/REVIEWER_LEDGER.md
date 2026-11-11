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

## 2. 当前状态（2026-11-11 24:00 JST）

- **方法路线状态：** “轻量过滤器超过 RAGDefender”路线已结束。QAG NO_GO；QWEN_VERIFY（单次 LLM 核验）在测试集两项指标上全面胜过 RD_B2。
- **当前研究问题：** LLM 核验型防御的裁决能力是否来自参数知识；对模型不知道的事实（新修订、冷门地方规定、虚构）是否失效。
- **PK-STRAT：** 预注册裁决 INCONCLUSIVE（3/5 合并差距 33.3pp）；事后切片方向性支持很强（D3 按类别：K 3/24 vs U/F 24/24）。见 `PK_STRAT_VERDICT_20261111.md`。
- **下一步：** 第 5 节 NEXT_ACTION = PK-CONFIRM（预注册确认实验，全新事实）。
- **不可宣称：** 正式 ASR、答案准确率、统计显著性、“优于 RAGDefender 原论文”（原论文未复现）、RQ3 已证实。所有数字为 AGENT_PROVISIONAL 候选级。

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

## 4. 决策记录

| 日期 | 决策 | 理由 |
| --- | --- | --- |
| 11-05 | 受限恢复（v0.2 Rescue）降级为对照 | 恢复条件恰好是隐蔽污染满足的条件 |
| 11-06 | 增加 RD-zh 公平基线；S0 先行 | 区分中文迁移问题与方法贡献 |
| 11-11 | 停止 Q-CER、V-CARE、候选 A | 均未胜过同预算基线；候选 A 新颖性不足 |
| 11-11 | 给“Qwen 抽取 + 答案分组”最后一次机会 | Owner 决定；免除治理流程 |
| 11-11 | **QAG NO_GO；转向“LLM 核验在未知事实上的失效”** | 见 `QAG_VERDICT_20261111.md` |
| 11-11 | PK-STRAT INCONCLUSIVE → 做 PK-CONFIRM，不改写本批口径 | 预注册门未达，最强信号来自事后切片 |

## 5. NEXT_ACTION：PK-CONFIRM（预注册确认实验）

已完成的 PK-STRAT 设计与原门槛保留在 `NEXT_PROMPTS_PK_STRAT.md` 与 `PK_STRAT_VERDICT_20261111.md`，不再修改。

- **新事实**（不得复用 PK-STRAT 的 24 个事实）。分层：K = 闭卷连续 2 次答对的知名事实；UNK = U（2025 后修订/冷门地方规定）或 F（虚构）且闭卷 2 次都答错。闭卷答对的 U/F 单列，不进主分析。每层 ≥ 12 个事实。
- **设计**：D1（1 假 + 1 真 + 3 背景）、D3（3 假改写 + 1 真 + 1 背景）为主；FORGED 单独报告。
- **对比臂**：NONE、RD_B2、QWEN_VERIFY；若可用，再加一个非 Qwen 的核验模型。
- **主门槛（预注册）**：D3 上 UNK 的 Poison 保留率 − K 的 ≥ 40pp → GO；< 15pp → NO_GO；其余 INCONCLUSIVE。
- **次门槛**：D1 上 UNK 的 Clean 误删率 ≥ 25% 且 K ≤ 10%。
- **GO 之后**：防御方向为“闭卷置信度低时才调用可信版本来源”；论文核心发现为“LLM 核验继承模型的知识边界，版本更新是天然攻击面”。
- **NO_GO 之后**：论文按“基准 + RAGDefender 中文失效 + 过滤诱发攻击 + 单次 LLM 核验强基线”收口。

提示词：`NEXT_PROMPTS_PK_CONFIRM.md`。

## 6. 开放风险

- 所有数据为项目自写改写或虚构，非自然网页；每批事实单位少（4–8 个），世界不独立。
- Human Gold = 0；RAGDefender 原论文 Claims 1–3 未复现。
- QWEN_VERIFY 与生成器同为 Qwen，存在同模型偏差；后续需换一个核验模型做对照。
- 新颖性待核：需检索 2025–2026 年是否已有“LLM 核验防御依赖参数知识 / 对未知事实失效”的工作。

## 7. 台账维护规则

- 每轮结束：在第 3 节加一行事实、第 4 节加一行决策、更新第 2、5 节；裁决写成本目录下独立文件 `*_VERDICT_YYYYMMDD.md`。
- 接手者（GPT）若改动路线，在第 4 节追加记录，不删除旧行。
