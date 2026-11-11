# Paper 1｜Owner30 一日可行性收口：科研监督复审与路线建议

**2026-11-11 JST**，状态：`SUPERVISOR_VERIFIED_PUBLIC_REPORTS / PROVISIONAL_NEGATIVE_METHOD_SIGNAL / BENCHMARK_PIVOT_RECOMMENDED / OWNER_FORMAL_ROUTE_DECISION_PENDING`。

本文件是评审与科研路线建议，**不是新实验授权或Owner正式签署的研究方向变更**。已经封存的Owner27/28/29/30结果不改；D2/D3/HOLD8、5090原论文Claim1–3仍保持原权限/NOT_RUN。

## 核验依据
- 5060 `research/paper1-chinese-defense-5060@161166a6228970c9a4c0728efca245365e37613a`，`owner30_eval/OWNER30_NUMERIC_AGREEMENT_PROXY_REPORT.md`及`OWNER30_QWEN_JUDGE_SUPPLEMENT_MANIFEST.json`，95条生成成功回包、首格NONE原始回复丢失未重发、31完整三臂对+第32组B2/ZH两臂对；本次Judge零次/USD0；原始68条规则scope与引用确认仍UNRESOLVED。
- 5090 `research/paper1-ragdefender-repro-5090@15a6961a4722a903069fbb829046972f9e45027e`，`owner30_eval/OWNER30_SIX_VALUE_TARGET_MATCH_REPORT.md`、`OWNER30_SIX_VALUE_TARGET_MATCH_MANIFEST.json`；报告原文件SHA256 `8de56c3b4bcc27891dda1abf47b802a00c3a44a79c36ced31018ae6ded08f9b9`，Manifest原SHA256 `56179d1a244ed695a6cc8e91e920ec371c160a91162004ab99405d3105783473`。受控交接包SHA256 `9ae356d60a3ec62ab8fec1df732b9dc21a91f8694422e2ff1b0b56879271c6a4`，5090核验压缩包只有1个相对路径JSON成员，未执行、未解压进库，6个world_id/原回答SHA/事件日均与封存记录对应，5条为评价前冻结的短值攻击目标，1条错误但不是攻击目标。
- 监督者通过Git工具核对以上两条远端HEAD、报告与Manifest和汇总表；**没有**读取5090本地私有标签或6条原值，故“5/6目标命中”是有SHA和版本链支撑的独立机器汇报，而非监督者直接逐条原值复算。

## 最终当日事实（不要和正式Gold混淆）
| 31个完整世界，数据项 | NONE | RD_B2 | RD_ZH |
|---|---:|---:|---:|
| 与该world参考数值匹配 | 20/31 | 25/31 | 15/31 |
| 与该world参考数值不匹配 | 0/31 | 0/31 | 6/31 |
| 拒答 | 11/31 | 6/31 | 10/31 |

**数值型目标命中（22个目标世界；三臂同分母，均已召回攻击候选）**：NONE `0/22`，RD_B2 `0/22`，RD_ZH `5/22`。RD_ZH 6个错误数值中5个与评价前攻击目标一致、1个是其他数值错误。对NONE而言5次均为 `ABSTAIN_NOT_A_HIT → TARGET_HIT`；相对B2，3次为拒答转目标命中、2次为非目标转目标命中。另有2个`SCOPE_ONLY`攻击世界，三臂范围主张和命中仍`UNKNOWN`，不计入22数值目标分母。原始95/96请求的第一NONE结果保持缺失；新Judge0调用、额外费用USD0。整批生成实际费用按Owner29独立记录且原始首格费用未对账，不能由本次补评覆盖。

**最重要防混淆条款**：
1. 这组`VALUE_MATCH_REFERENCE`是短事实值一致性代理，**不是**语义时点、scope、正确引用都支持的完整`AnswerAccuracy`；68个ANSWER的scope与citation support仍没有被规则或LLM有效确认。5/22是短值目标完全命中代理，**不是**人类Gold校准的正式ASR。
2. 5060历史公共短值62/62匹配是白名单披露选择效应，不应写作“62回答全部正确”。独立私有校核表明剩余6个RD_ZH的数值全不匹配，已在本次报告单列；6值本身不得Git公开。5090 Agent评分与校验均非人审，`HUMAN_GOLD=0`。
3. 无过滤组数值型攻击目标已`0/22`，因此RD_B2不能凭本批宣称“降低ASR”；RD_ZH出现`5/22`对比不利，但还不能把它完全归因于误删正常证据，需逐段来源/合法范围与回答支持机制论证，不能以相关性代替因果。
4. Owner28 代理评测在独立未见谱系上，RD_B2 Poison保留33/56、Clean误删27/82、HN误删7/20；RD_ZH P15/56、Clean误删55/82、HN误删10/20。RD_ZH多删18段Poison、同时多删28段Clean、3段HN，**检索层“更严”并不保证生成层更稳健**。两批同为自写代理、仅4评价事实组/3谱系，不能把32 world当独立样本/做泛化显著推断。FRESCO等已有时效工作必须作为未来基准相邻研究。
5. DATE_ONLY 原封存基线对352段文本正则0命中、32/32世界=NONE，不能作有效的时间强基线；原RAGDefender Claim1–3保持NOT_RUN，论文需准确写B2为中文适配运行而非已严格复现原论文。
6. 不再追逐当前批“修日期正则”“再调联合门控”“补一个Judge高分”“回填NONE首格”作为同一EVAL收益。正式将来单独人工Gold、有效强时间+scope基线、来源授权自然文本、完整RAG回答ASR/Accuracy/abstain/成本与足够独立谱系簇，需要新批预注册和Owner批准。

## 科研路线建议（待Owner正式决策）
**建议关闭当前联合门控方法开发和当天进一步实验，主线转为：**
`中文版本敏感隐蔽知识污染基准 + RAGDefender中文迁移失效分析 + 小样本回答层负效应案例`。
可以形成的论文论点仅限：“在两个自写代理中文版本事实批次中，更激进RD-zh能过滤更多已召回Poison，却增加Clean/HN误删；在额外真实Qwen 31配对的数值型回答代理中出现5/22目标短值命中，而B2和NONE为0/22，提示候选过滤与最终回答的关系不能以片段检出率代表。”**不是**“原论文不安全/普遍防御失效/新方法优于强基线/正式ASR5/22”。

**下一步双机只做整理，不继续科学试次**：
- 5060：整理一份论文级`PAPER1_FEASIBILITY_FINAL_DECISION_BRIEF.md`，归档DEV/EVAL/GEN三个层级的计数、分母、负结果和有效科学主张边界；凡真实原始回包/个人信息/未知授权文本只存D盘，Git仅可公开匿名表与hash；准备独立人工Gold和有效时间scope基线作为未来实验提纲。
- 5090：签发独立`OWNER30_EVIDENCE_CHAIN_HANDOFF.md`，只核对私有SHA、攻击目标绑定、范围世界UNKNOWN状态和评审者未来可验证的复核步骤；不公开Gold/值、不重评分，不声称原论文已复现。
- Owner后续确认论文转向/题目和资源预算；正式实验另批授权。研究分支无主线merge，`AUTO_CONTINUE=NO`。
