# 生成内容与 Git 管理规范

## 1. 目录职责

| 目录 | 内容 | Git 策略 |
| --- | --- | --- |
| `src/` | 可复用框架代码 | 跟踪 |
| `llm-security-stage1/` | Stage 1–4.1 历史代码和脚本 | 只读保留 |
| `data/` | 合成攻击、benign 数据、manifest | 脱敏后跟踪 |
| `tests/` | TDD、回归、完整性与安全校验 | 跟踪 |
| `scripts/` | 可复跑命令与 Git preflight | 跟踪 |
| `deliverables/` | 阶段报告、脱敏结果、学习文档 | 跟踪 |
| `experiments/` | 跨阶段实验注册表 | 跟踪并持续更新 |
| `provenance/` | 文件清单、历史基线、修正账本 | 跟踪 |
| `interview_prep/` | 面试前集中复习入口 | 跟踪 |
| `docs/project_context/` | 长期协作上下文 | 跟踪并随阶段更新 |
| `runtime/`、`.venv/`、缓存 | 本地运行状态和依赖 | 忽略 |
| `.worktrees/` | 本地 Git worktree | 忽略 |

## 2. 每次实验的最小证据链

每次正式运行至少记录：

- `run_id`、时间和 Git commit；
- 数据集版本/manifest/hash；
- 模型、base URL 类型、参数和 seed；
- Guard 模式、Detector 来源和规则版本；
- 脱敏 Attempt 日志；
- 聚合 JSON/CSV/Markdown；
- 校验器结果与 `run_status`；
- 失败命令、错误类别和修复记录。

原始证据、聚合结果和人工解释必须分层保存，不能只保留一份 Markdown 结论。

## 3. 历史产物保护

- 已完成阶段的 JSON、JSONL、HTML、日志和摘要不覆盖。
- 重跑必须进入新的 `runs/<run_id>/`。
- 如果历史报告确有错误，新增 `corrections/<date>-<topic>.md`，写明原结论、错误原因、修正证据和影响范围。
- 不为了“目录更整齐”移动历史文件；导航层使用 README 和链接解决可发现性。

## 4. 敏感信息与危险内容

- 禁止提交 `.env`、API Key、Authorization header、Bearer token。
- 自动扫描 `GROQ_API_KEY`、`OPENAI_API_KEY`、`gsk_`、`sk-`、`Bearer`。
- 日志不保存完整危险输出、完整污染文档或真实隐私数据。
- 保存 SHA-256、字符长度、有限脱敏摘要、命中规则、决策和必要元数据。
- 截图前检查终端历史、地址栏、环境变量和用户目录信息。

## 5. 大文件和在线数据

- 小型合成数据和脱敏报告直接进入 Git。
- 10–100 MB 文件优先 Git LFS。
- 更大、受许可限制或可公开下载的数据只保存稳定 URL、版本、license、SHA-256 和获取脚本。
- ChromaDB 索引、Embedding 模型缓存和可重建运行时数据不进入 Git。

## 6. 分支与提交

- 一个阶段使用独立功能分支，例如 `feature/stage6-rag`。
- 一个 Task 或一个可验证行为形成一个小提交。
- 提交前运行对应测试、静态检查、秘密扫描和 `scripts/git_preflight.ps1`。
- 未提交修改必须在阶段状态里明确说明，不能当作稳定基线。
- 合并后更新 `experiments/registry.json`、阶段 README、本目录进度页和面试材料。

## 7. 面试材料的复制原则

`interview_prep/` 可以集中整理知识点和实现过程，但不复制大量源码或原始日志。优先使用：

- 阶段一页摘要；
- 架构图和调用链；
- 关键指标表；
- 一个成功案例、一个失败案例、一个工程排错案例；
- 30 秒、1 分钟、3 分钟话术；
- 指向真实代码和报告的相对链接。

这样既方便复习，也避免多份副本随代码演进而失真。
