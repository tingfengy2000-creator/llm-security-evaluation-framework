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
