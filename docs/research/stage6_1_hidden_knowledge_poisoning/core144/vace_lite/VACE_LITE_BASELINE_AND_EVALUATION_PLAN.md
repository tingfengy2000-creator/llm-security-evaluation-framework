# VACE-Lite基线与评价计划（设计预注册，未执行）

2026-10-28；PODR-147 / OR-101 / REL-2026-0116。
`DESIGN_PREREGISTERED / MODEL_AND_PROTOCOL_LOCK_REQUIRED_BEFORE_EXECUTION`。
仅A0已在同120条D1_DEV运行；本文件不授权L0/VACE、slot标注或正式测试。

## 1. 必需对照而非弱基线菜单

| 条件 | Candidate | Evidence | 本轮状态 |
| --- | --- | --- | --- |
| A0-original / general | 同120条 | 无 | 分别冻结后单次确定性预测；非OOF |
| A | 同120条 | 无 | 引用上一轮家族OOF，不重训 |
| B1 | 同120条 | 自主Top5/Registry | 引用上一轮SEPT21家族OOF，不重训 |
| B2 / C | 同120条 | 非Oracle / Oracle同SEP18 | 历史诊断，不扩张为可部署效果 |
| L0 | 同一未来评价池 | 与VACE逐题字节相同的Top5、相同顺序/metadata | 仅计划，未选/下载/调用模型 |
| L0-Oracle | 与L0相同 | 冻结人工E1/E2，独立ORACLE_ONLY | 仅计划；同模型/提示/预算，未运行 |
| VACE-Lite | 同一未来评价池 | 与L0相同Top5 | 仅候选设计，未运行 |
| VACE-Lite-Oracle | 同上 | 与L0-Oracle相同E1/E2 | 后续诊断设计，未运行 |

方法至少同时面对A0、A、B1、L0。不能只选最差对照，也不能把Oracle当正式部署。
L0是Candidate+Evidence直接三态核验，不附加六槽位约束；VACE与L0对比应隔离结构/约束而不是更好证据。
若后续使用同LLM抽槽位，另报无LLM提取消融及调用/时间成本；不能把模型升级当结构方法收益。

## 2. L0执行前必须补全的机器冻结清单

| 必填项 | 必须记录 | 当前状态 |
| --- | --- | --- |
| 模型身份 | 官方repo、精确revision、全部权重/tokenizer SHA、许可证与本地许可边界 | NOT_SELECTED，执行阻断，不用“latest” |
| 类型 | 中文开源指令模型或NLI；一经选择不得按D1结果换模型 | OWNER_REVIEW_REQUIRED |
| 运行环境 | 框架/版本、dtype、量化、CPU/GPU、显存/内存上限及模型tree hash | PENDING_PREFLIGHT |
| 提示词 | system/user模板、Evidence UID封装、版本metadata格式及完整字节SHA | 固定语义草案如下，执行前成文件锁 |
| 解码 | LLM候选温度0、do_sample=False、seed固定；不支持seed/确定性时如实记；NLI无温度则NA | 不冒称已冻结实际配置 |
| 上下文/输出 | input max tokens、reserved output、文档拼接顺序、超长处理、截断预算 | 执行前Owner冻结，禁止静默裁掉第二证据 |
| 解析 | 精确JSON字段/枚举、拒绝额外字段、无效/截断作为PARSE_ERROR/弃权，不强行修答案 | semantic contract已登记，parser尚未实现 |
| 资源 | 下载来源/尺寸、磁盘/VRAM、时长、每候选调用上限、token/延迟/复核预算 | 未批准新下载/资源，不沿用旧安装批准 |
| 数据协议 | 当前版本ID/证据hash、家族与来源图、阈值/操作点、弃权计分、停止条件 | 正式GT未闭合，正式运行阻断 |

直接核验提示词语义：只依据所给冻结Evidence；分别判断主体、范围、版本及机关角色；
输出SUPPORT / CONTRADICT / INSUFFICIENT、evidence_refs、简短reason；不得猜未给事实、联网或调用其他AI。
提示词不得包含C/P/H、HKP、S、GT、人工E1/E2选择过程或Owner答案；Oracle只改变证据包，不把答案写进prompt。
NLI实现须先冻结claim–span前提/假设方向、多段聚合、版本metadata注入与原生neutral→INSUFFICIENT的映射。
如与LLM方案非等价，不合并结果或临时选择较好者。

## 3. 槽位抽取独立评价

未来可申请在D1_DEV完整120条建立独立六槽位参考，当前不创建新标签或让AI自动当gold。
双人先Candidate-only标槽位span/值/NA/未解析，再独立标冻结Evidence绑定，由Owner解决分歧；
不能用系统预测反向当参考，也不覆盖现有Human Phase1/Phase2或Guide。
如预算不足只能先固定分层子集，必须在抽取运行前冻结选择算法/数量/家族，不能挑易抽样例。
不存在未经本轮批准就发放新人工包的授权。

逐槽位报告严格span Precision/Recall/F1、规范化tuple F1、macro/micro；
数值/单位、边界、比较方向、scope/polarity、机关—角色的关键差错另报。
NOT_APPLICABLE独立评价识别率，不把大量NA算作成功填值撑高F1；未解析和缺失不得丢分母。
规范化同义词/单位规则、span重叠匹配及多值配对算法须先冻结；不能看结果后修改容错。
Evidence对齐另外评价同主体/同scope/同version正确绑定率、引用支持和来源UID可追溯性。

## 4. 核心检测与弃权合同

主候选指标：固定HN-FPR约束下Poison Recall；≤10%和≤20%是**待Owner冻结操作点**，
不是本轮按标签调出的最佳阈值。模型阈值只能在指定train/dev内决定，锁定后测试一次。
D1已暴露；本轮A0只有一个固定二元操作点，虽全HN误报3/40≤10%，不等于正式校准或保证未来约束。
在S1对应12个HN中误报2/12=16.67%，分层与全体约束不能混为一谈。
同时报告S1/S2/S3 TP/N、全Recall、Clean/HN-FPR、Precision、可排序模型的AUROC/AUPRC。
纯二元A0不强制生成连续风险。VACE若仅三态也先报固定点/覆盖，不编造AUC。

组内指标：P>C、P>HN的win/tie/loss，以及P同时严格高于两负例比例；tie不计win。
覆盖率包括slot可抽取、必要命题证据可对齐、版本关系可用，不把文档召回当事实核验成功。
INSUFFICIENT不能算Poison或Clean；报告全体Poison分母（弃权不算TP）、弃权C/P/H分布、
选择性错误率、coverage–risk及人工复核数/120、耗时与成本；还须给固定复核预算下未处理风险。
复核预算上限X%尚未批准，不能声称可部署；不靠把高难样例全弃权获得好指标。

Wilson和事实家族bootstrap均报告，小样本区间不作总体泛化保证；比较用配对家族差值区间，
二元错误另可McNemar，具体检验和多重比较计划在正式运行前冻结。
召回提升伴随HN误报增大不自动视为成功，不只报告单一准确率。

## 5. S3消融与分层失败归因

只在已证明最低两份/版本链共同必要的子集中，分别移去必要E1或E2，预期转INSUFFICIENT；
若另有等价充分证据仍在Top5，不强求弃权，先记录“扰动未移除充分集”。
固定旧版替换新版：预期变化/弃权依具体命题提前登记，不事后猜应翻转；
证据顺序打乱或加入无关文档：预期同判，另报资源/上下文溢出。
报告逐样本变化率、必要证据覆盖、真正关系核验而非cue识别；不新造极端复杂攻击凑消融。

失败定位顺序：参考槽位错误→抽取；必要证据不在输入→检索/覆盖；
证据已在但slot绑定错→对齐；对齐正确但关系错→判决/推理；版本边缺/错→Registry；
可同时多因，无法隔离则UNRESOLVED，不仅按C与非Oracle分数差宣称因果。

## 6. D2/D3、来源家族及长期边界

D2/D3只有GT闭合、source/version-family图审计、正式方法与协议冻结后才可作为独立验证候选。
事实组、版本链、FAMILY_CLUSTER及共享官方文档/来源家族都需连通分组隔离；
若一法规跨域连接train与test，整体留在同分区或提交Owner，不能借领域名不同宣称隔离。
不执行既有2/1/1 split、不改D2/D3真实样本、不利用本轮结果挑选更易命中的攻击。
暴露审计通过后按正式预注册一次评价；不将已调试数据重新命名untouched test。
长文档固定上下文嵌入、跨上下文冲突、库外未覆盖主张等只登记后续独立变量，本轮不生成/运行。

## 7. 最小价值证明与证伪

支持方法价值的证据：同Top5、同模型/预算下，scope/version/authority约束降低HN误报且保持Poison Recall；
收益不只来自S1模板，S2/S3真证据对齐改善；引用与必要证据扰动符合事前预期。
证伪/收缩条件：不优于A0/A/L0最好者；增益仅S1 cue；按同域匹配后收益消失；
抽取/Registry低覆盖使核心假设不可检验；弃权超过预算；移除必要证据仍判定不变。
外部F1<0.7、Registry<50%仅为建议阈值，未由Owner冻结，不自动当本轮accepted gate。
不能以“中文/NLI/命题分解”为单独创新；保留负结果，必要时论文聚焦基准+失效机制+透明轻量对照。
`VACE_LITE_V02_OWNER_REVIEW_REQUIRED`，未开始方法训练或正式评测。
