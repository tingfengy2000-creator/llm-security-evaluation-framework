# Paper 1 | 5090 官方资产与许可准入 — Owner 正式授权（PO-MHEP 十二字段）

- **Owner ID（跨机唯一）**：`W1-OD-20261105-5090-ASSET-GATE-07`
- **日期**：2026-11-05 JST
- **状态**：`OWNER_EXPLICITLY_APPROVED / OFFICIAL_METADATA_ONLY_AND_STATIC_REPRO_PREFLIGHT`
- **授权来源**：Owner 在 Paper 1 本次监督会话中的明确指令；本文件是可核验的脱敏转录，不是原会话原始字节，也不是执行结果。
- **只授权 5090 分支**：`research/paper1-ragdefender-repro-5090`
- **授权前远程 HEAD**：`c3e16609832bce9531ac517975b006b44dd522da`
- **上游冻结源码**：`SecAI-Lab/RAGDefender@ba2a17efba165d45409114df2d70b030ade1e1b8`
- **参考控制面**：5060 `W1-OD-20261105-RESOURCE-REPRO-05`、当前Fast-Track C `W1-OD-20261105-FAST-C-06`；本决定不得修改或干预5060分支。
- **说明**：本 ID 不重用两分支同号异义的 `PODR-154`。跨机引用使用本 Owner ID + 当前分支 + 完整 Git SHA。

## 1. Issue ID
`W1-OD-20261105-5090-ASSET-GATE-07`。

## 2. Issue name
5090 论文基线主要可复现实验前的官方模型/BEIR许可、固定revision、文件尺寸与资源约束、代码副作用和 Claim 执行前审批包的只读核验。

## 3. Discovery stage / task
Paper 1 / RAGDefender ACSAC 2025 主基线 / 5090。先前完成 `W1_5090_RAGDEFENDER_MAIN_RESULTS_REPRO_PLAN.md`；Claim1 PoisonedRAG 计划24格、Claim2 Tan计划6格、Claim3 GARAG计划6格。全部 `NOT_RUN`，ASR/QA `NOT_MEASURED`；官方环境 Torch2.4+cu121 在RTX5090 sm_120上GPU失效，已另设兼容环境但存在数值偏差风险。

## 4. Evidence, separated by grade
- **OBSERVED_GIT**：此前5090已推送的覆盖矩阵、资源门、只读脚本审计及官方/兼容环境报告可在上列SHA查到；这些报告表明未下载权重/BEIR、未运行Claim。当前Owner确有本轮明确授权。
- **SOURCE_DERIVED（需本轮重新核查）**：模型 `meta-llama/Llama-2-7b-chat-hf`、`lmsys/vicuna-7b-v1.3`、`facebook/contriever` 和作者脚本实际使用的段落模型 `paraphrase-MiniLM-L6-v2`；BEIR `nq/hotpotqa/msmarco` 归档来源；已有静态记录表明 Claim1=24、Claim2/3=6，Tan日志目录名不匹配、Table7 `--p/--m` 与 CLI 不匹配。
- **OWNER_CONFIRMED**：仅允许官方来源的只读许可/资产元数据查询、静态本地预检、D/E缓存路径与资源预算核验、审批包准备；不允许任何下载和Claim。
- **INFERENCE**：先填资产身份与脚本副作用链再批准逐批下载/单格，可减少模型门禁、路径和显存导致的无效运行。兼容环境的结果不能视作论文原环境重现。
- **UNKNOWN（不默认为已批准）**：Llama2门禁与账号条款接受状态、Vicuna非商业许可是否满足本研究实际使用、Contriever许可授予依据、MiniLM的精确仓库与许可、BEIR具体子数据集许可和解压峰值、完整下载峰值与硬上限、CUDA内存峰值、Claim2缺陷处理方案、单格真实耗时/结果。

## 5. Affected constraints
`AGENTS.md`、Context Authority Map、PO-MHEP、独立分支原则、模型/语料许可证、作者 artifact 与论文实现偏差、不可变历史、禁读 D1/D2/D3/Reviewer/GT Vault、D/E存储+C禁新增项目可控内容、Owner每阶段资源下载/实验逐批批准、实验结论证据等级。

## 6. Why now
5060已获Fast-Track C只读归因授权；5090可在不等待科研结论的同时独立消除真实论文基线复现的许可、来源与资源信息缺口。但任何真实下载或Claim都必须先建立可信准入与独立Owner批准。

## 7. Downstream risks
- **许可**：Meta门禁、Vicuna非商业限制与Llama1衍生条款、Contriever无license字段、BEIR数据使用/再分发边界未证实。
- **工程/资源**：`from_pretrained`/BEIR加载器隐式下载、token/login副作用、HF缓存/Windows TEMP默认写C、WSL VHDX宿主位置、解压膨胀/zip slip、RTX5090 CUDA环境差异、显存OOM、输出日志未保存。
- **论文**：Claim2日志目录与Table7参数不一致、Claim1与其余Claim覆盖矩阵差异、作者遗留算法不等同论文公式、8bit/兼容环境造成数值不等价。
- **证据**：将网页展示误当许可证接受、将Content-Length当解压体积、将计划格数当完成格数、将未来命令清单当实际结果。

## 8. Options and comparison
- **A【OWNER ACCEPTED】**：只读官方来源 metadata/许可与本地源代码副作用、磁盘配置审计，做分批资源和命令审批包。优点：取得必要事实且不启动昂贵计算；新增权重/数据/依赖=0；仅消耗公开元数据的小量网络和D/E日志空间；可逆；保留论文公平性。缺点：无法通过纯metadata验证解压峰值/真实模型显存，必要时保留 UNKNOWN 交Owner。
- **B【NOT SELECTED】**：停在旧准备材料等待，无新增合规风险但许可和执行前阻断原样存在。
- **C【PROHIBITED】**：直接接受许可/下载全套权重与BEIR或先运行Claims，可加快结果但违背版权/门禁/资源/批准门；模型与论文比较风险大。不可用。

## 9. LOCAL recommendation
执行 A：逐项官方身份→许可证据→必要文件与容量→BEIR压缩/解压界→脚本隐式I/O与修补选择→D/E落点→分批下载+最小单格+Claim1/2/3逐批Owner审批包。每项缺证据标`UNKNOWN/BLOCKED`，绝不猜测。

## 10. Rationale and confidence
本次Owner授权及5090既有 Git 计划可核且高置信；许可证适用性、解压后大小与真正GPU表现尚未得到新证据。研究目标是将来完整复现三条开源Claims，而不是本轮得到任何正式 ASR 或 Accuracy。

## 11. Explicit approvals, questions and hold points
**本轮确切批准**：
1. 仅在5090原分支，读公开官方许可证/模型卡/元数据：HF模型官方仓库、Meta/LMSYS或模型权利方正式许可页面、BEIR官方论文/代码/数据托管与许可说明。可通过 HTTPS GET 获取小型 HTML/JSON/文本元数据，或无body且不自动跟随权重重定向的 HEAD 请求；记录URL、HTTP状态、UTC时间、响应hash/ETag/提交revision和证据置信度。可以只读GitHub官方上游源码与论文说明。**公开数据网页查询不等于允许模型推理API**。
2. 查询必须遵守不登录、不发送HF token、不点击同意、不提交门禁申请、不上传任何私有文件、不接收模型权重/zip正文。禁止HF`snapshot_download`、`from_pretrained`、`git lfs pull`、BEIR自动下载/解压，以及任何云模型推理服务。
3. 只读审计确定的资产与来源：`meta-llama/Llama-2-7b-chat-hf`、`lmsys/vicuna-7b-v1.3`、`facebook/contriever`、**脚本真正使用的**`paraphrase-MiniLM-L6-v2`（先确定完整repo ID与revision；不得拿5060的`all-MiniLM-L6-v2`代替）；BEIR`nq/hotpotqa/msmarco`。固定候选revision必须由官方metadata佐证，不能只靠floating`main`。逐文件大小、名称/权重分片、重复备份、hash/ETag可用性与真实必要加载路径都要记录；身份/许可缺失则保持阻断。
4. BEIR压缩长度、官方发布的未压缩容量或文件列表可核验并记录来源；**若无可信未压缩字节数据，明确 UNKNOWN**，只能提出未来下载时的上限/zip-bomb检查方案，不得偷偷 Range 提取zip中央目录（这仍是未获准数据下载）、不得据压缩大小捏造解压峰值。
5. 只读静态检查 `claim1/claim2/claim3` 当前源码调用链、具体参数/格数、implicit download、日志路径、`trust_remote_code`、GPU/CPU offload、config/CLI差异、作者算法分歧、成本与复现结论口径。可`bash -n`或Python`ast.parse`纯静态语法检查（避免导入/pyc/编译副作用）；不得修复源码或运行模型。
6. 查验C/D/E与WSL宿主盘、Windows TEMP/TMP、HF_HOME/HF_HUB_CACHE、TRANSFORMERS_CACHE、XDG_CACHE_HOME、CONDA_PKGS_DIRS、PIP_CACHE_DIR及工具缓存未来的D/E安全设置，不迁移/修改现有环境；仅可创建合规D/E审计日志。磁盘预算需分别列模型文件、语料zip、解压、复制/临时、运行日志、容器/VHDX与20GiB安全余量；未知项不可作为已冻结预算。
7. 生成可审议的**分批**Owner决策包：模型许可证与固定版本、每模型白名单/预计下载量与校验、三个BEIR语料与解压硬停、最小实验格(NQ/Contriever/Llama7b/100%/seed12)预检命令和建议超时/VRAM/退出条件、Claim1其余23格、Claim2六格与路径差异处理选项、Claim3六格及可选Table2–8，明确每批还需的具体Owner批准。
8. 本次只提交新治理/报告/清单与脱敏证据到自己的5090研究分支，完成文档closeout并停止；不碰5060，且不得自动推进下一批。

**明确禁止（下一Owner gate之前）**：接受Meta或任何license/gated条款、登录或使用token、下载任何模型权重/BEIR数据/依赖（包括小额原始数据分片、受限LFS和自动snapshot）、安装/升级依赖、改官方/兼容环境及源码、真实Claim1/2/3或单格预检、商业API、D1/D2/D3/Reviewer/GT Vault、5060数据、跨机merge/rebase/cherry-pick、生成任何正式ASR/QA结论。

## 12. Allowed/prohibited until new decision
只允许第11节的官方**元数据级**网络核验、纯本地只读静态审计、D/E脱敏证据写入、基于证据的资源/许可风险与审批包编写、自分支合法Git提交推送；任一页面需要登录/接受许可、metadata返回权重body/zip、下载量无法确定、涉及私有token或非官方镜像、需语义patch、证据冲突→`HUMAN_DECISION_REQUIRED / STOP`受影响子项，按12字段报告，不能用替代源/假设绕过。无需等待5060 Fast C结束。

## Deliverable and STOP gate
`W1_5090_OFFICIAL_ASSET_LICENSE_METADATA_GATE_REPORT.md`、`OFFICIAL_ASSET_METADATA_MATRIX.json`、`BEIR_LICENSE_AND_UNPACK_BOUNDARY.json`、`CLAIM_STATIC_SIDE_EFFECT_AUDIT.md`、`DRIVE_CACHE_PATH_PREFLIGHT.md`、`BATCHED_REPRO_OWNER_APPROVAL_PACK.md`、`OFFICIAL_SOURCE_ACCESS_LOG.json`（仅脱敏状态/响应hash，不含密钥）、`FINAL_QA.json`及资源门未闭合条目；如果未取得重要官方证据，按`PARTIAL_METADATA_BLOCKED`交付，禁止以文档准备冒充Claim复现。完成 AGENTS.md 所需Human/Agent Ledger、Current Work State、Research Execution Log和Git交付后 STOP。三个Claim始终 `NOT_RUN`、ASR/QA始终 `NOT_MEASURED`，直到有后续明确实验审批和实际sealed输出。
