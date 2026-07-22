# LLMGuard 上下文恢复协议

## 目的

本协议让新的 Codex Thread、Agent、Workspace 或 Worktree 在旧对话不可用时，仅依靠仓库文件与 Git
恢复项目目标、当前状态、审批门和结论边界。它不授权任何业务实现。

## 新 Thread 启动流程

1. 从仓库根 `AGENTS.md` 开始，按其中的 Canonical Context Sources 顺序读取。
2. 读取长期需求、项目负责人决策登记册、项目总控、动态状态、Experiment Master Record、当前 Stage README、当前 design spec 和 implementation plan。
3. 运行 Git 只读检查：repo/worktree 根、branch、HEAD、status、upstream sync、最近 15 条 commit。
4. 检查根与当前目录层级是否存在更深的 `AGENTS.md`/`AGENTS.override.md`，并说明作用域。
5. 用中文输出 Context Recovery Report。
6. 若当前任务未批准、文档与 Git 冲突或存在来源不明的未提交修改，停止并等待用户决定。
7. 用户已明确批准当前任务时，报告后按批准范围执行；不得扩大到下一 Task/Stage。

## 新 Worktree 启动流程

1. 用 `git worktree list --porcelain` 确认目标 worktree、branch 和 HEAD。
2. 在目标 worktree 中重新读取所有权威文件；不要假设另一个 worktree 的工作树状态相同。
3. 核对 upstream、ahead/behind、未跟踪文件、忽略的 runtime 和本地依赖状态。
4. 检查当前任务所需依赖和测试，但不因缓存存在就宣称真实集成已运行。
5. 输出独立 Context Recovery Report，明确该 worktree 与主 worktree 的差异。

## 权威文档读取顺序

1. `AGENTS.md`
2. `docs/governance/long_term_research_requirements.md`
3. `docs/governance/project_owner_decision_register.md`
4. `PROJECT_MASTER_CONTEXT.md`
5. `docs/governance/current_work_state.md`
6. `docs/governance/experiment_master_record.md`
7. 当前 Stage README
8. 当前任务 design specification
9. 当前任务 implementation plan
10. 最近 15 条 Git commit
11. 当前 branch、HEAD、status 和 remote sync

长期需求负责能力基线，项目负责人决策登记册负责已确认的解释与决策；`PROJECT_MASTER_CONTEXT.md` 负责
架构与长期阶段叙事，`current_work_state.md` 负责当前任务与审批门，Experiment Master Record 负责实验路线、
运行、指标和证据恢复；这些来源不得相互替代。

## 可复制启动模板

```text
你正在继续开发 LLMGuard Research Framework。

不要依赖旧对话记忆，也不要立即修改代码。

请先完整阅读：

1. AGENTS.md
2. docs/governance/long_term_research_requirements.md
3. docs/governance/project_owner_decision_register.md
4. PROJECT_MASTER_CONTEXT.md
5. docs/governance/current_work_state.md
6. docs/governance/experiment_master_record.md
7. 当前 Stage README
8. 当前任务 design spec
9. 当前任务 implementation plan
10. git log 最近 15 条
11. 当前 branch、HEAD 和 git status

然后用中文报告：

1. 项目长期目标；
2. 用户能力优先级；
3. 当前已完成到哪个 Stage 和 Task；
4. 当前 branch 和 HEAD；
5. 当前任务；
6. 本任务允许修改什么；
7. 本任务禁止修改什么；
8. 下一审批门；
9. blocker 和技术债；
10. 两篇论文路线与 Stage 7 是否属于论文二；
11. 项目负责人已确认的不可变决策；
12. 当前 blocker 与已批准解决方向；
13. 是否有新任务错误改写已接受决策；
14. 文档与 Git 是否一致；
15. 当前可以宣称什么；
16. 当前不能宣称什么。

在我确认前不要修改代码。
```

## Context Recovery Report 模板

```text
Context Recovery Report
1. 长期目标：
2. 能力优先级：
3. 已完成 Stage/Task：
4. Branch：
5. HEAD：
6. 当前任务：
7. 允许修改：
8. 禁止修改：
9. 下一审批门：
10. 两篇论文路线/Stage 7 定位：
11. 已确认不可变决策：
12. blocker 与已批准解决方向：
13. 已接受决策是否被错误改写：
14. 文档/Git 冲突：
15. 未提交或未推送修改：
16. 可以宣称/不能宣称：
```

## 指令冲突优先级

当前会话用户最新明确要求 > 长期研究需求 > 项目负责人决策登记册 > 项目总控 > 动态工作状态 > 当前 design spec > 当前
implementation plan > 历史计划/学习笔记。Git 单独决定 branch、HEAD、工作树、文件、commit 和同步事实。

若长期需求与项目负责人决策登记册冲突，必须停止并报告。若较低优先级只是历史快照，由较新文件明确标记即可；若冲突会改变允许范围、数据、历史资产或审批门，
必须停止并报告，不得自行选择。

## 未批准任务停止规则

- `Approved now` 未包含的代码、实验、模型下载、外部 API 或下一 Task/Stage 均不得开始。
- 设计获批不等于实现获批；子任务获批不等于整个 Stage 获批。
- 不以“顺手补齐”“测试需要”或“后续肯定会用”为理由跨越审批门。
- 存在来源不明的工作树修改时，先说明并保留，不覆盖、不回滚。

## 任务结束更新流程

1. 更新动态状态、项目总控、当前 Stage README 和学习笔记。
2. 运行任务要求的测试、架构/兼容性、Ruff、MyPy、标签泄漏、secret 和 runtime-ignore 检查。
3. 确认未越界修改历史资产、legacy namespace、数据或未批准业务代码。
4. 创建范围清晰的 commit，push upstream，确认 ahead/behind 为零和工作树 clean。
5. 在动态状态中保留下一个任务和审批门；暂停，不自动开始。

## Git 与文档不一致时

Git 状态事实优先；文档不能覆盖不存在的 commit、错误 branch 或未提交文件。先保存只读证据，再判断：

- 文档落后：当前任务范围内更新动态状态，保留历史叙述；
- Git 有未知修改：停止并报告来源，不覆盖；
- HEAD 超出预期：阅读新增 commit，重新输出恢复报告；
- 本地未推送：在用户授权范围内完成验证后再 push；
- 远端领先或分叉：停止，先说明合并/变基风险，不强制改写历史。

## 旧上下文丢失时

不要尝试凭记忆重建旧对话。以 `AGENTS.md` 为入口，结合长期需求、项目总控、动态状态、Experiment Master Record、Stage 文档、
任务 spec/plan、Git history 和原始实验证据恢复。缺失的信息标记为 unknown，等待用户补充；不能把推测写成
已接受事实。
