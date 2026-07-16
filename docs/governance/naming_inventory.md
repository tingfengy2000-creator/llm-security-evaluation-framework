# A1R 命名使用清单

审计时间：2026-07-16，审计范围：当前 worktree 的 Git 跟踪文本文件。命令使用完整项目标识
`CodeGuarder`、`codeguarder`、`CodeGuard`、`codeguard`、
`codeguarder-llm-security-lab`、`LLMGuard`、`llmguard`、`llm_guard`、`llm-guard`，不对普通
`guard` 术语做替换。

## 基线结论

### 可复核起点

- worktree：`feature/stage6-rag` 的独立工作树；开始迁移时 `HEAD` 为
  `0648420744a55e66db345e3e033fcbde1aef7c51`，相对 `main` 的 merge base 为
  `f7cda5066656f68e64c8b92472b377e92eb6c235`，工作树干净。
- Stage 6 离线回归基线：`104 passed, 1919 subtests passed`；no-label-leakage
  基线：`7 passed, 1221 subtests passed`。
- 已知环境限制：全仓 `pytest -q` 在历史 Stage 4/5 的 `openai` 依赖缺失处收集失败；
  全仓 Ruff/MyPy 还存在历史代码问题。本轮只对 A1R 新增或迁移范围执行定向静态检查，
  不以改写 Stage 1–5 为代价消除这些既有问题。
- 可见性：未登录 GitHub API 对远端返回 404，结合已有私有仓库审计与可认证远端配置，
  当前按 **Private** 管理；本轮不变更可见性或远端仓库名称。

| 名称 | 命中文件数 | 处理 |
| --- | ---: | --- |
| `CodeGuarder` | 31 | 当前有效文档迁移；历史文本和台账保留 |
| `codeguarder` | 66 | Stage 6 迁移为 facade；Stage 5 legacy 与历史测试保留 |
| `codeguarder-llm-security-lab` | 1 | 迁移 `pyproject.toml` distribution |
| `LLMGuard` / `llmguard` | 0 | A1R 新增规范名称 |
| `llm_guard` / `llm-guard` | 0 | 永不作为本项目 distribution 或 namespace |

下方路径由 `git grep -l` 快照得到；精确的允许路径由
`config/naming_legacy_allowlist.yaml` 管理。每次 A1R 后续提交都必须重新运行命名校验。

## 1. 当前业务代码

| 路径 | 处理策略 |
| --- | --- |
| `src/codeguarder/stage6_rag/contracts/{models.py,schemas.py,__init__.py}` | 迁移规范实现至 `src/llmguard/domains/retrieval/contracts/`；旧路径改为 re-export facade |
| `src/codeguarder/stage6_rag/attacks/{attack_matrix.py,attack_renderer.py,__init__.py}` | 迁移规范实现至 `src/llmguard/domains/retrieval/attacks/`；旧路径改为 re-export facade |
| `src/codeguarder/__init__.py` | 作为旧 namespace 标识保留，增加兼容说明 |
| `src/codeguarder/{evaluation,proxy}/` 中 6 个命中文件 | Stage 5 当前实现，冻结 legacy；本轮不复制、不移动、不改写 |
| `src/codeguarder/stage5_paper/{audit,detectors,evaluation,proxy}/` 中 5 个命中文件 | Stage 5 Paper 历史实现，冻结 legacy |

`src/codeguarder/{attacks,metrics,reporting,taxonomy}/` 及所有 Stage 5 源文件虽可能不含文本
命中，但其路径包含旧 namespace。它们同样属于受保护 legacy，不在 A1R 重命名范围。

## 2. 当前配置、脚本和测试

| 路径集合 | 处理策略 |
| --- | --- |
| `pyproject.toml` | 更新 distribution、description 与包发现兼容说明 |
| `scripts/{build_file_manifest.py,run_stage5_*.ps1}` | 历史/当前 Stage 5 脚本；不批量替换历史运行语义 |
| `tests/stage6_rag/{test_contracts.py,test_no_label_leakage.py,test_rag_attack_matrix.py}` | import 迁移为 `llmguard`，新增独立旧 namespace compatibility 测试 |
| `tests/stage5/**`、`tests/stage5_paper/**` 命中文件 | 受保护 Stage 5 回归；保持旧 import，精确白名单保留 |

## 3. 当前有效文档与导航

`README.md`、`README.zh-CN.md`、`PROJECT_MASTER_CONTEXT.md`、`docs/architecture/**`、
`docs/research/project_alignment.md`、当前 Stage 6 规格与实施计划、`stages/**` 将迁移为
LLMGuard 名称和规范 stage slug。名称首次出现使用 “LLMGuard Research Framework（简称
LLMGuard）”，并加入中英文第三方消歧说明。

## 4. 历史实验资产

以下命中均保留旧名称，不改写：`deliverables/stage1/**`、
`deliverables/stage1_learning/04_stage1_output_analysis.md`、`deliverables/stage2/**`，以及
`deliverables/learning_notes.md` 中 A1R 之前的记录。它们记录了实验发生时的命令、路径、
结果或 hash。

## 5. Git 路径、外部链接与清单

`docs/git/REPOSITORY_MAP.md`、`provenance/file_manifest.json`、
`provenance/historical_baseline.sha256` 记录旧路径或 hash，不在本轮改写；远端 URL 只在当前
README、identity 与 rename ledger 中记录建议迁移，不自动执行 GitHub 重命名。

## 6. 第三方名称、绝对路径与普通 guard

- 本次扫描未发现本项目以外的 `llm-guard` 代码或依赖；仅在新 identity 文档中加入中性消歧；
- 公开风险审计已有 116 个历史绝对路径候选，它们与本次项目名迁移解耦，不修改原始资产；
- `guard`、`guardrail`、`GuardEngine` 及输入/输出 guard 是安全领域术语，不是项目名称，保留。

## 已发现的事实差异

目标要求 `src/codeguarder/` 仅做兼容外观，但当前目录还包含受 Stage 1–5 保护的 Stage 5/
Stage 5 Paper 实现。A1R 的可逆解决方案是：只迁移允许的 Stage 6 Task 1–3，冻结并精确
登记 Stage 5 legacy，禁止任何新业务代码进入旧 namespace。直接清空或复制该目录都会违反
历史不可变或单一实现原则。
