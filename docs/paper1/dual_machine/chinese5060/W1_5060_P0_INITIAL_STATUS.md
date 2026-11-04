# W1_5060_P0_INITIAL_STATUS

2026-11-04 JST；任务 PAPER1-W1-5060-P0。本页首先保存初始状态，执行后另加有SHA绑定的验证记录。
状态：P0_IN_PROGRESS；付费Pilot与D1-40均NOT_RUN。

1. **Git与治理**：独立工作目录为仓库内`.worktrees/paper1-chinese-defense-5060`；origin为
   `https://github.com/tingfengy2000-creator/llm-security-evaluation-framework.git`；分支
   `research/paper1-chinese-defense-5060`；初始完整HEAD/开发基线均为
   `8dec9453de2ebd5ea03e4cbdf753b2f0d7347177`。根原工作区与历史研究工作树保留。
   适用`AGENTS.md`及`docs/governance/project_owner_decision_register.md`已读；仓库最新PODR-160，
   本次Owner明确指令另登记。缺失的总合同不伪造为存在；[授权收据](owner_instruction_receipt.md)为转录。
2. **D1授权**：已签署开发包private_input_v2；manifest SHA256
   `a7e05d2ebedbc68abc21fff46a0ad1597747712020957ac30cf1445353714a60`；F5 SHA256
   `c849260e2a41fa9186e6d69ed6442cbebdaa7ff272beece9dfadc22e61cf535c`。
   既有合同为40组120条13家族，Poison的S1/S2/S3=12/15/13；8组24条HOLD排除。
   本次独立计数/hash审计待运行。D2/D3/Reviewer内容未读取、不索引、不进API；GT不改。
3. **工程资产**：Chroma1.5.9/ST5.6.0真实依赖可用；现有ChromaVectorStore、ST provider、DenseRetriever可静态复用。
   旧Top5来自Candidate驱动查询，不能移作新query的召回成绩；新真实查询索引未建。论文embedding、中文chunk/token预算尚未冻结。
   新增21项隔离/快照/预算单测已通过；Ruff通过；首次MyPy仅sklearn缺类型声明，修正后待正式留档检查。
4. **Pilot12**：沿用旧结果无关选择：按SHA256(TASK|20261104|S|group)每S升序前4组；seed20261104；
   既有记录12组36条9家族。选择hash
   `2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`，待独立复核。
   全语料lineage查混世界、独立索引目录、冻结TopK hash、重开索引查排名；不只检查TopK。
5. **基线/协议**：B0仅上下文接口；B1/B2/B3/B4真实查询实验NOT_RUN；B5/B6尚未提出。
   T0/T1/T2分层，同证据强Qwen对照必需；真实生成器精确qwen3.7-plus-2026-05-26。
   真实TopK、证据快照、prompt/sampling/token budget/评分合同未闭合，尚无真实实验Run Manifest。
6. **Qwen/费用**：精确模型有旧北京调用记录，当前可用性未重新核验。旧累计361calls、输入2,984,761/
   输出205,288tokens；usage估算CNY7.611826；旧单价输入2/输出8 CNY每百万，不冒充现价。
   Owner当前报费用CNY7.528095914、无未结算、可继续使用；具体余额及费用差额原因UNKNOWN。
   本任务新增0calls/0费用。累计USD30/25预警/28停止新批，旧费用保守保留，不因新run清零。
7. **当前执行**：新真实smoke/Pilot尚未运行；D1查询效能有效分母0，ASR/Answer Accuracy为NOT_MEASURED。
   旧E1的37/40是候选核验，不能冒充RAG结果。后续仅运行虚构Chroma工程smoke和只读D1身份审计，保存命令/退出码/输出hash。
8. **下一门**：可继续零费用非语义工程、数据/协议审计与Git记录；真实Pilot需场景/迁移/信息权限/费用门闭合。
   未确认新方法收益，B5首次冻结须Owner批准；D1-40不具备冻结或启动条件。当前NOT_READY不代表方法已被实测否定。

详见[数据清单](authorized_data_manifest.md)、[场景](scenario_protocol.md)、[公平性](baselines_and_fairness.md)、[费用](cost_ledger_summary.md)。
