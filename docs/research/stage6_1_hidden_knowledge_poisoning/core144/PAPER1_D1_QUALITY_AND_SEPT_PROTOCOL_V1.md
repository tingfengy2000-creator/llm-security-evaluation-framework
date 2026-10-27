# D1开发资格收口与SEPT物化协议 V1

2026-10-27；Owner任务`P1-D1-QUALITY-HOLD-CLOSURE-AND-D1-SEPT-MATERIALIZATION-01`。
PODR-144/OR-098/REL-2026-0113；source HEAD2ce4b1cdc0dc9d3953a0c11afc1d5961468bab4e。

## 质量轨道

三份AI辅助输入原字节另锁；核55非空建议/2空值、原表身份、V4–V4.3和同题冻结证据。
原8个HOLD组三元组整体隔离，优先独立审余40组；不按分数或构造角色决定真实事实。
每题记录可见命题/证据span/规则/建议与问题，锁定后才受限join构造role和S设计路径。
资格状态仅ELIGIBLE_CANDIDATE/HOLD_REQUIRES_OWNER/BROKEN_EXCLUDE。
ELIGIBLE_CANDIDATE只是建议准入，evaluation_eligible仍为false，直到Owner签署本次D1_DEV。
Owner最终值初始空，批量确认仅覆盖准入组适用的有证据建议和无争议机械验收；
HOLD-only建议不转评价标签、未决值不填，不要求重做54条。
evidence_selection保留实际过程差异，不生成唯一GT。原题/原答/Evidence/Guide不改，不加新事实来源。

## 独立工程轨道

从本机冻结官方快照建立统一语料，按原始SHA及原文/来源标识去重，区分host/publisher/issuer。
注册表只用可溯源metadata和显式原文，未知留null，不由Human或C/P/H反推当前/历史身份。
查询只用Candidate书名主体+原文，继承Q_NO_TITLE，不使用人工source title、E1/E2或role。
Sparse字符2/3-gram BM25 k1=1.2,b=0.75；Dense继承MiniLM多语L12-v2、
revision16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1、tree SHA
14be5b8d047148b787bcca877c4b91722c10bc3e1a184ea3aaffe8b6fd3d1fb7，CPU/L2/local-only。
Hybrid按逐查询min-max sparse/dense等权；K=1/3/5/10，主Top5，不调参。
先锁完整检索/确定性重放，再加载Oracle身份评价。缺依赖/身份不符不得换模型或冒称Hybrid。
全部Top5按原排名保留；不得挑最支持Poison的文档。Registry仅作版本分区，不按标签挑证据。

## 同列特征与实验门

复用Feature Set V1.1精确21列（S3/E9/P6/T3）、原extractor与PTS V3适配，R不进入Stage A。
Oracle使用本题原分配冻结E1/E2，非Oracle仅独立Top5；科学定义/列序相同，另记可用状态。
不适用/缺失留null，不常量填安全值、不新造缺失指示器。两列deferred关系特征继续排除。
继承V1.1训练折mode/median/连续标准化策略和固定LR，仅在资格获签且全部门通过后才可fit。
如果整列无观测或来源角色不能绑定，报告具体缺口，不擅自删列或改科学合同。
Owner签署前不fit A/B/C、不计算Recall/FPR/AUC，不复用或重生成旧126隔离OOF。
本轮D1_DEV_EXPOSED；Core正式GT/2/1/1未执行，D2/D3不根据本轮反馈改写。

## 风险与交付

前瞻/论文风险：QA误升GT、证据映射入检索、角色反灌语义、全域同类漏检、metadata角色混淆、
缺失变类别shortcut、旧分数复用、Oracle误称部署性能。各自独立留input/output/source/config hash。
交付逐组资格CSV、待签XLSX、可信语料manifest、检索trace、B/C同列CSV及状态/来源明细、
泄漏与parity审计、路线决策。Owner未签时有效检测指标只记NOT_ESTIMATED，不伪造目标状态。
