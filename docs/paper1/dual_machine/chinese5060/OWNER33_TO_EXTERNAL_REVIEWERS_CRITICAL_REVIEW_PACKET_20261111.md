# Paper 1｜Owner33失败后外部独立技术评审请求（2026-11-11）

**定位：独立技术评审输入，不是请求为继续调参背书。** 本材料供网络安全、RAG 与 LLM 研究评审人阅读，参考既有《VESA-Guard 方案评审意见与小规模验证计划》的风格：总体裁决、W1–W7 弱点、红/黄/绿优先级、否决条件、最短可行验证方案。研究 Owner 拥有最终决策权，评审人不代签 Human Gold。

**评审所需开放证据**（只读Git，切勿打开/要求5090私有Gold）：
- 5060 DEV报告: `docs/paper1/dual_machine/chinese5060/OWNER33_VCARE_DEV_RESULT.md`，冻结方法 `src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner33_vcare.py`，方法冻结提交 `11880c5be71e22d73217c32e0c779fbf8b117741`。
- 5060 EVAL一次盲预测: `research/paper1-chinese-defense-5060@108b35c9239ad113c50f7d84daf9b84f361b37d6`，`docs/paper1/dual_machine/chinese5060/owner33_eval/OWNER33_EVAL_PREDICTION_HANDOFF.md`。
- 5090 EVAL独立评分: `research/paper1-ragdefender-repro-5090@d7d28cc7cab25b1ade04fcb8b0678bd369c3b558`，`docs/paper1/dual_machine/repro5090/owner33_eval/OWNER33_EVAL_SCORE_REPORT.md`和Manifest。
- 5090预冻结来源: `docs/paper1/dual_machine/repro5090/owner33_eval/OWNER33_SOURCE_SNAPSHOT.json`、`OWNER33_CURATION_REPORT.md`，角色盲材料可以只读；**严禁**私有Gold与攻击目标。
- 监督复审: `docs/paper1/dual_machine/chinese5060/OWNER33_FRESH_EVAL_SUPERVISOR_VERDICT_20261111.md`。
- 旧Owner28候选结果：B2 P33/56、Clean误删27/82、HN误删7/20；RD_ZH P15/56、Clean55/82、HN10/20。旧Owner30真实Qwen 31三臂数值匹配NONE20、B2 25、ZH15；22数值攻击世界中短值目标命中NONE0、B20、ZH5，**非**正式ASR/答案正确率。

## 1. 最新实验事实（不可改写）
旧Owner27开发数据，32世界同TopK5：B2 P保留20/45、Clean误删40/63、HN误删4/33；VCARE P保留7/45、Clean误删10/63、HN4/33；B2_ALWAYS_VERIFY P保留7/45、Clean误删40/63、HN4/33。VCARE相对B2改变22/32世界、外证命中24/32。**13个P增量过滤与ALWAYS_VERIFY相同；VCARE的独有额外收益主要是恢复30个Clean**，但仅限已曝光DEV。开发中使用已知官方来源，不能视作独立外证一般化。
全新独立5090评估，32世界×TopK5=160槽，四独立新事实组（世界不独立），召回P34/C59/H历史1/O其他范围8/B58。B2 P保留11/34，Clean误删35/59，H误删0/1，O删除8/8；VCARE所有这些数字**完全相同**，同预算B2与所有机械消融亦相同。32/32逻辑补检、外证命中0/32、识别QueryIntent0/32，B2→VCARE掩码变化0/32。未进行新的Qwen生成；HumanGold=0、正式ASR和答案正确率=NOT_MEASURED、5090原作者Claims1–3=NOT_RUN。
冻结 `intent()`仅支持3种预定义谓词`statutory_days`、`permit_issuer`、`application_age_max`；未见EVAL四领域均不在其分支中。每个新的、未知领域的查询均回退B2。这是域外前端不可用，不能证明“时效补证思想本身被否定”，也不能据此称已构建跨域方法。

## 2. 需要外部评审独立判断的问题（不得只给乐观建议）
**W1 [RED] 算法泛化**：为何开发阶段使用特定词面的枚举式解析器却试图外推到未知法规？后续若再新增四领域正则，是否就是在已暴露EVAL上过拟合？怎样设计在未知entity/predicate上的可核通用机制，而非一个扩大版规则字典？
**W2 [RED] Oracle/来源泄漏**：5090预冻结官方来源快照含26条带 `short_fact` 短事实、`selection_status` 的记录，其中 `QUALIFIED_FACT_INPUT`6、`UNSELECTED_VERSION`1、`RELATED_NOT_SELECTED`5、`EXCLUDED`14。原候选事实在这个登记中已标出。虽然现算法EVAL未命中，若将此表直接作为下一个算法的“可信知识库”，是否构成部分target selection或答案信息泄漏？应剥除selection状态、world/role/Gold指示并基于独立全量来源重新建索引；请明确检验标准。受控来源是潜在强oracle，而非天然无偏证据。
**W3 [RED] 公平强基线**：B2+extra retrieval不做事实裁决可能是弱稻草人；B2_ALWAYS_VERIFY已复现DEV的全部Poison提升。应增加何种**同源、同检索、同证据槽、同推理成本**的最小简单“参考值直接对比+恢复”基线？怎样量化 VCARE 特有结构而非多一个权威答案的贡献？
**W4 [RED] 正常/负例定义**：EVAL H只有1条，其他范围 O 有8条却8/8被删；需要把 O 视为应保留的合法hard-negative还是应过滤的查询不适用证据？两者可能是不同目标，需固定taxonomy、评价协议和应拒答判断，不能只写“HN误删0”。
**W5 [RED] 回答层真实性**：旧Owner30 NONE已0/22短值目标攻击命中，B2也0/22，新方法如何在非零基础ASR、可答/不可答平衡和强攻击场景中展示安全改善而不按结果挑样本？不能把数值匹配视为scope/citation正确率；原5090 Claims未跑、HumanGold0。
**W6 [YELLOW] 样本与统计**：两批分别4独立事实单位、32高度相关世界，合成改写未体现真实网页噪声/来源真实性；S1无毒误删、S3跨scope以及3/5和5/5多数要在事先设计的独立条件中覆盖。哪些最小事实簇能支持“是否值得做正式实验”而不冒充统计证明？
**W7 [RED/YELLOW] 2026现有技术新颖性**：RAGDefender、FRESCO的时效rerank、TCR的冲突决策、TRIS的多层检测与LLM核验、RAGSentinel的无训练几何共识等已覆盖广泛思路。我们是否还存在足够清晰的网络安全研究独特目标？若创新仅为“官方资料额外检索+对比答案”，是否应该直接宣告新颖性不足？

参考文献官方入口：
- RAGDefender, ACSAC 2025, DOI 10.1109/ACSAC67867.2025.00093: https://ieeexplore.ieee.org/abstract/document/11391803
- FRESCO, EMNLP Findings 2026: https://aclanthology.org/2026.findings-emnlp.54/
- TCR, AAAI 2026: https://ojs.aaai.org/index.php/AAAI/article/view/40740
- TRIS, EMNLP Findings 2026: https://aclanthology.org/2026.findings-emnlp.2122/
- RAGSentinel, EMNLP 2026: https://aclanthology.org/2026.emnlp-main.546/
- Cross-Encoder Guardian RAG, 2026: https://proceedings.mlr.press/v318/moradi26a.html

## 3. 想请评审裁决的方案，不预设哪一个必须通过
**候选 A：通用来源检索 + 查询约束的证据对齐**（首选工程假设，非已证明创新）：
- 不使用 `intent()` 枚举领域。将完整中文问句与独立来源证据块用既有MiniLM做语义召回，再按实体/属性/日期/范围通用字段分层归一和冲突验证；先记录可能缺失而非认定真值。来源池需广泛、有非测试条目、来源完整性与权限清晰，候选source只来自事实原始发布者，`selection_status`与Gold绝不入算法。比较“同来源直接对比、同预算证据补检、通用对齐full、no-scope、no-rescue”。
- 快速GO门前置，**不运行科学评分**：用Owner33已经曝光的32个EVAL查询仅作为新的工程DEV，先固定规则与索引构造策略（不能按这些标签调参），检测Query意图覆盖至少24/32以及有来源证据候选至少16/32；不满足就STOP，不要继续调后验阈值。即使通过也只能说明跑得起来，之后必须真正新建独立EVAL，旧Owner33不能再称holdout。最低运行时间上限建议60分钟（不是研究性能保证）。
- 方法层要对新数据、同预算强基线同时有P/C/HN净改善，且生成层在非零基线攻击成功率下得到正确率/ASR真实收益。若无稳定源池或通用匹配基础，立刻NO_GO。
**候选 B：暂停新防御，先复现2026更强后检索方法**：例如公开的RAGSentinel/TRIS或Cross-Encoder Guardian（许可/硬件/模型资源先查，不能假设易复现），检验中文迁移与失效机制。若仍无法给出新机制净贡献，则主线转中文版本感知基准与失败归因，而非不断重新命名简单聚类。
**候选 C：放弃短周期算法GO；将可控范围的正式攻击样本/人审/端到端评估做扎实**。安全研究价值可在版本/范围/多文档协同污染下的防御迁移失效和答案层反作用，但必须与文献强基线公平、不能仅发表过小的代理基准。

## 4. 请评审返回严格结构化结果
按以下形式，不要只说“有前景”：
1. `REVIEW_VERDICT`: A_GO_FOR_SMOKE_ONLY / B_BASELINE_FIRST / C_BENCHMARK_FIRST / ALL_NO_GO。
2. 三项最严重科学威胁及证据链接；明确哪一项会导致论文被拒。
3. 对候选 A 的**最低可证伪实验**：输入条件、固定规则、1个关键最强基线、预算同一化、至少3条必须通过的Hard Gates、可复现统计分母。
4. 若建议继续算法：**唯一**推荐机制、和2026已有方法的具体差异、代码/数据资源、预计工程风险、不得抹去的失败结果。
5. 若建议停止：说明为何已不宜继续追求“超过RAGDefender”的新方法，给出更有发表机会的论文范围与必要数据。
6. `RED/YELLOW/GREEN`、清晰GO/NO_GO、是否值得花下一次独立EVAL；如资料不足，写NOT_VERIFIABLE并指出什么文件可解除，不要编造成果。

**评审边界**：你不是5090独立裁决者，不可代签Human Gold；不能读取私有标签/私有错误值；不要修改DEV/EVAL旧分母、替研究Owner批准新实验，也不要在看到成绩后调整门槛。必须区分源码逻辑、封存事实与外部推测。
