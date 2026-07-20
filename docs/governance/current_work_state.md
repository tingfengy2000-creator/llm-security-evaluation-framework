# Current Work State

## Repository

- Active branch: `feature/stage6-rag`
- Current HEAD: 以 `git rev-parse HEAD` 为实时事实；S6-T5 Design Hardening 启动基线为 `e64063e`
- Worktree: `feature/stage6-rag` 的 linked worktree；用 `git rev-parse --show-toplevel` 实时解析
- Working tree status: CP-2 完成后应为 clean；每次启动必须用 `git status` 验证
- Remote sync status: CP-2 启动时 `0 ahead / 0 behind`；每次启动必须与 upstream 复核

## Accepted Baseline

- Last accepted architecture task: `A1R` namespace migration and governance freeze
- Last accepted stage task: `S6-T4 Hardening`
- Last accepted governance commit before S6-T5 Design Hardening: `e64063e docs(retrieval): freeze s6-t5 controlled retrieval context design`

## Current Task

- Task ID: `S6-T5-DESIGN-HARDENING`
- Task name: `S6-T5 Design Hardening`
- Task type: Design and governance documentation
- Status: `Completed, pending second human review`; `S6-T5 implementation: Not started`
- Objective: 加固唯一 stable contract、运行时 Query 投影、ContentRef、敏感序列化与异常/abstention 边界

## Approval Gate

- Approved now: S6-T5 Design Hardening 文档、ADR、治理状态和必要验证
- Not approved now: `S6-T5.1 implementation: Not approved`，以及任何 Retriever、Chunker、ContentResolver、ContextBuilder 或 EvidenceEnvelope 业务实现
- Next human approval: Second human review of hardened design, contract migration matrix and implementation plan

## Must Not Start

- S6-T5 Python implementation or DenseRetriever
- ContentResolver、ContextBuilder 或 EvidenceEnvelope 业务实现
- Trust、EvidenceSignal、TrustAggregator 或 RetrievalPolicy 实现
- LLM、Groq 或任何真实模型调用
- 新模型下载或正式 Chroma runtime
- S6-T6、Stage 6.1、Stage 6.2 或 Stage 7 实现

## Blockers and Technical Debt

- No blocking implementation issue is accepted for S6-T5 Design Hardening.
- 旧历史 SHA 测试存在 CRLF/LF 跨 worktree 假阳性；只能登记技术债，不修改历史文件或 hash 基线。
- 动态 HEAD 和 upstream 状态不可可靠自写入同一个提交；Git 命令始终优先于本文快照。

## Canonical Context

1. `AGENTS.md`
2. `docs/governance/long_term_research_requirements.md`
3. `PROJECT_MASTER_CONTEXT.md`
4. `docs/governance/current_work_state.md`
5. Current design specification
6. Current implementation plan
7. Git history

## Last Update

- Date: `2026-07-19`
- Commit: S6-T5 Design Hardening 启动基线 `e64063e`；完成提交由 Git 实时解析
- Updated by: Codex under explicit user-approved S6-T5 Design Hardening task

## 2026-07-20 Runtime Override: S6-T5.1 Completed Pending Human Acceptance

- 最新人工批准已覆盖上方 Design Hardening 时的历史快照：本轮只允许并已完成
  `S6-T5.1 Chunking Contracts + IdentityChunker`。
- 新增规范契约位于 `src/llmguard/domains/retrieval/contracts/chunking.py`；行为代码仅位于
  `src/llmguard/domains/retrieval/chunking/`。未向 legacy `src/codeguarder/` 新增实现。
- 已完成的能力仅为：`DocumentRecord` 加显式 corpus snapshot、确定性 `identity` 配置与一文一块
  `ChunkRecord`。它不检索、不读取 Chroma、不构造 Context、不调用 LLM。
- 本轮仍禁止：S6-T5.2 Retrieval Contracts/IDs、Retriever、ContentResolver、ContextBuilder、Trust、
  Evidence/Trace 业务对象、Groq、RAG 指标和正式实验。
- 下一审批门：人工审查 S6-T5.1 的代码、TDD 证据与本状态后，才可单独批准 S6-T5.2。

## 2026-07-20 Current Task: S6-T5.1 Implementation Hardening

- Current task: `S6-T5.1 Implementation Hardening`。
- Status: `Completed, pending final human acceptance`。
- S6-T5.1 implementation: `Completed and hardened`。
- S6-T5.2 implementation: `Not approved`。
- 本轮冻结修复：token 策略只使用 `max_tokens`，稳定 API 已删除无效的 `window_size`；Chunking
  领域异常唯一归属 `contracts/errors.py`，`chunking/errors.py` 仅 re-export；ChunkRecord 现在显式持有
  `chunk_schema_version` 并重算验证 canonical chunk ID；metadata 先检查 key 类型再排序，且拒绝路径 key。
- Next approval gate: `Final human review of S6-T5.1 deterministic contracts, error model, identity validation and acceptance tests`。
- 禁止项不变：不得开始 S6-T5.2、Retriever、Evidence、Trace、Resolver、Citation、Context、Trust、Groq
  或正式实验。
