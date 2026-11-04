# 5060 中文RAG工作线：P0交付

先读[初始状态与实际验证报告](W1_5060_P0_INITIAL_STATUS.md)。当前只完成P0与虚构基础工程检查；
真实Pilot12、D1-40与B5/B6效果均未运行，不宣称方法成功或RAGDefender中文失效。

- [治理与Git审计](governance_audit.md)、[Owner授权收据](owner_instruction_receipt.md)
- [授权数据](authorized_data_manifest.md)、[场景协议](scenario_protocol.md)、[基线公平性](baselines_and_fairness.md)
- [Pilot12](pilot12.md)、[D1-40/消融NOT_RUN](d1_40_and_ablation.md)、[累计成本](cost_ledger_summary.md)
- [5090脱敏交接](handoff_5090.md)、[后续门与决策](gates_and_decisions.md)

新代码仅`src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/`，与既有正式方法分离。
重放验证工具是`scripts/research/validate_chinese5060.py`：在已装pytest/Ruff/MyPy/Chroma/sklearn的隔离环境中运行，
需要显式给出已签D1 bundle和既有selection路径；只认固定hash，禁止自动找数据。
每次使用新run-id；输出在Git外`experiments/paper1_chinese5060/`，不覆盖旧run。
当前脚本不提供API调用，不下载embedding、不读Oracle或Reviewer；公开结果只保留聚合/hash。
`evidence/`的JSON是新生成脱敏证据的逐字节副本；目录属性禁止换行归一化，确保Git与本地SHA一致，不改任何历史hash。
