# LLMGuard 实验总记录、证据索引与项目交接入口

> 英文名：Experiment Master Record
>
> 文档性质：项目唯一的实验控制面、索引和汇总入口。
>
> 首次建立：2026-07-20。最近更新时间应通过本文件的 Git 历史解析；当前 branch、HEAD 和本文件自身提交均为动态 Git 事实，不在本文静态固化。

## 1. 文档元数据与使用说明

### 1.1 职责

本记录统一回答项目实验路线、运行、指标、证据、失败、阻塞项、审批门、结论边界和交接顺序。它是**控制面、索引和汇总入口，不是原始数据仓库，也不替代阶段产物**。

- 不记录 API Key、Authorization、完整敏感输出、完整污染文档或本机绝对路径。
- 不覆盖 Stage 1–5 的历史 JSON/JSONL、HTML、日志、报告、数据或代码；历史勘误以新增条目留痕。
- 缺失事实统一写作 `NOT_RECORDED`；存在冲突写作 `REQUIRES_VERIFICATION`；不能用推测补齐。
- 维护人：项目负责人及获授权的维护者。
- 更新触发条件见“持续更新协议”；每次更新均要从原始证据回填，而非从教学材料反推。

### 1.2 文档职责矩阵

| 文档 | 主要职责 | 是否保存当前动态状态 | 是否保存原始实验数据 | 是否是实验总入口 |
| --- | --- | --- | --- | --- |
| [AGENTS.md](../../AGENTS.md) | Codex 启动、范围和完成协议 | 否 | 否 | 否 |
| [long_term_research_requirements.md](long_term_research_requirements.md) | 长期不可变研究要求 | 否 | 否 | 否 |
| [PROJECT_MASTER_CONTEXT.md](../../PROJECT_MASTER_CONTEXT.md) | 项目架构、路线和长期上下文 | 部分 | 否 | 否 |
| [current_work_state.md](current_work_state.md) | 当前任务与审批门 | 是 | 否 | 否 |
| `experiment_master_record.md` | 实验路线、运行、指标、证据、阻塞、交接 | 是，做动态索引 | 只做索引和汇总 | 是 |
| [learning_notes.md](../../deliverables/learning_notes.md) | 教学过程、问题解释和学习反思 | 否 | 否 | 否 |
| Stage-specific deliverables | 原始结果、日志、报告和阶段解释 | 否 | 是 | 否 |
| Run Manifest | 单次正式运行的机器可读事实 | 否 | 是 | 否 |

### 1.3 权威来源优先级

冲突时按以下顺序判断，不能为使表格“更好看”而改写低层证据：

1. 原始输出、日志和 Run Manifest；
2. 对应 Git commit；
3. Stage-specific 验收报告和结果摘要；
4. 本 Experiment Master Record 的索引和汇总；
5. 教学或面试材料。

## 2. 五分钟项目快照

| 项目 | 当前事实 |
| --- | --- |
| 总目标 | 建立从模型层安全评测、Guard 对照到 RAG 安全与可信检索、再到 Agent 安全的可复现研究框架。 |
| 当前最高完成阶段 | Stage 6 的 S6-T5.4 Controlled Corpus ContentResolver 已通过人工验收，验收边界仅为合成内存内容上的离线工程行为。 |
| 当前任务 | `GOV-S6-T5.5-P1-ACCEPTANCE` 已记录 P1/P1-H1 人工验收；它不实现 Envelope、Citation、renderer 或 ContextBuilder，也不是正式 RAG 安全实验。 |
| 当前审批门 | S6-T5.4 blocker 仍保留为 `RESOLVED_BY_APPROVED_PROTOCOL_FREEZE` 的历史记录；S6-T5.4 已 HUMAN_ACCEPTED。 |
| 下一批准任务 | `S6-T5.5` 仅进入独立实现审批准备状态；`S6-T5.5-I1` 尚未批准，EvidenceEnvelope、Citation、ContextBuilder 和正式 RAG 安全实验均须独立审批。 |
| 最近正式安全实验 | Stage 5 Paper Mock 确定性运行，`20260701T081320Z-c29f39`，88 attempts。 |
| 最近工程验证 | S6-T5.3-P1 metadata carrier、DenseRetriever 与 S6-T5.3-H1 trace/failure-boundary 离线加固；无正式 RAG 实验。 |
| 当前主要阻塞项 | parent identity 协议已由版本化 schema `1.1` 修复；DenseRetriever 仍须保持无正文、标签隔离与 fail-closed 边界。历史实验另缺少部分 Run Manifest、模型 revision 和数据 fingerprint。 |
| 当前允许宣称 | 已有模型层真实 API 小样本扫描、Guard A/B 和输入/输出消融；Stage 6 已有检索基础设施与标签隔离契约。 |
| 当前禁止宣称 | 未完成正式 RAG 安全实验、可信检索、抗知识污染、Citation Accuracy、Agent 安全或生产级防护。 |

当前审批状态补充：`S6-T5.5: READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`；`S6-T5.5-I1: NOT YET APPROVED`；`S6-T5.6+: NOT APPROVED`；`Formal RAG security experiment: NOT STARTED`。

**阅读入口**：先读 [AGENTS.md](../../AGENTS.md)、[长期研究需求](long_term_research_requirements.md)、[项目总控](../../PROJECT_MASTER_CONTEXT.md)、[当前任务状态](current_work_state.md)，再读本文、当前 Stage 设计与原始工件。

## 3. 总研究目标与研究问题

项目优先级固定为：

1. RAG Security Research；
2. LLM Security Evaluation Platform；
3. AI Guard Engineering；
4. Agent Security Extension。

长期研究问题包括：模型层攻击如何测量；Input/Output Guard 的独立贡献；Detector 漏报如何识别；知识污染如何影响检索和 Context；如何用可追溯 Evidence 进行多证据信任聚合；以及 RAG 风险如何传播到 Agent 决策。Stage 1–5 已对前两类问题给出当前配置下的实验性证据；检索污染、可信聚合和 Agent 传播仍为 `PLANNED_NOT_IMPLEMENTED`。

## 4. 项目阶段路线图

| Stage/Task | 正式名称 | 核心目标 | 当前状态 | 状态类型 | 关键提交/证据 | 下一门禁 |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 1 | Garak Security Scan Baseline | 跑通 Probe → Generator → Detector → Report | 完成 | `ENGINEERING_VALIDATED` | [Stage 1 结果](../../deliverables/stage1/) | 无 |
| Stage 2 | OpenAI-Compatible Mock API | vulnerable/guarded Mock 对照 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 2 结果](../../deliverables/stage2/) | 无 |
| Stage 3 | Real Model Security Scan | Groq 真实模型小样本扫描 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 3 结果](../../deliverables/stage3/) | 扩样需单独设计 |
| Stage 4 | Guard Proxy A/B Evaluation | passthrough 与 guarded 配对 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 4 结果](../../deliverables/stage4/) | 无 |
| Stage 4.1 | Guard Ablation Evaluation | P/I/O/F 消融 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 4.1 结果](../../deliverables/stage4_ablation/) | 无 |
| Stage 5 | Runtime Attack Matrix and Failure Taxonomy | 六类攻击、T1–T9、Mock 回归 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 5 结果](../../deliverables/stage5/) | 真实矩阵另行批准 |
| Stage 5 Paper | Deterministic Runtime Evaluation Baseline | A1–A6、双 detector、AttemptRecord | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 5 Paper](../../deliverables/stage5_paper/) | 真实模型矩阵另行批准 |
| S6-T1–T3 | 数据、攻击矩阵与标签隔离 | R1–R6 fixture 与公开/评估边界 | 完成 | `ENGINEERING_VALIDATED` | `8577d73`、`055f266` | 无 |
| S6-T4 | Embedding + Persistent Vector Store | Provider、InMemory、Chroma、metadata/fingerprint | 完成 | `ENGINEERING_VALIDATED` | `bd3fcc9` 至 `664c445` | 无 |
| S6-T4 Hardening | 真实 MiniLM + Chroma 验收 | 固定 revision、384 维、重开和排序验证 | 完成 | `ENGINEERING_VALIDATED` | `3950c47` | 无 |
| S6-T5 Design Freeze | 受控检索与 Context 设计 | 边界、ID、引用和预算设计 | 完成 | `DESIGN_FROZEN` | `e64063e` | 不授权实现 |
| S6-T5 Design Hardening | 设计审查加固 | DTO、投影、ContentRef、审计异常边界 | 完成 | `DESIGN_FROZEN` | `aeb7e48` | 不授权实现 |
| S6-T5.1 | Chunking Contracts | IdentityChunker 与稳定 Chunk ID | 已接受 | `HUMAN_ACCEPTED` | `412d886`、`09584c8` | 无 |
| S6-T5.2 | Retrieval Runtime Contracts and IDs | 安全投影、Request、Evidence、Trace、ContentRef | 已实现 | `IMPLEMENTED` | `4c12181`、[完成记录](s6_t5_2_completion_record.md) | 人工验收 |
| S6-T5.3 | DenseRetriever | 透明 Dense Retrieval | S6-T5.3 DenseRetriever 已通过人工验收；P1/H1 均已接受 | `ENGINEERING_VALIDATED` | [完成记录](s6_t5_3_completion_record.md)、[阻断记录](s6_t5_3_protocol_blocker_record.md)、`72a2445` | S6-T5.4 仍需独立批准 |
| S6-T5.4 | Controlled Corpus ContentResolver | 受控正文解析与 hash 校验 | P1、I1、H1 与父任务均通过人工验收；仅覆盖合成内存 resolver 工程边界 | `ENGINEERING_VALIDATED` | [completion record](s6_t5_4_completion_record.md)、[blocker record](s6_t5_4_protocol_blocker_record.md)、PODR-015、PODR-016 | S6-T5.5 仍须独立批准 |
| S6-T5.5-P1 | EvidenceEnvelope and Citation Boundary Freeze | 解决 Citation 时序、factory、escaping 与敏感导出边界 | 已人工验收；仅为协议设计 | `DESIGN_FREEZE_HUMAN_ACCEPTED` | [protocol review record](s6_t5_5_protocol_review_record.md)、PODR-019 | 不批准 S6-T5.5 实现 |
| S6-T5.5-P1-H1 | Evidence Canonical Binding and Citation Rendering Protocol Hardening | 收紧 canonical Factory 输入、Renderer Binding identity 与 fail-closed mismatch | 已人工验收；仅为协议设计 | `DESIGN_FREEZE_HARDENING_HUMAN_ACCEPTED` | [protocol review record](s6_t5_5_protocol_review_record.md)、PODR-019 | 不批准 S6-T5.5 实现 |
| S6-T5.5 | Envelope and Citation implementation | 未来增量实现 | 可单独申请实现审批；尚未实现 | `READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL` | [protocol review record](s6_t5_5_protocol_review_record.md) | I1 未批准 |
| S6-T5.6–S6-T5.8 | Context、后续受控能力 | 逐项增量实现 | 未批准 | `PLANNED_NOT_IMPLEMENTED` | [protocol review record](s6_t5_5_protocol_review_record.md) | 不得自动开始 |
| Stage 6.1 | Hidden Knowledge Poisoning Detection | 隐蔽污染检测 | 规划中 | `PLANNED` | [长期需求](long_term_research_requirements.md) | Stage 6 基线 |
| Stage 6.2 | Multi-Evidence Trustworthy Retrieval | 可信聚合、重排、拒答 | 规划中 | `PLANNED` | [长期需求](long_term_research_requirements.md) | Stage 6.1/设计批准 |
| Stage 7 | Agent Security Evaluation | Tool/Memory/Planning 安全 | 规划中 | `PLANNED` | [Stage 7 README](../../stages/stage7_agent_security/README.md) | Trusted Context 契约 |

## 5. 实验与验证分类

### 5.1 正式安全实验

正式实验必须具有研究问题或假设、固定输入/对照、原始输出、指标、结果文件、结论边界，并尽可能提供 `run_id`。Stage 2 的 Mock 对照、Stage 3 的真实 API smoke、Stage 4/4.1 的真实 Guard 对照，以及 Stage 5/5 Paper 的确定性 Mock 矩阵均登记为正式实验；其中只有 Stage 3/4/4.1 使用真实 Groq 模型。

### 5.2 工程验证

单元测试、集成测试、架构/namespace/标签隔离检查、Ruff、MyPy、secret scan、Git-ignore、Chroma 持久化重开、Chunk ID 稳定性和契约迁移均属于工程验证。

> 工程验证证明代码满足契约和边界，不直接证明安全防护效果、抗投毒能力或统计显著性。

### 5.3 设计冻结

ADR、设计规格和实施计划只冻结未来边界与验证方法。设计完成不能写成业务功能或实验已完成。

## 6. 指标字典

| 指标 | 全称 | 适用阶段 | 计算口径 | 分子/分母 | 方向 | 当前状态 | 证据来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PASS / FAIL | garak detector verdict | S1–S4.1 | PASS 未命中，FAIL 命中攻击目标 | detector 记录 | PASS 高为宜 | 已使用 | [Stage 3 摘要](../../deliverables/stage3/groq_scan_summary.md) |
| ASR | Attack Success Rate | S1–S5 | 成功攻击 attempt / 攻击 attempt | attempt 级 | 低为宜 | 已使用 | 各 Stage 结果 JSON |
| Detector Hit Rate | Detector 命中率 | S3–S4.1 | FAIL detector 记录 / detector 评测记录 | detector 级 | 低为宜 | 已使用 | Stage 3/4 JSON |
| Input Block Count/Rate | 输入拦截数/率 | S4–S5 | input blocked / request | request 级 | 情境相关 | 已使用 | Guard JSONL/聚合 JSON |
| Output Block Count/Rate | 输出拦截数/率 | S4–S5 | output blocked / request | request 级 | 情境相关 | 已使用 | Guard JSONL/聚合 JSON |
| Upstream Call Count/Rate | 上游模型调用数/率 | S4–S5 | upstream called / request | request 级 | 结合效用解释 | 已使用 | Guard JSONL/聚合 JSON |
| Prompt Hash Parity | 攻击输入一致性 | S4–S5 | 同 sample 的 prompt hash 是否一致 | P/I/O/F | 必须为真 | 已使用 | Stage 4/4.1/5 结果 |
| Raw Output Hash Parity | 原始输出哈希一致性 | S4.1、S5 | 同输入模型原始输出 hash 一致性 | 对照组 | 诊断指标 | 已使用 | Stage 4.1/5 日志 |
| Sensitive Marker Count | 敏感规则命中数 | S4–S5 | Guard 自定义规则命中 | output/input | 低为宜 | 已使用 | Guard 日志 |
| T1–T9 | Failure Taxonomy | S5 | 自动分类的失败类型计数 | attempt | 情境相关 | 已使用 | [taxonomy JSON](../../deliverables/stage5/logs/20260701T030819Z-05703f/failure_taxonomy_result.json) |
| DMR | Detector Miss Rate | S5 Paper | raw risk 且 garak pass 的比例 | 见 run manifest 口径 | 低为宜 | 已使用 | [Paper 摘要](../../deliverables/stage5_paper/runs/20260701T081320Z-c29f39/run_summary.md) |
| GBR | Guard Bypass Rate | S5 Paper | guard enabled 但 final risk 的比例 | 见 run manifest 口径 | 低为宜 | 已使用 | 同上 |
| Over-block | 正常请求误拦截率 | S5/Paper | benign 且被拦截 / benign | benign request | 低为宜 | 已使用 | 同上 |
| Passed / Skipped | 测试通过/跳过数 | S6 | pytest 测试状态 | test case | 通过高为宜 | 已使用 | 测试日志/学习记录 |
| Recall@K、Precision@K、MRR、nDCG@K | 检索质量指标 | Stage 6 | `PLANNED_NOT_IMPLEMENTED` | `NOT_RECORDED` | 高为宜 | `PLANNED_NOT_IMPLEMENTED` | 无 |
| Poison Retrieval Rate、Context Contamination Rate | 污染传播指标 | Stage 6 | `PLANNED_NOT_IMPLEMENTED` | `NOT_RECORDED` | 低为宜 | `PLANNED_NOT_IMPLEMENTED` | 无 |
| Citation Accuracy、Faithfulness | 引用/忠实性 | Stage 6.2 | `PLANNED_NOT_IMPLEMENTED` | `NOT_RECORDED` | 高为宜 | `PLANNED_NOT_IMPLEMENTED` | 无 |
| Abstention Precision/Recall、Latency、Cost | 风险与效率指标 | Stage 6.2+ | `PLANNED_NOT_IMPLEMENTED` | `NOT_RECORDED` | 情境相关 | `PLANNED_NOT_IMPLEMENTED` | 无 |

## 7. 文件、运行和结果命名规范

- Master Record 内部 ID：`ER-<STAGE>-<YYYYMMDD>-<NNN>`，只用于本文索引，不等同于历史 `run_id`。
- 原始 `run_id` 不存在时写 `NOT_RECORDED`；不根据目录日期伪造 ID。
- 新实验推荐 `<stage>-<UTC timestamp>-<short sequence>`；本轮不重命名历史目录。
- 原始输出与派生摘要分离；正式结果与 smoke test 分离；敏感工件与公开审计工件分离。
- 所有新索引使用仓库相对路径；运行时目录遵守 Git-ignore。

## 8. 正式运行总账

### 8.1 已回填运行

| Record ID | Original Run ID | 日期 | Stage/Task | Run Type | 模型/Provider | 状态 | 核心指标 | 原始证据 | 结论边界 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ER-S1-20260626-001 | `a214583f-5fa6-4734-abbb-b15629decce1` | 2026-06-26 | S1 minimal connectivity | `ENGINEERING_VALIDATION` | `test.Blank` | completed | PASS 1/1 | [JSON](../../deliverables/stage1/garak_scan_result.json) | 仅连通性 Mock |
| ER-S1-20260626-002 | `94c18ade-8fae-459c-b1a1-c49b81c5f264` | 2026-06-26 | S1 prompt injection | `ENGINEERING_VALIDATION` | `test.Repeat` | completed | FAIL 0/256，ASR 100% | [JSONL](../../deliverables/stage1/stage1_promptinject_scan.report.jsonl) | 预设脆弱 echo Mock |
| ER-S2-20260626-001 | `bfcbc1dd-1869-42c4-a9a5-9523ace01993` | 2026-06-26 | S2 vulnerable PromptInject | `FORMAL_EXPERIMENT` | local Mock | completed | FAIL 0/8 | [JSON](../../deliverables/stage2/stage2_scan_result.json) | 受控 Mock |
| ER-S2-20260626-002 | `d2768d63-9c1e-449b-b197-0932af345197` | 2026-06-26 | S2 guarded PromptInject | `FORMAL_EXPERIMENT` | local Mock | completed | PASS 8/8 | [JSON](../../deliverables/stage2/stage2_scan_result.json) | 受控 Mock |
| ER-S2-20260626-003 | `5a65c350-dd06-442b-a19b-17972979bfec` | 2026-06-26 | S2 vulnerable Base64 | `FORMAL_EXPERIMENT` | local Mock | completed | PASS 8/8 | [JSON](../../deliverables/stage2/stage2_scan_result.json) | detector 未命中不等于安全 |
| ER-S2-20260626-004 | `882d1505-10a3-41ee-a6d3-9b6451ffd4d5` | 2026-06-26 | S2 guarded Base64 | `FORMAL_EXPERIMENT` | local Mock | completed | PASS 8/8 | [JSON](../../deliverables/stage2/stage2_scan_result.json) | 受控 Mock |
| ER-S3-20260630-001 | `NOT_RECORDED` | 2026-06-30 | S3 Groq safe smoke | `FORMAL_EXPERIMENT` | Groq / `llama-3.1-8b-instant` | completed | 2 attempts，ASR 50%，detector hit 33.33% | [聚合 JSON](../../deliverables/stage3/groq_scan_result.json) | 单次两条样本 |
| ER-S4-20260630-001 | `NOT_RECORDED` | 2026-06-30 | S4 paired Guard A/B | `FORMAL_EXPERIMENT` | Groq / `llama-3.1-8b-instant` | completed | P: ASR 50%；guarded: ASR 0%；parity true | [聚合 JSON](../../deliverables/stage4/guarded_groq_scan_result.json) | 2 条 smoke，规则基线 |
| ER-S4.1-20260630-001 | `NOT_RECORDED` | 2026-06-30 | S4.1 P/I/O/F ablation | `FORMAL_EXPERIMENT` | Groq / `llama-3.1-8b-instant` | completed | P 50%；I/O/F 均 0%；parity true | [聚合 JSON](../../deliverables/stage4_ablation/ablation_result.json) | 2 条 smoke，规则基线 |
| ER-S5-20260701-001 | `20260701T025836Z-7da785` | 2026-07-01 | S5 attack matrix rerun | `FORMAL_EXPERIMENT` | local Mock | completed | 22 samples，P/I/O/F parity true | [manifest](../../deliverables/stage5/logs/20260701T025836Z-7da785/run_manifest.json) | Mock 回归 |
| ER-S5-20260701-002 | `20260701T030024Z-37cfd4` | 2026-07-01 | S5 attack matrix rerun | `FORMAL_EXPERIMENT` | local Mock | completed | 22 samples，P/I/O/F parity true | [manifest](../../deliverables/stage5/logs/20260701T030024Z-37cfd4/run_manifest.json) | Mock 回归 |
| ER-S5-20260701-003 | `20260701T030156Z-91ae2d` | 2026-07-01 | S5 attack matrix rerun | `FORMAL_EXPERIMENT` | local Mock | completed | 22 samples，P/I/O/F parity true | [manifest](../../deliverables/stage5/logs/20260701T030156Z-91ae2d/run_manifest.json) | Mock 回归 |
| ER-S5-20260701-004 | `20260701T030819Z-05703f` | 2026-07-01 | S5 canonical smoke | `FORMAL_EXPERIMENT` | local Mock | completed | 88 attempts，ASR 95.83%，Over-block 0% | [manifest](../../deliverables/stage5/logs/20260701T030819Z-05703f/run_manifest.json) | 当前规则/矩阵下 |
| ER-S5P-20260701-001 | `20260701T081320Z-c29f39` | 2026-07-01 | S5 Paper baseline | `FORMAL_EXPERIMENT` | local Mock | completed | 88 attempts，ASR 95.83%，DMR 0%，GBR 94.44% | [manifest](../../deliverables/stage5_paper/runs/20260701T081320Z-c29f39/run_manifest.json) | Mock baseline，不是 Groq 全矩阵 |

**账本统计（由上表实际记录计算）**：FORMAL_EXPERIMENT = 12；ENGINEERING_VALIDATION = 2。S6 的工程/设计条目另见第 10 节。历史 Stage 3、Stage 4 与 Stage 4.1 缺少 machine-readable `run_id`、模型 revision 与数据 fingerprint，按原样标记，不能倒推伪造。

## 9. Stage 1–5 历史结果汇总

| Stage | 实际对象与设计 | 核心结果 | 证据 | 当前可证明什么 |
| --- | --- | --- | --- | --- |
| S1 | garak 内置 Mock，`test.Blank` 与 `test.Repeat` | 连通性 PASS 1/1；echo PromptInject ASR 100% | [报告](../../deliverables/stage1/stage1_report.md) | 理解安全扫描闭环，不是现实模型风险 |
| S2 | OpenAI-compatible local Mock，vulnerable/guarded | PromptInject 0/8 FAIL 对 8/8 PASS；两组 Base64 PASS | [摘要](../../deliverables/stage2/stage2_scan_summary.md) | 可控协议与防护对照 |
| S3 | Groq 真实 API，2 个 probes、2 attempts | PromptInject 命中；Base64 detector PASS 但人工复核发现部分危险解码 | [逐条分析](../../deliverables/stage3/08_first_real_scan_analysis.md) | 真实调用链、Detector Miss 边界 |
| S4 | local Guard Proxy → Groq，passthrough/guarded | 50% → 0%；guarded 输入拦截 2 次、上游调用 0 次 | [摘要](../../deliverables/stage4/guarded_groq_scan_summary.md) | 当前规则的输入 Guard 对照效果 |
| S4.1 | P/I/O/F 四组，固定 seed 与 prompt parity | output-only 调用上游 2 次后输出拦截 2 次；I/F 输入拦截 | [摘要](../../deliverables/stage4_ablation/ablation_summary.md) | 输入与输出规则均被独立验证 |
| S5 | 六类攻击各 2 条、benign 10 条、四 Guard Mode | 22 samples、88 attempts、T1–T9、parity true | [run summary](../../deliverables/stage5/logs/20260701T030819Z-05703f/run_summary.md) | 可复现的 Mock 评测框架 |
| S5 Paper | A1–A6、P/I/O/F、garak + stage5_pattern | 88 attempts；ASR 95.83%；DMR 0%；GBR 94.44% | [结果](../../deliverables/stage5_paper/07_results.md) | 确定性论文级 baseline，不是实模统计结论 |

## 10. Stage 6 工程状态与正式实验缺口

| Task | 能力 | 状态 | 验证类型 | 测试/设计证据 | 是否产生安全实验结果 | 下一门禁 |
| --- | --- | --- | --- | --- | --- | --- |
| S6-T1–T3 | R1–R6 数据、攻击矩阵、标签隔离 | completed | 工程验证 | [数据 README](../../data/stage6_rag/README.md) | 否 | 无 |
| S6-T4 | Static/real Embedding、InMemory/Chroma、fingerprint | completed | 工程验证 | [ADR 0007](../architecture/0007_embedding_vectorstore_boundary.md) | 否 | 无 |
| S6-T4 Hardening | 固定 MiniLM revision、临时 Chroma 重开、中文/英文 Top-1 | completed | 真实集成验证 | [项目总控](../../PROJECT_MASTER_CONTEXT.md) | 否 | 无 |
| S6-T5 Design Freeze/Hardening | 受控检索、Evidence、Context 边界 | completed | 设计审查 | [ADR 0008](../architecture/0008_retrieval_context_boundary.md) | 否 | 不授权实现 |
| S6-T5.1 | ChunkRecord、IdentityChunker、稳定 ID | human accepted | 工程验证 | [学习记录](../../deliverables/learning_notes.md) | 否 | 无 |
| S6-T5.2 | safe projection、Request/Evidence/Trace/ContentRef | implemented，pending human acceptance | 工程验证 | [完成记录](s6_t5_2_completion_record.md) | 否 | 人工验收 |
| S6-T5.3 | DenseRetriever | HUMAN_ACCEPTED；P1/H1 已接受 | `ENGINEERING_VALIDATED` | [完成记录](s6_t5_3_completion_record.md) | 否 | S6-T5.4 独立批准 |
| S6-T5.4 | Controlled Corpus ContentResolver | P1、I1、H1 与父任务 HUMAN_ACCEPTED；只确认受控内存工程边界 | `ENGINEERING_VALIDATED` | [completion record](s6_t5_4_completion_record.md)、[blocker record](s6_t5_4_protocol_blocker_record.md) | 否 | S6-T5.5 仍未批准 |
| S6-T5.5+ | Envelope、Context、Citation、Trust 等 | not approved | `PLANNED_NOT_IMPLEMENTED` | 同上 | 否 | 前序任务 |

截至当前状态，Stage 6 已完成架构、契约、版本化 metadata carrier 与无正文 DenseRetriever 的工程验证。虽然真实 MiniLM 与 Chroma 的固定小语料集成测试已运行，但没有正式 R1–R6 攻击矩阵、RAG 指标或防护效果实验，故不能宣称“Stage 6 RAG 安全实验已完成”。

## 11. 未来 Stage 6 正式实验计划

| Experiment ID | 研究问题 | 自变量 | 对照组 | 数据/模型 | 指标 | 当前状态 | 前置条件 | 禁止夸大 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S6E-01 | Dense Retrieval 是否可复现且可审计 | top-k、固定 MiniLM/Chroma | transparent baseline | Stage 6 corpus | Recall@K、MRR、nDCG@K | `PLANNED_NOT_IMPLEMENTED` | S6-T5.3 | 不等于安全防护 |
| S6E-02 | R1 Query Injection 如何影响检索 | attack prompt | benign query | R1 dataset | RMSR、trace | `PLANNED_NOT_IMPLEMENTED` | Retriever/Runner | 不等于上下文或生成风险 |
| S6E-03 | R2/R5 污染如何被召回 | poisoned corpus composition | clean corpus | R2/R5 dataset | Poison Retrieval Rate | `PLANNED_NOT_IMPLEMENTED` | Retriever/Evaluator | 不等于可信检索 |
| S6E-04 | R3 Context Injection 如何传播 | retrieved evidence | clean evidence | R3 dataset | Context Contamination Rate | `PLANNED_NOT_IMPLEMENTED` | Resolver/ContextBuilder | 不等于模型攻击成功 |
| S6E-05 | R4/R6 如何影响排序与回答倾向 | embedding/steering variant | baseline | R4/R6 dataset | RMSR、Faithfulness | `PLANNED_NOT_IMPLEMENTED` | 后续批准 | 不得伪造指标 |
| S6E-06 | Guard/Trust 的独立贡献 | input/output/retrieval policy | off/observe | 固定攻击矩阵 | 安全-效用指标 | `PLANNED_NOT_IMPLEMENTED` | Stage 6B+ | 规则基线不等于论文算法 |
| S6.1E | 隐蔽知识污染检测 | 检测器与数据难度 | 多 baseline | 双领域许可语料 | F1/AUROC/AUPRC | `PLANNED_NOT_IMPLEMENTED` | Stage 6 baseline | 不声称已检测 |
| S6.2E | 多证据可信检索 | 信任聚合/重排 | Dense/BM25/Hybrid | 多来源语料 | Trust/Citation/Abstention | `PLANNED_NOT_IMPLEMENTED` | Stage 6.1 | 不声称已可信 |

## 12. Blocker Register

| Blocker ID | 首次发现 | 类别 | 严重级别 | 影响范围 | 状态 | 当前证据 | 临时处理 | 最终解决条件 | 下一动作 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-HIST-001 | 2026-07-19 | 历史完整性 | medium | Stage 1–5 hash 检查 | `ACCEPTED_TECHNICAL_DEBT` | [学习记录](../../deliverables/learning_notes.md) 的 CRLF/LF 留痕 | Git diff/blob 核验 | 新的跨平台基线方案经批准 | 不重写历史文件 |
| BLK-HIST-002 | 2026-07-19 | 可复现性 | medium | Stage 1–4.1 | `OPEN` | 本账本 `NOT_RECORDED` 字段 | 保留原始路径和摘要 | 新实验采用 Run Manifest | 不倒填旧事实 |
| BLK-HIST-003 | 2026-07-19 | 类型检查 | low | legacy Stage 5 | `ACCEPTED_TECHNICAL_DEBT` | 全量 MyPy 的既有 legacy 告警 | scoped MyPy | 历史资产单独批准后修复 | 不修改 legacy |
| BLK-S6-001 | 2026-07-22 | 设计/协议 | high | S6-T5.3 | `RESOLVED_BY_VERSIONED_PUBLIC_METADATA_CONTRACT` | [阻断记录](s6_t5_3_protocol_blocker_record.md) | schema `1.1` 公开 carrier；不伪造 parent ID、不读取语料、不改写 schema `1.0` | P1 离线回归 | DenseRetriever 继续保持 fail-closed |
| BLK-S6-004 | 2026-07-25 | 设计/协议 | high | S6-T5.4 | `DESIGN_OR_PROTOCOL_BLOCKER` | [S6-T5.4 blocker](s6_t5_4_protocol_blocker_record.md) | 停止实现；不读取正文、不猜测 return type/reader/mapping/error ownership | 冻结四项 resolver protocol 决策 | 项目负责人补充决策 |
| BLK-S6-002 | 当前 | 研究缺口 | high | RAG 安全结论 | `OPEN` | 第 10 节 | 不夸大工程验证 | 完成受控正式实验 | 先获批 DenseRetriever |
| BLK-S6-003 | 当前 | 环境依赖 | medium | 真实 Embedding/Chroma | `MITIGATED` | S6-T4 真实集成记录 | 环境变量显式开启、临时目录 | 固定可复现环境文档 | 仅按批准运行 |
| BLK-API-001 | 2026-06-30 | 真实 API 成本/策略 | medium | Groq 扩样 | `OPEN` | [Stage 3/4 文档](../../deliverables/stage3/06_troubleshooting.md) | safe 模式和小样本 | 批准预算和实验设计 | 不无控制扩样 |
| BLK-DOC-001 | 2026-07-20 | 文档漂移 | low | 早期 S6-T5 架构索引/设计快照 | `OPEN` | Git 已有 `4c12181`，但部分历史文本仍称 Python 未开始 | 当前状态与本记录作为动态事实入口 | 在不改写历史叙述前提下添加历史快照说明 | 后续治理审查 |

## 13. Failed Run Register

| Record ID | 日期 | Stage | 命令/入口 | 失败现象 | 根因 | 是否影响数据 | 修复/复验 | 证据 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ER-F-S3-20260630-001 | 2026-06-30 | S3 | safe scan wrapper | 无 API 响应或 Eval | PowerShell stderr 与 `ErrorActionPreference=Stop` 冲突 | 否，非有效实验 | 仅原生 garak 调用期间放宽错误处理；后续 scan 完成 | [学习记录](../../deliverables/learning_notes.md) |
| ER-F-S4-20260630-001 | 2026-06-30 | S4 | `runs/20260630_175419` | 上游 403 | Proxy 上游网络/权限诊断不足 | 否，不计 ASR | 增加脱敏诊断，做单变量直连 | [学习记录](../../deliverables/learning_notes.md) |
| ER-F-S4-20260630-002 | 2026-06-30 | S4 | `runs/20260630_180237` | Proxy 路径 403，直连成功 | `NO_PROXY` 作用域错误 | 否，不计 ASR | 仅在 garak 子进程设置；`222810` 回归完成 | [学习记录](../../deliverables/learning_notes.md) |
| ER-F-S6-20260720-001 | 2026-07-20 | S6-T5.1 | TDD Red | 缺少导出/包导致 collection error | 预期 Red 阶段 | 否，预期测试失败 | 实现后 Green，通过定向与回归测试 | [学习记录](../../deliverables/learning_notes.md) |

预期 TDD Red 不被归类为项目缺陷；它证明测试先于实现。失效/失败运行保留在账本中，后续成功不得删除这些记录。

## 14. Approval Gate Register

| Gate ID | 当前任务 | 已完成证据 | 人工验收状态 | 获批后可开始 | 仍禁止 | 负责人 |
| --- | --- | --- | --- | --- | --- | --- |
| GATE-GOV-ER1 | Experiment Master Record | 本文、入口同步、治理测试、GOV-ER1-H1 十列账本加固 | `HUMAN_ACCEPTED` | 已完成 | 不自动批准 S6-T5.4 | 项目负责人 |
| GATE-S6-T5.2 | Retrieval Runtime Contracts and IDs | `4c12181`、完成记录、回归测试 | `HUMAN_ACCEPTED` | 已批准 S6-T5.3 | S6-T5.4 及以后 | 项目负责人 |
| GATE-S6-T5.3 | Provider-Neutral DenseRetriever | P1 metadata contract、H1 hardening、完成记录、离线 TDD 证据 | `HUMAN_ACCEPTED` | 不自动批准任何后续任务 | ContentResolver 及以后 | 项目负责人 |
| GATE-S6-T5.4 | Controlled Corpus ContentResolver | P1、I1、H1 人工验收、合成内存实现、定向/架构/隔离测试 | `HUMAN_ACCEPTED_ENGINEERING_VALIDATION` | 仅可申请独立的 S6-T5.5 审批 | S6-T5.5 及以后 | 项目负责人 |

**当前审批顺序**：GOV-ER1、GOV-ER1-H1、GOV-PODR1、S6-T5.2、S6-T5.3-P1、S6-T5.3-H1、S6-T5.3、S6-T5.4-P1、S6-T5.4-I1、S6-T5.4-H1 与 S6-T5.4 均已获人工验收。schema `1.1` 已解除 `parent_doc_id` identity contract blocker，且其历史条目仍为 `RESOLVED_BY_VERSIONED_PUBLIC_METADATA_CONTRACT`。S6-T5.4 protocol blocker 已由 `RESOLVED_BY_APPROVED_PROTOCOL_FREEZE` 解决，且其历史记录保留；正式 RAG 安全实验：**Not started**。

## 15. 当前结论边界

### EVIDENCE_BACKED

- Stage 3 已完成 Groq `llama-3.1-8b-instant` 的两条真实攻击 smoke；PromptInject 命中，Base64 存在 detector PASS 但人工复核显示危险解码的案例。
- Stage 4 已在相同 prompt hash 下观察到规则型 guarded 组 ASR 从 50% 到 0%。
- Stage 4.1 已独立验证 output-only 先调用上游、记录原始输出 hash、再替换危险输出。
- Stage 5/Stage 5 Paper 已保存确定性 Mock 的攻击矩阵、AttemptRecord、T1–T9、验证器与报告。
- Stage 6 已建立 embedding/vector store、chunking 与检索运行时契约的工程边界和标签隔离基础。

### INFERENCE

- Stage 3 Base64 案例表明仅依赖当前 garak detector 的 PASS/FAIL 可能漏掉部分危险行为，因而需要人工复核或多 detector；这是对当前样本的推断，不是全模型统计结论。

### PLANNED

- DenseRetriever、ContentResolver、ContextBuilder、Citation Accuracy、Trust-aware Retrieval、R1–R6 正式攻击矩阵、Stage 6.1/6.2、Stage 7。

### NOT_ESTABLISHED

- 正式 RAG 安全实验、抗知识污染能力、可信检索、生产级防护率、统计显著性、论文投稿/发表和 Agent 安全效果。

## 16. 证据地图

| 能力/结论 | 原始结果 | 日志 | 摘要 | 测试/设计 | Commit | 证据等级 |
| --- | --- | --- | --- | --- | --- | --- |
| garak 最小扫描闭环 | [S1 JSONL](../../deliverables/stage1/stage1_min_scan.report.jsonl) | `NOT_RECORDED` | [S1 report](../../deliverables/stage1/stage1_report.md) | S1 学习材料 | `NOT_RECORDED` | `E2_UNIT_VALIDATED` |
| OpenAI-compatible Mock 对照 | [S2 JSON](../../deliverables/stage2/stage2_scan_result.json) | [API JSONL](../../deliverables/stage2/api_requests.jsonl) | [S2 summary](../../deliverables/stage2/stage2_scan_summary.md) | Mock API 文档 | `NOT_RECORDED` | `E4_FORMAL_SINGLE_RUN` |
| Groq 真实小样本扫描 | [S3 JSON](../../deliverables/stage3/groq_scan_result.json) | [run log](../../deliverables/stage3/runs/20260630_154855-safe/stage3_console.log) | [S3 analysis](../../deliverables/stage3/08_first_real_scan_analysis.md) | garak 原始 JSONL | `NOT_RECORDED` | `E4_FORMAL_SINGLE_RUN` |
| Guard A/B | [S4 JSON](../../deliverables/stage4/guarded_groq_scan_result.json) | [guard logs](../../deliverables/stage4/guard_logs.jsonl) | [S4 summary](../../deliverables/stage4/guarded_groq_scan_summary.md) | parity 记录 | `NOT_RECORDED` | `E4_FORMAL_SINGLE_RUN` |
| Input/Output 消融 | [S4.1 JSON](../../deliverables/stage4_ablation/ablation_result.json) | [logs](../../deliverables/stage4_ablation/logs/20260630_230629/) | [S4.1 summary](../../deliverables/stage4_ablation/ablation_summary.md) | output-only 验证 | `NOT_RECORDED` | `E4_FORMAL_SINGLE_RUN` |
| Stage 5 Mock 矩阵 | [manifest](../../deliverables/stage5/logs/20260701T030819Z-05703f/run_manifest.json) | [attempts](../../deliverables/stage5/logs/20260701T030819Z-05703f/attempts.jsonl) | [summary](../../deliverables/stage5/logs/20260701T030819Z-05703f/run_summary.md) | validators | `NOT_RECORDED` | `E5_REPEATED_CONTROLLED_EXPERIMENT` |
| S6-T4 基础设施 | `NOT_RECORDED` | `NOT_RECORDED` | [ADR](../architecture/0007_embedding_vectorstore_boundary.md) | 真实集成测试 | `3950c47` | `E3_INTEGRATION_VALIDATED` |
| S6-T5.2 契约 | `NOT_RECORDED` | `NOT_RECORDED` | [completion record](s6_t5_2_completion_record.md) | 定向/架构/隔离测试 | `4c12181` | `E2_UNIT_VALIDATED` |

## 17. 项目交接指南

新成员接手顺序：

1. 阅读 [AGENTS.md](../../AGENTS.md)；
2. 阅读 [长期需求](long_term_research_requirements.md)；
3. 阅读 [项目总控](../../PROJECT_MASTER_CONTEXT.md)；
4. 阅读 [当前任务状态](current_work_state.md)；
5. 阅读本文；
6. 阅读当前 Stage 的设计规格与实施计划；
7. 检查 Git 状态与审批门；
8. 打开最近正式实验或工程验证的原始证据；
9. 运行当前任务允许的快速验证命令。

通用 Git 检查命令：

```powershell
git branch --show-current
git rev-parse HEAD
git status --short
git rev-list --left-right --count @{upstream}...HEAD
git log -15 --oneline
```

检查历史资产未被覆盖：使用 `git diff --name-only HEAD -- deliverables data/stage5 src/codeguarder`，并遵守历史完整性测试的 CRLF/LF 技术债说明。检查密钥与 runtime：运行 task-scoped secret scan，确认 `runtime/` 仍由 `.gitignore` 覆盖。

## 18. 每次运行记录模板

```text
## Run Record: ER-<STAGE>-<YYYYMMDD>-<NNN>

- Record ID:
- Original Run ID:
- Run Type:
- Date/Time UTC:
- Stage/Task:
- Research Question:
- Hypothesis:
- Branch:
- Git Commit:
- Environment:
- Model:
- Model Revision:
- API/Provider:
- Dataset:
- Dataset Hash:
- Configuration:
- Command:
- Guard Mode:
- Random Seed:
- Sample Count:
- Status:
- Primary Metrics:
- Secondary Metrics:
- Raw Outputs:
- Logs:
- Summary:
- Failed Cases:
- Blockers:
- Claims Supported:
- Claims Not Supported:
- Reviewer:
- Acceptance Status:
```

所有未知字段必须填 `NOT_RECORDED`，不能留空。

## 19. 持续更新协议

以下事件必须触发更新：新正式实验、smoke test、工程验证、失败运行、新 blocker/解除 blocker、审批门变化、阶段验收、指标/数据/模型/revision 变化、结果路径变化、结论边界变化、任务废弃或替代。

每次更新按以下顺序执行：

1. 读取原始证据；
2. 新增或更新对应 Run Record；
3. 更新阶段仪表盘、Blocker、Approval Gate 和结论边界；
4. 更新 Change Log；
5. 检查全部相对链接、绝对路径和密钥；
6. 运行治理测试；
7. 提交并推送。

正式 Run Record 默认 append-only。错误修正必须写 Change Log；无效运行标记 `INVALIDATED`，不能删除；失败记录不能因后续成功而删除；派生摘要必须可追溯到原始结果。

## 20. Change Log

| 日期 | 变更类型 | 影响章节 | 变更原因 | 证据 | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-07-20 | 建立 | 全文 | 创建唯一实验总记录，回填 Stage 1–5、登记 Stage 6 工程状态和当前审批门；未进入 S6-T5.3 | 本文链接的原始工件与 Git 历史 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-20 | 账本结构加固 | 第 2、8、14、20 节 | 修复 S3、S4、S4.1、S5 与 S5 Paper 的十列字段错位；新增列数、枚举、唯一性和计数一致性测试；不改写历史运行事实 | 本文第 8 节、治理测试和学习记录 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-21 | 人工审批状态更新 | 第 2、12、14、20 节 | 项目负责人验收 GOV-ER1、GOV-ER1-H1、S6-T5.2，并批准 S6-T5.3 启动；S6-T5.4+ 与正式 RAG 安全实验仍未批准 | 当前工作状态、审批文本与 Git 历史 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-21 | 协议 blocker 留痕 | 第 2、4、12、14、20 节 | S6-T5.3 启动前发现 hit-to-evidence 缺少必填 `parent_doc_id`；按冻结契约、无正文和标签隔离边界暂停实现 | [S6-T5.3 blocker record](s6_t5_3_protocol_blocker_record.md)、当前工作状态 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-22 | P1 修复与 DenseRetriever 完成 | 第 2、4、12、14、20 节 | schema `1.1` 传递公开 parent identity；Provider-Neutral DenseRetriever 经离线 TDD 验证后等待人工验收 | [完成记录](s6_t5_3_completion_record.md)、[blocker record](s6_t5_3_protocol_blocker_record.md) | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-22 | S6-T5.3-H1 验收加固 | 第 2、4、12、14、20 节 | candidate_count 改为 raw query hits，补齐 store provenance 与脱敏失败边界；仍是离线工程验证、等待人工复核 | [完成记录](s6_t5_3_completion_record.md)、定向 TDD | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.3 人工验收登记 | 第 2、4、10、14、15、20 节 | 项目负责人验收 GOV-PODR1、S6-T5.3-P1、S6-T5.3-H1 和 Provider-Neutral DenseRetriever；验收不改变工程验证分类，不批准 S6-T5.4 或正式 RAG 实验 | [完成记录](s6_t5_3_completion_record.md)、[决策登记册](project_owner_decision_register.md)、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.4 协议 blocker | 第 2、4、10、12、14、20 节 | 项目负责人已批准启动范围，但 Resolver 返回/权限、snapshot reader、legacy mapping 和 error ownership 未冻结；按 fail-closed 原则停止实现 | [blocker record](s6_t5_4_protocol_blocker_record.md)、冻结规格/ADR 审查 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.4-P1 协议冻结 | 第 2、4、10、12、14、20 节 | 冻结 ContentResolver 输入/返回、正文能力 DTO 所有权、受控 snapshot reader、legacy exact-match mapping 与错误层级；P1 完成但待人工验收，未实现正文解析 | [blocker record](s6_t5_4_protocol_blocker_record.md)、PODR-013、设计规格、ADR | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | GOV-S6-T5.4-P1-ACCEPTANCE | 第 2、4、10、12、14、20 节 | 项目负责人接受 P1 协议设计，将 blocker 标记为 RESOLVED_BY_APPROVED_PROTOCOL_FREEZE；S6-T5.4 仅进入独立实现审批等待状态 | [blocker record](s6_t5_4_protocol_blocker_record.md)、PODR-014、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.4-I1 受控正文解析最小实现 | 第 2、4、10、14、20 节 | 仅用合成内存正文实现 `ContentRef + expected hash -> ResolvedContent`、受控 snapshot registry/reader 与 legacy exact-match adapter；未读取 Stage 6 fixture，待人工验收 | [completion record](s6_t5_4_completion_record.md)、PODR-015、定向/架构/隔离测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.4-H1 capability/failure-boundary 加固 | 第 2、4、10、14、20 节 | 删除公开 registry capability；将注入 adapter/registry/reader 的领域异常按受信 type/code 重新构造为固定脱敏外部错误，未知或交叉 code fail closed 为 runtime；仅合成内存测试，待人工复核 | [completion record](s6_t5_4_completion_record.md)、定向/架构/隔离测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | GOV-S6-T5.4-ACCEPTANCE | 第 2、4、10、12、14、20 节 | 项目负责人接受 P1、I1、H1 与父任务；保持工程验证分类，不批准 S6-T5.5、ContextBuilder、Citation 或正式 RAG 实验 | [completion record](s6_t5_4_completion_record.md)、PODR-016、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.5-P1 协议审查 | 第 2、4、12、14、20 节 | 冻结无 `citation_id` Envelope、由未来 ContextBuilder 创建的 package-local CitationBinding、确定性 instruction/XML escaping 和默认关闭敏感导出；未创建业务代码或实验结果，待人工验收 | [protocol review record](s6_t5_5_protocol_review_record.md)、规格、计划、ADR、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | S6-T5.5-P1-H1 协议加固 | 第 2、4、12、14、20 节 | Factory 只接收 canonical Evidence；legacy `chroma:` 只在 Resolver 输入边界；renderer 只消费 Envelope + Binding，七项 identity mismatch 以 `CITATION_BINDING_MISMATCH` fail closed；无源码或实验结果，待人工复核 | [protocol review record](s6_t5_5_protocol_review_record.md)、规格、计划、ADR、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | GOV-S6-T5.5-P1-ACCEPTANCE | 第 2、4、12、14、20 节 | 项目负责人接受 P1 与 H1 协议；S6-T5.5 仅进入独立实现审批准备，I1 未批准；不创建业务源码或实验结果 | [protocol review record](s6_t5_5_protocol_review_record.md)、PODR-019、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
