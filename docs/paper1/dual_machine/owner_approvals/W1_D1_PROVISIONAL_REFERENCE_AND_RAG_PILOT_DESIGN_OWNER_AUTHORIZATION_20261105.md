# Paper 1 | D1 Pilot12 暂定参考答案接受与最小 RAG Pilot 设计授权

- Owner Decision ID：`W1-OD-20261105-5060-PROVISIONAL-PILOTDESIGN-08`
- 日期：2026-11-05 JST
- 状态：`OWNER_EXPLICITLY_APPROVED / D1_PROVISIONAL_REFERENCE_ONLY / DESIGN_AND_BUDGET_ONLY`
- 授权来源：Owner 在本次 Paper 1 项目监督会话明确接受12题 AI 辅助暂定答案，仅用于 D1 可行性；明确允许准备最小端到端 RAG Pilot 的执行设计和预算审批包，**未批准任何新增模型/API调用、样本重选、D2/D3 或正式ASR评分**。
- 本分支：`research/paper1-chinese-defense-5060`，授权前远程HEAD：`60134dc7fcdd10d0ffbfee86ef732ce3d72e1c74`。
- 原来阶段：P2 36/36真实TopK5；Fast B B1/B2各36/36离线过滤；Fast C `PARTIAL_DIAGNOSTIC_UNRESOLVED`，保留Stage内部trace不足结论。
- 原始独立交接ZIP SHA-256：`2e289f68c8adee54187a4520d116182e20171a3dca3cd05daf3312a98a37f8c7`。
- AI辅助暂定答案参考文件（由监督会话提供，**不直接写入公开Git**）：
  - `PAPER1_PILOT12_AI_PROVISIONAL_REFERENCE_V1.md` SHA-256：`7b0c8303ccb9976648fbd02efdcf2c4cc2d1d8f470bdc92c7c36097f12107092`
  - `PAPER1_PILOT12_AI_PROVISIONAL_REFERENCE_V1.json` SHA-256：`5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31`
- 参考范围：12题、38事实原子、16来源快照、56引用定位，仅在各题给定时间/版本/条件内形成暂定答案；它们不等同2026年法律现行性完整核证，也不等于Human Gold或攻击目标。
- 5090仍执行自己的资源/许可核验，不受本决策影响。跨分支用本W1-OD+branch+完整Git SHA，避免两分支PODR-154同号。

## 1. Issue ID
`W1-OD-20261105-5060-PROVISIONAL-PILOTDESIGN-08`。

## 2. Issue name
Owner接受 D1 Pilot12 的AI辅助暂定事实参考，批准零推理的最小端到端RAG Pilot方案及成本门准备。

## 3. Discovery stage / task
Paper1/Week1/5060完成D1 P2、PAIR01及Fast C只读归因后，准备受限下一代查询级生成实验设计，但**不执行**。

## 4. Facts by evidence grade
- `OBSERVED_GIT`：旧P2、PAIR01及FastC封存与报告在本分支，含36世界、29候选hit@5和7miss、B1/B2过滤计数；该旧结果不能因本授权重新计算或覆盖。
- `USER_SUPPLIED_ARTIFACT`：监督端验证上述 AI provisional MD/JSON和原ZIP文件的存在/字节SHA；其12答案按上传的来源快照形成，非经独立人工审核的真值，也未在5060物理工作区证实存在。
- `OWNER_CONFIRMED`：Owner明确允许将它们用作D1可行性**参考答案**，许可仅限下阶段设计与预算，不包括实际生成和正式效果判分。
- `INFERENCE`：36个冻结世界采用一致模型、prompt、输入分组的B0/B1/B2三臂方案适合做首个低成本可行性Pilot；具体调用量、指标和价格应方案化但不能由本决定直接执行。
- `UNKNOWN`：5060是否已安全收到AI参考JSON字节、正式Human Gold、攻击目标/C3、实际生成模型可用性、账户余额/当前价格、可行性Pilot真正的QA/ASR及效果。

## 5. Affected constraints
AGENTS.md、PO-MHEP、D1/D2/D3隔离、GroundTruthVault/Evaluator独立、原P2/PAIR01/FASTC不可变、零新增调用/下载、模型/调用成本合同（USD30累计上限、USD25警戒、USD28禁开新付费批）、存储C盘禁新增受控数据/D/E可用、5090独立分支与论文Claim、实验公平性和证据封存。

## 6. Why now
正式双人Gold流程不是D1可行性Pilot规划的前提；将现有AI证据绑定为“暂定”可尽早编排最小生成实验和预算，避免在不必要的文档周期中推迟方向验证。

## 7. Downstream risks
AI辅助答案可能携带快照偏差或对历史适用范围的误读；对攻击目标与拒答目标没有独立审定；开发阶段曾查看B1/B2而非真正独立盲审；将答案放入运行时导致标签泄露；样本量12个事实组、36关联世界；B2 Clean误删较B1增加，安全门已经发出警示；无预先价格或实际Token预算就启动付费；自动调用、意外下载或把“Provisional Consistency”说成正式Accuracy/targeted ASR；公开Git泄露查询-参考答案映射。

## 8. Options with consequences
A【OWNER ACCEPTED】：仅允许计算/审计所需的离线设计、预算、指标与准入说明。优点：最短时间得到可直接再批的端到端方案、此次无新增API费用；风险：后续需重新显式准入，参考答案可能需要修改；可逆、不修改科学资产。
B【NOT SELECTED】：先完成完全独立人工Gold后才开始方案设计。科学边界更强，但阻碍D1快速可行性判断；后续可再做。
C【NOT APPROVED】：直接调用Qwen/LLM、以AI参考答案当GT，或生成正式targeted ASR。或许更快产数字，但越权且科研结论不成立。

## 9. LOCAL recommendation
执行A，先形成一份可审核的**全12组/36世界固定三臂(B0,B1,B2)**最小设计（推荐待审108次生成请求上限，不是本轮许可），采用原始P2 TopK和PAIR01过滤后的冻结上下文，不重建检索也不自适应选例。可将B3/B4列为未来备选但不能默认加入108请求。只提供出价计算和候选命令文本，不能做API连通性探测。

## 10. Rationale and confidence
Owner的当前授权高确定性；已核文件SHA仅表明提交材料字节，不代表独立Gold；旧过滤与检索事实有可查来源；端到端生成收益、实际模型可用性和真实成本均未知。最低统计粒度为12事实组，任一类别单个案例对应8.33个百分点，原2.5pp安全阈值不能在小样本下被“证明满足”，所有结果只能作为风险信号。

## 11. Explicit Owner decisions / next choices
**已允许**：
1. 接受以上固定SHA的12题AI辅助暂定参考答案仅作为D1开发可行性**下游评分参考候选**，标 `AI_ASSISTED_PROVISIONAL_REFERENCE_NOT_HUMAN_GOLD`、`HumanGold=0`、`attack_target=UNKNOWN`、`C3=NOT_ADJUDICATED`。不得将暂定参考映射回 Guard/Generator/检索执行输入；仅用于未来后封存的独立开发评分。
2. 在5060原分支零调用、零模型加载、零数据下载的前提下，设计固定36世界的生成输入编排、统一prompt/config、B0/B1/B2配对、answer scope一致性/拒答与条件分母统计、失败保持和seal-first独立评价、token/价格/延迟/剩余额度核算方法及最小运行硬门。
3. 只对已批准且在D/E合法获得的源和输出做只读元数据核验；若本机未获得参考JSON，写成`AWAITING_PRIVATE_ARTIFACT_TRANSFER`，可完成不依赖答案字节的方案设计，但**不得通过Git公开答案、web搜索或自行生成替代数据**；由Owner单独在D/E提供SHA匹配的MD/JSON后再闭合映射。新脚本仅允许不调用科学路径的静态验证或数据格式测试，不访问D2/D3。
4. 仅将脱敏方案与hash清单/Git治理文件提交5060原分支；完整12题答案、私有审阅包及任何角色映射均不进入公开Git。

**未批准**：任何真实或免费API试探、Qwen或其他生成/校验模型的真实调用、embedding/Guard/检索再执行、B1/B2重跑、B3/B4支付Pilot、B5/B6新方法、D1-40/新增样本与重选、D2/D3/Reviewer/GT Vault、预设targeted ASR或正式Answer Accuracy、正式GT导入、5090 Claim、外部网络或下载、主线/跨分支合并；不得覆盖旧证据。

下一Owner Gate：按明确最小候选实验格数与Token上下界、最新账户价格与余额、模型/上下文输入哈希、统一配置、生成/后封存评分边界、预算与停止阈值重新单独批准；本次**绝不自动进入执行**。

## 12. Allowed/prohibited until next decision
允许有限静态方案、预算预测、旧冻结元数据只读核验、脱敏治理和仅本分支commit/push；禁止模型/API/付费、语义代码变更及数据/标签越权。遇到预算不闭合、真实参考字节不可用、公式/参数冲突或样本范围改变：标`DESIGN_GATE_BLOCKED`，保存PO-MHEP风险清单；不以设计阶段未知变量阻挡其他可写部分。

## Delivery & STOP
`docs/paper1/dual_machine/chinese5060/W1_5060_MINIMAL_RAG_PILOT_DESIGN_AND_BUDGET.md`、`docs/paper1/dual_machine/chinese5060/pilot_design/PILOT_EXECUTION_PROPOSAL.json`、`PROVISIONAL_REFERENCE_SHA_HANDOFF.json`、`BUDGET_AND_STOP_GATES.md`、`PILOT_EVALUATION_BOUNDARY.md`、`DESIGN_QA.json`、剩余需Owner确认的最简审批包。所有报告写明`DESIGN_ONLY_NOT_RUN`、新增模型/API调用0、HumanGold0、targetedASR/正式Accuracy NOT_MEASURED。保留Agent/Human ledger、current state、execution log和历史记录，合法Git commit/push后STOP。
