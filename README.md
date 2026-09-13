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

Paper 1 当前门：A/B 的 Phase1 与 Phase2 四份 raw 已全部按字节锁定，裁决前复现性已经重新冻结；Expected V3 未加载。
中文 Owner 工作簿已准备，要求先处理五个 late-candidate-defect flags，再处理 78 个 material field disagreements；所有
Owner 决定均为空并等待人工填写。Ground Truth、
Dataset freeze、Detector、Training 与 Formal Experiment 均未启动。详见
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
