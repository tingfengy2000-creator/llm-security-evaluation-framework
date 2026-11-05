# 5060 Codex｜Paper 1 Week 1 Fast-Track B 受限执行指令（可从 Git 读取的正式恢复版）

> 作用：解决先前“完整最终 Prompt 仅通过 ChatGPT 文件链接交付，执行端无法访问”的阻断。本文件是根据既有完整最终 Prompt 及已入 Git 的两项 Owner 授权恢复的执行合同，并非新增下载/算法/付费许可。原先聊天附件文件名：`PAPER1_W1_FAST_TRACK_B_5060_FINAL_PROMPT_V2.md`。其监督端文件 SHA-256 为 `5103427161969394d8b40c78c02917d8f64f01fd0b8b46ce93232ffd58757617`；**本恢复版不宣称与原附件逐字节相同，不应拿本文件 SHA 冒充该源哈希**。
>
> Owner 授权：`W1-OD-20261105-FAST-B-04`；资源补充：`W1-OD-20261105-RESOURCE-REPRO-05`。授权已正式写于 `docs/paper1/dual_machine/owner_approvals/`，并编入 Owner Decision Register、Current Work State 与 Research Execution Log。
>
> 被阻断的前一轮 checkpoint：`14d718f9481ace613246c6c59f77a982d7368704`，已报告 `PARTIAL_DELIVERY / HUMAN_DECISION_REQUIRED`，**该历史阻断状态不能擦除或改成已执行**。本文件为缺失合同补齐，不要求重复已完成的4项静态测试与12题盲审包。

## 0. 唯一目标与治理前置门

在已封存的 D1 Pilot12/36 世界 TopK5 上，严格在源、模型、预算、公平性准入合格后完成 B1（未修改RAGDefender v0.2公开库轨道）与 B2（除中文 embedding 外保持B1语义完全相同）的零商业 API、离线过滤开发对照；并行整理/更新盲于本轮检索与结果的12题待人工裁决卡。**不重新检索，不生成答案，不进行付费或正式论文评测**。

1. 先在本分支检查 `git fetch --prune --tags origin`、HEAD、上游 ahead/behind、`status --porcelain`、最近提交和未提交变更；读取 AGENTS.md、Context Authority Map、PO-MHEP、Owner Decision Register、Current Work State、Research Execution Log、原P1/P2配置与Run Manifest。非预期脏工作树或分叉即STOP；不得stash/reset/rebase/force-push/merge/cherry-pick。
2. 使用 `git show` / 只读方式核对两份 Owner 授权原件，绝不根据本消息扩大其内容：
   - `docs/paper1/dual_machine/owner_approvals/W1_FAST_TRACK_B_OWNER_AUTHORIZATION_20261105.md`
   - `docs/paper1/dual_machine/owner_approvals/W1_STORAGE_AND_REPRO_RESEARCH_DIRECTION_20261105.md`
3. 必须复核原 P2 执行源码 `9aa21be13ae206dbbadb03b99528e362eba29378`、原最终报告 `3ca27c9416ea630e7f82c5b98ceed93099bd57ac`、输出 seal SHA256 `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`、Pilot12选择hash `2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`；选择hash必须与 P2 Run Manifest 逐字节核对。已封存36份TopK原始字节与完整成员逐项校验；原P2 TOPK seal和历史结果保持不可变。
4. 修订前记录新的 run_id、输入源hash、模型/源码身份、运行计划与失败保留机制；即使此轮受阻也必须保留原有 checkpoint 不覆盖。

## 1. 模型资产获取、空间与网络硬门

- **C盘不得新增项目可控内容**。只读核查本地模型、现有工具/原始环境可继续；但新模型、HF/Xet/ST/Torch缓存、Python bytecode、pip/conda缓存、虚拟环境、TEMP/TMP、解压、实验数据库、日志和归档均必须放D/E。确认宿主真实磁盘，包括Windows环境变量、WSL VHDX（如适用）和Python缓存路径；无法保证某受控项目操作不写C则该操作停止，不迁移/删除已有C环境，也不谎称OS层零写。
- D/E原1GiB总新增硬限已放宽，但需事先冻结单项最大预计新增量（模型、临时分片、失败重试/缓存、归档）及真实磁盘余量，**至少保留20GiB安全余量**。放宽空间不代表允许无限存储。
- 本轮**唯一可下载模型**：HF官方 `sentence-transformers/all-MiniLM-L6-v2`，固定revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`。先只读核对官方commit、Apache-2.0模型卡许可、加载调用链与必要文件清单/远端字节长度、请求累计传输上界及本地目标路径。不可下载整个仓库、动态`main`、镜像/替代代理/备份源/依赖或模型自动fallback。
- 尽可能选择一份 `model.safetensors` 及必需 tokenizer/config/Pooling 文件；避免重复 `pytorch_model.bin`、`rust_model.ot`、TF/ONNX/OpenVINO等无关导出文件。若必须新增非白名单文件才可运行则STOP，申请新授权。
- **累计网络实际下载≤250 MiB（262,144,000 bytes）**，包括所有请求/重定向/失败下载传输，不能每次重试重新计数。未经确认无法有效限制累计流量时，不要开始下载；失败后不得自动重试突破上限。
- 资产落Git外D/E隔离缓存。下载完成要验证固定revision、每文件SHA-256、size、model config、tokenizer、pooling、依赖和许可证文件身份；禁止把模型二进制、受限文档或密钥提交Git。
- B1/B2实验时强制 `HF_HUB_OFFLINE=1`、`TRANSFORMERS_OFFLINE=1` 等离线门，禁止自动下载/联网；若加载器尝试网络访问即fail closed，不可换模型、补依赖或修改科学参数继续。

## 2. 对照模型与方法身份

- B1上游源码固定 `SecAI-Lab/RAGDefender@ba2a17efba165d45409114df2d70b030ade1e1b8`，为未修改v0.2公共库算法。使用固定HF all-MiniLM-L6-v2，不使用`artifacts/main.py`或宣称等于作者论文原始数值。作者legacy grouping和Stage2实现/阈值不允许为结果作无审批修补。若需要代码语义patch才能加载授权模型，则该基线BLOCKED并发起PO-MHEP。
- B2以完全同样的公开库、query/input、TopK顺序、预算、p/m、clustering、TF-IDF/stopwords、stage selection/异常路径运行，**仅**将B1 embedder对象替换为已存在/已核的 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2@16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`。tokenizer差异属于模型差异，必须披露；不可额外改分词、阈值、删片策略、聚类或打补丁。两组唯一变量不成立就STOP。
- 允许运行前按P2只读验证数据；禁止重建36个Chroma索引、重新检索或改善29/36命中率、手动补回7 miss、调参选优、改query或candidate chunk。原B0不重复跑，不覆盖既有结果。

## 3. 盲审与数据隔离

- 检索/过滤进程仅见36份role-free已封存TopK、Query和必要文档元数据，不读取Candidate角色、Poison/Clean/HN、S、expected、Reviewer、HumanGT/Oracle、D2/D3。
- 在所有36世界成功/失败输出**完整封存**后，独立Evaluator才可打开获准D1开发标签并计数；不把全套开发标签或target信息泄露给防御模块。全世界实验失败/未运行仍留分母，不自动重跑挑选好结果。
- 另行准备12张盲于检索命中、旧预测及B1/B2输出的来源/问题裁决材料。保留38个事实原子、原始问题、有效时间与条件范围、证据引用、答案等价范围、独立target证据缺口与C3拒答边界。AI不能署名为Human Gold，不能从候选角色猜攻击目标；未裁决写 `NEEDS_ADJUDICATION`。若已有盲审包合规且hash不变，直接复用，不必再生成一份冗余包。

## 4. 输出指标与科学边界

固定分母：全部36世界（Poison12、Clean12、HN12）；Candidate确实出现在TopK的29世界（Poison10、Clean10、HN9）。保留未召回7世界（P2、C2、HN3），不得把miss算防御成功或隐藏。
报告每世界/每方法的选中chunk、删除chunks、是否有任一Candidate召回chunk被删、是否全部Candidate召回chunk被删、部分删除残留、空上下文、异常、并列处理、平均/中位/p95时延、API/model调用次数。分别计算Poison Recall、Clean-FPR、HN-FPR的全分母与条件分母，附TP/FP绝对数；背景未标真值不得随意加入Clean/HN分母。
没有生成器与独立评价Gold，所以 Targeted ASR、Answer Accuracy、生成拒答、Unsupported QA全为`NOT_MEASURED`，不得写0。负结果应原样保留，不能把B2中文迁移直接算论文新算法贡献。
原P2/历史R0/5090 Claim保持原证据与身份等级，不合并不同tier、模型或检索数据。

## 5. 交付与止步

先做Forward/Paper Risk Review和适用测试、Ruff、MyPy；记录身份清单、所有批准文件blob SHA、资产白名单与实际累计下载、磁盘占用、完整argv/cwd/time/stdout/stderr/exit、输入/输出seal、资源成本、失败/skip、私有归档hash/index。
主报告继续使用 `docs/paper1/dual_machine/chinese5060/W1_5060_FAST_B_B1_B2_OFFLINE_RESULT.md`，但**保留此前checkpoint原文和证据，采用新增阶段/文件或追加新版本方式**，不能覆盖/重写历史阻断。另交 `ASSET_MANIFEST.json`、`PAIRWISE_B1_B2_METRICS.json`（仅脱敏汇总）、`ADJUDICATION_PENDING_INDEX.json`、Run Manifest、失败日志、两级分母及所有输入/输出/源码hash。
仅本分支commit/push，工作区clean、ahead/behind=0/0，交付报告最新git SHA、run_id、执行状态和仍需Owner裁决的具体问题，然后**STOP**。
绝不启动商业API、B3/B4、B5/B6、D1-40、D2/D3、GT/Reviewer、T1/T2、5090 Claim、其他模型/依赖/语料下载、跨分支/主线合并或自动推进P3。

## 6. 授权来源优先级

本恢复Prompt只能在两份Owner授权及AGENTS.md/PO-MHEP允许的交集内执行，不能替代或扩大授权。若本提示与原签名P2模型/选择hash、P1/P2正式protocol或任何Owner原始准入条件不一致，**以已经核实的原始Owner授权和冻结证据为准，保留冲突记录并按PO-MHEP升级**，严禁静默按方便的文本执行。
