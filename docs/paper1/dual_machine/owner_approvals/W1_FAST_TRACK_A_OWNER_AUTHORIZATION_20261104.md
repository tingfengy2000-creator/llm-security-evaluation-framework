# Paper 1｜Week 1 加速方案 A — Owner 明确执行授权

- 日期：2026-11-04 JST
- 唯一跨分支授权 ID：`W1-OD-20261104-FAST-A-03`
- 状态：`OWNER_EXPLICITLY_APPROVED / BOUNDED_ZERO_PAID_API_EXECUTION`
- 授权来源：Owner 在本次 ChatGPT 项目监督会话中针对《PAPER1_W1_FAST_TRACK_OWNER_APPROVAL_PROPOSAL.md》明确批准；此文件为脱敏授权转录，不假称包含原始聊天消息字节。
- 原候选提案 SHA-256：`90cbc72d673b0d03f0bddc0c2758cad31d554e409141c3726215c9966207cf8c`（本次批准使提案 A 的限定范围生效；原提案仍保留为历史 PROPOSED 文本，不覆盖）。
- 5060 基线（登记前远程）：`research/paper1-chinese-defense-5060@14fb943d39df0e0286a5b52fc733ec509dc85ed3`
- 5090 基线（登记前远程）：`research/paper1-ragdefender-repro-5090@01554702b0bc14b7203712c83423d8245eacb3d3`
- 两分支保持独立；未授权 merge、rebase、reset、cherry-pick 或向 main 合并。
- 不借用冲突编号 `PODR-154` 作跨分支批准身份证明；引用本 W1-OD ID、分支、完整提交 SHA。正式分支内治理编号须动态核对。

## 1. Issue ID
`W1-OD-20261104-FAST-A-03`。

## 2. Issue name
有界加速：5060 D1 Pilot12 的零付费本地 T0 真实检索与 B0/B1/B2 条件式离线诊断；5090 既有兼容环境的纯离线无权重 Smoke。

## 3. Discovery stage/task
Paper 1 / Week 1；5060 P1 准备完成但真实索引、TopK 未运行；5090 环境兼容已核查但 Claim1–3 未运行。

## 4. Facts by evidence grade
- OBSERVED_FACT（远程 Git）：5060 远程 HEAD 为 `14fb943d39df0e0286a5b52fc733ec509dc85ed3`，5090 远程 HEAD 为 `01554702b0bc14b7203712c83423d8245eacb3d3`，仅说明审批前的 Git 快照。
- SOURCE_DERIVED_FACT：5060 P1 报告记录 Pilot12 选择 hash `2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`；36 互斥世界仅设计、索引 0、TopK 0；5090 三 Claim 为 NOT_RUN；兼容环境 CUDA 基本检查通过。
- OWNER_CONFIRMED：Owner 明确批准本文件所述加速方案 A，仅此有限范围。
- INFERENCE：优先获取真实 TopK 和离线过滤行为有利于尽早定位检索与中文迁移失效，但尚无新科研结果。
- UNKNOWN：真实 TopK、B1 原始 embedding revision/缓存、每题攻击目标与答案裁决、完整论文复现数值及 API 账单余量。

## 5. Existing constraints
`AGENTS.md`、`context_authority_map.md`、PO-MHEP、双机冻结合同、D1/D2/D3 隔离、Ground Truth Vault 只向 Evaluator 开放、原始 Stage1–5 不可变、强基线公平性、证据哈希/Run Manifest、审批与文档收口。

## 6. Why decision is required now
避免因等待全套模型权重、论文 Claim 及正式人工 GT 而阻塞已经具备的本地检索工程诊断；但不允许以速度替代许可、标注、公平性和付费准入。

## 7. Downstream risks
工程：索引串世界、缓存自动下载、tokenizer/embedding 漂移；科研：检索缺失被错算防御成功、将公开库当论文 artifact、D1 暴露数据及强基线不公平；费用/法律：未经授权 API、模型或 BEIR 下载；复现：无原命令/参数/哈希；安全：D2/D3、Reviewer、密钥、GT 或私有内容泄漏。所有此类异常按 PO-MHEP 停止受影响任务。

## 8. Options and decision
- A【OWNER ACCEPTED】：两机在各自原分支并行开展下述零付费、零新模型/数据下载的限定工作。优点：最快取得真实检索/算法工程证据；成本：无新增商业 API，使用既有本地计算，需保存日志与私有归档；风险：尚不是查询级 ASR/QA；可逆，不修改已冻结历史。
- B【NOT SELECTED】：等待所有权重/数据、正式 GT 及全套 Claims 后再启动本地检索；优点：减少阶段交错；缺点：时间损失显著；资源与论文收益无法保证；可逆。
- C【PROHIBITED IN THIS ROUND】：绕过数据/来源/许可/评分或预算门，直接付费或下载运行；短期可能产生数字，但结论混杂、成本和合规风险高，可能损害后续科研有效性。

## 9. LOCAL recommendation
采用 A，分离 5060 真实 T0 检索/过滤开发诊断与 5090 无权重 Smoke；只对符合前置核验的子任务继续，失配子任务局部停止；不得自行升级为付费或新方法实验。

## 10. Rationale and confidence
Owner 授权范围：高置信（明确文字）；先前 Git 快照：高置信（远程接口）；后续实验效果：未知。零付费工程通过不代表安全有效、论文 Claim 复现或统计显著性。

## 11. Owner's explicit decisions / remaining questions
**本次明确批准：**
1. 5060：仅在已固定 D1 Pilot12 / 36 互斥世界，复用已审 P1 候选协议，使用本地已存在、身份可核的依赖和模型缓存，运行不下载、不付费的 T0（无独立可信证据）真实检索索引、TopK5 冻结、可重放检查与 B0 离线直通。
2. 5060：**有条件批准** B1 为原样 RAGDefender v0.2 公开库轨道，不能当作者论文 `artifacts/` 或严格论文复现；B2 只能在 B1 同一框架上替换中文 embedding。运行前必须冻结 B1 库源码 SHA、实际默认 embedding 的精确 model revision、缓存来源、tokenizer/依赖、参数/预算及与 B2 的唯一变量；任何缺失，B1/B2 停止，不用替代物顶替。允许离线过滤开发指标，保留分母和 retrieval-miss 归因。
3. 5060：可形成 12 张待 Owner/独立裁决的答案、时间范围、条件、攻击目标和 C3 边界卡；不得由开发 Agent 自批为 Human Gold，也不得用 AI 草案算 targeted ASR 或 Answer Accuracy。
4. 5090：只在已存在的 `artifact_acsac_compat` 使用提前静态检查、确认不会触发模型/语料加载、自动下载或网络调用的本地单测与虚构样本算法 Smoke；原 `artifact_acsac` CUDA 失败证据不改；不运行 Claim1–3。
5. 两机：各自保留现有远程分支与起点，在完成 Git 动态 preflight、治理登记、脱敏日志、Run Manifest、归档哈希和文档收口后，仅向各自分支提交推送，随后停止。允许为正常 Git 审计/交接而执行的已授权 Git fetch/push；测试和运行时严禁外部联网。

**仍未批准（需要新 Owner Decision）：** 任何商业 API/付费探测、B3/B4 付费 Pilot、模型权重/BEIR/新 embedding/依赖下载、5090 Claim1–3、B5/B6、D1-40、D2/D3 或 Reviewer、T1 独立官方证据授信、T2、C3 实际评价或新裁决规则、正式 GT、正式论文数值复现声明、重大算法/协议语义改变、主线/跨机合并。

## 12. Work allowed and prohibited until the next gate
**Allowed**：上面明确范围的离线本地检索、B0 与符合全部缓存/源码/参数条件的 B1/B2 开发诊断；5090 静态审计后选定的纯本地 Smoke；独立评价侧的 D1 开发过滤计数；12 张待审卡、证据/治理/私有归档、各自分支 commit/push。
**Prohibited**：一切第 11 节未批准事项；越权读 D2/D3/GT、自动联网/下载、将新工程 Smoke 升格成 ASR/QA 或 Artifact Claim；因某个子任务阻断而静默换模/改样本/改阈值/忽略失败。

## Completion and next gate
- 5060 交付 `W1_5060_P2_T0_RETRIEVAL_DIAGNOSTIC.md`，包括 36 世界 TopK 哈希（或明确未成功的分母）、retrieval coverage/candidate hit@5、rank/score、B0/B1/B2 实际有效条件及有条件的 Poison Recall/Clean-FPR/HN-FPR、失败与零新增 API、私有 raw/index SHA。若真实索引因缓存缺失不能运行，必须报 BLOCKED 而不是虚构进度。
- 5090 交付 `W1_5090_OFFLINE_SMOKE_AND_RESOURCE_GATE.md`，包括静态无联网检查、实际测试命令/退出码、分层声明、兼容差异及 Claim1–3 仍未运行；私有 raw SHA 与新资源审批清单。
- 两机完成各自治理与脱敏 Git closeout 后停止，报告提交 SHA。后续如需付费 Pilot、模型/语料下载或具体 Claim，Owner 再行决定。

> 该文件由 Owner 本次明确授权转录并在 5060 控制面分支保存；文件内容不是新科学结果、不证明两台机器已经执行，也不覆盖原 `PAPER1_W1_FAST_TRACK_OWNER_APPROVAL_PROPOSAL.md` 的历史 PROPOSED 状态。
