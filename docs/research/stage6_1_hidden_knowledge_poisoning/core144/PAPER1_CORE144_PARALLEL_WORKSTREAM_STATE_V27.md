# Core144状态V27：实验与D2/D3数据标注对话分工

2026-10-29（JST）；PODR-152 / OR-106 / REL-2026-0121。
Owner将开启本机本项目新Codex对话负责D2/D3标注/数据准备；原对话继续实验。
[新对话交接入口](PAPER1_CORE144_D2_D3_DATA_THREAD_HANDOFF_V1.md)。

| 工作线 | 当前可核实状态 | 下一门 |
| --- | --- | --- |
| 原对话实验 | L0 Cursor代码/私有输入交接已推a83437a；未收到新的5090实验结果，远端实际运行状态未观察 | 原固定源码运行/回包审计，硬门不豁免，不启动D2D3实验 |
| 新对话D2 | 48组144条，37建议已处置、两个HN最小修复待原R3/R4定向两阶段复审 | 先两题Phase1原件锁/验收，再正式targeted Phase2；全144验收前不发Human |
| 新对话D3 | 48组144条；两个拟S3路径可单源反驳，Phase2 withheld | Owner先决定有界修复/重分配/HOLD，本次分工不替代决定 |
| 新对话本身 | 交接包就绪；Owner将开新对话，无新对话ID | 按AGENTS恢复并只读核查，不假称新线已执行 |

现有两个worktree中仅研究worktree用于本任务；未新建worktree。共享checkout的Git/文档写入必须串行，显式stage，不覆盖另一线或原无关design/PDF。
D1_DEV40/120/13家族及8/24HOLD、原数据/Guide/人工/Evidence/历史均不变；Core正式GT/split未执行。
新分工无新科研授权、Human放行或D3修题；新对话可准备上下文/盘点与既有门的清单，不能运行检测或按D1效果修改数据。
