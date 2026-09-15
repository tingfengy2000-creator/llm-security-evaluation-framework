# LLMGuard Research Framework

LLMGuard Research Framework is a research-grade project for reproducible LLM,
RAG, and agent security evaluation. It covers garak scanning, OpenAI-compatible
APIs, real-model A/B guard experiments, ablation studies, the Stage 5 runtime
attack matrix, and the Retrieval Security research baseline.

LLMGuard Research Framework is an independent research and evaluation project.
It is not affiliated with or derived from Protect AI's llm-guard project.

中文学习入口：[README.zh-CN.md](README.zh-CN.md)  
面试复习入口：[interview_prep/README.md](interview_prep/README.md)
项目总控：[PROJECT_MASTER_CONTEXT.md](PROJECT_MASTER_CONTEXT.md)

Paper 1 当前门：Final72 GT 已正式接受为 development/method-engineering set；42 项五视角 signal 已在无标签输入上提取并
锁定 3,024 条 raw records，之后才加载分析标签。当前为 `READY_WITH_VIEW_LIMITATIONS`：S/E/P/T 可用于后续工程，
Retrieval 因缺少冻结 query/retrieval trace 暂不可用。尚未训练 Detector、选择阈值、冻结正式 Dataset 或执行 Formal
Experiment。详见
[Paper 1 Start Here](docs/research/stage6_1_hidden_knowledge_poisoning/README.md)。

## Repository Map

- `src/llmguard/`: canonical evaluation framework code
- `src/codeguarder/`: legacy namespace and protected historical Stage 5 code
- `tests/`: TDD and regression tests
- `data/`: synthetic attack and benign datasets
- `scripts/`: reproducible entry points
- `deliverables/`: sanitized reports and experiment logs
- `experiments/registry.json`: experiment registry
- `provenance/`: SHA-256 manifests and correction ledger

No real destructive tools are connected or executed. Secrets, environments,
runtime caches and full sensitive model outputs are excluded from Git.
