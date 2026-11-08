# Paper 1｜Week 1 双机 Tracker

**更新于 2026-11-08 JST · 版本 3 · 维护位置 `research/paper1-chinese-defense-5060`。**

当前研究状态为 **5060 R2 四臂完成并停在 K1-C**。5090 已完成离线 Smoke 和非 Llama 资产下载，Claim 1–3 均未运行。Paper 1 正式实验仍未启动。

旧名 `PAPER1_WEEK1_TRACKER_INIT` 可在旧对话中定位到一次提及。2026-11-06 检查 GitHub 的 9 条公开分支、1 个标签及其可达文件历史，未找到对应文件，原稿的仓库路径、最后修改时间及全文均为 **UNKNOWN**。本页是从已提交证据建立的第一个可维护版本。

## 2026-11-08 5060 R2 实测收口

本批仅为 D1 开发诊断。高置信模板 6/180、3/36 世界，蒙版对两个分词臂均为零变化。char2 使 Clean 误删 4/10→5/10、HN 隔离 2/9→4/9、Poison 删除 2/10→4/10。可比被删候选 0。S1–S5 未放行。

[四臂结果与封存证据](chinese5060/vesa_guard_reviewer_replan/W1_5060_R2_FAIR_CONTROL_RESULT.md)。

## 2026-11-08 控制面恢复与 R2 放行

GitHub 远端实查确认：交接包记录的 5060 HEAD `533a6efed519f9251f4b4848306e232c9710a497` 与检查时远端完全一致；5090 HEAD `dbd91f3667964baca69aeb82a6292c4fe193c965` 亦完全一致，说明新会话恢复前没有遗漏的远端实验提交。随后控制面仅写入治理授权，不伪造实验结果。Owner 本轮 `W1-OD-20261108-5060-R2-OFFLINE-15` 已释放有界 R2 离线任务：`S0-TEMPLATE-COVERAGE_READONLY` + `B2_RAW / RD_ZH_ONLY / RD_TEMPLATE_ONLY / RD_ZH_TEMPLATE` 四臂，并批准 R1-10(A) 仅使用历史 B2 固定 revision 的本地已缓存 encoder。网页模板 mask 只可作用于 Stage1 lexical view；原 TopK、原文、embedding/Stage2、生成上下文、参数和历史结果保持不变。role-free 结果须先封存，再独立揭盲。

在本页第 2 版记录的控制面放行时，**尚无新的模板覆盖计数、四臂结果或 K1 判定**，所以这些仍为 `NOT_RUN / NOT_MEASURED`。R1-10(B)、S1–S5、5090 Claim1–3、D2/D3、正式测试、商业/免费在线模型调用及主线合并均未放行。完成本批后必须按已预注册 K1-A/B/C 选择路线并 STOP 返回 Owner。

[2026-11-08 PO-MHEP 授权](owner_approvals/W1_5060_R2_OFFLINE_FAIR_CONTROL_AUTHORIZATION_20261108.md)。

## 双机 Git 快照

| 工作线 | 分支与本次整理前的远端 HEAD | 该提交时间（JST） | 机器端观测 |
| --- | --- | --- | --- |
| 5060 Codex · 中文检索后防御 | `research/paper1-chinese-defense-5060` · 2026-11-08 恢复前远端核验 `533a6efed519f9251f4b4848306e232c9710a497`；随后仅新增治理授权提交 | 2026-11-08 | R2 有界离线任务已放行；机器本地 HEAD、未提交改动和实时进程仍 UNKNOWN，实验结果须以之后 Run Manifest 为准。 |
| 5090 Cursor · RAGDefender 复现 | `research/paper1-ragdefender-repro-5090` · [dbd91f3667964baca69aeb82a6292c4fe193c965](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/dbd91f3667964baca69aeb82a6292c4fe193c965) | 2026-11-06 02:58:38 | Git 下载清单可查，机器本地 HEAD、工作树及实时进程为 UNKNOWN。 |

分支 HEAD、控制合同和实验执行 SHA 分开记录。5060 S0 证据收口提交为 [25936c71f96d775cca9a7603d27164e952f3a0af](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/25936c71f96d775cca9a7603d27164e952f3a0af)，R1 追加只读核验的控制提交为 [9bd8e29](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/9bd8e29d49b774add5eafb700077e1750d41f309)。RAGDefender 固定上游为 [ba2a17e](https://github.com/SecAI-Lab/RAGDefender/commit/ba2a17efba165d45409114df2d70b030ade1e1b8)。

## 5060 已封存结果

| 项目 | 状态与结果 | 证据 |
| --- | --- | --- |
| D1 Pilot12 检索 | **VERIFIED** · 12 个相关事实组、36 个独立建索引的世界，每世界 1 个候选和 18 个背景文档，TopK5 共 180 片段。候选 hit@5 为 29/36，Poison 10/12、Clean 10/12、HN 9/12。7 次漏召回另计。 | [S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md) |
| B1/B2 离线过滤 | **VERIFIED** · 各 36/36 世界。B1/B2 总删片段 78/180、81/180。以已召回候选为分母，Poison 删除 1/10、2/10，Clean 误删 1/10、4/10，HN 隔离均为 2/9。B2 仍保留 8/10 个已召回 Poison 候选。 | [S0 脱敏证据索引](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_EVIDENCE_INDEX.json) |
| G0/G1/G2 真实 Qwen | **VERIFIED** · `OWNER12_LIVE_108` 108 次请求成功，0 重试。三臂回答分别 15/36、13/36、11/36，拒答分别 21/36、23/36、25/36。输入/输出 Token 合计 44,426/5,154。CNY 0.130084 为公开费率估算，实扣为 UNKNOWN。 | [Owner12 运行结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/c6e36685cd948700f2d65e53031f82d8d13d2f51/docs/paper1/dual_machine/chinese5060/pilot_rapid_live/RAPID_LIVE_OWNER12_EXECUTION_RESULT.md) |
| 回答与拒答暂定评价 | **VERIFIED / PROVISIONAL** · 18 格拒答暂定合理，另 51 格拒答和 39 份回答的整体判断未决。Human Gold = 0，正式 Targeted ASR、Answer Accuracy 与 C3 均未测。 | [暂定评价](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/59ceb4ff2267299aa7ed1c6fb0819f952098fcd5/docs/paper1/dual_machine/chinese5060/pilot_rapid_live/PILOT12_D1_AI_PROVISIONAL_EFFECT_REPORT.md) |
| VESA v0.1 / v0.2 | **VERIFIED · 零变化** · 两版均 0/36 上下文改变，G3 与 G2 请求体逐字节一致，0 恢复、0 新 Qwen、G3 未运行。v0.2 识别到 24/36 个查询世界、102/180 个片段，49/180 个片段抽到具体值。 | [v0.1 结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/bfcfaa6490de96b97b12b3304297049dfa627910/docs/paper1/dual_machine/chinese5060/vesa_guard_v01/VESA_V01_OWNER13_RESULT.md) · [v0.2 结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/8db8d9f8b48f86dae9f8f9211e1092fbe4ae534d/docs/paper1/dual_machine/chinese5060/vesa_guard_v02/VESA_V02_OWNER14_RESULT.md) |

D1 是 `D1_DEV_EXPOSED`。本页 Pilot12 的 12 组、36 世界与 D1 开发范围的 40 组、120 候选分别计数。D2/D3、独立留出、答案与攻击目标留在各自授权和隔离边界内。上下文变化、候选过滤和回答/拒答计数分别记录。

## 5060 评审、S0 与放行门

S0 run 为 `W1-5060-REVIEWER-REPLAN-S0-20261106-01`，状态 **S0_COMPLETE / OWNER_CHECKPOINT_PENDING**。零新编码、零新检索、零模型调用、零 API 费用。[S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md) · [S0 脱敏证据索引](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_EVIDENCE_INDEX.json)。

| 评审 | 本次核验状态 |
| --- | --- |
| R1-01 | **VERIFIED，静态完成**。RD-zh 只将 Stage 1 TF-IDF 改为字符二元组，`stop_words=None`。4 项定向单测通过，真实 D1 编码和过滤均 **NOT_RUN**。历史 B2 的 TF-IDF 仍沿用英文词规则和停用词。 |
| R1-02 | **VERIFIED**。旧 `n_tfidf` 36/36 一致，12/36 世界进入大簇分支。两次本地 top5 重放相同，旧记录未存逐词清单。分词造成误删的因果效应尚待反事实对照。 |
| R1-03 | **VERIFIED**。旧抽取器在 B2 被删的 81 片段中抽出 25 个具体值，0/81 与查询范围绑定，81/81 同值/异值判断为 UNKNOWN。保留集合中 1/36 世界有同范围唯一值，独立可信来源锚 0/180。以上按冻结输入及现有抽取器口径统计。 |
| R1-04 | **DESIGN / NOT_RUN**。M1-safe 为探索臂，保留重复同值片段可能提高错值采纳的残余风险。 |
| R1-05 | **DESIGN / NOT_RUN**。M2-detect 与 M2-vote 分臂，后者需要可验证的攻击者控制上界，多数与全毒场景单列。 |
| R1-06 | **DESIGN / NOT_RUN**。S1 独立记录错抽的两个分母、UNKNOWN、错因和区间。 |
| R1-07 | **DESIGN / NOT_RUN**。S2/S3 加入合法共享法规引用场景 I，保留 H 的 4 毒 1 净、5 毒两个变体。 |
| R1-08 | **VERIFIED**。72/72 个世界×B1/B2 臂的历史 Stage 2 计数和索引对齐修复后逻辑，实际余弦先做 L2 归一化，当前无 Stage 2 归一化修正臂。 |
| R1-09 | **HARD_STOP**。S0 已封存，S1–S4 **NOT_RUN**，S5 **NOT_AUTHORIZED**，Auto Continue = NO。 |
| R1-10 | **OWNER_DECISION_REQUIRED**。A 为 36 世界、180 片段的缓存编码器及 RD-zh 离线实跑权限，B 为 S3 独立造题与保管方。 |

R1 源附件由 Owner 提供，公开记录含原件摘要与 SHA-256。[R1 修订合同](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fbb176f6aa232212a44d336ecb037c39b1220cd4/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R1_TRACKING_AMENDMENT_20261106.md)。

**S4 证据门（INFERRED）**。冻结输入可信锚 0/180。按严格 P0 和原 B2，Clean 误删下界为 4/10，原门要求 <4/10，故当前输入标记 `S4_FAIL_EVIDENCE_BOUNDARY`，S4 本身仍是 **NOT_RUN**。公平臂出结果后按各臂重新计算。Poison 保留 ≤8/10 是原 D1 开发不退化门。[S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md)。

**R2（历史预注册，实测见页首）**。评审观察的约 100/189 来自上游证据，D1 TopK180 的网页模板覆盖率为 **UNKNOWN**。下一项诊断限于冻结 TopK 的只读覆盖统计。已预注册 `B2_RAW`、`RD_ZH_ONLY`、`RD_TEMPLATE_ONLY`、`RD_ZH_TEMPLATE` 四臂，控制 Stage 1 分词与词面模板遮蔽，固定原 TopK、向量、Stage 2 和生成正文。四臂对照未实跑。K1 路线选择待证据，M2 与 X-MADAM-RAG 的重叠已登记。[R2 预注册与路线决策](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/1499561c8091fec1aaa042b81b9168ee63ff908d/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R2_S0_CHECKPOINT_TEMPLATE_TFIDF_ROUTE_20261106.md)。

## 5090 原论文复现

| 项目 | 级别与状态 | 证据 |
| --- | --- | --- |
| 上游审计、环境、离线检查 | **VERIFIED · SMOKE / ALGORITHM_CHECK**。官方环境在 RTX 5090 的 CUDA 内核存在兼容问题，独立兼容环境的最小 CUDA 检查通过。 | [离线 Smoke 与资源门](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/5def0ff/docs/paper1/dual_machine/repro5090/W1_5090_OFFLINE_SMOKE_AND_RESOURCE_GATE.md) |
| 冻结非 Llama 资产 | **VERIFIED（仓库下载收据）**。Vicuna、Contriever、paraphrase-MiniLM 与 NQ、HotpotQA、MS MARCO 已下载。Llama 2 7B chat 未下载，本批模型加载 0、付费 API 0。 | [5090 下载记录](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/W1_5090_NON_LLAMA_ASSET_DOWNLOAD.md) · [下载清单](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/NON_LLAMA_DOWNLOAD_MANIFEST.json) |
| Claim 1 PoisonedRAG、Claim 2 Tan et al.、Claim 3 GARAG | 三条均 **NOT_RUN**。无防御/有防御 Targeted ASR 与 QA Accuracy 均 **NOT_MEASURED**。 | [下载清单](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/NON_LLAMA_DOWNLOAD_MANIFEST.json) |

## Owner 待决

| 决策 | 当前状态与前置 |
| --- | --- |
| 5060 · `S0_CHECKPOINT_RELEASE` | **待放行**。先确认追加只读的 D1 TopK 模板覆盖与四臂计划。进入 S1 需 Owner 显式放行。 |
| 5060 · R1-10(A) | **待授权**。是否准许仅用冻结缓存编码器对原 36 世界、180 片段做离线公平对照。限制为零下载、零新检索、零商业 API，历史 B2 证据原样保存。 |
| 5060 · R1-10(B) | **待指定**。选择独立于 5060 方法开发方的 S3 构造与保管人。任何跨机委派须单独授权。 |
| D1 定位与人工裁决 | **待证据/安排**。公平臂、可作用池和可信来源证据进入 K1 决策。独立人工审阅尚待安排，Human Gold 仍为 0。 |
| 5090 · 后续批次 | **待授权**。Llama 2 获取状态和下载、单格、Claim 正式运行分别核验与批准。 |
| S5 与投稿目标 | S5 保持 **NOT_AUTHORIZED**，须前序门闭合后再单独确认模型、外传及预算。投稿场次与年份待 Owner 确定。 |

5060 放行与角色隔离依据 [Owner 决策登记](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fa70d97f86d0bf21364907e15447ced80f0e284e/docs/governance/project_owner_decision_register.md)、[5060 动态状态](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fa70d97f86d0bf21364907e15447ced80f0e284e/docs/governance/current_work_state.md)、[R2 检查点](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/1499561c8091fec1aaa042b81b9168ee63ff908d/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R2_S0_CHECKPOINT_TEMPLATE_TFIDF_ROUTE_20261106.md)。5090 批次依据 [5090 分批审批包](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/BATCHED_REPRO_OWNER_APPROVAL_PACK.md) 和最新下载清单。

## 更新规范

1. **事件触发维护。** 每次两机推送新证据、Run 完成/失败/零变化、评审修订或 Owner 改门后，负责更新的控制端先核验双方远端 HEAD，再在本文件更新受影响条目并追加下面的变更记录。无新证据时保留上一已核状态与时间，机器本地状态记 UNKNOWN。
2. **每条带证据。** 记录 JST 时间、分支、远端 HEAD、合同/执行 SHA、Run ID、阶段和分母。证据链接固定到提交。优先核对 Run Manifest、脱敏证据索引及封存汇总，再核对 Owner 决策和动态状态。`VERIFIED` 表示仓库或可访问证据已核，注明证据层级。`REPORTED` 为仅机器或评审回传，`INFERRED` 为由证据推导，`UNKNOWN` 为缺证，`BLOCKED` 为有明确门或缺项。计划、未运行和未测分别标记。
3. **保留历史和权限。** 失败、零变化、分母和旧快照由证据提交与变更记录保留。纠正用追加记录引用原提交，区分开发、Smoke、正式实验和人审。Owner 的新授权引用登记或合同。公开 Git 仅收脱敏汇总与哈希，原 TopK、逐样本标签、目标答案、私有评审附件及凭据保留在受控位置。
4. **独立维护。** 维护提交基于最新远端，从独立副本快进发布到 5060 研究分支。发现远端前移时先复核新证据。运行中的工作树由机器执行者在其收口节点自行协调同步，远端更新与工作会话已接收分别记录。
5. **状态权威。** 本页是双机索引。5060 动态状态以 [Current Work State](../../governance/current_work_state.md) 为准，证据索引以 [Experiment Master Record](../../governance/experiment_master_record.md) 为准，授权以 [Owner Decision Register](../../governance/project_owner_decision_register.md) 为准，冲突按 [Context Authority Map](../../governance/context_authority_map.md) 处理。

## 变更记录

| 日期（JST） | 版本 | 变更与核验基点 |
| --- | --- | --- |
| 2026-11-08 | 2 | 新会话按交接包恢复并动态核对双机远端；5060/5090 均与交接 SHA 一致。登记 Owner R2 有界离线授权，释放模板覆盖诊断与四臂公平对照；无新实验结果。 |
| 2026-11-06 | 1 | 建立双机维护页。记录 5060 的旧 G3 零变化、S0 完成、R1/R2 与待放行状态，以及 5090 非 Llama 资产下载后 Claim 未运行。整理前 5060 `fa70d97`，5090 `dbd91f3`。 |
| 2026-11-08 | 3 | 5060 实测四臂、封存、K1-C，保持 5090 历史快照。 |
