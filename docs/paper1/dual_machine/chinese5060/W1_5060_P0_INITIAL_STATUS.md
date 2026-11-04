# W1_5060_P0_INITIAL_STATUS

2026-11-04 JST；任务 PAPER1-W1-5060-P0。状态：P0_ENGINEERING_PASS / REAL_PILOT_NOT_READY。
本次验证更新覆盖初稿的“待运行”，初稿保留在ca75c38提交；未改写历史实验。

1. **Git与治理**：独立工作目录为仓库内`.worktrees/paper1-chinese-defense-5060`；origin为
   `https://github.com/tingfengy2000-creator/llm-security-evaluation-framework.git`；分支
   `research/paper1-chinese-defense-5060`；初始开发基线为
   `8dec9453de2ebd5ea03e4cbdf753b2f0d7347177`；实际执行/报告组装HEAD为
   `ca75c381546247ad3377013a75bb21133cc078ed`（已推送）。最终交付commit由最终Git检查和回复提供，
   不在文件内制造自引用SHA。公开报告目录脱敏；本机绝对目录在交付回复提供。根原工作区与历史研究树保留。
   适用`AGENTS.md`及`docs/governance/project_owner_decision_register.md`已读；仓库最新PODR-160，
   本次Owner明确指令另登记。缺失的总合同不伪造为存在；[授权收据](owner_instruction_receipt.md)为转录。
2. **D1授权**：已签署开发包private_input_v2；manifest SHA256
   `a7e05d2ebedbc68abc21fff46a0ad1597747712020957ac30cf1445353714a60`；F5 SHA256
   `c849260e2a41fa9186e6d69ed6442cbebdaa7ff272beece9dfadc22e61cf535c`。
   既有合同为40组120条13家族，Poison的S1/S2/S3=12/15/13；8组24条HOLD排除。
   本次独立hash/计数与Pilot选择复核通过；签署原件/HOLD本体未重开，只核开发包与既有授权链。
   D2/D3/Reviewer内容未读取、不索引、不进API；启动文件名发现曾显露受限路径名，随后停止全树发现并改固定白名单。
   不宣称全程零路径触达或OS强制沙箱；[隔离范围修正记录](isolation_incident.md)保留；GT不改。
3. **工程资产**：Chroma1.5.9/ST5.6.0真实依赖可用；现有ChromaVectorStore、ST provider、DenseRetriever可静态复用。
   旧Top5来自Candidate驱动查询，不能移作新query的召回成绩；新真实查询索引未建。论文embedding、中文chunk/token预算尚未冻结。
   新增21项隔离/快照/预算单测、Ruff、MyPy（7源码）均在记录run通过。新smoke只用虚构字符bigram向量，
   没有新跑ST embedding或原论文复现；旧19项与作者测试仅继承记录，未复跑。
4. **Pilot12**：沿用旧结果无关选择：按SHA256(TASK|20261104|S|group)每S升序前4组；seed20261104；
   既有记录12组36条9家族。选择hash
   `2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`，本次已独立复核一致。
   全语料lineage查混世界、独立索引目录、冻结TopK hash、重开索引查排名；不只检查TopK。
5. **基线/协议**：B0仅上下文接口；B1/B2/B3/B4真实查询实验NOT_RUN；B5/B6尚未提出。
   T0/T1/T2分层，同证据强Qwen对照必需；真实生成器精确qwen3.7-plus-2026-05-26。
   真实TopK、证据快照、prompt/sampling/token budget/评分合同未闭合。工程smoke固定TopK3、
   每世界6文档、独立索引、T0、B0上下文重放；配置由执行前固定源码确定，事后生成证据Manifest，非预注册科研协议。
6. **Qwen/费用**：精确模型有旧北京调用记录，当前可用性未重新核验。旧累计361calls、输入2,984,761/
   输出205,288tokens；usage估算CNY7.611826；旧单价输入2/输出8 CNY每百万，不冒充现价。
   Owner当前报费用CNY7.528095914、无未结算、可继续使用；具体余额及费用差额原因UNKNOWN。
   本任务新增0calls/0费用。累计USD30/25预警/28停止新批；较高usage按旧6CNY/USD保守界占用约USD1.268638，
   不是现汇/最终账单或已核可花余额。现价/费用差额/精确余额未核，付费停止；不再索要已确认的预算授权。
7. **实际执行**：run_id=`W1-5060-20261104-P0-01`，源码ca75c38；5项检查全部exit0：21tests、Ruff、
   MyPy、D1身份审计、虚构Chroma smoke。3/3世界独立建库，每库6文档、TopK3，关闭重开后顺序一致；
   3/3快照和B0重放通过，9个retrieval hits仅工程计数。实际环境Python3.12.14（宿主Python3.13.9）。
   生成器/真实Pilot未运行，D1查询效能有效分母0，ASR/Answer Accuracy=NOT_MEASURED。
   旧E1 37/40不能冒充RAG。已证缺口：旧F5 120/120无独立query/答案裁决；新V2草案不在该断言范围。
   初次MyPy缺sklearn声明已作非语义修复；初次新测试EOF空行已修复；原工具观察和最终raw日志边界见失败记录。
8. **下一门**：可继续零费用非语义工程、数据/协议审计与Git记录；真实Pilot需场景/迁移/信息权限/费用门闭合。
   未确认新方法收益，B5首次冻结须Owner批准；D1-40不具备冻结或启动条件。当前NOT_READY不代表方法已被实测否定。

SHA256（完整公共索引见[evidence](evidence/RUN_MANIFEST.json)；raw命令/响应、Chroma文件和zip留Git外）：

| 项目 | SHA256 |
|---|---|
| 工程配置 | `e9fe008cf77950b6e051c1da595c3fa4a44a6b4accf523092e3557922efd0a07` |
| Run Manifest | `96b792e857e86efd7b7311cdbc65bde7b30cffae98aa30389652519612f537b5` |
| D1身份审计输出 | `f86770cdbe5d2b99babdc3d2563664c374042c158fefa475cbaed81aaf6ff76f` |
| smoke输出 | `54146ef9df6211e9fd174e518089bc775e9152d209fe73dc7a2a0019b843f99a` |
| 验证命令输出索引 | `814ac7f5d13a0b82770a9a83b521234401599744d65c68eaecaf8dd8f160115e` |
| 最终私有证据索引 | `0332e0dc60177e754a28afada9a32048cdf9fa6de33faccc643dd0c10ad14f3d` |
| 私有归档 | `6a19d88de44fea033b62956fb0ee51683cf422c16b72fcd577d51ba12cf47c90` |

三个TopK快照分别为`2f561769dbd68e5d566b17f57dc5ee9aaf88377348a29cc4dc2d73324b0663e8`、
`739329ef3593fb63add0971963b8a8ef3871d64f15df6d6168332dc93a12a056`、
`146bbef0c2fa172dd2e5dc7b9478faae3a4b60348ec95f9f93c102cab2a9d426`。
hash证明绑定与变更检测，不替代来源真实性、语义正确性或跨机器重建一致性。
smoke输出中的unknown-billing为负向准入fixture，并非覆盖Owner同会话可用声明。

详见[数据](authorized_data_manifest.md)、[场景](scenario_protocol.md)、[公平性](baselines_and_fairness.md)、
[费用](cost_ledger_summary.md)、[失败/阻断](evidence/failures_and_blockers.json)、[下一门](gates_and_decisions.md)。

内容交付commit `d70454f31d7ab9b438390a1b47971533c5bf5161` 已核远端一致、clean、ahead/behind=0/0；
最终证明提交仅补Git验收记录，见[evidence/GIT_DELIVERY_VERIFICATION.json](evidence/GIT_DELIVERY_VERIFICATION.json)。
