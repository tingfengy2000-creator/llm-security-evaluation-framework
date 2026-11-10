# Paper 1｜Owner26：中文无锚知识污染防御快速对照（D1-40、Qwen API ≤USD3）

**PO-MHEP ID** `W1-OD-20261110-5060-D1-QWEN-NOANCHOR-26`  
**Date** 2026-11-10 JST  
**Status** `OWNER_EXPLICIT_APPROVAL / D1_INTERNAL_FROZEN_COMPARISON / QWEN_API_USD3_CAPPED / NOT_YET_EXECUTED`  
**Branch** `research/paper1-chinese-defense-5060`；Owner25已核远端 `e50bd630cceaf0cacdf41194ea59fc60415a033e`，真正开工时以Git远端HEAD为准。  
**Owner原话要点**：“Paper 1｜Owner 决策：1–2 天内验证 VESA 能否在中文数据上胜过 RAGDefender”，“本轮批准”固定`qwen3.7-plus-2026-05-26`、temperature0做片段抽取与直接验证、≤USD3；允许已有本地Embedding补RD，检验7臂；Pilot12开发最多修改一次；冻结后其余28事实组一次评估。Owner还明确允许无锚M1-safe/M2-vote作为**研究候选**，自称来源或版本不得直接增加信任；失败转中文版本敏感污染基准+RAGDefender中文失效分析。本授权特指此范围，不解封D2/D3/8组HOLD、不批准正式生成或主线合并。

## 十二字段

1. **Issue ID**：`W1-OD-20261110-5060-D1-QWEN-NOANCHOR-26`。
2. **Issue**：在中文D1开发数据上比较无锚一致性恢复与答案分组投票是否比RAGDefender中文迁移有安全—可用性净收益，并比较同一Qwen模型直接核验作为成本/精度强基线。
3. **Discovery**：Owner25合成64 DEV+32 HOLDOUT，Oracle联合Poison保留32/54→7/54、Clean误删30/78→15/78，相对随机固定父掩码、**不是同世界RD**；真实D1可信锚0/180、Rule-V2正文部署0/160，Owner25裁决路线调整。`FEASIBILITY_NO_GO`等历史保持。
4. **Observed / inferred / unknown**：
   - `OBSERVED` 签署D1-40数据包登记**40事实组×3候选角色=120世界候选**、13家族；Pilot12早已固定12组×3=36检索世界，36×TopK5=180片段，另有**28组×3=84个拟建世界**。D1-40及其标签作为DEV_EXPOSED，不是新的独立测试/正式HumanGold；独立声明`HOLD8`为额外排除对象。
   - `OBSERVED` 原D1 Pilot12 B2已召回候选Poison/Clean/HN=10/10/9，删除2/10、4/10、2/9；RD-zh删除4/10、5/10、4/9，部分TopK候选未召回不能算过滤成功。
   - `SOURCE_DERIVED` 阿里云官方模型卡确认固定快照`qwen3.7-plus-2026-05-26`真实存在、结构化输出支持视所选地域/模式而定。必须读取该地域官方实时计价、兼容参数和合法endpoint，而不是猜测；混合思考/JSON模式兼容约束需单独工程探针。
   - `INFERENCE` 先把模型抽取和索引映射可靠性固定，后做同世界7臂，既能得到候选级安全收益，也能检出无锚多数投票的自证失效。
   - `UNKNOWN` 28组可否按原版本/索引/查询身份构造公平TopK5，原证据向API跨域传输权限，商业API端点/余额/地域/最大token/思考行为、真实成本、最后候选级增益。
5. **Inherited contracts**：AGENTS/PO-MHEP、旧S1 FAIL、R2 K1-C、Owner20规则NO_GO、Owner25 `BASELINE_INCOMPLETE`与无锚边界不可覆盖；原108/Qwen生成实验不重跑；`D2/D3`、`HOLD8`和5090 Claims严格禁；无正式AnswerAccuracy、Targeted ASR或HumanGold；P0真实可信源限制不得虚构，若无锚恢复则标明是一条**实验性P0放松（Reinclusion Risk）**，不将其描述为证明安全。
6. **Why now**：Owner明确转回中文防御方法主线，希望快速拿到足以决定继续/停止的同数据RAGDefender对照证据；本次测试仅需本地已缓存Embedding和≤USD3在线模型，且后续正式评估另立合同。
7. **Risks**：无锚M1可能将同假答案污染放回，M2多数可被3/5、4/5或5/5伪造操纵；自称来源/版本可能欺骗；Qwen同为提取与核验可能相关失误；角色标签/目标被泄漏造成幻觉式正结果；额外28组的TopK没有历史索引冻结，查询变化和检索遗漏混淆；商业接口数据外传/版权与计费越界；开发选最佳臂后再宣称独立测试；直接Qwen一world比片段抽取五次成本可能低很多。
8. **Options**：A `APPROVED` 有界7臂同TopK D1内部分组开发+一次性28组后冻结对照（适用快速方向裁决，不是正式论文证据）；B先真实公开有锚来源独立采集（更稳但慢）；C继续纯规则或Windows环境（既有负证、低科研收益）。Owner选A并保留失败后B的基准路线。
9. **Recommendation**：不将无锚一致性/票数偷称可信证明。以最强RD-zh和QWEN_VERIFY公平比较，所有7臂同一份有序TopK，不改索引和Embedding；显式报告P0放松引起的Poison放回、少数派误杀、Clean/HN代价。
10. **Confidence**：高于模型ID存在与D1-40登记；中于工程基线公平可复现；关于M1/M2确有收益、强基线能否胜过、是否可发表均为未知。
11. **Approved scope**：
    - 固定百炼`qwen3.7-plus-2026-05-26`、`temperature=0`、关闭联网搜索/工具/外部检索，**只在确认该接口有效且所选模式真实支持时**计费调用，最多2个使用无隐私虚构文本的接口握手请求，计入USD3；如`enable_thinking=false`/JSON不兼容，允许在开发开始前把该snapshot调为官方支持的有界thinking模式和文本JSON解析一次性冻结，记录差异；禁止换模型/地区/费用套餐来回试，必须新许可。
    - `ALLOWED_QWEN_EXTRACTION=YES` 每`(question, original_topk_chunk, frozen_prompt, model_config)`唯一哈希输入一次预测，规范化值/单位/类型/引用span/版本/时间/条件；显式`NO_ANSWER`与`UNKNOWN`、否定/自相矛盾；原文字符与UTF8半开span逐字回指。无原文证据即UNKNOWN而非Qwen自我证明。输出角色盲。
    - `ALLOWED_QWEN_VERIFY=YES` 每世界完整TopK一次（不附Gold/role/目标），指出待删除索引和可见原文证据理由，严格schema，独立API费用按一world计算。
    - `ALLOWED_RD_BASELINE_LOCAL_ENCODER=YES` 只用已存在且identity pin通过的本地Embedding缓存，B2与RD-zh固定来源、向量只编码一次共享；无新下载、无替代预训练模型、无参数临时调优。RD-zh字符二元组是基线中文迁移，不是创新点。
    - `ALLOWED_D1_PILOT12_DEV=YES` 既有12组×3世界=36，至多原始方案+1次改进方案，所有开发中间结果保留。选择最优方法只能基于DEV、并冻结首要VESA arm和阈值。
    - `ALLOWED_D1_REMAINING28_ONE_SHOT=YES` D1-40减去Pilot12固定组，预先定义28组×3=84世界；无原TopK的，只有核原检索协议/查询冻结/原始Index/背景/候选注入方式后才能用**固定索引同协议新建并封存**；角色盲输入和评分标签分进程；**只做一次VESA及7臂预测后封存，再独立揭盲**。这些仍是D1内部评估，绝不是独立新基准或正式泛化。
    - `D1_HOLD8/D2/D3/5090=LOCKED`；`PAPER_FORMAL_S2_S5/NEW_GENERATION/ASR/ANSWER_ACCURACY/HUMAN_GOLD=NOT_AUTHORIZED`。
12. **Hard gates/stop & reporting**：
    - **外传门**：Owner已批准Qwen API用途，但对每个具体D1来源/原文仍需**数据出境/版权/服务地域、敏感信息与传输许可**可追溯裁决；原先Owner20没有外传批准不能被本次误解为原始第三方内容可任意上传。无合法证明的D1原文**不得上传**，可先跑本地RD、在纯虚构文本做API连通/抽取诊断，标D1_API_BLOCKED，并立即报告真正阻断。API key仅从既有受控ENV，不能记在Git或日志。
    - **接口门**：官方确定唯一地域endpoint、snapshot、实际计价/Token、FX折算上界、余额/账户与单请求max_output/ thinking预算/超限即拒绝。总新增请求**USD3绝对上限**，且保留历史 USD25/28/30 门（本轮更严），低于USD2.40预警、USD2.70只允许已预留合法请求收口、USD2.85禁止发起新请求；硬停止不超过USD3，不能等账单后才发现超额。所有尝试包括错误请求计数、失败也不隐形重试；费用使用**最大可能费用（已付+在途预留+未结风险）**控制，不信任estimated_total低估。调用数、input/output/reasoning_tokens、CNY/USD单位与计费tier、median/P95延时均记录，预估全批超USD3则优先冻结较小**预注册平衡分母**或停止，不能临时选择有利子集。
    - **基线门**：相同TopK原顺序、原rank和内容；无本地固定Embedding或模型hash drift=停止比较，不允许用Owner25固定掩码代替B2。若28组原协议缺失/不能按角色盲构建索引，也停且仅报告36 DEV诊断，绝不声称84世界完成。
    - **安全**：M1_SAFE按已保留唯一答案匹配放回已删同答案句，但**P0无锚恢复豁免=已授权风险臂**，只作为候选评估，不将相似/多数/自称源升为独立可信来源。M2_VOTE按已冻结归一化答值分组删少数，转载及完全重复文本算同一传播源；不可依赖自称URL/机构作为独立源票数，无法可靠区分改写传播时记录`SOURCE_CORRELATION_UNKNOWN`；未证版本声称不得推升信任，保留跨scope/合法历史变化的冲突诊断。必须统计3/5、4/5、5/5和错误多数及同一值异scope、文字自相矛盾案例，不能仅总体平均掩盖放毒。
    - **比较7臂**：`RD_B2`,`RD_ZH`,`QWEN_VERIFY`,`RD_ZH+M1_SAFE`,`RD_ZH+M2_VOTE`,`M2_VOTE_ALONE`,`RD_ZH+M1_SAFE+M2_VOTE`。七臂同一query×TopK5和评价分母；每臂独立部署的成本应含Qwen抽取5段所需Tokens及调用费，不能只按物理共享缓存分摊开销；Qwen直接核验每世界1次，清楚区分逻辑方法成本与物理实际调用成本。
    - **预注册判定**：DEV挑选的单一VESA主臂在84世界对应的已召回候选上相对RD_ZH `Poison retained(candidate)不增`且`Clean false deletion至少减半`；并`Poison retained/Clean false-delete/HN false-delete各不劣于QWEN_VERIFY`且**总Tokens严格更少**，记`GO`。符合相对RD_ZH但不满足直接Qwen全部条件为`PARTIAL`。未达到相对RD_ZH核心条件为`NO_GO`。`GO`也只是D1内候选级方向信号，不证明正式ASR；另单列自相矛盾Poison、合法版本/scope误删、恢复Poison、拒识和“自证多数”失败。
    - 数据/身份/报价不闭合、预算上限不可证明、Qwen传输权限不合法、错误模型版本、泄漏评价角色或目标、重跑84世界、变更算法/阈值/Gold/TopK、改变原先B2/RD-zh历史，立即`STOP`，证据不隐瞒；整批输出`GO/PARTIAL/NO_GO/INCONCLUSIVE/BLOCKED`和数字分母、费用、SHA/Git证据及论文路线单一建议，`Auto Continue=NO_AFTER_BATCH`。

**特注**：Owner本轮的无锚候选与此前P0无锚不可恢复的强安全策略确有实质冲突；这里将其定义为新获批的**科学候选与安全压力臂**，并非将旧P0证据涂改成已经支持无锚恢复。论文若要主张安全，必须拿独立非攻击者控制证据或显示在攻击者可控多数情况下仍满足限制，不能仅靠本轮无锚票数实验宣称。
