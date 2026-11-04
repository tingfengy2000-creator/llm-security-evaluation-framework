# Pilot12 选择与执行记录

状态：SELECTION_VERIFIED / QUERY_PILOT_NOT_RUN。本次不重抽样、不读取旧E1成败选组。
结果无关规则沿用已有TASK=PAPER1-RAG-DEFENSE-RECONSTRUCTION-01，seed20261104：
SHA256(TASK|seed|S|group)每S升序前四组；组内三变体整体纳入。
本次Evaluator在固定D1 labels hash下重算，组顺序与既有选择完全一致。
12组36条，C/P/H各12，Poison S1/S2/S3各4，覆盖9事实家族；覆盖是观察值，不声称按家族最优抽样。
不公开组/家族映射，不把S与variant传防御/模型。8组24HOLD不在本轮集合，不读取本体。

选择SHA256：`2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`。
审计run：W1-5060-20261104-P0-01；审计输出SHA256：
`f86770cdbe5d2b99babdc3d2563664c374042c158fefa475cbaed81aaf6ff76f`。
代码SHA：`ca75c381546247ad3377013a75bb21133cc078ed`。

既有V2的12题来源支持草案仍AI_PROVISIONAL、非Human Gold；本次没有读取其答案提案或原始独立复审材料。
仅证明既有选择身份和旧包数据缺口，不证明新题逐世界足证性。
真实query Pilot有效执行分母0，ASR/最终Answer Accuracy/过滤Recall/FPR/Abstain/Unsupported均NOT_MEASURED。
后续先生成不含答案的逐世界manifest、确认独立官方证据权限和模型/评分合同，才进入真实检索/Pilot。

虚构Chroma smoke另计，不算这12组的任何一个样本，不得将3世界×TopK3=9检索hit当作9次攻击或QA。
