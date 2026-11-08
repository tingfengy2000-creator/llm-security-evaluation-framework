# 5060 Codex｜S1-B 文献复用与模型准入包（DESIGN-ONLY）

你现在仅进行 Paper1 S1-B **设计与只读评估**。Owner选择“规则+本地开源模型公平比较”的研究选项B，且明确“未经另行批准不得下载或调用新模型”。这是研究**方向与设计授权**，不是S1-B科学试次/模型资产/推理/独立验证许可。

## 0. 恢复
Repo `tingfengy2000-creator/llm-security-evaluation-framework`；仅 `research/paper1-chinese-defense-5060`，先核最新远端HEAD/分支/工作树，按AGENTS.md、PO-MHEP读取权威/恢复日志，不能覆盖他人正在运行的工作树。

第一权威计划：
`docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_LITERATURE_MODEL_RESOURCE_INDEPENDENT_VALIDATION_PROPOSAL_20261108.md`
历史S1失败：
`docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_RESULT.md`。
旧S1 Run `W1-5060-S1-CHINESE-EXTRACTION-20261108-01` 状态 `S1_FAIL_STOP`，旧 R2为`K1-C`，证据不覆盖。

## 1. 文献复用审计（不改科研方向）
阅读固定RAGDefender源码/论文的Stage1/Stage2及 query未被核心判据使用的限制，区分原2025论文与2026 v0.2.0源码；梳理 X-MADAM-RAG 候选抽取/证据修复/聚组/冲突聚合，MADAM-RAG、ACL 2022 UIE、PaddleNLP中文UIE、EMNLP ODIE/2023 InstructUIE 的可借鉴接口和与VESA M2重叠的部分。禁止“论文存在就声称官方代码已可复现”。列每个技术的作者/论文/Repo/实际许可与Model权重许可差异，以及“直接复用 / 参考设计 / 尚无有效实现证据”三分法。

## 2. 比较臂冻结建议
Rule-V1（原S1不可改）、Rule-V2（仅旧73暴露样本作为dev）、PaddleNLP UIE轻量中文唯一候选、Qwen2.5-1.5B-Instruct本地对照唯一候选。所有臂同 (query,evidence)、同标准schema、同span/scope后处理与同错误/UNKNOWN定义；模型输出是候选，不具有来源可信性的证明。提案中对UIE/模型prompt、tokenizer、语言、CUDA后端/版本、GPU成本做资源风险清单。不要选择浮动main；具体revision若未完成原始可信核实标UNKNOWN。

## 3. 资源准入包（只读）
只读取官方已公开元数据和本机本就有权限的硬件/缓存清单；冻结候选checkpoint ID、license、模型卡与权重使用条件、白名单逐文件大小/hash可得性、磁盘下载峰值估算、GPU及CPU内存预算、依赖冲突、C盘缓存物理落点、D/E空间门、trust_remote_code禁用、offline保障、爆内存停止与量化条件。原UIE论文repo CC-BY-NC-SA和PaddleNLP Apache-2.0代码不得混用许可；Qwen2.5-3B Qwen Research许可与Qwen2.5-1.5B Apache-2.0不同。**任何不可直接核实字段保留UNKNOWN，不能猜。**

## 4. 独立验证预注册及分母
建议100个全新不同语义事实/应拒识案例；20个额外显式/自然化配对仅作为从属观测，主指标分母不能虚增；由独立于5060开发方的Owner批准审核者冻结标注与gold。旧73只能dev，不当独立test。预计记录可回答正确率、wrong/decided、wrong/total、严格scope/span一致性、自然化分层、未证新版误答、覆盖/拒识、Wilson区间、GPU/延迟/费用，使用原S1 90%与2%硬门，不改变合同；任何新增“未证新版误答=0”作为候选guard要向Owner单独申请。Rule-V2和模型均在一次性独立评价前冻结prompt/revision/参数/代码。若未取得独立数据与资源许可，拒绝“试运行看看”。

## 5. 严格禁止
- **新增模型下载、缓存预热、依赖安装、从在线仓加载模型、模型推理调用、付费或免费在线生成、商用API、联网Token探测全部禁止；也禁止执行已有新模型权重的首次推理。**
- 不运行新的S1-B实际科学试次、不生成冒充真实独立Gold的数据、不碰D2/D3/5090 Llama2/Claims、不改RAGDefender历史B2/R2/S1、旧Qwen108或P0约束、不启动S2/S3/S4/S5、不跨分支合并。
- 不能因为模型名称带Open或仓库README显示Apache就自动判权重许可证合格。
- 不给5090安排工作，5090仍等待Meta的Llama2权限确认。

## 6. 单次交付与STOP
一个精简 Owner审批包：文献对照（源码或论文证据）、推荐的第一模型与备选模型、精确checkpoint/revision或UNKNOWN、文件/许可/硬件资源表、真正独立验证流程及Gold控制、完成/风险/阻断、需要Owner选择/批准的最少事项。
更新治理与Tracker为 `S1B_DESIGN_ONLY / MODEL_DOWNLOAD_NOT_AUTHORIZED / MODEL_INFERENCE_NOT_AUTHORIZED / VALIDATION_NOT_AUTHORIZED / S2_S5_LOCKED`，如果远端已有更新先核对。仅提交脱敏方案和hash；Git提交推送成功、核remote HEAD后STOP。不要执行下一阶段。
