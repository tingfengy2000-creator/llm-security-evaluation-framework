# LLMGuard 命名规范

生效任务：`A1R`。本规范约束 A1R 之后的新文件、新模块、新配置、新实验和新文档；历史证据
由 `project_rename_ledger.md` 与精确白名单保护，不做回写。

## Namespace 与目录

```text
src/llmguard/                 # 唯一规范实现
src/codeguarder/              # 旧 namespace 兼容及冻结 legacy 例外
```

新业务代码只能进入 `src/llmguard/`。`src/codeguarder/stage6_rag/` 只允许 re-export；
Stage 5/Stage 5 Paper 位于 `src/codeguarder/` 的受保护历史实现是当前过渡例外，不能移动、
覆盖、复制或新增业务逻辑。

新目录、Python 文件、YAML、JSON、JSONL 均使用 `lowercase_snake_case`。Python 类使用
`PascalCase`，函数和变量使用 `lowercase_snake_case`，常量使用 `UPPER_SNAKE_CASE`。不使用
空格、中文、连字符、连续下划线、末尾下划线或大小写混排目录。

## 阶段名称

| stage_id | canonical_name | canonical_slug |
| --- | --- | --- |
| S1 | Garak Security Scan Baseline | `stage1_garak_baseline` |
| S2 | OpenAI-Compatible Mock API | `stage2_openai_mock_api` |
| S3 | Real Model Security Scan | `stage3_real_model_scan` |
| S4 | Guard Proxy A/B Evaluation | `stage4_guard_ab` |
| S4.1 | Guard Ablation Evaluation | `stage4_1_guard_ablation` |
| S5 | Runtime Attack Matrix and Failure Taxonomy | `stage5_runtime_attack_matrix` |
| S5P | Deterministic Runtime Evaluation Baseline | `stage5_paper_baseline` |
| S6 | RAG Security Evaluation | `stage6_rag_security` |
| S6.1 | Hidden Knowledge Poisoning Detection | `stage6_1_hidden_knowledge_poisoning` |
| S6.2 | Multi-Evidence Trustworthy Retrieval | `stage6_2_trustworthy_retrieval` |
| S7 | Agent Security Evaluation | `stage7_agent_security` |

阶段目录与文件名不使用小数点；小版本写作 `stage4_1`、`stage6_1`、`stage6_2`。新实验 ID 使用
`s6_e0_engineering` 至 `s6_e5_groq_smoke`；新 run ID 使用
`<stage>_<experiment>_<UTC timestamp>_<short commit>`。

## 文件与脚本

- 顺序型 Markdown：`00_overview.md`、`01_architecture.md`；
- 新 ADR：`0006_namespace_migration.md` 这一种下划线格式；旧连字符 ADR 是历史命名，不重写；
- PowerShell：`verb_noun_context.ps1`；
- 测试：`test_<subject>.py`；
- 数据：新 dataset version 使用 `lowercase_snake_case.jsonl`。

普通安全术语 `guard`、`guardrail`、`GuardEngine`、`input_guard`、`output_guard` 不是项目名称，
不得因为本次迁移被替换为 `llmguard`。名称校验只检查完整项目标识、namespace、distribution
和规范 stage slug。

## 自动校验

`tests/architecture/` 校验 namespace compatibility、依赖方向、单一规范实现和新增目录/文件
命名。历史例外只能出现在 `config/naming_legacy_allowlist.yaml` 的精确路径中。
