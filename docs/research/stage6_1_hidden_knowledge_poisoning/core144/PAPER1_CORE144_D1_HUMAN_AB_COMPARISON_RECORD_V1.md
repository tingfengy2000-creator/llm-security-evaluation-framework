# D1 Human A/B 比较结果 V1

2026-10-16；`P1-CORE144-D1-HUMAN-PRESENTATION-EXCEPTION-AND-AB-COMPARISON-01`。
源HEAD2845e8e715430057cb8e372457e736c1e583af39；PODR-140 / OR-094 / REL-2026-0109。
这是独立人工原答的描述性比较，不是正确率、仲裁、GT或正式论文结果。

## 1. 本次批准与输入保护

Owner明确：“批准仅本次123格呈现等价，原件不改，继续A/B比较。”
只向前接受本次A01原件绑定的123格首尾空白例外，不修改旧字面校验失败事实，不推广strip/归一化。
原始答卷、发放Excel、题文/ID/顺序、冻结证据、Guide/schema、旧回收审计均未改写。
[原回收记录](PAPER1_CORE144_D1_HUMAN_PHASE2_RAW_LOCK_AND_RECEIPT_GATE_V1.md)与V14保持历史快照。
原50份封存文件核验不变，发放版/本人Phase1/两份raw在读取前后复哈希一致。

本轮末检时原微信临时接收路径已不可访问，原因未知，不声称重新核验该临时位置。
上轮先锁定的本机原字节副本及E盘Owner镜像均仍匹配接收时SHA；它们才是本轮权威输入。
未重建/回写临时文件，也没有原答证据丢失或要求真人重交。

| 原件 | SHA256 | 字节 |
| --- | --- | ---: |
| HUMAN-A01 Phase2 | `75b444a135c9b7df01a494912047ec2a2513f8552befaecc572a91760c5ca45e` | 200781 |
| HUMAN-B01 Phase2 | `b66984a7247d7dff86492cef48549506bd743a511710fd0dfcab9c348d648052` | 217867 |

例外逐格审计SHA `1e5a9747598e9701d0db9c27ae1e85a1ae102f84f306fff1bebbe1758c420ec8`。
Owner直接独立性确认继续仅为OWNER_ATTESTED，不因本次批准升级成机器隔离证明。

## 2. 怎样对齐

按完整、精确、唯一Candidate题文建立144↔144双射，不按Excel行号、不同盲号猜匹配，
不读取隐藏mapping/构造角色。保留双方原盲号与Excel行号，新增中性comparison_id只用于审计。
逐条确认双方分配的E1/E2题包内容与身份相同，再比较这些局部证据别名。
本人的题号/题序/题文/表头/1152枚举/144理由/既有minimum规则重新检查通过。
匹配不排序或改写任何raw。方法在[比较协议](PAPER1_CORE144_D1_HUMAN_AB_COMPARISON_PROTOCOL_V1.md)先冻结。

## 3. Phase2结果

| 字段 | 一致/144 | 一致率 | Cohen κ |
| --- | ---: | ---: | ---: |
| overall_fact_status | 139 | 96.5278% | 0.922680 |
| version_claim_status | 128 | 88.8889% | 0.789011 |
| authority_claim_status | 131 | 90.9722% | 0.765560 |
| minimum_external_evidence_needed | 140 | 97.2222% | 0.944785 |
| evidence_selection（过程记录） | 123 | 85.4167% | 0.742726 |
| phase2_issue | 141 | 97.9167% | -0.009346 |
| possible_accidental_secondary_error | 144 | 100% | 不可估：双方恒NO |
| evidence_sufficiency | 141 | 97.9167% | -0.009346 |

七个语义分类字段（排除evidence_selection）964/1008一致，95.6349%。
113条七字段全同；31条至少一处语义分歧，合计44个不同单元格。
21条仅实际证据选择不同；92条八个分类字段全部相同。31+21+92=144。
这不是31条已判某方错误；reason/note文字相同不是门，未自动修理由或实际使用记录。

issue/sufficiency的少数异常反馈不重合：A两条、B一条，各自缺证据反馈仍待有界核查，
不能据此确认材料有缺陷。两项虽141/144一致，κ近零/略负是类别边际高度偏斜下的结果，
应连同完整confusion/marginals理解，不仅凭97.9%宣布高可靠。
secondary全NO只表示原答相同，不证明不存在意外错误。未做显著性或正确率结论。

## 4. Phase1与待审集合

Phase1自然度143/144、内部冲突142/144，其余自包含/指代/meta三个字段各144/144一致。
3条有分歧；其中2条local冲突与Phase2 minimum差异联动，应一起审，不跨人覆盖本人的raw。

Owner待审集合去重54条：31条Phase2语义分歧+1条额外Phase1分歧+22条额外质量/理由线索。
独立质量线索27条，其中含A两条/B一条缺证据反馈和B24条理由/selection引用核对线索。
这些计数重叠，不相加冒充更多问题。21条Phase2过程差异中10条另有待审线索，11条仅归档。
不给全部过程差异贴“错误”标签；实际看证据数量不等于最低证据需求。

## 5. Owner-only产物与下一步

私有命名空间 `experiments/core144_d1_human_ab_comparison_20261016/`；
E盘镜像 `E:/LLMGuard-Handoff/paper1_core144_d1_human_ab_comparison_owner_only_20261016/`。

- `OWNER_APPROVAL_RECEIPT_V1.json` / `A01_PRESENTATION_EQUIVALENCE_OVERLAY_V1.json`：仅123格、有界SHA链。
- `INPUT_PREFLIGHT_V1.json`：原50份/本人三份工作簿/固定文字与native检查。
- `AB_PAIRED_COMPARISON_V1.json`：144对原答、题文、ID、Excel行和E1/E2定位。
- `AB_FIELD_AGREEMENT_V1.json`：逐字段一致率、κ、confusion与marginals。
- `OWNER_REVIEW_QUEUE_V1.json` / `OWNER_REVIEW_PACKET_V1.md`：54条去重待审，原答/理由/证据定位。
- `PROCESS_ONLY_DIFFERENCES_V1.json` / `REVIEW_QUEUE_DECOMPOSITION_V1.json`：21条过程差异与集合拆分。
- `NEXT_OWNER_DECISION_PACKET_V1.md`：十二字段下一审批门，不含已执行仲裁。
- 验证、命令、笔记与封存索引保留于同一Owner-only目录。

本轮51项审计检查通过；封存索引46份文件，SHA256
`185d16967ef87fa051ccc21220dd77cc2c792e74a638fd6c15b422baba8002f7`。
该索引/代码文档快照在本公开恢复指针追加前生成；随后Git/镜像回执独立post-seal追加，
不改原索引。旧50份原回收审计另有原索引，未重新计算替换历史hash。

所有proposed/effective adjudicated values仍为null。未生成一致行GT/最终标签；agreement不是正确性。

验证：24项任务相关合成测试、Ruff/MyPy、13字段独立Fraction复算、7份核心JSON独立命名空间
重建字节一致。扩展79项任务/治理测试中73通过、6失败；六项均在源HEAD的原文上复现，属于
历史绝对路径、人类文档语言比例和旧stage-process措辞约束，不是本次新增回归。
不改历史文件或测试迎合变绿；不能声称整仓测试全过。失败原输出与基线对照已保存。

只读复算笔记 `AB_COMPARISON_CALCULATION_COMPANION_V1.ipynb` 全部Python单元按顺序执行；
未安装nbformat/nbclient、未做官方nbformat/Jupyter内核或GUI验证。主证据仍是原件与验证脚本/JSON。
此可选笔记限制不影响已独立核对的匹配与计数，也不被隐瞒为完整笔记视觉验收。
建议下一任务 `P1-CORE144-D1-HUMAN-AB-BOUNDED54-TRIAGE-AND-OWNER-ADJUDICATION-PREP-01`，
先按既有V4–V4.3有界审查54条并准备Owner仲裁，需另批，不直接要求A/B全量重标。
本轮未给真人/外部Reviewer发件，未读取Expected/构造标签/其他Reviewer答案，未补搜新证据，
未改Candidate/Guide/raw或执行GT/切分/训练。D2载体/范围与D3两S3门不变。

Human/Agent Ledger、Current State、Owner Register、Execution Log、Master Record、Stage Process、两层README、
Project Master Context与[状态V15](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V15.md)同步。
Research Plan Authority/长期要求/Guide/canonical lessons保持：不接受新科学规则、方法或论文结论。
Git最终SHA/远端同步见实际Git与post-seal回执；原无关design/PDF不纳入提交。

`D1_A01_PRESENTATION_EXCEPTION_ACCEPTED / D1_HUMAN_AB_COMPARISON_COMPLETE / OWNER_BOUNDED_TRIAGE_PENDING / NO_GT`。
