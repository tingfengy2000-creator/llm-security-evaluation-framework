# Paper 1｜评审与临时负责人台账（Reviewer Ledger）

本文件是 Paper 1 当前研究判断的**单一接手入口**。任何接手者（GPT 网页版、Claude、5060 Codex、5090 Cursor）先读本文件，再按文末链接读原始报告。完整背景（Owner 需求、分工、方法、数据、全部结果、约束）见 `HANDOFF_20261114.md`。只记录结论、证据位置与下一步，不复制原始数据。

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

## 2. 当前状态（2026-11-14 18:30 JST）

- **交接：** 评审线由 Claude Fable 5.2 接续，完整交接见 `HANDOFF_20261114.md`。
- **论文定位（Owner 已同意）：** 主贡献 = 两类防御的失效机理（RAGDefender 中文迁移失败；LLM 核验继承知识边界、把冲突下的拒答变成被骗作答）。次贡献 = KAG（“不知道就不删”）。不把 KAG 包装为主角，不宣称“轻量”。
- **已成立：** RQ3（PK-CONFIRM GO）；RQ2 回答层（PK-GEN：UNK 目标命中 QV 26/42 vs NONE 1/42）。
- **阻塞 1：** KAG-V1/V1T 的 5090 评分未做（私有包未送达 5090）。
- **阻塞 2：** PK-TEST 闭卷与七臂均 NOT_RUN。5060 已冻结防御代码（`3c9d9a1`），并提出“测试输入须在探针前封存”的协议异议，评审裁定成立，改用 V2 顺序（第 5 节）。
- **不可宣称：** 正式 ASR、答案准确率、统计显著性、“优于 RAGDefender 原论文”、跨模型普适、KAG 有效。

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
| KAG v0 推导回答层 | ORACLE 上界显示门控可达空间 | K（D1+D3）命中/答对/拒答：v0 1/4/19，ORACLE 2/21/1；UNK：均 1/0/41 | 5090@`2a82707` · `repro5090/pk_gen_kag/DERIVED_ANSWER.md` |
| KAG-V1/V1T 运行 | 失配根因确认，待评分 | v0 冲突 123 个：A 0 / B 11 / C 112，60 个涉及缺单位；判知道 V1 58/136、V1T 48/136；时效门触发 22/136；USD 0.0105 | 5060@`9a5aa01`（冻结 `972f540`）· `chinese5060/kag_v1/RESULT.md`；私有包 SHA256 `7c8c9e9f…c75faf` |
| PK-TEST 阶段 1 | 题目封存 | 42 题，无标签；FORGED 预分配 U 4、F 4 | 5090@`2a82707` · `repro5090/pk_test/PKT_PHASE1_QUESTIONS.json`（`fee8f4ec…6509d`） |
| PK-TEST 防御冻结 | 代码冻结，未实跑 | 按需触发、TAG 模板、披露格式；离线测试通过；模型请求 0 | 5060@`aafbfad`（冻结 `3c9d9a1`）· `chinese5060/pk_test/RESULT.md` |

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
| 11-12 | 论文定位：失效机理为主、KAG 为缓解 | Owner 质疑“KAG 是否只是又套一层 RAG”；KAG 不发起新检索，可信源回退不作为贡献；需引用自适应检索（Mallen 等 2023）与 Sufficient Context 并说明用途差异 |
| 11-12 | PK-TEST 增加 TAG 冲突提示臂、CLEAN 设计、按需触发与 DISCLOSED 结果类别；主变体选择规则预先写死 | Owner 提议“过滤不掉的在生成阶段打标”；须同时报告命中、答对、拒答、披露，防止靠拒答“刷”安全 |
| 11-14 | PK-TEST 改 V2：主面板在闭卷前由 5090 封存；PA 改为闭卷后的独立面板，只报告；预注册门不变 | 5060 异议成立：输入不应在看到模型探针结果后构造；PA 作为自适应攻击本就依赖探针，须与主面板分开 |
| 11-14 | 评审线交接给 Claude Fable 5.2 | Owner 要求；写 `HANDOFF_20261114.md` |

## 5. NEXT_ACTION：PK-TEST V2

提示词：`NEXT_PROMPTS_PKTEST_V2.md`（执行顺序）；固定规则沿用 `NEXT_PROMPTS_PKTEST.md`（七臂、按需触发、结果类别、预注册门 G1/G2、主变体选择规则）。

顺序：Owner 把 KAG-V1 私有包拷到 5090 → 5090 评 KAG-V1 并在闭卷前封存、发布 PK-TEST 主面板（D1、D3、CLEAN、FORGED）→ 5060 跑闭卷 + 主面板七臂 → 5090 事后分层、构造 PA 面板 → 5060 跑 PA 七臂 → 5090 一次性评分（主面板给 GO / SAFE_LOW_UTILITY / NO_GO，其余只报告）。

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
