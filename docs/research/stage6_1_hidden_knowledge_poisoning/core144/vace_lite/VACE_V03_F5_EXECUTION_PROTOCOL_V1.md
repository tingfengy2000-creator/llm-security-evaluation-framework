# VACE V0.3-F5：一次性D1开发诊断执行合同

2026-10-28；PODR-149 / OR-103 / REL-2026-0118。
Task `P1-VACE-LITE-V03-F5-IMPLEMENTATION-AND-D1-DIAGNOSTIC-01`。
Owner最新明确批准有界实现和D1评分，supersedes PODR-148仅限本任务的“尚未批准实现”状态。
旧规格、设计稿、数据、Guide和历史结果不改；不是正式科研合同、GT或split批准。

## 先冻结，再预测，最后加载评价标签

固定签署40组120条13家族；8组24条HOLD。候选文本SHA
`6be97906cb9de7587491e84e4c13131a22f93e07b87336772c913534dc7e79e2`。
Runtime白名单只接收opaque ID和Candidate文本；构造角色、HKP、S、Human/Expected/GT、
最低证据及人工E1/E2映射都不能参与提取、检索、路由和证书。ID仅trace键，cache/查询按正文内容。
源码、合成测试、检索配置、三态政策和评价器在预测前生成逐文件SHA/协议锁；
240条新预测及路由先封存，再启动独立进程评价。旧126条预测永不复用。

## 两条件共享语义，只有执行调度不同

- V03-F5：E0六槽位→I证明；仅有有效内部证书才早退CONTRADICT；否则F→Q按缺口T/P/J一次。
- V02-NA-F5：相同E0/I/F/T/P/F再绑定/J全流程，终态用相同逻辑；内部证书不会被任意外证覆盖。
- I没有证书绝不SUPPORT。A0仅记录cue，不提供判决；无B1兜底、无训练/模型调用/新下载。
- 正文仅原Hybrid Top5，版本注册表只获冻结元数据；不扩池，不由Registry免费回取正文。
- 证书含原文span/hash、主体/关系/单位/scope/版本及规则；格式校验不是自然语言gold证明。

第一版是**闭合关系规则原型**，不是完整中文NLI。支持狭义年休假肯否互斥、显式同域功能值，
周/日工时的同范围功能值反证，派遣上限/临时岗位期限仅抽取观测（不同上限不直接判冲突），完整条文payload逐字支持，
确切命令编号的公布机关角色，以及明确两版一次性伤残补助金方向反证。
未覆盖的条件/量词/别称/日期/修订次数等返回UNRESOLVED/INSUFFICIENT；不会凭关键词或任意数字不同判毒。
未明示版本的规范数值必须获得CURRENT元数据，UNKNOWN不靠最新年份猜补。
来源事件与当前实体规范分离，不用host/publisher猜issuer。
联合比较的局部正确不足以证明整条SUPPORT，未覆盖断言仍需弃权。

## 冻结检索、预算与成本

复用原33文档官方语料及Registry V2。Q_NO_TITLE沿用第一书名（无则前20字符）＋Candidate全文，
不是人工正确文档标题。BM25中文字符2/3-gram，k1=1.2,b=0.75；Dense原MiniLM，CPU/L2/local-only，
revision `16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`，tree
`14be5b8d047148b787bcca877c4b91722c10bc3e1a184ea3aaffe8b6fd3d1fb7`。
query内min-max后equal-weight Hybrid，UID稳定打破同分。相同Top5用于两条件，不看命中率改配置。
必须复核新Top5与旧冻结Top5身份120/120一致；差异FAIL而非评分后挑池。
T/P/J各最多一次，F初始＋再绑定最多两次，无新增正文/外部API/LM调用；无进展停止。
共同准备全部120条Top5的CPU成本独立计入，不把预计算当免费；I早退仅减少核验正文/模块消费。
实际计时mean/median/p95及模型/索引准备、确定性复跑分开；不能据毫秒噪声宣称生产加速。

## 评分事前定义

仅CONTRADICT计污染flag，SUPPORT和INSUFFICIENT分开；弃权保留全体分母。
正例S1/S2/S3为12/15/13，Clean/HN各40。TP/N、Recall、Clean/HN-FPR、Precision、三态及分层弃权；
无连续分数，AUROC/AUPRC为NOT_REPORTED，不填0或把三态伪造为排序分数。
严格三元组成功=P判CONTRADICT且C/HN均SUPPORT；涉及弃权的pair单列unresolved，不算win。
Wilson95和13事实家族bootstrap2000次，seed20261028；只作开发描述，不是总体泛化置信区间。
两条件共享bootstrap抽样，报告配对差值。I早退假阳性、外证成功及未解析原因单列。
检索reference命中率只在锁后分析，非检测率；冻结E1/E2不是所有合法证据的穷尽真值。
只引用同120历史A0/A/B1，LR固定阈值0.5与三态政策不可伪装为相同FPR预算的优势。

## FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW

已知批准内限制：闭合语法覆盖低、Registry UNKNOWN及Dense长文截断、D1作者开发暴露；
这可能导致高弃权/低S2S3 Recall，不是调规则追分的理由。置信区间可能退化，应同时保留Wilson。
潜在错误：提取混域、日期/机关错绑、局部反证误用于全篇；用合成边界、证书及全部Top5同域冲突检查控制。
充分性不是世界事实完备性；机械span/重放不是独立人工语义验收，不称证书错误率为已完备测量。
L0/NLI/LLM仍未运行，不得据本轮声称优于它们；非自适应语义相同，预期精度可相同而成本不同。
不承诺提高任何一级Recall，不使用无效75%拼接，失败结果也必须封存。
这是D1开发算法工程，不修改正式贡献/研究合同，不暴露D2D3；下一门Owner审阅，不自动进入L0。

私有命名空间：`experiments/vace_v03_f5_20261028_run01/`。
最终输出六份报告、CSV、240行预测、源码/配置/输入/模型SHA、trace、测试与复现manifest。
完成文档收口/Git后STOP `VACE_V03_F5_DEV_DIAGNOSTIC_COMPLETE / OWNER_REVIEW_REQUIRED`。
