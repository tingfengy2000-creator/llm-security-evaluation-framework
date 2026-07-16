# 仓库目录地图

## 快速入口

- 项目目标与当前进度：`docs/project_context/`
- 面试集中复习：`interview_prep/`
- 实验注册表：`experiments/registry.json`
- 上传前检查：`docs/git/UPLOAD_CHECKLIST.md`

## Stage 1–4.1

- 代码与运行脚本：`llm-security-stage1/`
- Stage 1 报告：`deliverables/stage1/`
- Stage 1 教学文档：`deliverables/stage1_learning/`
- Stage 2 Mock API 对照：`deliverables/stage2/`
- Stage 3 Groq 真实扫描：`deliverables/stage3/`
- Stage 4 Guard A/B：`deliverables/stage4/`
- Stage 4.1 四模式消融：`deliverables/stage4_ablation/`

`llm-security-stage1/.venv/`、Python 缓存和 garak 本地运行状态不进入 Git。

## Stage 5

- 基础框架代码：`src/codeguarder/attacks/`、`evaluation/`、`metrics/`、`reporting/`、`taxonomy/`、`proxy/`
- 论文级框架：`src/codeguarder/stage5_paper/`
- 数据：`data/stage5/`、`data/stage5_paper/`
- 测试：`tests/stage5/`、`tests/stage5_paper/`
- 脚本：`scripts/run_stage5*.ps1`
- 报告：`deliverables/stage5/`、`deliverables/stage5_paper/`

## 治理目录

- `docs/project_context/`：长期协作上下文和路线图。
- `interview_prep/`：中文面试集中复习区。
- `experiments/registry.json`：阶段状态、入口和结论边界。
- `provenance/`：历史 baseline、文件 manifest 和修正账本。
- `deliverables/`：脱敏报告、日志和学习文档。

## Stage 6 说明

Stage 6 当前位于独立分支 `feature/stage6-rag`，暂未合入 `main`。因此 GitHub 默认分支看不到 Stage 6 源码是预期状态，不代表文件丢失。
