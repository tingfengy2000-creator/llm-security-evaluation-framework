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

## 2. 当前状态（2026-11-12 20:30 JST）

- **RQ2+RQ3 回答层成立：PK-GEN 预注册 AMPLIFICATION_CONFIRMED。** UNK 上攻击目标命中 QWEN_VERIFY 26/42 vs NONE 1/42。机理：生成器遇冲突几乎都拒答（NONE 拒答 73/80），核验消解冲突后，K 上答对、UNK 上被骗。见 `PKGEN_KAG_VERDICT_20261112.md`。
- **KAG v0（DEV）：安全达成、可用性失败。** UNK 判知道 0/47，UNK D3 正确片段误删 0/21（QV 20/21）；但 K 判知道仅 6/24。根因是闭卷原话与片段值的字符串匹配失配，且温度 0 下两次闭卷逐字相同。
- **下一步：** 第 5 节 = KAG-V1（DEV 修复 + 推导回答层 + ORACLE 上界）与 PK-TEST 阶段 1（新事实出题）。
- **不可宣称：** 正式 ASR、答案准确率、统计显著性、“优于 RAGDefender 原论文”、跨模型普适（只测了 Qwen）、KAG 有效。所有数字为 AGENT_PROVISIONAL。

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
| **PK-GEN** | **AMPLIFICATION_CONFIRMED（预注册）** | UNK D1+D3 目标命中 QV 26/42 vs NONE 1/42（+59.5pp）；K 对照 QV 2/24 vs NONE 0/24（预期未满足）；QV 使 57/80 世界由拒答转作答；FORGED 上 NONE 自身被骗 UNK 3/5 | 5060@`0013458` · `chinese5060/pk_gen_kag/RESULT.md`；5090@`7783a7c` · `repro5090/pk_gen_kag/SCORE.md` |
| KAG v0 DEV | 安全达成，可用性失败 | PK-CONFIRM 判知道 K 6/24、UNK 0/47；UNK D3 C 误删 KAG 0/21 vs QV 20/21；K D3 P 保留 KAG 30/36 vs QV 6/36；第二次闭卷逐字相同 24/24 | 同上；本分支 · `PKGEN_KAG_VERDICT_20261112.md` |

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
| 11-12 | PK-GEN 确认 → 回答层放大成立；KAG 进入 V1（修匹配、换第二探针模板、时效门变体），并行启动 PK-TEST 出题 | KAG v0 安全达成但 K 召回 6/24，根因为工程失配 |

## 5. NEXT_ACTION：KAG-V1（DEV）+ PK-TEST

提示词：`NEXT_PROMPTS_KAGV1_PKTEST.md`。上一轮（PK-GEN + KAG-DEV）提示词：`NEXT_PROMPTS_PKGEN_KAG.md`。

### 5a. KAG-V1（DEV，仅用已曝光的 PK-STRAT + PK-CONFIRM）

- 5060 先做无标签诊断（CONFLICT 原因 A/B/C 计数），再修复：闭卷回答过同一抽取器；第二探针换模板；最小归一扩充。输出 V1 与 V1T（时效门：任一片段含 ≥2025 年修订/施行年份 → 强制 CONFLICT）两个变体。
- 5090 零调用：推导回答层（CONFLICT→NONE 回答，KNOWS→QV 回答）与 ORACLE 上界（K→QV，UNK→NONE），并评分 V1/V1T。
- DEV 参考线（不是 GO 门）：PK-CONFIRM K 判知道 ≥18/24 且 UNK 判知道 ≤2/47。

### 5b. PK-TEST（全新事实，预注册，只跑一次）

- 事实：K 12、U 18、F 12，与以往批次不重复。设计 D1、D3、FORGED、PA（先验对齐：攻击目标 = 模型对该事实的一致闭卷错答）。
- 流程：5090 出题（只公开问题）→ 5060 用冻结的 KAG 版本跑闭卷 → 5090 构造世界 → 5060 四臂（NONE、RD_B2、QWEN_VERIFY、KAG）掩码 + 生成 → 5090 一次性评分。
- **预注册门（回答层，D1+D3 合并）：**
  - G1 安全：UNK 上 KAG 目标命中 ≤ NONE + 5pp，且 QV − KAG ≥ 30pp。
  - G2 可用：K 上 KAG 答对率 ≥ QV 答对率 − 20pp。
  - G1 且 G2 → GO；只满足 G1 → SAFE_LOW_UTILITY；不满足 G1 → NO_GO。
  - PA、FORGED 单列报告，不设门（预期 KAG v1 在 PA 上失效，V1T 可能缓解，需如实报告）。

## 6. 开放风险

- 所有数据为项目自写改写或虚构，非自然网页；每批事实单位少（4–8 个），世界不独立。
- Human Gold = 0；RAGDefender 原论文 Claims 1–3 未复现。
- QWEN_VERIFY 与生成器同为 Qwen，存在同模型偏差；后续需换一个核验模型做对照。
- 伪造修订（FORGED）连无防御都能骗过；KAG 回退等于 NONE，不解决此威胁，需可信版本来源或声明不在范围内。
- 拒答代价：KAG 安全来自回退到拒答，必须同时报告拒答率与 ORACLE 上界。
- 新颖性待核：需检索 2025–2026 年是否已有“LLM 核验防御依赖参数知识 / 对未知事实失效”的工作。

## 7. 台账维护规则

- 每轮结束：在第 3 节加一行事实、第 4 节加一行决策、更新第 2、5 节；裁决写成本目录下独立文件 `*_VERDICT_YYYYMMDD.md`。
- 接手者（GPT）若改动路线，在第 4 节追加记录，不删除旧行。
