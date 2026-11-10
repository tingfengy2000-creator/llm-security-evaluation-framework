# Paper 1｜Owner25 来源、版本与适用范围机制小试

2026-11-10 JST · `W1-5060-OWNER25-SYNTHETIC-P0-20261110-01`

**裁决为调整。** 当前 D1 恢复与原 Rule‑V2 部署路线均为 **NO_GO**。合成 Oracle 对固定过滤掩码显示了机制空间，同时暴露了可信签发者被攻陷的失败。公平同世界 RD 基线缺失，登记 `BASELINE_INCOMPLETE`，没有达到相对 RD 的预注册通过条件。

## D1 已知能力边界

D1 冻结 TopK 为 36 世界、180 片段，36 个候选中 29 个召回。过滤分母为已召回的 Poison 10、Clean 10、HN 9。B2 分别删除 2/10、4/10、2/9，RD‑zh 仅分词迁移分别删除 4/10、5/10、4/9。真实独立收据覆盖 **0/180**，因此严格 P0 无法恢复 B2 已误删的 4 个 Clean，原门槛要求小于 4/10，本输入下不可达。该结论只引用 S0/R2 已公开聚合证据，本轮 D1 运行次数为 0。 [S0 边界](vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md) · [R2 公平对照](vesa_guard_reviewer_replan/W1_5060_R2_FAIR_CONTROL_RESULT.md) · [P0 方法边界](vesa_guard_reviewer_replan/VESA_REVIEW_RESPONSE_P0_M1M2M3_S0S5_DESIGN_V1.md)

## 实验设计与身份

12 个虚构语义事实组，覆盖 4 个主题域与 24 个模拟签发家族，8 组 DEV、4 组 HOLDOUT。每组 8 情境，每世界 5 段。两份拆分在开发运行前封存，64 个 DEV 世界和 32 个 HOLDOUT 世界共享同一设计但事实组不重叠。签发资格取决于固定发布路由与登记范围，未使用评价角色字段；真实受信路由中的恶意内容作为签发者被攻陷的反例保留。签发是独立输入台账的模拟，生产签名和真实来源覆盖均未测。

算法验收据的片段 ID、正文 SHA256、来源父哈希、登记权限和签发时间，再核对查询与证据的事实、范围及有效区间。有相符锚且同族去重后无已核值冲突时，允许恢复同一片段的可核收据，并滤除同范围、同时间的冲突值。没有可比较锚时精确退回冻结父掩码。历史及其他范围证据不参与当前可信锚，联合臂保留父掩码对这些证据的决定。Scope-only 记录风险线索并维持父掩码。原 Rule‑V2 原样处理正文，缺少原生字段或严格跨度时不修补。

只用一版 JOINT。冻结了源码、输入、模拟收据、Oracle 字段、评价 Gold、分组和协议。预测进程只读本拆分白名单，不能读评价 Gold 和分组映射。HOLDOUT 预测封存后，由单独进程核验预测 SHA、读评价文件并评分一次。数据与评分均为同一 Agent 构建，标 `SYNTHETIC_PROVISIONAL / NONINDEPENDENT_AGENT / ORACLE_UPPER_BOUND`，Human Gold 为 0。

每臂使用相同原始五段与排序。固定父掩码预先删除种子打乱后排名 1、4，完全不看正文和角色，是恢复机制的实验扰动。历史 B2 与 RD‑zh 的 Stage 2 均要求在这批新上下文编码，本轮零模型且无同世界封存 embedding，故两臂为 `BASELINE_UNAVAILABLE`，没有用 D1 旧指标或父掩码代替 RD。

## 实测对照

每格依次为 **Poison 保留、Clean 误删、HN 误删**。未决是没有唯一可用锚的世界数，并不计为最终回答拒答。

| 臂 | DEV 64 世界 / 320 片段 | HOLDOUT 32 世界 / 160 片段 | HOLDOUT 未决 |
| --- | --- | --- | --- |
| NONE | 108/108 · 0/156 · 0/56 | 54/54 · 0/78 · 0/28 | 32/32 |
| FIXED_PARENT_PROXY | 66/108 · 64/156 · 22/56 | 32/54 · 30/78 · 12/28 | 32/32 |
| ANCHOR_ONLY | 16/108 · 44/156 · 27/56 | 7/54 · 17/78 · 14/28 | 10/32 |
| SCOPE_VERSION_ONLY | 66/108 · 64/156 · 22/56 | 32/54 · 30/78 · 12/28 | 32/32 |
| JOINT_P0，Oracle | 16/108 · 41/156 · 22/56 | 7/54 · 15/78 · 12/28 | 2/32 |
| FORGED_RECEIPT_NEGCTRL | 66/108 · 64/156 · 22/56 | 32/54 · 30/78 · 12/28 | 32/32 |
| JOINT_P0_HALF_RECEIPTS | 48/108 · 54/156 · 22/56 | 22/54 · 23/78 · 12/28 | 15/32 |
| JOINT_P0_RAW_RULE_V2 | 66/108 · 64/156 · 22/56 | 32/54 · 30/78 · 12/28 | 32/32 |
| RD_B2 / RD_ZH | 各 0/64，未运行 | 各 0/32，未运行 | 未测 |

### HOLDOUT 联合臂分层与失败

| 情境 | 世界 | Poison 保留 | Clean 误删 | HN 误删 | 未决 / 错锚 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 全正常 | 4 | 0/0 | 2/20 | 0/0 | 0 / 0 |
| 合法换版 | 4 | 0/0 | 3/8 | 4/12 | 0 / 0 |
| 跨适用范围 | 4 | 0/0 | 1/8 | 6/12 | 0 / 0 |
| 单污染 | 4 | 0/4 | 4/16 | 0/0 | 0 / 0 |
| 三段同文本污染 | 4 | 0/12 | 2/8 | 0/0 | 0 / 0 |
| 三段改写同源污染 | 4 | 0/12 | 0/8 | 0/0 | 0 / 0 |
| 伪造修订与机构 | 4 | 1/8 | 3/8 | 2/4 | 0 / 1 |
| 4/5 或 5/5 污染 | 4 | 6/18 | 0/2 | 0/0 | 2 / 0 |

- **有锚可作用空间。** HOLDOUT 收据验证覆盖 58/160 片段、30/32 世界，42 段可作为当前锚，其中 4 个同来源冗余记录合并。相对同输入父掩码，有收据世界的 Clean 误删从 30/78 降为 15/78，Poison 保留从 26/44 降为 1/44，HN 误删为 12/28。联合臂 16 次恢复中 0 次无证恢复。相对 ANCHOR_ONLY，联合臂减少 2 个 Clean 误删和 2 个 HN 误删，污染保留同为 7/54。ANCHOR_ONLY 有 16 个不适用锚，联合臂为 0。
- **多数污染和回退。** 两个有正确锚的 4/5 世界保留 0/8 毒段，两个无锚的 5/5 世界保留 6/10，2/2 精确回退且均未决。三段改写污染共 12 段均未保留，文本票数不构成独立源。轮换收据负对照验证 0/160，32/32 精确回退。自称或伪借收据的 17 段均未通过收据绑定核验。半覆盖仅验证 29/160，15/32 未决，Clean 只从 30 降至 23，Poison 保留 22/54，观察到对覆盖率的依赖。
- **真签发者失陷。** HOLDOUT 的 1 个失陷世界发生 1 次错误锚定，Clean 误删 2/2，父掩码为 1/2，Poison 保留均为 1/2。这里的错锚来自真正已登记签发者发布错误内容，0 次无证恢复的结果不能消除此风险。总计 30 个锚定世界中 29 个锚值正确。DEV 两个同类世界也各发生错锚。
- **真实抽取瓶颈。** Rule‑V2 在 DEV 320/320、HOLDOUT 160/160 返回 UNKNOWN，原生严格绑定均为 0。正文臂在 32/32 测试世界均精确回退，未恢复一段。生成器带有固定句式和单属性限制，当前成绩不代表自然中文抽取可行。
- **描述区间。** 联合臂 HOLDOUT 的 Wilson 95% 为 Poison 保留 7/54［6.42%, 24.42%］，Clean 误删 15/78［12.02%, 29.33%］，HN 误删 12/28［26.51%, 60.93%］，未决 2/32［1.73%, 20.15%］。32 世界共享 4 个事实组，只作描述，不进行独立样本显著性推断。各臂情境分母、区间、分层结果和逐世界哈希均已登记。
- **开销。** HOLDOUT 机制端单世界中位数/P95 为 Oracle 联合 0.0153/0.0200 ms、原 Rule‑V2 联合 0.1789/0.8167 ms，均不含检索或生成。使用本机 CPU Python，模型加载、推理、实验外部 API、下载和新增费用均为 0，Owner24 仍停在 F0。无 D1 逐格数据、D2/D3 或 5090 访问，正式 ASR/Accuracy 未测。

## 论文判断与最快证伪路径

| 既有研究 | 与本路线的重合边界 |
| --- | --- |
| RAGDefender，ACSAC 2025，公开库 v0.2.0 | 检索后分组与恶意段落过滤、正常段保留已有先例。无额外 LLM 调用仍可依赖嵌入，合成掩码不能代替该基线。 [官方制品](https://github.com/SecAI-Lab/RAGDefender) · [v0.2.0 发布](https://github.com/SecAI-Lab/RAGDefender/releases/tag/v0.2.0) |
| SeCon‑RAG，NeurIPS 2025 | 实体、意图、关系抽取及问句、候选答案、检索知识之间的语义冲突过滤已有先例。 [会议论文](https://proceedings.neurips.cc/paper_files/paper/2025/hash/668563ef18fbfef0b66af491ea334d5f-Abstract-Conference.html) |
| X‑MADAM‑RAG，arXiv:2606.12903 | 逐段抽取、证据修复、分组和冲突聚合已有先例，作者亦报告自然化时抽取性能显著退化及 Oracle 差距。 [作者预印本](https://arxiv.org/abs/2606.12903) |
| GuardRAG，arXiv:2610.35071 | 检索后去重、HAC 聚类和协同污染过滤已有先例。 [作者预印本](https://arxiv.org/abs/2610.35071) |

待验证的差异是**可验证来源权限、有效时间和适用范围如何共同限制信任提升**，以及该限制在多数污染、低覆盖和真实签发失陷时的代价。当前实验未建立论文创新性或真实泛化。

**唯一建议为调整研究边界。** 暂停当前 D1 无锚恢复与 Rule‑V2 上线路线。下一项最短证伪实验是先独立挑选至少两个公开发布机构的真实版本化规范或办事指南，冻结原文、发布日期、生效/废止、适用范围和采集哈希，独立人工判定，预先报告实际可绑定收据覆盖。随后在同一固定 TopK 上比较 B2、RD‑zh、收据单模块与联合模块，成对覆盖同值不同范围、真实换版和伪新版多数污染。如果真实收据覆盖很低、严格抽取仍大面积回退或正常证据损失抵消收益，停止该路线。此提案未启动。

## 封存与治理

[Run Manifest](W1_5060_OWNER25_SCIENCE_FIRST_RUN_MANIFEST.json)记录冻结代码、数据 SHA、DEV 和一次性 HOLDOUT 预测/评分 SHA、命令、退出码及 60 件私有证据的索引。私有归档 `OWNER25_PRIVATE_EVIDENCE.zip` SHA256 `d8125e1f6f008c8dc6437c4f2326f4a4558aebe21915aac62d593bb00d0e3651`，所有成员重读核验。最终 4 项单测、Ruff、MyPy 通过，封存前初次类型检查失败及修复日志均保留。

更新 Human Ledger、Agent Ledger、Current Work State、Project Master、Experiment Master、Research Execution Log 和 Tracker。Owner 原授权保持，未新增或改变阶段、方法契约、历史结果和正式研究导航。执行结束 `AUTO_CONTINUE=NO_OUTSIDE_THIS_PILOT`。

    human_ledger_checked = true
    human_ledger_updated_if_required = true
    agent_ledger_checked = true
    agent_ledger_updated = true
    current_work_state_updated = true
    execution_log_appended = true
    experiment_master_condition_evaluated = true
    owner_decision_condition_evaluated = true
    stage_process_condition_evaluated = true
    lessons_condition_evaluated = true
    research_authority_condition_evaluated = true
    README_condition_evaluated = true
    cross_document_current_task_consistent = true
    cross_document_status_consistent = true
    cross_document_next_action_consistent = true
    cross_document_blocker_consistent = true
    markdown_links_valid = true
