# 上下文恢复与治理审计

日期2026-11-04 JST；input HEAD `8dec9453de2ebd5ea03e4cbdf753b2f0d7347177`。
项目长期目标LLMGuard RAG安全/可信检索，后续运行时与Agent安全保持；当前Paper1是中文自然事实污染开发研究，非正式测试。
Owner优先级为证据、公平对照、单核心机制和可复核失败，不以旧E1为新RAG成绩。

已读来源（均以input HEAD为身份，private包另核hash）：

- `AGENTS.md`：namespace、历史不可变、标签隔离、审批及文档收口；无适用的嵌套tracked AGENTS。
- `docs/governance/context_authority_map.md`、`project_owner_sovereignty_and_mandatory_escalation_principle.md`。
- 同目录`current_work_state.md`、`project_owner_decision_register.md`（最新相关PODR155–160）、
  `long_term_research_requirements.md`、`experiment_master_record.md`、`research_execution_log.md`、`dual_machine_execution_policy.md`。
- `PROJECT_MASTER_CONTEXT.md`；Paper1的`human/research_plan_authority.md`、`paper1_research_route.md`、`documentation_separation_contract.md`、Human/Agent Ledger。
- `core144/feasibility_sprint_01/FEASIBILITY_PROTOCOL_V1.md`及现有费用manifest；
  `core144/rag_defense_reconstruction_01/QUERY_LEVEL_PILOT_PROTOCOL.md`、RAGDEFENDER_REPRODUCTION_AUDIT、
  AI_DATA_PREPARATION_SCOPE_CLOSURE_V2、PRIVATE_EVIDENCE_INDEX、PAUSED_HANDOFF及恢复记录。
- D1签署资格补核：旧stage6研究树的`PAPER1_D1_FIRST_DETECTION_PROTOCOL_V1.md`，只读，不取人类原始表或复审内容。

实际Git：根`agent/stage1-5-sync`@20dad59b300fb774d49f2fbe3547c6e6d315c992，未跟踪文件保留；根无AGENTS。
最新研究树`research/paper1-rag-defense-reconstruction-01`@8dec9453… clean且origin同步，fetch和ff-only核对通过。
新分支`research/paper1-chinese-defense-5060`从该SHA创建，初始NO_UPSTREAM正常，首次push后核同步。
不使用根历史分支作为方法基线，不改`feature/stage6-rag`已接受基线，不合并其他分支代码。
5090指定远端分支fetch后未发现；不猜测其结果或权威SHA。GPU实际RTX5060，8151MiB，driver616.92，Python3.13.9。

文档与Git差异：较早恢复文件标暂停/WIP，后续PODR158–160和clean Git已覆盖；不据旧快照重复暂停。
旧B1=直接Qwen和本轮B1=RAGDefender有命名变化，显式映射；不把历史方法输出混用。
旧15美元/不得自动付费被本次Owner明确的条件式30美元授权覆盖；数据、账本、协议硬门仍保留。
没有科学合同被此授权替换为新方法接受。当前只完成P0工程审计，不升级正式方法或结果。

可改：新工作分支src/llmguard内独立模块、虚构测试、只读审计工具、脱敏文档及本分支治理镜像。
禁改：Stage1–5/历史结果、正式基线、GT、D2/D3、Reviewer/独立答案、其他工作树；不安装/下载/新增付费服务。
下一审批门：真实失败后B5唯一冻结；当前先闭合场景/迁移协议。正式实验NOT_STARTED。
可宣称：真实Git、代码存在、经hash验证的D1聚合与虚构工程检查；不能宣称RAGDefender中文失效、新方法收益、ASR或泛化。

FORWARD_RISK_REVIEW与PAPER_RISK_REVIEW见[公平性](baselines_and_fairness.md)。
主合同原件和编号02提示原件在核对的tracked树/指定根未见；当前消息是可用Owner指令，不伪造原件存在。
公共转录和hash随Git同步。之后收到原件才核实完整性与冲突。
