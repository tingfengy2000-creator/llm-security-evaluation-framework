# S6-T5.7 受控检索上下文管线集成验证记录

## 任务定位

- 任务：`S6-T5.7 Controlled Retrieval Context Pipeline Integration and Security Validation`。
- 性质：`INTEGRATION_ENGINEERING_VALIDATION / STATIC_AND_OPT_IN_REAL_INFRASTRUCTURE`。
- 当前状态：`Completed, pending human acceptance`。
- 最后已接受实现提交仍为：`b136ee2`。
- 本记录是候选集成证据，不是正式 RAG 安全实验，也不是新的已接受实现提交。

## 验证的调用链

```text
Dataset QueryRecord
  -> safe projection
  -> RetrieverQueryRecord
  -> RetrievalRequest
  -> DenseRetriever
  -> RetrievalEvidence[] + RetrievalTrace
  -> ContentResolver
  -> EvidenceEnvelope + CitationBinding
  -> DeterministicContextBuilder
  -> RetrievedContextPackage
```

静态测试使用 `StaticEmbeddingProvider + InMemoryVectorStore`；真实基础设施测试使用固定 MiniLM embedding provider 与临时 Persistent ChromaDB。两类测试的正文都只由 synthetic in-memory corpus reader 提供，Chroma 只保存向量和公开 metadata。

## 已验证事实

1. safe projection 后，攻击标识、期望文档、生成问题及 evaluator-only 字段不会进入 retriever runtime 的审计表示。
2. DenseRetriever 输出只有无正文 Evidence 和 Trace；正文只能由 canonical `corpus:` ContentRef 加 content hash 经 Resolver 获取。
3. 多条 Evidence 能产生连续的 `E1...En` CitationBinding，并且重复输入下 Request、Evidence UID、Trace hash、rendered-context hash 和 Package ID 稳定。
4. stable-prefix cutoff 会停止后续正文访问、Envelope factory 与 renderer 调用；未知 ref、hash mismatch、provenance mismatch 和 duplicate conflict 均 fail closed，且异常不回显 Query 或正文。
5. legacy `chroma:` 仅经 synthetic exact-match adapter 映射到 canonical `corpus:` ref；未从 Chroma 读取正文。
6. 显式设置 `RUN_REAL_RAG_INTEGRATION=1` 后，固定模型 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`、固定 revision `16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1` 实际输出 384 维有限向量；临时 Chroma collection close/reopen 后，Evidence UID、Trace hash、rendered-context hash 和 Package ID 一致。
7. 临时 Chroma 目录在测试 finally 块关闭 client 并清理；未生成可提交 runtime 数据。

## 验证结果

| 类别 | 命令范围 | 结果 |
| --- | --- | --- |
| 静态集成 | `test_static_retrieval_context_pipeline.py` | 7 passed |
| 真实基础设施集成 | `RUN_REAL_RAG_INTEGRATION=1 test_real_retrieval_context_pipeline.py` | 1 passed |
| Stage 6 离线回归 | `tests/domains/retrieval tests/integration/retrieval tests/stage6_rag` | 370 passed, 2 skipped, 1955 subtests passed |
| 架构治理回归 | `tests/architecture` | 75 passed, 884 subtests passed |

快速回归中真实集成测试默认 skip 是预期行为；完成前已单独显式启用并通过，不能将 skip 写成通过。

## 问题与处置留痕

1. 首次真实集成测试曾把 synthetic 请假文档的 Top-1 写成断言。该断言会把基础设施可重复性错误扩展成未获授权的检索质量结论，已删除；保留的是 close/reopen 前后同一运行结果和 Package identity 一致性。
2. 初次静态夹具遗漏篡改 Evidence 后的 UID 重算，且预算未保证第一个 block 能放入；这是测试装配错误，已修正，不涉及业务源码或协议变更。
3. 历史 SHA-256 manifest 检查在本 Windows 工作树报告 110 个既有 Stage 1-5 文件差异。已确认该类 CRLF/LF 基线差异属于既有 `BLK-HIST-001` 技术债；未修改任何历史文件。另以 Git protected-path diff 检查确认本轮未修改 Stage 1-5、Stage 6 fixture/data 或 legacy `src/codeguarder/`。

## 结论边界

可以说：已获得一条 label-isolated、可重复、可审计的受控 retrieval-to-context 工程集成候选证据，并实际运行过固定 MiniLM 与临时 Chroma。

不能说：检索质量、召回率、Citation Accuracy、Prompt Injection 防护、Knowledge Poisoning 检测、Trustworthy Retrieval、LLM 集成、正式 RAG 安全实验或生产可用性已经成立。

## 面试讲法

我把“检索到什么”与“允许把什么正文交给后续模型”拆成两层：DenseRetriever 只输出无正文的 Evidence/Trace；Resolver 依据受控 `corpus:` ref 和 hash 在最小权限边界内读取一条正文；ContextBuilder 再以确定性排序、预算和 Citation Binding 构建包。这样既能复现，也能证明 cutoff 后的候选根本没有被读取。真实 MiniLM/Chroma 测试只证明基础设施互操作，不把一次小型语义排序夸大为安全或质量结论。

## 下一审批门

等待项目负责人的 S6-T5.7 人工验收。`S6-T5.8` 仍为 `NOT APPROVED`，正式 RAG security experiment 仍为 `NOT STARTED`。
