# Stage 1–5 Git 同步审计

审计日期：2026-07-16。

## 审计结论

执行 `git fetch origin --prune` 后，本地基线与 `origin/main` 的 Stage 1–5 核心目录已跟踪文件数量一致。本轮不重新上传虚拟环境或缓存，只新增项目上下文、路线图和 GitHub 导航文件。

| 路径 | 本地跟踪文件 | 远端跟踪文件 | 状态 |
| --- | ---: | ---: | --- |
| `llm-security-stage1/` | 25 | 25 | 一致 |
| `data/stage5/` | 7 | 7 | 一致 |
| `data/stage5_paper/` | 4 | 4 | 一致 |
| `deliverables/stage1/` | 13 | 13 | 一致 |
| `deliverables/stage2/` | 17 | 17 | 一致 |
| `deliverables/stage3/` | 22 | 22 | 一致 |
| `deliverables/stage4/` | 59 | 59 | 一致 |
| `deliverables/stage4_ablation/` | 77 | 77 | 一致 |
| `deliverables/stage5/` | 33 | 33 | 一致 |
| `deliverables/stage5_paper/` | 28 | 28 | 一致 |
| `src/codeguarder/` | 56 | 56 | 一致 |
| `tests/stage5/` | 9 | 9 | 一致 |
| `tests/stage5_paper/` | 12 | 12 | 一致 |

## 大目录说明

`llm-security-stage1/` 工作目录约 1.36 GB、5 万余文件，主要来自本地 `.venv/`。Git 实际只跟踪 25 个配置、脚本和测试文件；虚拟环境和缓存由 `.gitignore` 排除。这是正确的仓库管理方式，其他机器通过 requirements 重建环境。

## 本轮排除项

- `feature/stage6-rag`：Stage 6 独立开发分支，本轮暂不合并。
- `figures/rag_poisoning_framework_cn.*`：属于后续 RAG 方向，不属于 Stage 1–5 同步范围。
- `tmp/proposal/`：临时提案模板，不属于实验代码或脱敏交付物。

## 审计边界

文件数量一致只能证明路径覆盖一致；内容一致由 Git commit/tree 对象保证。推送完成后应以 Pull Request diff、CI/本地测试和 `scripts/git_preflight.ps1` 共同作为发布证据。
