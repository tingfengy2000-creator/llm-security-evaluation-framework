# 5060 中文RAG工作线

当前工作 W1-5060-FAST-UNBLOCK-20261105-01。V2 冻结及离线验收完成，真实准入仍阻断，0 调用。 [唯一审批入口](fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md)。下方为历史导航。


当前工作 W1-5060-PILOTLIVE-20261105-01。真实准入受阻，POST 0，108格未运行。 [准入、证据与后续门](W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_REPORT.md)。以下为历史导航。


当前工作 W1-5060-RUNNER-20261105-01。108格离线运行器验收完成，真实API 0，真实Pilot NOT_RUN。 [报告和下一审批门](W1_5060_PILOT_RUNNER_IMPLEMENTATION_AND_ADMISSION_REPORT.md)。下方均为历史导航。


当前：最小RAG Pilot仅设计/预算完成，108格全部NOT_RUN，参考JSON已核、未进入Generator。[候选方案和下一门](W1_5060_MINIMAL_RAG_PILOT_DESIGN_AND_BUDGET.md)；以下为历史。


当前Fast C：只读归因统计/独立盲审交接已完成，根因仍PARTIAL_DIAGNOSTIC_UNRESOLVED。[报告](W1_5060_FAST_C_READONLY_FAILURE_ATTRIBUTION_REPORT.md)，本轮不重跑模型；下方历史。


当前Fast B实际完成：B1/B2各36世界离线过滤及独立计数。见[Pair01实测](W1_5060_FAST_B_PAIR01_RESULT.md)，ASR/QA未测；以下为历史导航。


当前Fast B：合同已修复，唯一HF直连请求超时，模型/B1/B2未执行。见[恢复01结果](W1_5060_FAST_B_RECOVERY01_RESULT.md)；以下旧当前均为历史快照。


当前Fast-Track B：准入审计及12题独立待审包已保存；因最终Prompt缺失，下载/B1/B2未运行，整体未完成。
见[Fast B状态与下一门](W1_5060_FAST_B_B1_B2_OFFLINE_RESULT.md)；以下P2/P1/P0均为历史导航。



当前：Fast-Track A零API T0/B0已完成，36世界TopK与重放均成功；B1/B2因默认模型身份前置未闭合BLOCKED。
先读[P2真实检索诊断](W1_5060_P2_T0_RETRIEVAL_DIAGNOSTIC.md)及[56测试/命令摘要](p2/evidence/COMMAND_SUMMARY_PUBLIC.json)。
后续P1/P0为历史导航；本轮无生成、ASR/QA未测，交付后STOP不进P3。


当前：P1零付费准备与双机治理同步完成，真实Pilot仍BLOCKED。先读
[Owner治理与P1准入](W1_5060_OWNER_GOVERNANCE_AND_P1_GATE.md)及
[12题场景/公平性矩阵](W1_5060_P1_SCENARIO_AND_FAIRNESS_GATE.md)。
固定候选参数见[p1机器合同](p1/P1_PROTOCOL_CANDIDATE.json)，不是运行批准。
本轮未建真实索引、未生成TopK、未调用Qwen；完成Git交付后停止。

以下保留P0导航；其中场景/成本/交接状态是P0快照，后续状态以上述P1报告为准。

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
