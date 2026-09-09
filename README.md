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

Paper 1 当前门：Owner 已接受 Pilot4 标注协议并批准两个真人 A/B 执行；A/B 已独立完成 Phase1，两份原始 CSV 已按字节
锁定且双 Phase1 gate 通过。两套人类可用 Phase2 V3 工作簿已就绪，等待 Owner 分别发放；mapping/Expected、agreement、
Ground Truth、Dataset freeze、Detector、Training 与 Formal Experiment 均未启动。详见
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
