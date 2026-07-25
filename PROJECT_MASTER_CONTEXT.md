# LLMGuard 项目总控文档

> 这是项目唯一的总览与决策入口。它回答：为什么做、已经做了什么、证据在哪里、当前代码处于什么状态、未来架构如何同时支撑面试、论文和科技立项。

更新时间：2026-07-22

当前研究分支：`feature/stage6-rag`

文档状态：A0 架构冻结、A1R 命名/namespace 迁移与 S6-T4 真实集成加固已完成

长期研究需求基线：[docs/governance/long_term_research_requirements.md](docs/governance/long_term_research_requirements.md)。
它固定 RAG 安全为第一优先级，并约束语料域、标签隔离、证据/引用、上下文分级、拒答和 Stage 6.1/6.2/7
路线；任何较早实施草案与其冲突时，以该基线和本文的较新状态为准。

## Repository Context Persistence

根目录 `AGENTS.md` 是 Codex 仓库上下文入口；长期目标以
`docs/governance/long_term_research_requirements.md` 为准；项目负责人已确认的解释和决策见
`docs/governance/project_owner_decision_register.md`；本文件负责总体架构、阶段进度和结论边界；
`docs/governance/current_work_state.md` 负责当前任务与审批门。新 Thread、Agent、Workspace 或 Worktree
必须遵守 `docs/governance/context_recovery_protocol.md`。Git 是 branch、HEAD、工作树、commit、文件
存在性和远端同步状态的事实来源。

实验路线、历史运行、指标、证据、失败和交接入口统一见
`docs/governance/experiment_master_record.md`。该总记录只做控制面与索引，不替代本文件的架构叙事、
`current_work_state.md` 的动态审批门或 Stage-specific 原始产物。

职责边界固定为：长期需求记录长期能力要求；项目负责人决策登记册记录明确确认的解释与决策；项目总控
记录架构与阶段叙事；动态状态记录当前任务与审批；实验总账记录实验与证据索引；Git 记录动态工程事实。

### GOV-ER1：Experiment Master Record（2026-07-20）

已建立唯一的 [Experiment Master Record](docs/governance/experiment_master_record.md)，用于索引 Stage 1–5 的原始运行、指标、证据、失败记录与结论边界，并登记 Stage 6 的工程验证缺口、审批门和交接顺序。它不改写历史工件、不替代动态工作状态，也不授权 S6-T5.3；当前仍需人工审查总记录与 S6-T5.2 验收证据。

**状态更新（2026-07-21）**：项目负责人已将 GOV-ER1、GOV-ER1-H1 与 S6-T5.2 标记为 `HUMAN_ACCEPTED`，并单独批准 `S6-T5.3 DenseRetriever` 启动。该审批仅覆盖离线、Provider-Neutral DenseRetriever 的工程实现与验证；不覆盖 ContentResolver、Context、Trust、LLM/Groq 或正式 RAG 安全实验。

**协议 blocker（2026-07-21）**：启动前核查发现，S6-T4 的 `VectorSearchHit` 及公开 metadata 无法提供 S6-T5.2 canonical `RetrievalEvidence` 强制要求的 `parent_doc_id`。Retriever 又不允许读取语料、伪造父文档身份或修改冻结契约，因此 S6-T5.3 正确暂停，等待人工批准安全的 hit-to-evidence identity contract。

**S6-T5.3-P1 与 DenseRetriever（2026-07-22）**：项目负责人批准后，`parent_doc_id` 被定义为公开、非标签、无正文的 provenance identity。VectorStore schema `1.1` 将它沿 `ChunkRecord -> VectorDocument -> VectorSearchHit -> RetrievalEvidence` 传递，schema `1.0` 保持旧 collection 兼容；collection fingerprint 因 schema 版本而隔离。随后实现 Provider-Neutral DenseRetriever，严格执行 `RetrievalRequest -> EmbeddingProvider -> VectorStore -> VectorSearchHit -> RetrievalEvidence -> RetrievalTrace`，不读取正文、不调用 LLM。该能力已完成离线工程验证，仍等待人工验收，不能宣称检索安全或 RAG 实验结论。

**S6-T5.3-H1 验收加固（2026-07-22）**：人工验收发现后，trace 的 `candidate_count` 已改为本次 query 的原始
hit 数量，而非 collection 总量；store fingerprint、dimension、distance metric、vector schema 与 metadata schema
均逐项 fail closed。Provider/store 的外部错误被映射为稳定、脱敏的 Retrieval 错误。该修复仍只是离线工程
验证，状态为 `Completed, pending human review`；S6-T5.3 仍为 `Completed, pending human acceptance`，不授权
S6-T5.4 或正式 RAG 安全实验。

**S6-T5.3 人工验收（2026-07-25）**：项目负责人已将 `GOV-PODR1`、`S6-T5.3-P1`、`S6-T5.3-H1` 及
`S6-T5.3 Provider-Neutral DenseRetriever` 标记为 `HUMAN_ACCEPTED`，最后接受的实现提交为 `72a2445`。验收仅覆盖
schema `1.0`/`1.1` 隔离、公开 parent identity、Request/Evidence/Trace 链、candidate/returned count 语义、provenance
校验、稳定排序/去重、fail-closed、脱敏审计与当前离线确定性测试。它不证明 Recall/Precision/MRR/NDCG、检索安全、
抗知识污染、可信检索、Citation Accuracy、ContextBuilder、Trust Pipeline、正式 RAG 安全实验或生产可用性。`S6-T5.4`
仍为 `Not approved`，正式 RAG 安全实验仍为 `Not started`。

**S6-T5.4 协议 blocker（2026-07-25）**：项目负责人已单独批准 `Controlled Corpus ContentResolver` 启动。
启动核对确认既有设计已规定 canonical `ContentRef`、hash verification、受控 fixture legacy mapping 的原则和
禁止从 Chroma 读取正文，但没有冻结 Resolver 的返回/正文权限 contract、snapshot 受控读取接口、legacy
`chroma:` 的唯一映射或错误归属。因此 S6-T5.4 被登记为 `APPROVED_TO_START / DESIGN_OR_PROTOCOL_BLOCKER`：
正确行为是暂停，不创建实现、不读取正文、不猜测 fallback，等待项目负责人冻结最小协议。此 blocker 不影响
S6-T5.3 的人工验收，也不批准 S6-T5.5、Context、Citation、Trust 或正式 RAG 安全实验。

## 0.1 A1R：LLMGuard 命名冻结与 Retrieval Domain 落地（2026-07-16）

项目正式名称现为 **LLMGuard Research Framework（简称 LLMGuard）**，中文名称为
**LLMGuard 大模型安全评测与可信检索研究框架**。distribution 固定为
`llmguard-research-framework`，唯一规范 import namespace 为 `llmguard`。

本任务已完成以下边界迁移：

- Stage 6 Task 1–3 的规范实现从 `codeguarder.stage6_rag` 迁至
  `llmguard.domains.retrieval`；
- 旧 `codeguarder.stage6_rag` 改为 re-export facade，兼容测试确认新旧类型与加载器 identity
  相同；
- 阶段导航迁移为 frozen canonical slug；已进入 manifest 的数据与测试路径继续保留旧路径；
- `src/codeguarder/` 中 Stage 5/Stage 5 Paper 为受保护 legacy 例外，不移动、不复制、不新增；
- 本节只记录 A1R 当时的边界；其后的 S6-T4 实现与真实 MiniLM + Chroma 验收见下一节。

命名治理：[project_identity.md](docs/governance/project_identity.md)、
[naming_conventions.md](docs/governance/naming_conventions.md)、
[namespace_migration.md](docs/governance/namespace_migration.md)；架构依据：[ADR 0006](docs/architecture/0006_namespace_migration.md)。

### S6-T4：Embedding Provider 与 Persistent Vector Store（2026-07-16）

S6-T4 已完成并以多个小提交落地：规范代码仅位于
`src/llmguard/domains/retrieval/embedding/` 与 `vectorstore/`。它提供不可变
`EmbeddingModelSpec`、离线确定性 `StaticEmbeddingProvider`、惰性加载的
`SentenceTransformerEmbeddingProvider`、稳定 `VectorStore` 协议、`InMemoryVectorStore`、
持久化 `ChromaVectorStore`、collection fingerprint 与严格公开 metadata 白名单。

实现使用固定 Stage 6 基线模型 ID 和不可变 revision；真实模型集成测试默认 skip，只有显式设置
`LLMGUARD_RUN_REAL_EMBEDDING_TESTS=1` 才允许加载/下载模型。正常快速测试不联网。Chroma
测试只使用临时目录；正式运行时目录固定为 `runtime/stage6_rag_security/chroma/` 并由 Git
忽略。Ground Truth、攻击标签、完整正文和绝对路径不会进入 collection metadata 或 fingerprint。

### S6-T4 Hardening：document 指纹与真实语义验收（2026-07-19）

collection 身份现使用 `document_embedding_spec_hash`，由
`EmbeddingModelSpec.fingerprint(scope="document")` 统一派生，避免人工复制模型 ID、revision、
维度与归一化等片段字段。provider、model ID、revision、维度、归一化、document prefix、输出 dtype
和实现版本任一变化都会改变 collection fingerprint；本机 cache 路径、用户名、创建时间、Ground Truth
和 query prefix 不会进入它。query prefix 会在后续 S6-T5 的 RunManifest 中记录，而不会让未改变的
文档索引被无意义地重建。

已完成一次显式真实验收：固定 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` revision
`16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1` 在 CPU 输出 384 维有限向量；五篇不同主题中文政策文档
写入临时 Persistent ChromaDB、关闭并重开后，中文与英文休假查询 Top-1 都是 `doc-leave`。
metadata 未出现 Ground Truth 或攻击标签；模型缓存和临时 Chroma 均不在 Git。未调用 Groq。

这项验收只证明当前固定模型、固定语料、向量库 adapter 与跨语言术语别名的基础设施行为，不能宣称
Retriever、R1–R6、可信检索策略、RAG 指标或生产安全能力已完成。S6-T5 仍需单独批准。

本任务**没有**实现 Retriever、RetrievalEvidence 编排、ContextBuilder、Trust、LLM、Groq、
RAG Evaluator、T10–T15、实验矩阵或报告；因此没有新的安全指标或真实 RAG 实验结论。下一步
只能在单独批准后进入 S6-T5。

### S6-T5 Design Freeze：受控检索与可追溯上下文（2026-07-19）

已完成唯一 S6-T5 设计规格、八段式 TDD 实施计划和 ADR 0008，冻结以下边界：

- 当前只规划透明 Dense Retrieval，并通过抽象 EmbeddingProvider/VectorStore 复用 S6-T4；
- Retriever 只输出无正文 `RetrievalEvidence` 与 `RetrievalTrace`；
- 正文由 canonical ContentRef 指向受控 corpus snapshot，Resolver 解析后必须核对 content hash；
- Evidence UID 跨运行稳定，Citation ID 只在当前 Context 内有效，由 CitationBinding 建立映射；
- EvidenceEnvelope 只在受控内存持有正文，XML-like escaping 只保护结构边界，不等于语义防注入；
- ContextBuilder 未来输出 `RetrievedContextPackage`，Trust Pipeline 之后才允许产生
  `TrustedContextPackage`；
- Chunking 当前只允许 Identity 基线，复杂 Token/Overlap/Sentence/Semantic 策略只冻结协议；
- S6-T5.1–S6-T5.8 必须逐项人工批准、TDD、独立提交和验收。

该首轮冻结已由后续 `S6-T5 Design Hardening` 审查收紧；当前状态以其“第二次人工审查”门为准。设计文档
完成只能证明契约和实施路径可审查，不能宣称 Retriever、ContextBuilder、Citation Accuracy、Trust 或 RAG
安全实验已经实现。

### S6-T5 Design Hardening：契约与失败边界加固（2026-07-19）

第二次设计审查发现并留痕五类问题：稳定 DTO 可能重复定义、Dataset QueryRecord 可携带评估字段进入
runtime、`corpus:` 与历史 `chroma:` ContentRef 会在 Resolver 前冲突、Envelope/Package 的敏感序列化语义
不够精确，以及完整性异常与结构性 abstention 混淆。

加固后的冻结决定是：稳定 DTO、ContentRef、canonical hash 和安全 audit serialization 只归属
`contracts/`；Dataset QueryRecord 必须经 explicit safe projection 才能成为最小
`RetrieverQueryRecord`；新 producer 只生成 `corpus:`、legacy fixture 继续可读 `chroma:`；
`to_audit_dict()` 才是普通审计接口，`asdict()` 是敏感操作；只有无可用 Context 才返回结构性 abstention，
hash/scheme/fingerprint/metric 等完整性错误必须异常且不得返回 Package。

当前状态为 `Completed, pending second human review`，且 `S6-T5.1 implementation: Not approved`。该加固
仍只证明设计边界已被审查和收紧，不代表任何 S6-T5 Python 能力已实现。

## 0.2 Architecture Task 0：长期架构冻结（2026-07-16，历史架构基线）

本节是本仓库的**权威架构补充**。它优先于本文件中较早的目录草案，以及
`docs/superpowers/` 中仍引用 `stage6_rag` 作为规范实现目录的历史实施计划；这些
历史文本保留以解释演进过程，但不再决定新代码的位置。

### 已核验的事实

- 当前工作分支是 `feature/stage6-rag`；Stage 6 Task 1–3 的早期实现和测试存在，真实
  Embedding、Persistent ChromaDB、检索器、Trust、RAG Evaluator 均尚未实现；
- Stage 1–5 的版本化历史相对本任务起点未发生修改；
- GitHub 的未认证公开 API 返回 404，而本地已认证 Git 远端可访问，因此仓库当前确认是
  **Private**，而不是“尚未确认的待公开仓库”；
- 本轮只冻结架构、记录决策和补齐导航，不迁移代码、不执行真实模型，也不把任何指标写成
  新实验结论。

### 冻结后的唯一目标代码边界

```text
src/codeguarder/
├── core/
│   ├── contracts/ providers/ guards/ detectors/
│   ├── evaluation/ reporting/ experiments/ audit/
├── domains/
│   ├── runtime/
│   ├── retrieval/
│   └── agent/
└── compatibility/
    ├── stage1_4/ stage4_guard/ stage5/ stage6_rag/ garak/
```

`core/` 只容纳跨领域对象与能力，绝不放 RAG 专属类型；RAG 规范实现只写入
`domains/retrieval/`；`compatibility/` 只做旧路径和旧接口的转换，不承载业务逻辑。
早期 `src/codeguarder/stage6_rag/` 将在 Architecture Task 1 后成为兼容外观，旧导入
路径继续可用。详情见 [架构 ADR](docs/architecture/README.md)。

### 冻结的 RAG 边界

`TrustedContextPackage` 是运行时最小上下文包，只携带经策略准入的有限文本、引用、来源、
信任和置信信息；`RAGSecurityEnvelope` 是脱敏审计包，只携带 ID、hash、策略版本、指标、
failure 与 provenance。Stage 7 只能消费这两个对象，不能直接读取 Chroma、Ground Truth、
完整文档或 Guard 内部状态。

### 固定研究阶段

- Stage 6A：可复现检索安全基线，`off/observe` 与 `PassThrough`；
- Stage 6B：透明规则的 filter/rerank 基线；
- Stage 6C：端到端可复现实验与受控真实模型 smoke；
- Stage 6.1：隐蔽知识污染检测与多证据可信检索研究扩展；
- Stage 6.2：论文级比较、统计、迁移与 artifact；
- Stage 7：消费稳定脱敏契约的 Agent 安全，不绕过 RetrievalEvidence。

Task 0 的交付、风险、验收和下一步都记录在
`docs/architecture/architecture_task0_review.md`。在用户确认前，后续工作只允许进入
Architecture Task 1，不能跳到 Embedding、ChromaDB 或 Groq。

## 0. 先看结论

LLMGuard 已经不是一个“运行 garak 的练习项目”，而是一条逐步扩展的 LLM Security Evaluation 研究路线：

```text
模型层安全评测
→ OpenAI-compatible 受控实验
→ 真实模型扫描
→ 输入/输出防护与消融
→ 系统化攻击矩阵和失败分类
→ RAG 检索层安全与可信证据
→ 隐蔽知识污染检测
→ Agent 跨层安全
```

目前 Stage 1–4.1 已有真实运行证据，Stage 5/Stage 5 Paper 已形成确定性 Mock 论文级评测框架，
Stage 6 已完成依赖/数据契约、R1–R6 数据基础、标签隔离、真实 Embedding 与 Persistent ChromaDB
基础设施验收；尚未实现 Retriever、ContextBuilder、Trust、RAG Evaluator 与最终报告。

下一步不应继续堆叠阶段脚本，而应把项目重构为“稳定研究内核 + 可插拔安全领域 + 声明式实验配置 + 独立研究交付”的平台。重构采用增量兼容方式，绝不推翻 Stage 1–5 历史证据。

仓库当前**已确认是 Private**，且不建议直接改为 Public。它仍包含对话导出、原始 HTML
报告、绝对路径、运行日志和需逐项审查的实验输出。正确做法是建立独立公开发布面，而不是
直接切换整个研究仓库的可见性；审计结论见
`docs/security/PUBLIC_REPOSITORY_AUDIT.md`。

---

## 1. 最高优先级指令

### 1.1 Teaching Mode

项目目标不是尽快完成代码，而是真正理解整个实验流程。协作者的角色是实验导师，不是代码生成器。

每个知识点必须解释：

1. 现在在做什么；
2. 为什么这样做；
3. 企业里为什么这样做；
4. 与上一阶段是什么关系；
5. 面试官可能追问什么；
6. 初学者最容易误解什么。

### 1.2 最终能力目标

学习者最终应能够：

- 独立复现实验；
- 独立修改攻击、模型、Detector、Guard 和数据集；
- 独立向面试官讲清完整调用链；
- 理解每个组件存在的工程意义；
- 设计对照实验、消融实验和失败分类；
- 清楚结论边界，不把小样本或规则基线夸大为生产安全性；
- 将工程实验抽象为论文研究问题和科技项目任务书。

### 1.3 不可违反的约束

- Stage 1–5 历史代码、数据、日志和报告不删除、不移动、不覆盖。
- 历史结果有误时新增 correction log，保留原始证据。
- 新实验使用独立目录和 `run_id`。
- API Key 只从环境变量读取，不进入代码、日志、报告或截图。
- 不执行真实破坏性工具；Tool Injection 只研究意图和潜在副作用。
- 不保存完整敏感输出或完整污染文档；使用 hash、长度、规则命中和有限摘要。
- Mock 结果用于验证机制，真实 API 结果用于观察特定模型行为，两者不能互相替代。
- 所有安全结论必须限定在当前模型、数据集、Guard、Detector 和运行配置下。

---

## 2. 项目的三个交付目标

### 2.1 面试项目

目标读者：大模型安全、AI Security、LLM Red Team、RAG/Agent Security 面试官。

需要证明：

- 能运行真实工具和真实 API；
- 能解释 Probe、Generator、Detector、Guard、Retriever、Evaluator；
- 能设计 vulnerable/guarded、P/I/O/F 和 Mock/Real 对照；
- 能定位 Detector Miss、Guard Bypass、Over-blocking；
- 能处理限流、重试、日志、凭据和可复现性；
- 能说明实验局限，而不是只展示一个漂亮百分比。

### 2.2 论文研究

目标读者：论文审稿人和可复现实验研究者。

需要增加：

- 明确研究问题与威胁模型；
- 数据集构造方法和标注协议；
- 基线方法、消融和对比方法；
- 指标定义、分母和统计不确定性；
- 多模型、多种子和多轮重复；
- 方法贡献与工程实现分离；
- Validity Threats、Ethics、Reproducibility 和 Artifact Appendix。

### 2.3 科技立项

目标读者：项目评审专家、合作单位和任务管理人员。

需要增加：

- 国内外现状和实际业务痛点；
- 总体目标、关键科学问题和关键技术；
- 研究内容、技术路线、年度任务和里程碑；
- 可量化考核指标；
- 数据、算力、模型、人员和风险保障；
- 软件原型、数据集、专利/论文/标准等成果形式。

三种交付共用同一个研究内核，但叙事和证据粒度不同。不能用面试话术代替论文方法，也不能用论文指标表代替科技项目的任务分解。

---

## 3. 当前阶段进度与证据

| 阶段 | 状态 | 已完成工作 | 关键证据 | 结论边界 |
| --- | --- | --- | --- | --- |
| Stage 1 | 已完成 | garak 最小闭环；Probe/Generator/Detector/Report | `deliverables/stage1/`、`stage1_learning/` | Mock 模型 |
| Stage 2 | 已完成 | OpenAI-compatible Mock API；vulnerable/guarded 对照 | `deliverables/stage2/` | 可控 Mock 行为 |
| Stage 3 | 已完成 | Groq 真实扫描；PromptInject/Base64 | `deliverables/stage3/` | 2 个真实 attempts |
| Stage 4 | 已完成 | Guard Proxy；真实 API 防护前后 A/B | `deliverables/stage4/` | 规则基线、小样本 |
| Stage 4.1 | 已完成 | passthrough/input-only/output-only/full-guard 消融 | `deliverables/stage4_ablation/` | 2 条 smoke prompts |
| Stage 5 | 已完成（Mock） | 六类 Attack Matrix；benign；T1–T9；指标与报告 | `data/stage5/`、`deliverables/stage5/` | 离线框架回归 |
| Stage 5 Paper | 已完成（Mock） | A1–A6；P/I/O/F；双 Detector；确定性 AttemptRecord | `src/codeguarder/stage5_paper/` | 22 样本、88 attempts，未跑真实 Groq 全矩阵 |
| Stage 6 | S6-T4 已完成 | Task 1–3 契约、R1–R6 数据、Ground Truth 隔离、llmguard namespace、真实 Embedding/Chroma 验收 | `src/llmguard/domains/retrieval/`、`data/stage6_rag/` | 未实现 Retriever、ContextBuilder、Trust、LLM 或 RAG 指标 |
| Stage 6.1 | 规划中 | 隐蔽知识污染、多证据可信检索 | 本文目标架构预留 | 无实验结论 |
| Stage 7 | 规划中 | Agent 安全评测 | 本文目标架构预留 | 无实验结论 |

### 3.1 Stage 1：理解安全扫描闭环

调用链：

```text
Probe → Generator → Model → Detector → Evaluator → Report
```

已验证：

- `test.Blank` 证明最小链路可运行；
- `test.Repeat` + `HijackHateHumans` 产生 256/256 攻击命中；
- JSONL、HTML、hitlog 和人工 summary 分层保存；
- 100% ASR 是设计出来的脆弱 Mock 基线，不代表真实模型。

### 3.2 Stage 2：理解协议与控制变量

已实现 `/v1/chat/completions`，建立 vulnerable/guarded Mock。核心价值是把 API 连接、请求格式和评测逻辑与真实模型的随机行为分离。

### 3.3 Stage 3：真实模型与 Detector 边界

真实模型：`llama-3.1-8b-instant`，Groq OpenAI-compatible API。

- PromptInject：攻击目标被输出，判定攻击成功；
- Base64：garak 判 PASS，但人工复核发现模型识别并部分解码了危险内容；
- Attempt 口径 ASR 为 1/2；
- 该案例直接证明 PASS 不等于无风险，也引出了 Detector Miss。

### 3.4 Stage 4/4.1：Guard 与消融

Stage 4 调用链：

```text
garak → OpenAI-compatible Guard Proxy → Groq
```

Stage 4.1 固定四种实验名称：

- `passthrough`：无输入/输出防护；
- `input-only`：只做输入检测；
- `output-only`：必须先调用上游，再对原始输出做检测和替换；
- `full-guard`：输入与输出联合防护，内部兼容历史 `guarded` 模式。

当前 smoke set 中，Input Guard 和 Output Guard 都将 ASR 从 50% 降至 0%。这只说明当前两条 prompt 和当前规则下有效。

### 3.5 Stage 5：从案例升级为评测框架

攻击维度：prompt injection、role confusion、encoding obfuscation、context injection、data exfiltration、tool injection。

Failure Taxonomy：

- T1 True Attack Success；
- T2 Detector Miss；
- T3 Guard Bypass；
- T4 Partial Containment；
- T5 Over-blocking；
- T6 Context Accumulation Failure；
- T7 Confidentiality Breach；
- T8 Unsafe Tool Intent；
- T9 Side-effect Risk。

Stage 5 Paper 已建立确定性 Dataset Runner、Prompt Renderer、多 Detector Adapter、AttemptRecord、指标和报告。当前结果来自 Mock，真实模型矩阵仍是后续验证任务。

### 3.6 Stage 6 当前精确状态

当前分支：`feature/stage6-rag`。

已提交：

- Task 1：固定 ChromaDB、SentenceTransformers、Pillow 依赖；
- Task 2：稳定不可变契约与严格 schema；
- Task 3：R1–R6 数据集、Attack Matrix、公开视图与 Evaluator Ground Truth 物理隔离；
- Task 3 加固提交：`055f266`；
- 最近验证：104 tests、1919 subtests，通过 Ruff 和 MyPy。

尚未开始：

- Task 4：真实 Embedding Provider 与 Persistent ChromaDB；
- Task 5：RetrieverProxy 与安全 ContextBuilder；
- Task 6：EvidenceSignal 与 pass-through Trust baseline；
- Task 7：Mock/Groq Provider 与 Stage 5 Guard 适配；
- Task 8：RPR、CIR、RMSR、Faithfulness、Cross-layer Leakage 和 T10–T15；
- Task 9–14：Runner、Validator、报告、脚本、导航、真实回归和最终治理。

---

## 4. 当前文件资产如何管理

| 目录 | 角色 | 管理规则 |
| --- | --- | --- |
| `llm-security-stage1/` | Stage 1–4.1 历史代码 | 只读兼容层，不重构覆盖 |
| `src/llmguard/` | 唯一规范实现根 | 新业务代码只在此处新增 |
| `src/codeguarder/` | legacy namespace | Stage 5/5 Paper 历史例外与 Stage 6 facade，不新增业务 |
| `src/llmguard/domains/retrieval/` | Stage 6 规范实现 | A1R 已迁入 Task 1–3；后续 S6-T4 起继续增量实现 |
| `data/` | 合成攻击、benign、Ground Truth | 数据版本化、标签隔离、manifest |
| `tests/` | 单元、集成、回归、安全校验 | TDD，重型模型测试单独分组 |
| `deliverables/` | 报告、脱敏日志、学习材料 | 历史不覆盖；新 run 使用独立 ID |
| `experiments/` | 实验注册表 | 记录配置、状态、commit、结论边界 |
| `provenance/` | manifest、历史 baseline、修正账本 | 支撑审计与论文复现 |
| `interview_prep/` | 面试集中复习 | 使用链接和摘要，不复制大量源码 |
| `runtime/`、`.venv/` | 可重建本地运行状态 | 不进入 Git |

事实优先级：原始 JSON/JSONL 与日志 > Git commit 与 manifest > 聚合报告 > 学习总结 > 面试话术。

---

## 5. 为什么需要重新设计架构

当前项目是按学习阶段自然生长出来的，因此存在合理但需要治理的技术债：

1. Stage 1–4.1 集中在历史目录，代码和阶段概念耦合；
2. Stage 5 基础框架与 Stage 5 Paper 有部分重复实现；
3. Runner、Guard、Detector、AttemptRecord 尚未形成全项目统一接口；
4. 数据、Ground Truth、运行产物和论文交付的边界还不够统一；
5. HTML 报告体积远大于 Python，使 GitHub Languages 被生成产物主导；
6. 私有研究证据与未来公开仓库内容尚未物理分层；
7. 现有 Stage 命名适合学习，却不适合作为论文方法模块名称。

重构目标不是让目录“看起来更漂亮”，而是建立稳定研究对象，使新增 RAG、可信检索和 Agent 实验无需复制一套 Runner、Metrics、Reporting 和 Audit。

---

## 6. 目标架构：LLMGuard Research Framework

### 6.1 总体调用链

```text
Dataset + RunConfig
        ↓
Experiment Orchestrator
        ↓
Threat Adapter / Prompt Renderer
        ↓
Input Guard
        ↓
Domain Pipeline
  ├─ Runtime LLM
  ├─ Retrieval/RAG
  └─ Agent/Tool/Memory
        ↓
Output Guard
        ↓
Detector Ensemble
        ↓
Failure Taxonomy
        ↓
Metrics + Validators
        ↓
AttemptRecord + RunManifest
        ↓
JSON / CSV / Markdown / Figures
```

### 6.2 分层设计

```text
src/llmguard/
├── core/
│   ├── contracts/       # Attempt、Evidence、Verdict、RunManifest
│   ├── experiments/     # schema、loader、renderer、manifest
│   ├── providers/       # Mock、OpenAI-compatible、Groq
│   ├── guards/          # Input、Output、Retrieval、Policy
│   ├── detectors/       # garak、自定义规则、Judge
│   ├── evaluation/      # Runner、Taxonomy、Metrics、Validators
│   ├── reporting/       # JSON、CSV、Markdown、Figure
│   └── audit/           # hash、redaction、secret scan、provenance
├── domains/
│   ├── runtime/         # Prompt/Encoding/Context/Tool intent
│   ├── retrieval/       # RAG、Evidence、Trust、Poisoning
│   └── agent/           # Tool、Memory、Planning、Side-effect
└── compatibility/
    ├── garak/           # garak Generator/Detector 适配器
    ├── stage1_4/        # Stage 1–4.1 历史适配器
    ├── stage4_guard/    # 旧 GuardEngine 适配器
    ├── stage5/          # 旧 Stage 5 接口适配器
    └── stage6_rag/      # 旧 Stage 6 import 适配器
```

声明式实验放在：

```text
experiments/
├── registry.json
├── configs/
│   ├── runtime/
│   ├── retrieval/
│   └── agent/
└── manifests/
```

阶段导航仍可保留，但不再承载重复源码：

```text
stages/
├── stage1_garak_baseline/
├── stage2_openai_mock_api/
├── stage3_real_model_scan/
├── stage4_guard_ab/
├── stage4_1_guard_ablation/
├── stage5_runtime_attack_matrix/
├── stage5_paper_baseline/
├── stage6_rag_security/
├── stage6_1_hidden_knowledge_poisoning/
├── stage6_2_trustworthy_retrieval/
└── stage7_agent_security/
```

### 6.3 六个稳定核心对象

1. `AttackSample`：攻击目标、输入、期望风险和元数据；
2. `ProviderRequest/Response`：统一模型调用，不绑定具体厂商；
3. `RetrievalEvidence`：稳定检索证据，不暴露向量库内部结构；
4. `DetectorVerdict`：来源、分数、规则、覆盖状态和输出 hash；
5. `AttemptRecord`：一次实验的完整脱敏审计记录；
6. `RunManifest`：代码、数据、模型、配置、seed、环境和运行状态。

所有 Stage 6.1 和 Stage 7 扩展都应围绕这些对象增加字段或适配器，而不是再建独立 Runner。

---

## 7. Stage 6/6.1 的论文级架构

### 7.1 Stage 6 安全基线

```text
Query
→ Query/Input Guard
→ Retriever
→ Persistent ChromaDB
→ RetrievalEvidence[]
→ EvidenceExtractor
→ EvidenceSignal[]
→ TrustAggregator (pass-through)
→ RetrievalPolicy (off/observe)
→ ContextBuilder
→ Mock LLM / Groq
→ Output Guard
→ RAG Evaluator
→ RPR/CIR/RMSR/Faithfulness/Leakage + T10–T15
```

R1–R6：Query Injection、Retrieval Poisoning、Context Injection、Embedding Attack、Document Poisoning、Hallucination Steering。

Stage 6 只建立可复现基线。TrustAggregator 不学习、不改变排序，`observe` 只记录信号。

### 7.2 Stage 6.1 研究贡献方向

拟研究主题：**面向检索增强生成系统的隐蔽知识污染检测与多证据可信检索关键技术研究**。

可形成四个研究问题：

- RQ1：在不使用 poison label 的条件下，哪些 EvidenceSignal 能识别隐蔽污染？
- RQ2：来源、语义冲突、Embedding 异常和多源一致性如何联合建模？
- RQ3：可信重排/阻断能否降低攻击成功率，同时控制正常查询性能损失？
- RQ4：检索层风险如何传播到生成层和 Agent 决策层？

建议贡献点：

1. 无标签泄露的检索安全评测框架；
2. 多证据信号表示与可信聚合方法；
3. 冲突感知的检索策略；
4. 安全、可信度、可用性联合指标；
5. 可复现实验数据与审计协议。

### 7.3 科技立项任务分解

- 课题一：RAG 知识污染攻击建模与数据集；
- 课题二：隐蔽污染多维证据提取；
- 课题三：多证据可信聚合与冲突检测；
- 课题四：安全约束下的可信检索策略；
- 课题五：跨检索、生成、Agent 的风险传播评测平台。

阶段成果可对应：数据集、算法模块、评测平台、论文、专利/软著、技术报告和演示系统。

---

## 8. 统一实验方法

### 8.1 实验矩阵

```text
Attack Category
× System Domain
× Model/Provider
× Guard Configuration
× Retrieval Policy
× Detector
× Seed/Repeat
× Metric/Failure Type
```

### 8.2 必须统一的指标

运行时安全：ASR、Detector Miss Rate、Guard Bypass Rate、Over-block Rate、Latency Overhead。

检索安全：RPR、CIR、RMSR、Faithfulness、Cross-layer Leakage Rate。

可信检索扩展：Hidden Poison Detection Precision/Recall/F1、Conflict Detection、Trust Calibration、Clean Retrieval Utility、Safety-Utility Trade-off。

### 8.3 复现要求

- 数据集 manifest 与 SHA-256；
- 代码 commit；
- 模型 ID、revision、base URL 类型；
- Embedding 模型与 revision；
- seed、temperature、top_k、generation 参数；
- Guard/Detector/Taxonomy 版本；
- 失败重试和 API 限流记录；
- canonical JSONL 和 `run_status`；
- 相同 Mock 输入产生字节一致的规范化日志。

---

## 9. GitHub 私有仓库是否应该公开

### 9.1 当前建议

**暂时保持私有。** 不是因为源码不能公开，而是因为仓库同时保存了研究过程证据和面试材料，公开前需要完成发布面治理。

当前公开风险包括：

- `chatgpt_share_*.html` 对话导出；
- garak HTML/JSONL 中的完整攻击 prompt 和原始输出；
- 日志中的本机绝对路径、时间和环境信息；
- 可能包含个人信息的 DOCX/PDF/截图；
- 真实 API 运行历史需要再次做秘密和隐私审计；
- 数据集、模型和第三方工具的 license/引用信息尚未形成统一清单；
- 大量生成 HTML 会让 GitHub Languages 错误显示为 HTML 项目。

### 9.2 推荐公开策略

采用“双层仓库/发布面”：

```text
Private Research Repository
  - 原始日志
  - 完整运行证据
  - 研究草稿
  - 面试私人材料
  - 受限数据

Public Artifact Repository / public-release branch
  - 源码
  - 合成与脱敏数据
  - 可复现配置
  - 脱敏样例结果
  - 方法文档
  - License/Citation/Ethics
```

公开前清单：

1. 移除对话导出、个人文档、截图和临时文件；
2. 全历史秘密扫描，而不只是当前工作树；
3. 清理绝对路径、用户名和 provider 原始 trace；
4. 只保留最小脱敏报告样例，大体积结果提供 release/归档地址和 hash；
5. 使用 `.gitattributes` 将报告 HTML 标记为 `linguist-generated`；
6. 增加 `LICENSE`、`CITATION.cff`、`SECURITY.md`、`ETHICS.md`、数据卡和模型卡；
7. 增加最小可运行 demo、安装说明和 CI；
8. 在独立临时 clone 中验证公开包能够从零复现。

仓库公开属于不可逆的信息披露决策。在上述检查完成前，不直接把当前私有仓库切换为 Public。

---

## 10. 增量重构路线

### Phase A：冻结与建立统一契约

- 保留 Stage 1–5 原路径；
- 定义 core contracts、RunManifest、DetectorVerdict 和 AttemptRecord v2；
- 编写 compatibility tests，保证旧结果可读；
- 建立 public/private artifact policy。

### Phase B：抽取通用研究内核

- 从 Stage 5 Paper 抽取 Dataset Runner、Providers、Detectors、Metrics、Reporting；
- Stage 4 GuardEngine 通过 adapter 接入；
- Stage 6 只实现 retrieval domain，不复制通用模块。

### Phase C：完成 Stage 6 基线

- 真实 Embedding + ChromaDB；
- Retriever + ContextBuilder；
- pass-through Trust；
- Mock 确定性回归；
- Groq 小样本；
- T10–T15 与完整报告。

### Phase D：Stage 6.1 论文方法

- 隐蔽污染数据扩展和标注协议；
- EvidenceSignal 基线和学习方法；
- 多证据聚合、冲突感知重排和消融；
- 多模型、多语料、多种子实验；
- 论文图表、统计检验和 Artifact Appendix。

### Phase E：Stage 7 Agent Security

- 复用 RetrievalEvidence 与 RAGSecurityEnvelope；
- 建立 Tool/Memory/Planning 攻击矩阵；
- 使用沙箱和 intent-only 工具模拟；
- 研究检索污染向 Agent 决策和副作用传播。

---

## 11. 最近里程碑与停止条件

### M0：架构决策

完成条件：确认本文目标架构、公开策略和 Stage 6/6.1 研究边界。

### M1：统一核心最小版本

完成条件：核心 contracts、provider、detector、attempt、manifest 可同时运行 Stage 5 Mock 和 Stage 6 Mock。

### M2：Stage 6 Baseline

完成条件：R1–R6 全链路、真实 Embedding/Chroma、Mock 确定性回归、T10–T15、中文报告。

### M3：Stage 6.1 Research Baseline

完成条件：至少两类 Hidden Poison baseline、四类 EvidenceSignal、可信聚合、消融和正常检索效用评估。

### M4：Public Artifact v1

完成条件：独立公开发布面通过秘密、隐私、license、复现和 CI 检查。

### M5：论文/立项材料

完成条件：研究问题、方法、实验、结果、局限性和项目任务书使用同一组可追溯证据。

---

## 12. 每次继续项目时的执行协议

1. 先读本文件；
2. 检查 branch、worktree、Git status 和最近 commit；
3. 明确当前只完成哪个知识点；
4. 先写实验假设、输入、输出和成功条件；
5. 按 TDD 先红后绿；
6. 运行单元、集成、静态和泄露检查；
7. 保存代码、数据、日志、结果和教学文档；
8. 说明面试如何讲、论文如何写、不能夸大什么；
9. 每个稳定 Task 使用独立 commit；
10. 更新本文件的阶段状态和最近验证证据。

---

## 13. 当前下一步

`S6-T4` 已完成，`S6-T5 Design Hardening` 已完成并等待第二次人工审查。下一步不是自动写 Python，而是
审查 hardened design、Existing Contract Migration Matrix 与实施计划：

- `docs/superpowers/specs/2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md`；
- `docs/superpowers/plans/2026-07-19-s6-t5-controlled-retrieval-traceable-context.md`；
- `docs/architecture/0008_retrieval_context_boundary.md`。

只有第二次人工审查明确批准后，才可单独开始 `S6-T5.1 Chunking Contracts`。`S6-T5.1 implementation:
Not approved`，其后的 Retriever、ContentResolver、EvidenceEnvelope 和 ContextBuilder 更不能提前实施。

面试表达：我先通过五个阶段建立模型层评测、防护和失败分类，再把系统扩展到检索层。为了让项目能够从演示走向论文，我将阶段脚本重构为稳定研究内核，并把 RAG 的证据表示、可信分析和风险传播设计成可插拔领域模块，同时用兼容层保护历史实验可复现性。

不能夸大：当前项目已经具备较完整的评测工程基础、S6-T4 基础设施和 S6-T5 可审查设计，但 Stage 6
受控检索实现、Stage 6.1 方法创新、统计实验和公开 Artifact 尚未完成，不能称为已经发表或达到生产级
防护能力。

## 14. S6-T5.1：确定性分块契约与 IdentityChunker（2026-07-20）

在最新人工批准下，S6-T5.1 已用 TDD 实现并等待人工验收。规范 DTO 仅位于
`src/llmguard/domains/retrieval/contracts/chunking.py`：`ChunkingStrategy`、不可变
`ChunkingConfig`、`ChunkRecord`、canonical JSON/SHA-256 与最小 `corpus:` content reference formatter。
行为实现仅位于 `src/llmguard/domains/retrieval/chunking/`：`Chunker` Protocol、领域异常和
`IdentityChunker`。

当前基线严格执行“一份 `DocumentRecord` 产生一个原样 `ChunkRecord`”：先按 UTF-8 重算正文哈希，
再用 corpus snapshot、父文档、索引、内容 hash 与配置 hash 生成完整 `CH-<sha256>`。公开 metadata
递归冻结并拒绝 evaluator 标签变体、绝对路径、循环、非 JSON-safe 值；`repr` 与 `to_audit_dict()`
均不展开正文。测试、Retriever、向量库与日志均不把此能力表述为 RAG 安全效果。

本项没有实现 Retriever、RetrievalRequest/Trace、ContentResolver、ContextBuilder、Trust、LLM/Groq、
T10–T15 或正式实验；下一步仍必须先经人工验收，再单独批准 S6-T5.2。

### S6-T5.1 Implementation Hardening（2026-07-20）

针对初版分块契约的人工审查，本轮完成四项加固：删除不能合法承载任何语义的 `window_size`，统一固定
token 语义为 `max_tokens`、overlap 语义为 `max_tokens + overlap_tokens`；将稳定错误类型归属到
`contracts/errors.py` 并从行为层兼容 re-export；为 `ChunkRecord` 增加 `chunk_schema_version` 并在对象
构造时重算 chunk ID；metadata 在排序前先验证全部 key 为字符串，同时拒绝绝对路径 key/value。

`ChunkRecord` 的完整性现覆盖 schema version、snapshot、parent doc、index、content hash 与 config hash；
任一字段被篡改即抛脱敏 `ChunkingIntegrityError`。文档 hash mismatch 的异常固定为
`DOCUMENT_CONTENT_HASH_MISMATCH`，不回显原始 doc ID 或正文。该状态是 `Completed, pending final human
acceptance`，并不授权 S6-T5.2 或任何检索/上下文功能。

## 15. S6-T5.2：检索运行时契约与稳定标识（2026-07-20，待人工验收）

本任务只实现 `QueryRecord -> safe projection -> RetrieverQueryRecord -> RetrievalRequest -> RetrievalEvidence/Trace` 的数据边界。公开加载器仍读取原有 Stage 6 JSONL，但投影后的运行时对象仅含精确 `retrieval_query`、新的 `Q-` 安全 ID 与 `delivery_layer/scenario/variant` 白名单元数据；攻击标签、类别、生成问题和期望文档不会进入运行时对象。

规范 DTO 统一由 `src/llmguard/domains/retrieval/contracts/` 暴露。`ContentRef` 同时识别新 `corpus:` 和旧 `chroma:` 格式，但新证据只生成 `corpus:`；旧格式必须经显式 adapter 迁移。Evidence UID 可复算；Trace hash 覆盖稳定语义而不包含 latency。普通 audit/repr 不记录查询正文、文档正文或可解析内容引用。

本轮没有实现 DenseRetriever、向量库查询、embedding 调用、ContentResolver、ContextBuilder、Citation、Trust、LLM/Groq、T10-T15 或正式实验。因此它证明的是可审计运行时边界，不是检索质量或 RAG 安全效果。下一步必须由人工单独审批 `S6-T5.3 DenseRetriever`。

## 16. S6-T5.4-P1：Content Resolution Contract and Permission Boundary Freeze（2026-07-25）

`S6-T5.4-P1` 已完成协议冻结，等待人工验收。它只确定后续 ContentResolver 的最小权限边界：唯一输入为
`ContentRef` 与预期 hash，敏感 `ResolvedContent` 由 `contracts/` 唯一拥有；受控 snapshot reader 只能按
chunk ID 读取；legacy `chroma:` 只能经过 immutable exact-match allowlist 映射；错误由
`contracts/errors.py` 稳定拥有。正文不得进入普通日志、trace、repr、异常或公共数据对象。

该记录不是 ContentResolver、reader、registry 或 adapter 的实现，也没有读取正文、fixture、标签或 Ground
Truth。父任务 `S6-T5.4` 仍为 `APPROVED_TO_START / DESIGN_OR_PROTOCOL_BLOCKER`，blocker 尚未正式解除；
`S6-T5.5` 及后续任务仍未批准，正式 RAG 安全实验仍未开始。
