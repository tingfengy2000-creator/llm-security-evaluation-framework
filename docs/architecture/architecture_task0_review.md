# Architecture Task 0 架构评审报告

> A1R 后续记录：本报告描述的是改名前的 A0 事实。`A1R` 已将允许范围内的 Stage 6 Task 1–3
> 实现迁至 `src/llmguard/domains/retrieval/`，并保留旧 facade；完整现状见 ADR 0006。

## 结论

Architecture Task 0 冻结了 CodeGuarder 的长期边界，但没有实现或迁移业务代码。当前可安全进入 Architecture Task 1；在获得下一次明确指令前，不开始 `core/`、`domains/retrieval/`、真实 Embedding、ChromaDB 或 Groq 调用。

## 1. 当前事实

- 当前 worktree 为 `D:/llmProject/.worktrees/stage6-rag`，分支为 `feature/stage6-rag`，Task 0 开始 HEAD 为 `c68c7f2`；
- Task 1–3 已完成，标签隔离加固提交为 `055f266`；
- 基线验证为 104 tests、1919 subtests、Ruff 和 MyPy 通过；
- Stage 1–5 历史路径相对当前 HEAD 未变化；
- 真实 Embedding、Persistent ChromaDB、Retriever、Trust、Evaluator 尚未实现；
- GitHub 未登录公开 API 返回 404，结合已知远端地址可确认仓库目前为 Private。

## 2. 当前代码与目标架构差异

当前 Stage 6 实现在 `src/codeguarder/stage6_rag/`，包含 contracts 与 attacks；目标架构要求它们迁移到 `src/codeguarder/domains/retrieval/`，并由 `compatibility/stage6_rag/` 保留旧导入路径。

当前不存在通用 `core/`、领域 `runtime/agent/`、compatibility adapters、声明式 retrieval 配置、`TrustedContextPackage`。这些都是冻结后的后续增量工作，不是本轮已经实现的文件。

## 3. 需要迁移的文件

Architecture Task 1 只迁移以下 Stage 6 规范实现：

- `src/codeguarder/stage6_rag/contracts/models.py`；
- `src/codeguarder/stage6_rag/contracts/schemas.py`；
- `src/codeguarder/stage6_rag/attacks/attack_matrix.py`；
- `src/codeguarder/stage6_rag/attacks/attack_renderer.py`；
- 对应 `__init__.py` 与 Stage 6 测试导入路径。

未来 Task 4 起的新检索能力只写入 `domains/retrieval/`，不再向旧目录添加业务实现。

## 4. 不可修改的历史文件

`llm-security-stage1/`、Stage 1–5 交付物、`data/stage5/`、`src/codeguarder/stage5_paper/`、已有 run 与历史校验文件均不可移动、删除、覆盖或批量改写。

## 5. 迁移风险与回滚

主要风险是 Python import 路径改变、循环依赖、标签隔离在新路径中被削弱，以及把 RAG 字段错误放入 core。控制措施为：先写 import compatibility 测试、保持 facade 无业务逻辑、运行 104 测试基线、增加 portable history integrity 检查。

回滚方案是撤销 Architecture Task 1 的单独提交；历史 Stage 1–5 与 Stage 6 Task 3 数据不受影响。旧 `stage6_rag` facade 在迁移稳定前持续提供导入兼容。

## 6. 验收标准

- 历史 Stage 1–5 文件 hash 不变；
- 104 tests、Ruff、MyPy 持续通过；
- no-label-leakage 语义不变；
- core、retrieval、compatibility 职责无重叠；
- TrustedContextPackage 与 RAGSecurityEnvelope 分离；
- R1–R6、T10–T15 保持兼容；
- Stage 6A/6B/6C/6.1/6.2/7 边界清晰；
- 不产生 API Key、标签、完整文档或危险输出泄露；
- 每一阶段使用可执行配置、manifest 与独立运行证据。

## 7. 后续顺序

1. Architecture Task 1：最小 core contracts、Stage 6 Task 1–3 迁移、compatibility facade；
2. Stage 6 Task 4：EmbeddingModelSpec、Static/SentenceTransformer Provider、InMemory/Chroma Store；
3. Stage 6 Task 5：Retriever、Trace、Context、文档泄露防护；
4. Stage 6 Task 6：EvidenceSignal、off/observe、PassThrough；
5. 依次进入 Provider、Evaluator、Runner、规则基线、报告、Groq smoke 和收敛任务。

## 8. 面试、论文与立项价值

面试层面，该冻结展示了工程边界、向后兼容、审计与可复现性意识。论文层面，它把安全基线与算法创新分离，避免将工程规则包装为研究贡献。立项层面，它将“威胁建模—检测—可信检索—原型评测”映射为独立但可集成的研究任务。

## 9. 当前不能宣称完成的内容

不能宣称已完成真实 ChromaDB、真实 Embedding、可信重排、鲁棒聚合、中文隐蔽污染数据集、学习型检测、完整 RAG 评测、真实 Groq 矩阵、公开 Artifact 或论文成果。
