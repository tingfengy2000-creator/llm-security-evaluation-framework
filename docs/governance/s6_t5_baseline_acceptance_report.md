# S6-T5 Controlled Retrieval and Traceable Context Baseline Acceptance Report

## 1. 基线身份

| 字段 | 当前事实 |
| --- | --- |
| Stage | `S6-T5` |
| Scope | `Controlled Retrieval and Traceable Context Baseline` |
| Status | `Completed, pending human acceptance` |
| Active branch | `feature/stage6-rag` |
| Last accepted implementation commit | `b136ee2` |
| Last accepted integration evidence commit | `b6cedf3` |
| T5.7 governance acceptance commit | `c1e8c16` |
| T5.8 candidate baseline closure commit | `PENDING_GIT_COMMIT`；本报告不能在同一 Git commit 内写入自身 SHA，完成提交后以 Git `HEAD` 事实回填至后续人工验收记录 |
| T5.8 start approval | `PODR-032`；历史状态 `APPROVED_TO_START / DOCUMENTATION_IN_PROGRESS` |
| Formal RAG security experiment | `NOT STARTED` |

本报告是 S6-T5.1 至 S6-T5.7 已接受工程边界的统一证据索引，也是 S6-T5.8 的候选 baseline closure 文档。它不是
正式安全实验报告、研究论文结论或生产验收。项目负责人完成对本轮提交的最终人工验收前，不得将任何 SHA 称为
`accepted S6-T5 baseline SHA`，不得创建 tag 或 Stage 6.1 分支。

## 2. S6-T5.1 至 S6-T5.7 状态矩阵

| Task | 当前状态 | Protocol / closure commit | Implementation commit | Hardening / final accepted commit | Governance acceptance commit | 核心能力 | 证据 | 不可宣称事项 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S6-T5.1 Chunking | `HUMAN_ACCEPTED` | `NOT_SEPARATELY_RECORDED` | `412d886` | `09584c8` | `NOT_SEPARATELY_RECORDED`；状态由 [Experiment Master Record](experiment_master_record.md) 固化 | IdentityChunker、稳定 Chunk ID、hash/metadata 边界 | [Stage 6 README](../../stages/stage6_rag_security/README.md) | 不代表复杂 Chunking、检索质量或安全效果 |
| S6-T5.2 Runtime Contracts | `HUMAN_ACCEPTED` | `4c12181` | `4c12181` | `NOT_SEPARATELY_RECORDED` | `03750d9` | safe projection、Request、Evidence、Trace、ContentRef | [completion record](s6_t5_2_completion_record.md) | 不代表 Retriever、正文读取或 RAG 安全 |
| S6-T5.3 DenseRetriever | `HUMAN_ACCEPTED` | `2ad3d9c` | `bfc329b` | `72a2445` | `142528d` | provider-neutral DenseRetriever、无正文 Evidence/Trace、provenance fail-closed | [completion record](s6_t5_3_completion_record.md) | 不代表 Recall/MRR/NDCG、投毒防护或可信检索 |
| S6-T5.4 ContentResolver | `HUMAN_ACCEPTED` | `4155ed8` | `af55705` | `11a72f7` | `f7dc552` | canonical `corpus:` 解析、hash 校验、最小正文权限、legacy exact match | [completion record](s6_t5_4_completion_record.md) | 不代表真实 corpus adapter 或检索安全 |
| S6-T5.5 Evidence/Citation | `HUMAN_ACCEPTED` | `9a51457` | `2cacef7` | `6da27a6` | `ee905cb` | Envelope、CitationBinding、escaping、单 block rendering | [completion record](s6_t5_5_completion_record.md) | 不代表 Citation Accuracy、Trust 或生成效果 |
| S6-T5.6 Context Package | `HUMAN_ACCEPTED` | `432b07e`；协议验收 `b0c4ef6` | `71067d1` | `b136ee2` | `dbf590a` | deterministic Context Package、顺序解析、stable-prefix、结构 abstention | [completion record](s6_t5_6_completion_record.md) | 不代表 Context 安全、检索质量或生成质量 |
| S6-T5.7 Integration | `HUMAN_ACCEPTED` | 不适用；不新增协议 | 不适用；不新增业务实现 | integration evidence `b6cedf3` | `c1e8c16` | 静态与 opt-in MiniLM/temporary-Chroma 受控集成验证 | [integration record](s6_t5_7_integration_completion_record.md) | 不代表新实现能力、语义质量或正式实验 |

`NOT_SEPARATELY_RECORDED` 是证据分类，不是缺失事实的猜测：它表示在当前权威 Git log 与治理记录中没有独立、同名的
protocol/hardening/acceptance 提交，应以表中标注的主记录为准。不同提交性质不得互换，例如 `b6cedf3` 永远不能写作
implementation commit。

## 3. 已接受工程调用链与权限边界

```text
Dataset QueryRecord
  -> safe projection
  -> RetrieverQueryRecord
  -> RetrievalRequest
  -> DenseRetriever
  -> RetrievalEvidence[] + RetrievalTrace
  -> ContentResolver
  -> ResolvedContent
  -> EvidenceEnvelope
  -> CitationBinding
  -> DeterministicContextBuilder
  -> RetrievedContextPackage
```

| 层 | 允许持有的信息 | 明确边界 |
| --- | --- | --- |
| Dataset | 原始 `QueryRecord` 与 evaluator-only 数据 | evaluator-only 字段不能进入 runtime |
| Retriever runtime | safe query view、公开 metadata、向量命中 | 不持有正文、Ground Truth 或攻击标签 |
| Evidence / Trace | provenance、rank、distance/similarity、hash、计数 | 不保存正文或查询文本 |
| ContentResolver | `corpus:` ContentRef 与 expected content hash | 是唯一正文读取权限边界；unknown ref/hash mismatch fail closed |
| Chroma | embedding 与公开 provenance metadata | 不是正文权威源，不能绕过 Resolver |
| Envelope / Citation | 受控内存正文与结构身份绑定 | 普通 audit/repr 不展开正文 |
| ContextBuilder | 已验证 Evidence、预算、Citation mode | 顺序解析并在 stable-prefix cutoff 后停止正文访问 |
| Package | rendered context 的 hash、Trace 与结构化引用 | 普通审计不含 rendered context、Query、路径或 evaluator-only 字段 |

## 4. 已接受能力

以下是当前可以陈述的工程事实，均限定于合成/离线或明确记录的受控基础设施验证范围：

1. 确定性 Chunk、Chunk ID、Evidence UID、Trace 与 Package identity。
2. `QueryRecord` 经 safe projection 后才进入 Retriever runtime。
3. provider-neutral DenseRetriever 只输出无正文 `RetrievalEvidence` 和 `RetrievalTrace`。
4. `corpus:` ContentRef 加 UTF-8 SHA-256 的正文解析；unknown ref、hash mismatch、provenance mismatch 与 duplicate conflict 均 fail closed。
5. `EvidenceEnvelope`、`CitationBinding`、XML-like 结构 escaping 与 package-local `E1...En` Citation。
6. sequential resolution、stable-prefix budget selection、结构性 abstention 与 dependency error redaction。
7. safe `repr()` / `to_audit_dict()`、namespace ownership、标签隔离和公开 metadata 边界。
8. 静态 integration 以及显式固定 MiniLM + 临时 Chroma 的 close/reopen、identity stability、cleanup 互操作验证。

## 5. 不可宣称事项

当前不得宣称：

- RAG 已安全，或 Prompt Injection 已被防御；
- Knowledge / Retrieval Poisoning 已检测或缓解；
- Trustworthy Retrieval、Trust score、Trust policy 或 reranker 已实现；
- Citation Accuracy 已计算；
- Recall、Precision、MRR、NDCG 或统计检索质量已经验证；
- Groq 或其他生成式 LLM 已参与当前 Stage 6 链路；
- 正式攻击矩阵、正式 RAG 安全实验、论文结论或生产可用性已经成立。

## 6. 脱敏证据索引

| Task ID | Evidence type | Commit / status | 文档或测试入口 | Validation scope | Claim boundary |
| --- | --- | --- | --- | --- | --- |
| S6-T5.1 | implementation + hardening | `412d886`, `09584c8` | [master record](experiment_master_record.md) | deterministic chunk contracts | 无复杂 Chunking 或检索结论 |
| S6-T5.2 | contracts + acceptance | `4c12181`, `03750d9` | [completion record](s6_t5_2_completion_record.md) | safe projection and IDs | 无 Retriever/LLM 结论 |
| S6-T5.3 | protocol / implementation / hardening / acceptance | `2ad3d9c`, `bfc329b`, `72a2445`, `142528d` | [completion record](s6_t5_3_completion_record.md) | DenseRetriever offline contracts | 无质量或安全效果结论 |
| S6-T5.4 | protocol / implementation / hardening / acceptance | `4155ed8`, `af55705`, `11a72f7`, `f7dc552` | [completion record](s6_t5_4_completion_record.md) | synthetic resolver boundary | 无真实 corpus 结论 |
| S6-T5.5 | protocol / implementation / hardening / acceptance | `9a51457`, `2cacef7`, `6da27a6`, `ee905cb` | [completion record](s6_t5_5_completion_record.md) | synthetic envelope/citation boundary | 无 Citation Accuracy 结论 |
| S6-T5.6 | protocol closure / implementation / hardening / acceptance | `432b07e`, `71067d1`, `b136ee2`, `dbf590a` | [completion record](s6_t5_6_completion_record.md) | synthetic deterministic package | 无 Context safety / generation 结论 |
| S6-T5.7 | integration evidence / acceptance | `b6cedf3`, `c1e8c16` | [integration record](s6_t5_7_integration_completion_record.md) | static + opt-in real infrastructure | 无新 implementation 或正式实验结论 |
| Governance | architecture / namespace / label isolation | current T5.8 verification | `tests/architecture/`, `tests/stage6_rag/test_no_label_leakage.py` | ownership, approval, labels | 不替代安全实验 |
| Integrity | protected paths / scans / ignore | current T5.8 verification | Git diff, changed-file scans, `.gitignore` | no protected-path mutation | 不覆盖历史 manifest 技术债 |

证据索引不复制 Query、正文、向量、缓存路径或本机绝对路径。真实基础设施验证的输入仅为测试中的 synthetic content，
其正文不在本报告或普通治理日志展开。

## 7. 测试与验证证据矩阵

| 时间 / Task | 命令范围 | 结果 | 默认 skip | 解释 |
| --- | --- | --- | --- | --- |
| S6-T5.6 最终离线验收 | full Stage 6 offline regression | `438 passed, 2837 subtests passed` | 无此记录 | 已接受的 T5.6 离线工程证据；不能与后续数字合并 |
| S6-T5.7 静态集成 | `test_static_retrieval_context_pipeline.py` | `7 passed` | 否 | 受控静态链路 |
| S6-T5.7 真实基础设施集成 | `RUN_REAL_RAG_INTEGRATION=1 test_real_retrieval_context_pipeline.py` | `1 passed` | 显式启用 | 固定 MiniLM + temporary Chroma；单独记录，不与 skip 混写 |
| S6-T5.7 Stage 6 离线回归 | domains + integration + stage6_rag scopes | `370 passed, 2 skipped, 1955 subtests passed` | 是，2 skipped | skipped 不是通过；真实集成已由上一行单独证明 |
| S6-T5.7 architecture | `tests/architecture` | `75 passed, 884 subtests passed` | 否 | 候选集成时的历史快照 |
| S6-T5.7 治理验收 | `tests/architecture` | `75 passed, 887 subtests passed` | 否 | 后续治理断言增加，不替换历史运行事实 |
| Namespace + label isolation | namespace + label-isolation scopes | `10 passed, 1199 subtests passed` | 否 | 所有权与 evaluator-label 隔离 |
| S6-T5.8 文档/治理一致性 | context persistence + master record scopes | `22 passed, 371 subtests passed` | 否 | 基线报告、审批门、提交身份和链接一致性 |
| S6-T5.8 architecture | `tests/architecture` | `76 passed, 902 subtests passed` | 否 | 包含本轮新增基线报告治理断言；不替换早期运行事实 |
| S6-T5.8 namespace + label isolation | namespace + label-isolation scopes | `10 passed, 1199 subtests passed` | 否 | 本轮未改变 namespace 或标签边界 |

Ruff、scoped MyPy、Markdown relative links、changed-file secret/path scans、protected-path diff、runtime Git-ignore
和 `git diff --check` 只证明相应工程治理门通过；它们不产生 RAG 安全效果指标。

本轮历史 manifest 检查仍报告 `BLK-HIST-001` 的 110 个既有 Windows CRLF/LF 字节差异，不能写作“全仓完整性
通过”；与其并行的 protected-path Git diff 为零，才是本轮未改动 Stage 1--5 与 Stage 6 fixture/data 的事实证据。

## 8. 环境依赖说明

- MiniLM model ID：`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`。
- 固定 revision：`16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`；输出 dimension 为 `384`；CPU 运行。
- 真实基础设施测试仅在 `RUN_REAL_RAG_INTEGRATION=1` 时运行；默认快速回归 skip。
- provider spec 使用 `local_files_only=False`：缓存环境可直接执行，新环境只在显式启用测试时可能首次下载固定 revision。
- 网络与下载不是默认离线 CI 的隐含依赖；失败时不允许静默降级为 Static Provider 或替换模型。
- Chroma 使用临时目录，验证 close/reopen 后关闭并清理；不提交 Chroma 数据、模型缓存、向量或本机绝对路径。

## 9. 技术债与已知限制

### BLK-HIST-001：历史 SHA-256 manifest 的 Windows CRLF/LF 差异

- 这是既有历史基线债务，不是本轮引入的变更。
- 本轮保护路径 Git diff 是“本轮是否修改历史资产”的权威证据。
- 不得通过重写 Stage 1–5 文件或重算历史 hash 来消除差异。
- 因此不得把该 manifest 结果写成“本轮全仓 integrity 全部通过”；应如实写为“已知历史差异仍存在，本轮 protected-path diff 为零”。

其他限制：真实 MiniLM 仅为 opt-in 基础设施验证；尚无检索质量基准、生成式模型链、正式污染攻击语料、Trust、
Citation Accuracy 或正式统计实验。

## 10. 下一审批门

本轮结束后只应登记：

```text
S6-T5.8: Completed, pending human acceptance
S6-T5: Baseline closure completed, pending human acceptance
Stage 6.1 formal research: NOT APPROVED
Formal RAG security experiment: NOT STARTED
Last accepted implementation commit: b136ee2
Last accepted integration evidence commit: b6cedf3
```

只有项目负责人最终人工验收 S6-T5.8 后，才可以将该验收提交定义为 accepted S6-T5 baseline SHA，并另行决定是否：

1. 创建 annotated tag `s6-t5-rag-baseline-v1`；
2. 从该 SHA 创建 `research/stage6-1-hidden-poisoning`；
3. 新建独立 ChatGPT 分支；
4. 开始 Stage 6.1 正式实验协议设计。

本报告本身不创建 tag、分支或 Stage 6.1 任务。
