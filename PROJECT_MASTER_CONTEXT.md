# CodeGuarder 项目总控文档

> 这是项目唯一的总览与决策入口。它回答：为什么做、已经做了什么、证据在哪里、当前代码处于什么状态、未来架构如何同时支撑面试、论文和科技立项。

更新时间：2026-07-16

当前研究分支：`feature/stage6-rag`

文档状态：架构重设计基线 v1；Architecture Task 0 已冻结长期边界

## 0.1 Architecture Task 0：长期架构冻结（2026-07-16）

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

CodeGuarder 已经不是一个“运行 garak 的练习项目”，而是一条逐步扩展的 LLM Security Evaluation 研究路线：

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

目前 Stage 1–4.1 已有真实运行证据，Stage 5/Stage 5 Paper 已形成确定性 Mock 论文级评测框架，Stage 6 已完成依赖契约、核心数据契约、R1–R6 数据基础和标签隔离，尚未实现真实 Embedding、ChromaDB 检索、Trust、RAG Evaluator 与最终报告。

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
| Stage 6 | 架构冻结后待迁移 | Task 1–3 早期依赖、契约、R1–R6 数据、Ground Truth 隔离 | `feature/stage6-rag`、`docs/architecture/` | Task 0 已完成；Architecture Task 1 后才开始真实检索基线 |
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
| `src/codeguarder/` | Stage 5 基础框架 | 保留，逐步抽取稳定内核 |
| `src/codeguarder/stage5_paper/` | Stage 5 论文框架 | 作为新内核的重要来源 |
| `src/codeguarder/stage6_rag/` | Stage 6 早期实现 | 未来仅作兼容外观；新业务实现迁入 `domains/retrieval/` |
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

## 6. 目标架构：CodeGuarder Research Platform

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
src/codeguarder/
├── core/
│   ├── contracts/       # Attempt、Evidence、Verdict、RunManifest
│   ├── datasets/        # schema、loader、renderer、manifest
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
    ├── stage4_guard/    # 旧 GuardEngine 适配器
    ├── stage5/          # 旧 Stage 5 接口适配器
    └── garak/           # garak Generator/Detector 适配器
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
├── stage1_garak/
├── stage2_mock_api/
├── stage3_groq/
├── stage4_guard_ab/
├── stage4_1_ablation/
├── stage5_attack_matrix/
├── stage6_rag/
└── stage7_agent/
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

当前不应直接继续写 ChromaDB 代码。先完成架构决策评审：

1. 是否接受“稳定 core + domains + compatibility + 声明式 experiments”的目标架构；
2. 是否接受私有研究仓库与公开发布面分离；
3. Stage 6 是否作为 Baseline，Stage 6.1 是否作为论文/立项核心创新；
4. 确认后再为重构建立独立 design spec 和实施计划；
5. 重构只增量迁移，不修改 Stage 1–5 历史文件。

面试表达：我先通过五个阶段建立模型层评测、防护和失败分类，再把系统扩展到检索层。为了让项目能够从演示走向论文，我将阶段脚本重构为稳定研究内核，并把 RAG 的证据表示、可信分析和风险传播设计成可插拔领域模块，同时用兼容层保护历史实验可复现性。

不能夸大：当前项目已经具备较完整的评测工程基础，但 Stage 6 检索基线、Stage 6.1 方法创新、统计实验和公开 Artifact 尚未完成，不能称为已经发表或达到生产级防护能力。
