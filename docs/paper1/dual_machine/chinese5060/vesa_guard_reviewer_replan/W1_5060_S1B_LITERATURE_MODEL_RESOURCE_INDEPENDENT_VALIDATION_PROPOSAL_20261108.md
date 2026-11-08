# Paper 1｜S1-B 文献复用、规则与本地开源模型公平比较的受限研究方案
日期：2026-11-08 JST
状态：`OWNER_B_DESIGN_PREFERENCE_CONFIRMED / DESIGN_ONLY / NO_MODEL_EXECUTION_AUTHORIZATION`
分支：`research/paper1-chinese-defense-5060`
先前核对的 S1 HEAD：`39debd9f53d501a4df99f345fdf6d7b80d90d9d7`
Owner 本轮指令：“我选择B：允许规则与本地开源模型辅助抽取进行公平比较。请按PO-MHEP制定受限S1-B方案、模型资源和独立验证审批边界，未经我另行批准不得下载或调用新模型。”
Owner 进一步强调：优先参考 RAGDefender 或其他论文，避免无谓重复造基础抽取器。
**本记录只是方案选择、文献/公开资源只读调查与下一审批包；不代表下载、安装、加载、调用新模型或运行新实验得到批准。**

## I. 证据与前提

- 原研究路线仍是“面向中文 RAG 隐蔽知识污染的版本/作用域感知检索后防御”，不是泛化真假文本分类，也不是新做一个答案抽取论文。
- 5060 S1 `W1-5060-S1-CHINESE-EXTRACTION-20261108-01` 已封存 `S1_FAIL_STOP`：73 条合成验证（61不同语义案例、12组配对），有答案值命中31/61、已决定错抽4/34、UNKNOWN39/73、自然可用的scope绑定事实25/49、12条应UNKNOWN有2条误答；AI_AUTHORED/NOT_HUMAN_GOLD。不得调整原 73 Gold 或把同一组重跑结果作为新独立验收。
- R2 K1-C、旧 B2/RD-zh 公平对照、D1_DEV_EXPOSED、历史失败及原 Qwen108 均冻结，S2–S5 与 5090 Claim 未授权；5090 Meta Llama 2申请等待，不自动给5090新任务。
- RAGDefender ACSAC 2025 官方实现在检索后使用 Stage1 聚类+TF-IDF估计攻击片段数、Stage2相似对频率选择删除索引，`defend(query,R)` 核心判据不消费 query 语义。允许复用“插入生成前过滤”的接口、实验协议与代码合法部分；**不指望 RAGDefender 自身直接提供事实值、版本与来源证据抽取**。
- X-MADAM-RAG arXiv:2606.12903 采用候选抽取、证据修复、确定性分组、冲突聚合；与原 M2重叠，必须作为基线/相关工作，不把纯答案分组宣称创新。其自然化抽取实验提醒零样本自然语言外推风险；论文存在不等于官方完整实现可复用。
- MADAM-RAG arXiv:2504.13079与CEG-RAG PMLR 2026 用作冲突/安全场景对照文献，不自动允许额外模型、Judge或cross-encoder。
- UIE: Lu et al., ACL 2022, https://aclanthology.org/2022.acl-long.395/；独立 PaddleNLP UIE 中文官方说明：https://github.com/PaddlePaddle/PaddleNLP/blob/develop/slm/model_zoo/uie/README.md；专用抽取器支持可见 span。
- ODIE: Jiao et al., EMNLP 2023, https://aclanthology.org/2023.emnlp-main.620/；InstructUIE arXiv:2304.08085 作为按指令抽取能力参考，不默认存在可直接用的轻量中文权重。
- 一个可选本地小型指令模型是 `Qwen/Qwen2.5-1.5B-Instruct`，官方 Hugging Face 标记Apache-2.0，约3.09GB权重；仅候选，revision/完整文件清单/模型与权重许可、内存门仍未冻结。
- 避免静默选择 Qwen2.5-3B：其官方许可证是Qwen Research，而不是自动按Apache-2.0处理。原 UIE 论文仓库的代码许可与 PaddleNLP Apache-2.0 项目不同；具体UIE checkpoint许可需单独验证。

## II. 冻结方法结构与复用边界

建议整体连接：
`retriever (frozen TopK) -> RAGDefender (frozen B2/RD-zh comparators) -> candidate fact extraction (replaceable) -> source-span/scope deterministic verifier -> independent provenance/version proof P0 -> M1/M2/M3 risk selection -> generator`.

S1-B **仅比较 candidate extraction 层**，不运行 TopK、RAGDefender、新G3、M1/M2/M3或generator。模型只能输出受来源文字支持的候选事实；其模型自称的可信度、真实世界常识或“最新版”不能作为可信来源证据。

所有臂共享规范 `(query,evidence_original_bytes,schema)` -> `[{subject,attribute,value,unit,time/version,effective_range,condition,negation/exception,scope,spans}, UNKNOWN]`；span必须回指原文确切字节/字符位置，严格字段/单位/日期校验、确定性source-span重定位、冲突/来源不明时不能自动标TRUSTED。相同输入、分母、schema、span-checker和安全后处理，不得仅给某一臂Oracle提示、Gold或可信锚。
**候选公平臂**：
- `Rule-V1-locked`：已封存S1旧抽取器，只作为旧基线，不修改。
- `Rule-V2`：分阶段 query slot -> 全部可见候选 -> scope/time/version/condition/exception -> original span verifier。允许在旧73已暴露数据+独立development上研究修复，但不能用于独立验收后的再次调参。
- `UIE + identical verifier`：优先审计PaddleNLP `uie-nano/uie-mini/uie-base` 其中一个轻量中文 checkpoint；模型许可/依赖/真实容量检查后再由Owner固定单个revision。抽取原文候选spans，后处理按统一schema绑定。
- `Qwen-local + identical verifier`：候选 `Qwen2.5-1.5B-Instruct`，官方约3.09GB权重（不包括环境/运行开销），冻结prompt/temperature/max_new_tokens/seed/JSON解析及非答案补全策略；不借助模型常识判真伪。
每个神经候选均只能在**未来Owner明确逐项模型批准**后下载、安装、加载与推理；不批准则相应臂保持 NOT_RUN，不能用其他模型替代。

## III. 资源门、许可门与审批次序（必须显式Owner审批）

### Gate 0：Design-only（本轮允许）
允许5060仅阅读公开论文/源码/本地环境已有依赖与缓存元数据、编写无模型加载的设计/接口/估算与资源审批包；这不是任何模型实际运行许可。不得触碰旧数据/私有GT/5090，除允许的只读S1聚合审阅。访问公开站点本身不代表获得权重许可。
静态设计应记录：论文算法映射、源仓/代码commit、license、checkpoint候选的repo/revision、可信权重源、逐文件大小/hash（官方若不可见记UNKNOWN）、兼容runtime/Python/CUDA/Paddle/Torch、GPU型号与空闲显存、峰值VRAM候选区间（估算，不是实测）、CPU/RAM/D/E空间/主机C盘真实缓存映射、下载和解压上限、固定依赖/风险、许可证与数据出站判断；不能假装无资源证据时可运行。

### Gate 1：Single model asset admission（尚未授权）
须单独将唯一候选模型与固定revision、可下载白名单、完整文件总量、权重与代码许可证、remote-code禁用、运行时版本、联网主机/镜像策略、磁盘余量、VRAM退化/量化约束、停止边界提交Owner。**在Owner签署具体单模型资产许可之前**：下载数0，安装数0，模型加载次数0，模型推理0。不同模型需不同授权；无自动回退/换源/浮动main。
建议优先考察UIE小模型再考察Qwen1.5B；不是默认Owner全批接受。硬件能否在5060现有环境安全运行，目前UNKNOWN。5090仍在Meta Llama2审批，不能占用5090做S1-B。

### Gate 2：bounded development inference（尚未授权）
如果Gate1资产真实完成且Owner独立批准仅在已暴露73数据+新的development fixtures上本地运行固定模型、prompt/参数、调用上限/批量/GPU预算，才允许Rule-V2/UIE/Qwen在开发集调参。保存每版结果、OOM、拒识和自然表达问题，不覆盖旧S1失败。**禁止**查看S1-B新独立validation Gold/指标调参。
模型推理不应向外部发送任何文本，`local_files_only/offline` 前置测试为硬门；所有模型输入/输出与服务端端口绑定限制需脱敏封存。新模型未授权则仅Rule-V2设计/静态逻辑，不启动调用。

### Gate 3：independent one-shot validation（尚未授权）
由**不参与5060方法开发/模型选择的独立审阅方**提供未见过的中文事实/原文 span/版本/作用域Gold，封存映射与SHA；可分工先收集资料和设计数据schema，但在获得Owner许可前不得让5060自造、自评分并称“独立”。
建议至少100个**不同语义事实/拒识案例**的独立集合，优先自然中文并包含多事实、未证修订、合法多版本、否定例外、不同地域/机构、同名实体与无证据。额外至少20个自然/显式配对视图作为从属重复观测，主计数以100个不同语义事实为分母，按事实组/来源家族报告，不能把同义改写当独立100样本。明确写明20配对是否进入总预测表及统计依赖，不得混分母。
只有当 S1-B 抽取器版本、prompt、UIE或Qwen模型revision、统一verifier、已封存validation schema/Gold权限、评价者身份、打分脚本与Resource Manifest 都满足时，才向Owner申请单次validation运行批准；不得由Go/NoGo通过自动解封。算法仅见 role-free `query+evidence`，输出先seal，Evaluator后解锁标签，失败与未运行项留分母，不重试、不换模型/阈值。
保持原验收门：答案值命中/answerable≥90%；`wrong/decided≤2%`（决定>0且不能all UNKNOWN）；另报严格字段/span/scope正确率、coverage、wrong/total、拒识误答率、false unsupported version releases、自然化分层、Wilson 95%CI和语义组bootstrap。指标分母与拒识逻辑预注册，不能为了通过而换定义。错误上界与统计功效仍须如实报告，100例零错也不证明总体≤2%。
建议新增安全guard：未证新版和无证据误答均为0；**该项是提案，需Owner明确采纳后才能作为新硬验收门，不能回填修改旧S1合同**。

### Gate 4：S2（未授权）
只有Gate3成功且Owner再次确认，才可以提交S2 A-I多毒/版本/可信源有无实验许可；仍须先冻结P0/M1/M2/M3和来源锚真实收据。S3/S4/S5依旧后续独立批准。

## IV. 科研严格限制

- RAGDefender的无额外LLM查询优势是真实公平比较基准；引入UIE/本地LLM会增加计算成本和安全风险。论文必须报告GPU-time、p50/p95延迟、批大小、峰值显存、token/吞吐、单位世界推理成本，不能宣称“零核验成本”。
- UIE 与 Qwen输出可能有流畅但未被原文支持的事实；值和spans必须通过确定性原文核验。合法版本/来源凭证必须来自独立T1注册或等效不可由攻击者伪造的链，而不是模型生成的引用、URL、时间等。
- 旧73合成数据只用于失败归因与development；旧D1/D2/D3/旧108及5090 Claims继续冻结。历史实验、负结果、个人审阅与HumanGold0不变。
- S1-B整体目标仅修复一个防御使能模块；无论抽取器多好，都不构成知识污染防御已成功，正式ASR/AnswerAccuracy/C3仍NOT_MEASURED。
- X-MADAM/MADAM结构与M2重叠必须在Related Work中正面披露。新颖性只能由可信来源/版本/时间适用的攻击者可控信号限制及对RD-zh公平的风险-可用性收益来验证。

## V. PO-MHEP 十二字段决策记录（仅设计选择）

1. `Issue ID`: `W1-OD-20261108-5060-S1B-B-DESIGN-17`。
2. Issue: Owner选择B，要求借鉴相关论文、规则与本地小模型公平比较，但明确禁止未单批批准的下载/调用。
3. Discovery: R2 K1-C、Owner16 S1_FAIL_STOP 后，S2–S5依旧停。
4. Facts: `OBSERVED_FACT`旧73合成31/61值命中、4/34已决定错误、29有答案UNKNOWN、2/12应拒识误答；`SOURCE_DERIVED_FACT`RAGDefender无直接 query-scope抽取；ACL UIE、PaddleNLP中文UIE与Qwen2.5-1.5B权重可查；`INFERENCE`若用已有结构抽取模型可减少基础模块重复开发，但不能推断效果提升；`UNKNOWN`许可证完整链、checkpoint revision与固定逐文件白名单、5060实际资源与真实安全收益。
5. Existing constraints: R1/R2/Owner16失败和历史不变、P0/标签隔离、S2–S5不解封、D2/D3不接触、5090 Llama2权限未获核验。
6. Why now: S1抽取是M1/M2/M3必需前置；纯规则自然中文失败已经实测，继续从零堆正则有高返工风险。
7. Downstream risks: 许可证、GPU/存储不闭合、独立验证集污染、模型幻觉/伪scope、成本/效率退化、新颖性过度主张。
8. Options:
   - `A_RULE_ONLY`: 修规则，无新增模型/权重成本，但自然中文泛化风险高；可逆；研究价值局限。
   - `B_RULE_VS_OFFLINE_OPEN_MODEL`（Owner选定作为设计方向）: Rule-V1/V2 vs UIE/小型指令模型，审计原文span/来源；需要具体checkpoint审批、独立测试，增加资源和延迟；只做设计可随时停止/切换；可能提高支持率但无效果保证。
   - `C_LLM_ONLY`: 直接弃规则，会引入幻觉与费用且失去廉价baseline，未选定。
9. Recommendation: 冻结路线B为待执行研究设计，先Gate0只读核源/资源准备，Owner单独批准一个模型资产后再批准本地开发调用，最终单次独立验证再批；用UIE作为首要轻量候选，Qwen1.5B作为次级对照。
10. Confidence: `HIGH`（路线选择与法律/实验风险识别）；`UNKNOWN`（具体模型是否适配、性能与增益）。
11. Owner required decisions: (a) 先选哪一模型及revision和权重许可/资源批准；(b) 谁提供真独立 validation/标注及Gold密钥边界；(c) 接受建议的未证新版/无依据误答=0为额外gate否；(d) development推理/单次validation实际预算与模型运行合同；未获逐项签署均STOP。
12. Allowed/prohibited: `DESIGN_ONLY`可整理文献、方案、只读远端与本地资源清单以及静态接口；**禁止**下载/安装/加载/推理任何新模型、联网外传、构造并占用S3、重跑或改Gold旧S1、访问D2/D3/5090、自动执行 S1-B 的科学试次、S2–S5和main合并。

## VI. 结束状态

`S1B_DESIGN_READY_FOR_OWNER_MODEL_ASSET_SELECTION / MODEL_DOWNLOADS=0 / MODEL_INFERENCE=0 / NEW_SCIENTIFIC_TRIALS=0 / S2_TO_S5_BLOCKED / AUTO_CONTINUE=NO`。
本文件未签发任何新增模型或验证许可；后续必须遵循PO-MHEP十二字段、唯一分支、固定SHA与Owner显式权限链。
