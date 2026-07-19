# Current Work State

## Repository

- Active branch: `feature/stage6-rag`
- Current HEAD: 以 `git rev-parse HEAD` 为实时事实；CP-2 启动基线为 `59e29a9`
- Worktree: `feature/stage6-rag` 的 linked worktree；用 `git rev-parse --show-toplevel` 实时解析
- Working tree status: CP-2 完成后应为 clean；每次启动必须用 `git status` 验证
- Remote sync status: CP-2 启动时 `0 ahead / 0 behind`；每次启动必须与 upstream 复核

## Accepted Baseline

- Last accepted architecture task: `A1R` namespace migration and governance freeze
- Last accepted stage task: `S6-T4 Hardening`
- Last accepted commit before CP-2: `59e29a9 docs(governance): record long-term rag research requirements`

## Current Task

- Task ID: `S6-T5-DESIGN-FREEZE`
- Task name: `S6-T5 Design Freeze`
- Task type: Design and governance documentation
- Status: Design review pending; `S6-T5 implementation: Not started`
- Objective: 冻结透明 Dense Retrieval、Evidence/Citation 和 ContextBuilder 的设计与 TDD 实施计划

## Approval Gate

- Approved now: Context persistence governance and S6-T5 design documentation only
- Not approved now: S6-T5 Python implementation, Retriever, ContentResolver, ContextBuilder or EvidenceEnvelope business implementation
- Next human approval: Review S6-T5 design specification and implementation plan

## Must Not Start

- S6-T5 Python implementation or DenseRetriever
- ContentResolver、ContextBuilder 或 EvidenceEnvelope 业务实现
- Trust、EvidenceSignal、TrustAggregator 或 RetrievalPolicy 实现
- LLM、Groq 或任何真实模型调用
- 新模型下载或正式 Chroma runtime
- S6-T6、Stage 6.1、Stage 6.2 或 Stage 7 实现

## Blockers and Technical Debt

- No blocking implementation issue is accepted for CP-2.
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
- Commit: CP-2 启动基线 `59e29a9`；CP-2 完成提交由 Git 实时解析
- Updated by: Codex under explicit user-approved CP-2 governance task
