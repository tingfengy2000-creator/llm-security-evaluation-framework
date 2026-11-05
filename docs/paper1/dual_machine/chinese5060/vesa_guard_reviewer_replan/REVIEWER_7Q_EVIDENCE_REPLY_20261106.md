# Paper1｜外部评审七项追问的证据答复与S0优先级调整（2026-11-06 JST）

**性质：Git来源核实 + 明确证据缺口；非新模型/算法试次，不是Human Gold或新Owner付费授权。** 5060固定分支`research/paper1-chinese-defense-5060`，核验时HEAD`aaa167d06be83f1bcbdb2548d1d95ef1e1933cdb`；5090固定分支`research/paper1-ragdefender-repro-5090@eef08cdf08fee67169149b71d25fa9c4a14d9043`。只用仓库脱敏证据；**D/E私有TopK完整正文、攻击构造原稿、真实审阅者签约与会议选择不可从本记录推定**。

## Q1（最高优先）：B2版本与中文迁移范围

**已核的事实现况：**
- B1/B2共享未修改的SecAI-Lab/RAGDefender checkout `ba2a17efba165d45409114df2d70b030ade1e1b8`；5090独立Git审计确认其`main`相对`v0.2.0`只多一个`.github/workflows/codeql.yml`。B1是`B1_PUBLIC_V0_2_PINNED_MODEL`，B2仅向库注入另一固定SentenceTransformer对象，并不是作者ACSAC artifacts严格复现。
- B1 Encoder=`sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`，384维、max_seq_length256、Transformer/Pooling/Normalize；B2 Encoder=`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2@16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`，384维、max128、Transformer/Pooling。两者model package不同，不可把所有差异仅归为“中文”。
- RD `single_hop=true`,`p=2`,`m=5`、原scikit TF-IDF默认词边界及**英文停用词**、层次聚类`n_clusters=2`、Stage2删除频率、tie策略和错误语义保持完全不变；**没有中文分词、停用词或m的适配**。Query在当前检测器内部不参与决策。B2使用多语言Encoder并不等于中文Tfidf已正确。
- 原作者版本说明`v0.2.0`修正Stage2索引被误删，5060实际绑定该修正后代码系；因此不能以“B2基于旧版必然包含v0.1.1尾部截断bug”为事实。**仍缺直接的、静态受控删除indices对比（最终结果与原库的indices逐个校验，以及v0.1.1历史实现差异）**；首先只读比对实际运行的库源hash与`run_chinese5060_b12.py`调用路径，是否有任何兼容层覆写；确认后才决定是否需要新实验臂，不可重写历史B2结果。
- Pair01 36/36两臂执行，Stage1`n_adv`分布B1:{1:6,2:18,3:12}、B2:{1:6,2:18,3:9,4:3}。Stage2频率同分/移除集合有可核关联但cluster/pair-set中间trace缺失，不能把B2 Clean误删4/10归咎于Stage2历史bug。
**证据：** `W1_5060_FAST_B_PAIR01_RESULT.md`, `fast_b/pair01/RUN_MANIFEST.json`, `fast_b/pair01/ASSET_MANIFEST.json`, `fast_b/pair01/MODEL_AND_DIAGNOSTIC_OBSERVATIONS.json`, `W1_5060_FAST_C_READONLY_FAILURE_ATTRIBUTION_REPORT.md`，以及5090 `implementation_difference_audit.md`。以上均为已核Git记录，不是此次新试次。

## Q2：D1世界TopK5的另外四条究竟是什么？

**已核设计：** 每个事实组固定相同Query，Poison/Clean/HN三个**独立且互斥的索引世界**；每世界为`1个目标候选文档 + 同一套18份角色盲背景文档`，总共19份文档；分96 tokens/重叠16进Chroma；P2每世界752个chunks、TopK=5。在召回目标候选的29/36世界中，每个目标仅命中**1个chunk**，故其他4条TopK来自该世界背景库；在7个候选未召回的世界中TopK全部来自背景库。**每个实际TopK的4条具体全文、source_id、url、发布机构/时间需要从私有`TOPK_PRIVATE.json`按已冻结P2快照生成受控表格，当前公开仓库无此全文。**
Poison 10/12候选进入TopK；G0在Poison 11/12世界能看见至少一个**暂定参考来源片段**，G1=8/12，G2=9/12。这只证明存在引用覆盖线索，不能证明足证性、独立可信来源或模型答案正确。完整排序统计：目标候选首rank 1有25世界、rank2有3、rank4有1，MISS7（此分布跨全36、非Poison单独统计）。
**必须补一张受控的`D1_WORLD_TOPK_BACKGROUND_MATRIX_PRIVATE`**，字段：opaque_world_id、original rank C1..C5、source_document_hash、content_hash、candidate_hit_and_rank、role-blind background doc class、source_url/agency/time是否真已验证、是否含可被独立核验的参考事实span；标签与参考证据有效性只能在Reviewer独立后封存端合并，公开Git只能输出12/36汇总与hash。**不将私有TopK正文和角色-候选映射直接交给新算法开发或外部未授权评审人**。

## Q3：Poison如何构造？单条还是批量？是否模仿PoisonedRAG？

每个Poison世界**仅嵌入一个Poison候选文档**（另18固定背景），没有“同一世界插入3–6篇同样攻击目标假页”的批量投毒设计；在已召回的Poison世界内，被标候选也只占1个TopK chunk。11/12参考来源可见（G0）说明它与正确证据可能共存。该D1场景更接近`single-candidate fact contamination`，不应叫作`PoisonedRAG multi-page cluster attack reproduction`。
目前不能断言所有背景完全无事实错误，也不能断言污染候选文字“采用/没有采用PoisonedRAG话术”：需私有原F5构造协议/候选原文/签署链做**只读结构特征核验**（是否多种改写、指令句、错误值、版本冒称、注入位置、检索rank、文本相似度），禁止猜攻击目标；不要因仅1候选就声称RD“必然无效”，因为与背景的自然相似也会触发聚类。
这一事实支持**单条污染与正确/相关背景竞争的场景价值**，但外推到多条强攻必须在新构造S2/S3的E/F/H独立测试。

## Q4：来源metadata是否曾记录，只是没进入packet？T1可否实施？

已有来源登记链：15个法规规范快照、2个官方解释/网页、29个冻结D1候选；46/46实际发出文档身份可追溯。来源恢复私有矩阵能指向**原URI或候选构造根证**，但并非46/46拥有可核合法来源署名/发布时间/采集身份。29候选只证明从原D1签署候选到P2字节链闭合，**不是外部可信源**；17官方快照也未自动拥有T1独立证据权限。
B1/B2生产算法可见的Packet每chunk schema严格只有`{chunk_id,text,content_hash}`，外加worldID/query/snapshot hash；**没有URL、发布主体、发布日期、可信采集时间或来源签名**。因此`T1_READY=NO`，`EXISTENCE_OF_UPSTREAM_METADATA=PARTIAL_AND_NEEDS_PRIVATE_AUDIT`。
如D/E旧采集保存了真实source_url/publisher/issuance/effective/expiration、外部下载或可信采集hash/签名、并能通过P2 parent_doc_id回连，S0可以**只读验证**`verified_anchor_coverage`。未来要启用T1，必须以**额外实验臂及相同信息权限**给B3/B4和新方法，不能在保持“只用packet”对照下偷偷把真实来源信息附加给VESA，也不能把不可信网页的自称机构视为P0正向证明。

## Q5：5090 Claim进度和Stage2修复

5090当前HEAD `eef08cdf08fee67169149b71d25fa9c4a14d9043`、`repro5090/handoff.json`：Claim1 PoisonedRAG、Claim2 Tan、Claim3 GARAG全部`NOT_RUN`，`sample_n=null`，ASR/QA`NOT_MEASURED`；不能报告差距。原作者源码upstream`ba2a17ef...`已钉，发现官方`artifact_acsac`在RTX5090 sm_120上因CUDA核不可运行；`artifact_acsac_compat`用新PyTorch兼容栈，不可称作者原环境。Llama-2权重权限尚未获批，下载/运行Claim需新Owner批准。
独立静态审计证实官方v0.2.0 changelog报告Stage2索引修复；**v0.1.1 vs v0.2.0实际Before/After运行数值未测**。本分支B2使用v0.2.0谱系库，并无已知旧尾部截断代码。

## Q6：Human Gold谁审、何时完成？

当前有效Reviewer签署/可合法分发渠道**没有确认**。尚有12卡、38事实原子、16份来源的**未签署盲审包**，但未发布给审阅者，HumanGold=0。现行提议为**两位真正独立的人类R1/R2**先各自盲审并签署，分歧交**第三位独立仲裁者A**，由Owner核法务来源、身份/利益冲突/独立性和合法分发；Algorithm Worker不能读取其答案或帮忙签署。**预计完成日期未知**，只能在Owner确认审阅者与时间安排后提出排期；审阅完成还需另核攻击构造target及C3。
依据`adjudication/PILOT12_INDEPENDENT_HUMAN_REVIEW_HANDOFF_PREP_V1.md`、`vesa_guard_v02/VESA_V02_OWNER14_RESULT.md`。

## Q7：目标会议、截至日

**尚无Owner签署的target venue及投稿截止日期**；不能臆测是ACSAC/CCS/USENIX/NDSS，也不能把2026旧轮次deadline当2027投稿日期。待Owner在一个明确决策中确认目标venue与备选，届时核对应年份官网`submission deadline/AoE/format/artifact policy`并反推S2/S3样本量、HumanGold/5090严格复现/外部baseline与消融工期；当前不以不明deadline倒逼降格宣称。

## 评审补充四条：已经对齐或须修订

1. **S0-00先版本及Stage2代码**：顺序应为`upstream_sha/tag -> B2 wrapper -> Stage2 fixed index vs legacy tail truncation -> observed removed_indices -> 中文TF-IDF实测`。无需直接运行新模型即可静态验收；若怀疑错误，保留旧B2结果，新的修复版另建可比基线，**不能以修bug作为方法创新**。
2. **世界隔离只针对D1组内Poison/Clean/HN互斥索引**。新S2/S3 A–H场景则**必须**有同TopK的Poison+Clean混合（D–H），以及H全Poison变体；二者是不同实验设计约束，不冲突。
3. **S4的安全性检验能力有限**：旧B2仅删掉2/10已召回Poison候选，因此“新Poison保留≤8/10”不足以形成强安全证明。S2/S3 D/E/F/G/H是主要候选级安全压力证据，S4主要检验在D1中避免Clean误删及安全退化，HumanGold之前不能得正式ASR。
4. **2.5pp与40组的数学口径**：若比较分母真的都为40，且用**非严格`<=2.5pp`**，`1/40=2.5pp`，所以并非自动“0次额外成功”，**最多允许1次净新增**（其它变化/paired结构需要记录），但在**基线ASR=0时Owner规则明确任何新成功=0容忍**；若分母不等于40、ASR分母只算候选召回、或是CI非劣界则不能照搬`1/40`。正式需以同一个固定分母、paired误差、置信界和Owner具体判据执行。
5. **B4核验调用降低≥30%**：本候选在S0–S4纯本地，无额外Qwen判别器；如B4确实>0个Verifier call，本方法额外Verifier调用为0，可实现100%**Verifier-only count**下降。但**总商业API调用量/全部成本减少≥30%尚无实测**，需把B4每个chunk核验次数、生成调用、cache/ABSTAIN影响统一计费/分母。T1/T2证据不同不能冒充纯计算优势。Zero-verifier claim要跟低计算时间/内存及更完整文本解析方法的CPU成本一起报告。

**下一优先级：** 5060受限`S0-EVIDENCE-ONLY`只读D/E，做1份实测B2来源与Stage2核验、原D1 TopK私有组成矩阵（不公开原文）、单候选构造统计与source URL provenance可用性报告；5090按独立分支返回自身Claim最新RunManifest。没有这些证据，不要提前宣称RD原论文有缺陷或S4改进达成。双方不运行新模型、检索或更换数据。
