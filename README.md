# CodeGuarder LLM Security Lab

Research-grade LLM security evaluation project covering garak scanning,
OpenAI-compatible APIs, real-model A/B guard experiments, ablation studies and
the Stage 5 Paper cross-layer attack matrix.

中文学习入口：[README.zh-CN.md](README.zh-CN.md)  
面试复习入口：[interview_prep/README.md](interview_prep/README.md)

## Repository Map

- `src/`: evaluation framework code
- `tests/`: TDD and regression tests
- `data/`: synthetic attack and benign datasets
- `scripts/`: reproducible entry points
- `deliverables/`: sanitized reports and experiment logs
- `experiments/registry.json`: experiment registry
- `provenance/`: SHA-256 manifests and correction ledger

No real destructive tools are connected or executed. Secrets, environments,
runtime caches and full sensitive model outputs are excluded from Git.
