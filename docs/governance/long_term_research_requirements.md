# LLMGuard 长期研究需求基线

## 状态与优先级

**状态：已接受，2026-07-19。** 本文来自项目负责人的长期需求确认，是后续 Stage 6、Stage 6.1、
Stage 6.2 与 Stage 7 的治理基线。若它与较早的实施草案发生冲突，以本文、
`PROJECT_MASTER_CONTEXT.md` 和已接受 ADR 的较新约束为准；历史实验记录不因此重写。

本文不授权提前实现 S6-T5 或更晚阶段的代码。它规定未来实现的方向、稳定对象和验收边界。

## Paper-First Comparative Evidence Principle

**状态：已接受，2026-07-31。** 所有以 Paper 1 / Paper 2 论文结论为目标的任务必须先核验权威论文、
官方源码、许可、公开数据、模型、attack budget、Retriever、Top-K、指标与原始环境，再冻结内部实验协议。
`Published Result`、`Reproduced Result`、`Our Method Result` 必须严格分开；自建 Benchmark 必须通过 external
benchmark 验证泛化；复现失败必须登记 blocker，不得用不同设置的数字宣称超过 SOTA。

完整规则见 [论文优先的外部对标与比较证据原则](../research/paper_comparative_evidence_principle.md)。
该原则不覆盖安全、伦理、许可、标签隔离、历史不可变和审批门；文献对齐也不自动批准正式实验。

## Git-Native Research Context Recovery

**状态：已接受，2026-07-31。** 项目长期事实不得仅依赖聊天、Codex Thread、单机 memory、模型上下文或人工
记忆。所有正式任务必须能从 Git、raw evidence、Owner Decision、Project Master Context、Current Work State、
Experiment Master Record、Research Execution Log 和 accepted route/protocol 恢复。权威层级与冲突规则见
[Context Authority Map](context_authority_map.md)。无法安全解决的冲突必须登记 `CONTEXT_CONFLICT_BLOCKER` 并停止。

每个稳定 Stage 最终应有结构化 Learning Guide，但其性质固定为
`NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL` / `EDUCATIONAL / KNOWLEDGE_TRANSFER ARTIFACT`。Learning Guide 不是
Formal Experiment Acceptance 的前置科学证据，不得覆盖 Git、Owner Decision、Experiment Record 或 accepted
protocol。

## 1. 项目身份与目标顺序

- 英文正式名称：**LLMGuard Research Framework**；
- 中文正式名称：**LLMGuard 大模型安全评测与可信检索研究框架**；
- 规范 Python namespace：`llmguard`；旧 `codeguarder` 仅作兼容 facade；
- 项目是同时服务于面试、论文、科技立项和 Agent 安全研究的长期框架，不是单次工具演示。

目标优先级固定为：

1. RAG 安全研究；
2. 大模型安全评测平台；
3. AI 安全护栏工程；
4. Agent 安全扩展。

面试叙事必须呈现从模型输入输出安全，到知识库、检索、上下文构建、证据可信性，再到 Agent
决策安全的连续链路。

## 2. 用途与证据标准

### 面试

每项实验必须可复跑、可审计并能说明攻击变量、对照变量、层间传播、指标分母、标签隔离、
Mock/Real 边界、误杀、配置/日志/报告追溯及结论限制。

### 论文与立项

立项主题为《面向检索增强生成系统的隐蔽知识污染检测与多证据可信检索关键技术研究》。长期主线为：
隐蔽污染威胁建模、污染数据集、多视角检测、可信评分、冲突感知过滤与重排、可信证据选择、
鲁棒聚合、引用核验、低置信度拒答和多维原型评测。

论文工件从一开始采用英文术语、稳定字段、Method/Evaluation/Artifact 组织，投稿路线面向英文高水平
会议或 CCF 推荐会议；中文教学材料服务于学习和面试，但不能替代论文方法或统计证据。

## 3. 阶段路线与不可变资产

```text
Stage 1     Garak Security Scan Baseline
Stage 2     OpenAI-Compatible Mock API
Stage 3     Real Model Security Scan
Stage 4     Guard Proxy A/B Evaluation
Stage 4.1   Guard Ablation Evaluation
Stage 5     Runtime Attack Matrix and Failure Taxonomy
Stage 5 Paper  Deterministic Runtime Evaluation Baseline
Stage 6     RAG Security Evaluation
Stage 6.1   Hidden Knowledge Poisoning Detection
Stage 6.2   Multi-Evidence Trustworthy Retrieval
Stage 7     Agent Security Evaluation
```

Stage 1–5 的代码、数据、报告、日志、hash 和历史结论是不可变实验资产。发现历史错误时，只能增加
correction log 或新实验，不能覆盖原始证据。每个稳定任务使用独立提交、运行清单和 `run_id`。

## 4. 语料与数据治理

Stage 6 面试/工程基线优先使用合成、可控、无隐私的企业制度语料：人事休假、财务差旅、信息安全与
账户、项目采购研发科研管理。Schema 和代码必须支持 `enterprise`、`education`、`research` 等
`corpus_domain`，不得把企业领域写死。

Stage 6.1 论文数据扩展教育和科研制度语料，并采用规则生成、模型辅助生成、人工复核和公开许可文档；
真实企业内部文件不得直接作为公开论文数据。Ground Truth 只能由 Evaluator/ GroundTruthVault 读取，
不得进入 Retriever、VectorStore、ContextBuilder、Guard、LLM、日志、collection fingerprint 或
公开 metadata。

## 5. Stage 6 检索基线边界

S6-T5 的首个端到端检索基线固定为透明 Dense Retrieval：

```text
Query -> SentenceTransformers Embedding -> ChromaDB Top-K
      -> RetrievalEvidence -> ContextBuilder
```

S6-T5 不实现 BM25、Hybrid Retrieval、Query Rewrite、Cross-Encoder Reranker 或 Trust Reranker。
这些是后续 S6-T10 或论文比较实验的重要对照基线，不得提前混入基线而破坏变量控制。

当前短文档允许“一篇文档一个 chunk”，但必须为后续真实实现预留 `ChunkingConfig`、`Chunker`、
`ChunkRecord` 和 `IdentityChunker`。稳定字段至少包含 `doc_id`、`chunk_id`、`parent_doc_id`、
`chunk_index`、`chunking_strategy`、`chunking_config_hash`、`content_hash`、`content_ref`。未来要真实
比较 fixed token window、overlap、sentence 与 semantic chunking，不能以只有 `pass` 的占位类冒充能力。

## 6. 证据、引用与上下文契约

证据采用双层标识：

- **Evidence UID**：跨运行稳定，由 schema version、corpus snapshot ID、chunk ID 和 content hash
  的 canonical serialization + SHA-256 生成；
- **Citation ID**：当前 context 内局部标识，如 `[E1]`，必须可映射到 Evidence UID、chunk/parent
  document、content hash、corpus snapshot、source/version、rank、similarity/distance。

后续须基于该映射评估 Citation Accuracy、引用支持度和幻觉溯源，并区分无证据幻觉、错误引用、污染
引用以及引用正确但推理错误。

内部使用结构化 `EvidenceEnvelope`。给 LLM 的 Context 使用已转义的 XML-like evidence block，不使用
无边界纯文本或完整 JSON；必须转义 `<`、`>`、`&`、引号和伪造 `</EVIDENCE>`。该转义只防结构边界
突破，**不得**夸大为已消除语义层间接 Prompt Injection。

ContextBuilder 将支持 `off`、`available`、`required` 三种 citation mode。S6-T5 即使不调用 LLM，也要
能生成三种模式的结构化上下文和 prompt instruction；后续真实生成默认评估 `required`。

S6-T5 的产物命名为 `RetrievedContextPackage`，表示“已检索但未可信分析”。只有经过
`EvidenceSignal -> TrustAggregator -> RetrievalPolicy` 后，才可生成 `TrustedContextPackage`。Stage 7
只能消费 `TrustedContextPackage` 与脱敏 `RAGSecurityEnvelope`，不能直接读取 Chroma、Ground Truth 或
完整知识库。

## 7. 污染传播与拒答设计

当 Retrieval Policy 为 `off`，受控实验允许污染证据进入 Context，以观察“污染入库 -> 召回 ->
Context -> 输出”的传播链。审计日志只记录 ID、hash、长度、rank、similarity/distance、来源、版本和
context hash，不记录完整危险正文。

现在起所有相关稳定对象预留 `abstention_required` 与 `abstention_reason_codes`。Stage 6 基线默认不
自动拒答；Stage 6.2 必须真实实现无有效证据、严重冲突、低来源可信度、污染风险、引用不支持、低置信度
和单一可疑来源等拒答策略，不能长期停留在字段占位。

## 8. 后续阶段最低能力

### Stage 6.1

双领域语料、隐蔽污染/stealth level、多类来源/时间/实体/语义/Embedding/检索信号、至少两类检测
baseline、至少四类 EvidenceSignal、F1/AUROC/AUPRC、多模型多种子、跨领域迁移、消融和可解释输出。

### Stage 6.2

Dense、BM25、Hybrid、普通 reranker 对照；relevance 与 trust 联合建模；冲突检测、风险过滤重排、
可信证据选择、鲁棒聚合、Citation Accuracy、Evidence Consistency、Evidence Trustworthiness、
Faithfulness、Answer Correctness、低置信度拒答以及 Safety-Utility-Efficiency 权衡。

### Stage 7

评估 Tool Injection、Memory Poisoning、Planning Manipulation、Unsafe Tool Intent 以及检索污染向 Agent
决策/副作用传播；仅使用沙箱或 intent-only 工具模拟。

## 9. 实验与公开治理

- Static/Mock 用于确定性回归；真实 Embedding、ChromaDB 与小规模真实模型用于受控链路验证；
- 不用 Static Embedding 宣称真实语义效果，不用单次真实模型输出宣称统计结论；
- 每次运行保存配置、模型 revision、数据 hash、Git commit 与 RunManifest；
- 不保存 API Key、完整敏感输出或完整污染文档；
- 私有研究仓库与未来公开脱敏 Artifact 分离，公开前进行历史 secret/privacy/license 审核；
- 所有结论都限定于当前数据、模型、配置、检测器与防护策略，不夸大为生产安全率。

## 10. 本文对当前状态的影响

本文不修改已完成的 S6-T4 Embedding/VectorStore 基础设施，也不授权 S6-T5。下一次获批的 S6-T5 必须
首先将本文件第 5–7 节转化为测试先行的领域契约与最小 Dense Retrieval 实现。
