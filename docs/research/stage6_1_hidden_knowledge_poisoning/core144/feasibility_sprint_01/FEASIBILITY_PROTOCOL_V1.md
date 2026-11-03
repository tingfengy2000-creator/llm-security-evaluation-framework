# FEASIBILITY_PROTOCOL_V1 — 有界研发合同

2026-11-03；Task `PAPER1-FEASIBILITY-SPRINT-01`；Owner当前粘贴指令及后续Global外传批准。
`DESIGN_FROZEN / IMPLEMENTATION_VALIDATION / PAID_EXECUTION_GATE_PENDING`。
研发目标CCF C级可行性，不是发表保证；新增方法仍`PROPOSED / EXPERIMENTAL`，未被验收替换正式方法。

## 科研问题与样本

不读真实S标签，内部矛盾证书与证据约束的条件/版本/来源关系能否提高S2/S3检出并控制合法误报和弃权？
签署D1为`D1_DEV_EXPOSED`：40组120条13事实家族；Poison/Clean/HN各40，Poison分层12/15/13。
8组24条HOLD不进入本轮；不改D1/D2/D3、Human、GT、官方正文、Top5或任何L0封存件。
研究分支`research/paper1-feasibility-sprint-01`从L0收口512d928创建；源研究分支当时远端4dc9161。

直接复用原签署包`runtime/f5.jsonl`，SHA256
`c849260e2a41fa9186e6d69ed6442cbebdaa7ff272beece9dfadc22e61cf535c`；7384615字节；120行各5证据。
旧包manifest声明的评价文件SHA256为
`d904e349211ec7af648b68afadb31e46a30196ba20a53b5a40a382ec0df7afaf`；本轮准备不打开该标签文件。
不得输入Oracle映射。Runtime白名单只收candidate_id/candidate_text/evidence，ID仅本地配对，不发送模型；证据顺序不变。
递归检查模型可见正文、UID、title、URL及扁平metadata。未知字段/标签标记/错文本SHA直接拒绝整个输入身份，不静默删字段或重排。

## E1/E2/E3/E4与复用

| 条件 | 执行与判决 |
| --- | --- |
| E1 | 固定API直接核验Candidate+Top5；独立于内部证书，所有120条均运行 |
| E2 | 同一个内部模块；证书有效早退CONTRADICT；其余复用同候选E1外证输出 |
| E3 | 同内部模块；未证实者进入六槽结构化核验；最多一次同池缺口补查 |
| E4 | 禁用内部早退，其他结构化核验及补查完全相同；与E3相同输入的请求复用 |

共享是预注册的组件消融/共同输出设计，不伪装各条件独立重复抽样。E2沿用E1原输出；E4沿用E3相同结构化组件输出；保留call_id和完整成本来源。
每候选初始最多内部1+直接1+结构化1；结构化缺口补查最多1次。全矩阵最多480个实际请求，加1个纯虚构接口探测。
不按cue或真实S标签省略内部模块；A0词面本轮只可作为诊断线索，不能直接flag。
E4为预算允许时预先选定的可选条件，必须在预测前通过`--e4`锁定；中途不能为了分数增加或删减E4。
若未完成全120条，保留部分raw与失败，不将缺行补预测后宣称完整结果。

## 模型与预算

唯一候选精确ID `qwen3.7-plus-2026-05-26`，无别名替换。当前适配器仅实现已核验东京工作区域；账号实际地区未知，不自行认定为东京。
Owner已批准阿里云外传并允许Global推理；其他实际地区若不是当前实现，停止并审阅地区/价格差异，不自动切换。
首选`enable_thinking=false`、`temperature=0`、`stream=false`、`response_format=json_object`、`enable_search=false`，不传tools。
`max_completion_tokens`：direct1024/internal2048/structured4096/followup4096；保守费用额外预留16token，覆盖官方记载的至多10token计数差。
先用纯虚构JSON探测验证实际模型ID/非Thinking/usage/完成状态；不支持关闭Thinking或返回别名即停止，不自动改模式。
已读官方资料不证明账号已开通。精确端点、实际区域、许可与保密确认、密钥、当日价格/条款和探测receipt都闭合后才允许真实D1。

所有实际调用（含探测）共用一个任务级Git外费用账本，不因Run目录或条件重置。
总额USD<5；4.00预警，`已结算估算+待结算预留+下一请求最坏费用 >=4.50`即硬停；不假设免费额度或缓存折扣。
单请求即一个批次，最多一个in-flight；无自动重试、无并发、无服务商/模型替换。
UTF8字节数+4096作为输入保守包络而非实际token测量；输出按上限+16。若超过256000输入计价层则拒绝，不套低价。
usage缺失/超时保留全部预留；usage超包络停止并保留未决记录，不能将不明请求当免费。
实际消耗按usage和冻结单价估算；最终账单未对账不声称最终结算额。
全120的初始请求保守估算为$5.559951780（不含补查），超过硬停额；这**不是必然可跑完保证**。
逐请求根据真实usage释放已结算差额，仍按下一请求最坏费用准入；预算提前停止则不获得完整效能结论。
时间边界固定2026-11-03 00:00至2026-11-10 00:00 JST（七天），不自动延长。

## 冻结、封存、评价

先提交clean源码；付费Run的CONFIG_LOCK绑定commit、代码、prompt、parser、评价器、三份规格、私有配置与固定输入SHA。
原模型返回、parser错误、原判决、最终判决、spans/UID、缺口、路由、usage、延迟及费用分开保存，均Git外。
所有候选/条件预测及120份raw文件索引封存后，独立评价进程才能按冻结评价文件SHA打开标签。
Evaluator检查相同ID、40完整三元组、13家族、角色与S计数、Raw/config/code/prediction seal；失败则无分数。
所有弃权、JSON/引用失败保留分母；缺usage不填0。无连续分数，不计算AUROC/AUPRC。
报告Recall及S1/S2/S3/S2+S3、Clean/HN FPR、Precision、错误SUPPORT、合法SUPPORT、总/分角色弃权、严格三元组、解析失败、真实usage及成本。
报告实际去重请求费用与各条件单独执行的逻辑费用；共享调用不能相加冒充实际支出，也不能将前置模块算免费。
延迟mean/median/p95来自相应组件之和，复用设计不是独立墙钟速度实验。
Wilson95加家族配对bootstrap2000次、seed20261103，家族重复时三元组保持完整；零分母resample排除并报告有效数。
比较E2-E1、E3-E2、E3-E1，E4完成才比较E3-E4。所有区间是开发描述，不证明泛化。

## 事前GO规则

E3同时满足：Recall>=22/40；S1>=9/12；S2+S3>=12/28；CleanFP<=4/40；HNFP<=4/40；弃权<=24/120；Strict>=12/40。
还须相对同骨干E1有下列一种配对点估计实用优势：
1. TP至少多2且两类FP各不增加；或
2. TP不减少、两类FP各不增加且合计少至少2；或
3. 全部最终判决逐ID相同且单独执行逻辑费用降低至少10%。
达到可用性且有以上优势=GO；E1达到相同可用性而E3未证明增益=CONDITIONAL；否则完整实测为NO-GO。
仅点估计达到GO也须同时展示区间和混杂，不能称统计显著。E4未跑完不能称分级/自适应独立增益。
若付费未执行或被阻断：执行建议NO-GO（暂不启动），科学效果NOT_EVALUATED，绝不把它解释为方法被数据否定。
不更换第二付费模型、不扩预算、不加Prompt版本追分。新方法语义变更另交Owner。

## FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW

D1已暴露、13家族样本小、六槽抽取和coverage_complete仍依赖模型、引用正确不保证推理正确，故只能研发诊断。
内部规则闭合且保守：复杂隐含同域/跨单位换算/别称会漏检，不能对D1逐题补规则。
结构化关系只检验来源定位、槽位绑定和模型声明关系；不是已证明中文NLI或FactCG复现。
FactCG只启发多证据关系表示，不下载/训练，不据其原论文数字宣称当前方法有效。
与旧7B、OOF-LR/规则的比较混合了模型能力、策略、成本与Oracle差异；主要贡献比较只看同API E1/E2/E3/E4。
实际后端或Thinking不同、隐私/许可不明、超预算、输入身份变化、数据/算法语义变更立即按PO-MHEP停受影响部分。
