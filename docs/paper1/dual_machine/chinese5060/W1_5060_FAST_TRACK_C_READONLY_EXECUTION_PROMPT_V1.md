# 5060 Codex｜Paper 1 Fast-Track C 只读失败归因：完整执行 Prompt V1

> **这是可直接从 Git 读取的最终执行合同，不依赖任何 ChatGPT 附件。**
> 
> 唯一 Owner 审批：`W1-OD-20261105-FAST-C-06`；审批首次登记 commit：`ed70b08262c85b2a4ec8502d3911413fd1eed165`。授权原件：`docs/paper1/dual_machine/owner_approvals/W1_FAST_TRACK_C_OWNER_AUTHORIZATION_20261105.md`。
> 
> 分支仅限：`research/paper1-chinese-defense-5060`。旧 Fast-Track B 最新交付 SHA：`8d14dd180a121970ffb311a4176dca61336f91c2`。本任务只能分析既有数据，**不产生新的安全实验试次**。

## A. 启动、环境与法律权限

1. 按 `AGENTS.md` 完整 Context Recovery：按仓库所列权威顺序读 `context_authority_map.md`、PO-MHEP、current_work_state、PROJECT_MASTER_CONTEXT、Owner Decision Register、long-term-requirements、Experiment Master、研究方案、协议及Research Execution Log；核查最近15条Git提交。
2. 执行 `git fetch --prune --tags origin`、`git status --short --branch`、`git branch --show-current`、`git rev-parse HEAD`、`git log -15 --oneline`。仅在无未知修改、非分叉且可fast-forward时允许`git pull --ff-only`。如 HEAD 因监督登记更新而前进，必须检查新提交仅为治理/合同并精确记录当前实际SHA。禁止 reset、rebase、merge、cherry-pick、force-push、替其他分支提交。
3. 必须先从本分支 Git 原样读本 Prompt 与授权原件，不得依赖用户本地不可见附件；用户明确批准的只读权限已经生效，无需重复申请。但任何新型数据访问、额外试次、方法patch或疑义仍按PO-MHEP停止。
4. `FORWARD_RISK_REVIEW` 与 `PAPER_RISK_REVIEW` 必须记录：开发集暴露、阶段归因是否可识别、样本成组依赖、原始B1/B2模型属性差异、Query未参与公开库决策、隐蔽事实与恶意意图不可从Candidate文本证明。
5. 本任务新项目文件、临时解压、日志、统计中间结果、缓存、私有归档只能写D/E；严禁可控项目写C。保留20GiB安全空闲并预冻结合理I/O和磁盘峰值。**零新模型/数据下载、零网络实验、零商业API、零GPU依赖安装**。当前环境只读复用。

## B. 输入白名单：必须先验证身份，再读内容

- 允许的原开发实验：P2 `W1-5060-P2-20261104-T0-01`，Fast B `W1-5060-FAST-B-20261105-PAIR01`；本轮分析建议 ID `W1-5060-FAST-C-20261105-ATTRIB01`。
- 原 P2 事实组选择 `2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`。原P2 TopK seal `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`；PAIR01 输出 seal `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`、评价 seal `0027a03c490f80d98327fbdd8f787830affde3bcfbf9e6c02bd805bf260c79a1`，私有zip hash `445dbf97904706334acb2a2b890d4c51dae244285ff5f0607d72ed78340c4dec`。
- 从现有 Run Manifest/Archive Manifest 提取**已授权的精确路径白名单**，只允许打开上述 P2/PAIR01 原始检索、过滤、只读profile、manifest和批准 D1 开发评价文件。对 D2/D3、Reviewer、GT Vault、Oracle、其他工作线以及文件名广搜一律禁止；不要在目录树枚举、递归发现、全文搜索中暴露限制集的路径名。
- 校验SHA-256、来源、行数、输出seal、匿名worldID、原world顺序、全部36世界与role-free绑定。若档案不存在/损坏/路径不清，标 `EVIDENCE_BLOCKED`，不得重跑RAGDefender、重检索或重新生成原结果。可对原zip做只读解压副本，但必须在D/E，并核验解压对象hash和无路径穿越。
- 直接读取原公开聚合不等于独立重算成功：必须清楚标记哪条证据为 `GIT_SOURCE`、哪条为 `LOCAL_PRIVATE_EVIDENCE_VERIFIED`、哪条仅 `HYPOTHESIS`。

## C. 最小权限：三条严格分离的资料流

1. **ROLE_FREE_ANALYST**：仅读取封存的query/TopK chunk及B1/B2输出、已有程序profile/调试字段。不读取role/S/poison/clean/HN、target、预期答案、Ground Truth、旧模型预测、独立盲审内容或其他敏感标签。仅形成由原输出导出的角色盲特征：`rank, candidate_present, n_adv, stage1_count, stage2_input, TFIDF_count, frequency_score/tie, selected_indices, removed_indices, kept_indices, exceptions, latency` 等**存在才提取**。对Stage字段如果没有录入原trace，不可创造或补测。
2. **POST_SEAL_EVALUATOR**：在确认 ROLE_FREE_ANALYST 的输出 complete+SHA lock 后，采用另一个进程、显式只读批准D1开发标签/旧Evaluator材料进行对齐，生成按Poison/Clean/HN分层的聚合错误类别和私有行级差异表。此进程不得把标签返写Guard输入、role-free特征集或第一阶段脚本；任何未经授权标签/Ground Truth越界即STOP。公开Git仅发布必要脱敏聚合和不可逆摘要，禁止发布匿名worldID对应标签表。
3. **ADJUDICATION_HANDOFF**：单独处理原12题、38事实原子、16来源的未签盲审资料。严禁读取任何检索结果、PAIR01输出、角色身份、统计、旧AI比较意见或攻击候选映射；只能核对原封存卡hash、来源许可和引文定位，生成独立人工审阅清单、空白签署/时间范围/答案等价类/target证据/C3待裁决字段。**不能自行决定target或Human Gold，不能给Reviewer发未获批准的内部标签**。

## D. 只读失败归因分析具体项目

不得运行`ragdefender.defend`、`encode`、`SentenceTransformer`推理、检索、重建Chroma、原`run_chinese5060_b12.py`，不得改变任何模型、tokenizer、阈值、p/m、样本、TopK、chunk、index、query、world或源文件。允许新写无副作用的只读报表脚本，**读取旧JSON并计算统计不算重跑科学试次**；保留命令/参数/SHA。

1. **分母一致性**：全部36(P12,C12,HN12)、条件29(P10,C10,HN9)、MISS7(P2,C2,HN3)。核对 B1 TP1 / CleanFP1 / HNFP2，B2 TP2 / CleanFP4 / HNFP2，并复算每世界any-chunk、all-retrieved、partial-removal、残留数；每个被召回的candidate本次只有1chunk，partial0**不是多chunk鲁棒性证明**。对未标注背景不能推断真负类。
2. **配对翻转**：以同一worldID配对计算 B1(0/1)→B2(0/1)四格完整列联表，分别Poison/Clean/HN统计净增/恢复/共删；Poison新增2丢失1、Clean新增误删4恢复1、HN新增误删1恢复1共删1等先前公开聚合必须同私有行级证据独立核对。不要把汇总净增代替个案。
3. **Stage1/Stage2归因**：对原源码调用链做静态只读定位；抽取旧profile中的Stage1分组/n_adv与Stage2候选、TF-IDF权重/频率、实际删除indices；明确各错判发生于`Stage1_count/selection`、`Stage2_rank/score`、`tie_break`、`embedding_change`或`INSUFFICIENT_TRACE`的证据强度。不允许在只有最后输出时推断阶段反事实，不能把算法相关性写成因果结论。
4. **频率同分**：原观测 B1为29/36、B2为33/36有频率分数同分；使用已记录同分标记与排序索引，检验翻转与tie是否共现。若旧trace不含完整tie candidates及原规则输入，不可判定“如果无同分就不会误删”。不能修改稳定排序/低索引tie-break。
5. **Poison漏报与Clean/HN误删**：优先对命中TopK的P10、C10、HN9做私有行级归类，MISS7只做单独召回诊断；针对HN区分合法历史版本、失效时间、时间条件与文本一致性，但**不能用候选文本自行推断攻击者意图或target**。若来源真实性未经独立核验标 `SOURCE_UNVERIFIED`，不偷渡T1可信证据。
6. **批判性界限**：B1与B2除语言目标外还存在Normalize和max_seq_length等固有模型差异；英语stopwords/TF-IDF规则未变；本次n=12事实组而非36独立query；未warmup的时延不用于效率结论；背景chunk删除78/180、81/180只作风险提示，不能计无标签背景FPR。Query 未参与原库detector决策，不据此捏造版本感知能力。所有解释需有`evidence_ref+hash+field+confidence`或列为可检验假设。

## E. 输出、证据与停止条件

- 主报告：`docs/paper1/dual_machine/chinese5060/W1_5060_FAST_C_READONLY_FAILURE_ATTRIBUTION_REPORT.md`，清晰分为 Observed、Source-Derived、Inference、Hypothesis、Unresolved，结论保留完整与条件性分母；只写支持的局限/机制假说，不写新的成功率。
- `docs/paper1/dual_machine/chinese5060/fast_c/` 下：`FAST_C_ANALYSIS_MANIFEST.json`、`READ_ONLY_INPUT_AUDIT.json`、`PAIR_FLIP_AGGREGATE.json`、`STAGE_TRACE_COVERAGE.json`、`TIE_ASSOCIATION_SUMMARY.json`、`FAILURES_AND_LIMITS.json`、`ADJUDICATION_HANDOFF_INDEX.json`、`FINAL_QA.json` 和必要的私有archive hash/index。新分析代码有适用tests+Ruff+MyPy；可重放仅指对同一旧输出纯计算，不是对模型重新推理。
- 保存每次只读命令argv/cwd/time/exit、source_sha、file_access allowlist、input SHA验证、analysis output SHA与私有zip digest；必要时列 `READ_ONLY_RECOMPUTATION` 与 `NOT_REPLAYED_RAW_MODEL`。
- 任何封存不匹配、身份不明、非法标签读取、必需科学路径调用、新网络/模型下载/付费、与研究公平性冲突：按PO-MHEP停止受影响工作，保存12字段决策材料，状态`HUMAN_DECISION_REQUIRED`。旧证据不可覆盖、旧负结果必须保留。
- 完成后执行AGENTS/PO-MHEP规定的 DOCUMENTATION CLOSEOUT：human/agent ledgers、Current State、Research Execution Log、Experiment Master的适用条件、链接/脱敏、代码变更检测、Git commit/push仅本分支、远程HEAD/upstream与clean验证。报告最终SHA；**STOP**。
- 完成可写`FAST_C_READONLY_DIAGNOSTIC_COMPLETE`或`PARTIAL_DIAGNOSTIC_UNRESOLVED`；始终保持 `HumanGold=0`（除非另有真正独立人工签署，而本轮无此授权）、`targeted_ASR/AnswerAccuracy=NOT_MEASURED`。本轮没有B5/B6、没有新算法、没有D2D3、没有新的实验对照。
