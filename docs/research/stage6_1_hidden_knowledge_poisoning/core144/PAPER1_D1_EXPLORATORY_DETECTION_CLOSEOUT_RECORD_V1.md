# D1探索性诊断：可评估性未通过，不能报告检出率

2026-10-27；`P1-D1-EXPLORATORY-DETECTION-FEASIBILITY-SPRINT-01`。
PODR-143 / OR-097 / REL-2026-0112；源HEAD `892915a830f9762d2cf239fcfb21cb8b26f186fb`。
[执行前协议](PAPER1_D1_EXPLORATORY_DETECTION_PROTOCOL_V1.md)，
[并行状态V18](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V18.md)。

## 结论先行

`NOT_EVALUABLE / HUMAN_DECISION_REQUIRED / Auto Continue=NO`。
这是一次D1-only开发授权，不是Core正式训练、正式测试或GT冻结。
有效评价组/候选为 **0/0**；所有S分层Recall、置信区间、HN-FPR、AUROC、AUPRC及Oracle差距
均**未估计，不是0**。没有证据支持“方法无效”“长上下文有效”或任何方法优越性结论。

| 方法 | S1 TP/N、Recall | S2 TP/N、Recall | S3 TP/N、Recall | Overall Recall / HN-FPR / AUROC / AUPRC |
| --- | --- | --- | --- | --- |
| A Candidate-only字符TF-IDF+LR | NA / 未估计 | NA / 未估计 | NA / 未估计 | 未估计：预备OOF已隔离 |
| B 非Oracle可信检索+SEPT | NA / 未估计 | NA / 未估计 | NA / 未估计 | 未运行：D1绑定流水线未物化 |
| C Oracle匹配E1/E2上界 | NA / 未估计 | NA / 未估计 | NA / 未估计 | 未运行：D1同列适配未验证 |

## 三份输入与身份核验

Owner提供的AI辅助XLSX、57项JSON和阅读MD均在本机实际找到、原字节复制并记录SHA；
首次只读预览早于锁定，锁定时重新验证来源稳定，不虚报先锁后读。XLSX未重存。
原Owner仲裁表SHA `45b9829987321d6f40cadc93f7981d64c0611a9672f48d06271d0a3fccffaaac`不变。
XLSX/JSON的57项逐字段吻合，55个非空QA建议、2个空值属于0028；原54题/108份原答/
921段证据逻辑一致。JSON所列中间AI工作簿source SHA未找到独立原件，不谎称已验证该中间谱系。
当前三原件本身的哈希/内容匹配不受此未知影响；QA建议仍不是已批准Human GT。

144题精确题文身份、48组三元组及13个canonical family可恢复。构造role未进入特征、
检索或训练target；训练proxy来自人工二元判断，125条一致、1条有同题冻结证据支持的QA建议。
这些都不是正式GT。旧A/B raw、发放书、54审查、比较证据索引保持不可变。

## 质量排除与时间线：不能把不完整预检掩盖为合格实验

事先规定按证据/命题质量排除，不能按预测难度筛题；任一成员HOLD就排除完整三元组。
保留family用于隔离，不能仅因共享法规就删全family。共享损坏片段是否真正被命题依赖单独核查。

1. 五个Owner指定HOLD0028/0051/0121/0078/0116先闭包为5组15条，余43组129条。
2. 训练前新增0038的流产条件范围疑点；它是待核范围，不是已证实错误，整组HOLD，余42组126条。
3. 对这126条运行固定字符2/3-gram TF-IDF+L2 LR、13家族隔离OOF，阈值0.5；
   训练折内fit、未校准、无调参。预测原字节锁定，固定配置重复结果一致；尚未计算性能指标。
4. 随后完整性复查发现54队列之外0093/0098与0078/0116同类：双机关同次公布主张被人工
   判为YES/ZERO，但排他性前提未闭合。不能因为两人相同或构造role而认可其S1路径。
   **这说明预检在首次拟合前没有真正闭合。** 不继续重拟合或做指标，预备126条OOF隔离保留。
5. 再按同一质量标准闭包两组，合计8组24条排除；剩余40组120条仅是**待审结构上限**，
   不是有效评价集、最终标签或已接受分母。旧准入锁不覆盖重写，追加失效记录。

| 分布 | 原始 | 排除 | 暂存、尚未通过可评估门 |
| --- | --- | --- | --- |
| groups / candidates | 48 / 144 | 8 / 24 | 40 / 120 |
| C / P / HN，构造role仅锁后评价控制面 | 48 / 48 / 48 | 8 / 8 / 8 | 40 / 40 / 40 |
| HKP1 / 2 / 3 / 4 groups | 12 / 12 / 12 / 12 | 1 / 2 / 1 / 4 | 11 / 10 / 11 / 8 |
| S1 / 2 / 3 provisional groups | 16 / 16 / 16设计 | 4 / 1 / 3设计 | 12 / 15 / 13，人工最低路径恢复后核对 |

不因单个条文缺失或OCR损坏一律删除整family：其余命题依赖原文不同span。
13个family仍有成员，未来CV必须按整个family隔离；120条不能当120个独立事实家族。

## 三方法的真实工程状态

A有已隔离的126条真实预备OOF，不是“从未训练”。锁SHA
`95901034064467f56303fba96c93208219eae665ec31b7172766bd34e9c8419d`，
构造role在其锁定后才读取用于结构审计，未计算实样性能。源代码执行版本私有原字节保存；
后续只作格式/类型检查修正，未重跑模型。原拟合完整stdout/stderr未存独立文件，
仅工具会话摘要和模型/环境/配置/预测锁可恢复；不能宣称一次完整验收的科研复现运行。

B/C的通用Extractor、Retriever与轻量融合源码存在，不能声称完全没有实现或依赖。
但既有V1.1矩阵属于Final72，72×21，D1精确题文匹配0/144；没有已验证的D1统一可信语料/
Registry/独立检索锁/SEPT矩阵绑定，C也未完成与B同列的Oracle适配。不得用人工字段冒充特征，
不得拿旧72结果代替D1。当前质量阻断后不再继续物化/拟合。

## 对研究方向能说什么

- S1：文内矛盾应可仅凭文本判断，但本轮没有有效检出率；机关双归属不先验等同A与非A。
- S2：需要准确召回单份充分证据及命题核验；本轮未测量这一链路的失败比例。
- S3：没测得低Recall，更不能归因“缺第二份”或“模型不会推理”。下轮需同时保存必要两端
  证据命中、聚合输入及Oracle同列对照，区分语料缺证/检索/抽取/版本绑定/推理。
- 同分布扩样不能修复标签或质量门。新家族/领域可以加强外推检验，但不能替代先建立可测条件。
- 未证实上下文截断或完整证据下跨文档关系恢复失败，不应直接以长上下文代替缺条文、损坏数字
  或不明确的语义边界。长上下文仅在这些具体瓶颈被日志证实后做固定输入针对性消融。
- 当前较稳妥的贡献叙事是版本感知Benchmark、可复核质量门/失效机制和轻量检测有界证据；
  多视角仍是假设。本建议不修改Owner冻结的研究路线，也不宣布放弃方法。

## 物理证据与五份交付

私有命名空间：`experiments/core144_d1_exploratory_detection_20261027/`，Git忽略。
Owner交接目录标识：`paper1_core144_d1_exploratory_detection_20261027`；禁止作为Reviewer材料。

- `outputs/D1_EXPLORATORY_DETECTION_RESULTS.csv`：三方法NA与各类暂存/排除分母。
- `outputs/D1_EXPLORATORY_PREDICTIONS.jsonl`：144×3条状态记录，所有有效评分为null，
  引用隔离OOF的SHA而不冒充432个预测；隔离分数本身另存。
- `outputs/D1_S1_S2_S3_FAILURE_ANALYSIS.md`：已观察质量问题与未测试模型机制分开。
- `outputs/D1_METHOD_FEASIBILITY_DECISION.md`：逐项回答A–E，不虚构Oracle差距或HN误报。
- `outputs/D1_EXPERIMENT_REPRODUCIBILITY_MANIFEST.json`：配置、原件SHA、环境、实际运行与缺口。

另存原件、旧索引复验、预备模型manifest、预测锁、排除/family审计、12字段Owner决策材料、
代码检查回执和私有证据索引。新来源、模型下载、AI调用、D1修题和D2/D3数据修改均为零。

## Owner下一决策门（十二字段摘要）

1. Issue ID：`D1-EXPLORATORY-QUALITY-AND-PIPELINE-BLOCKER-01`。
2. 名称：同类机关角色/S1边界未闭合及D1 SEPT流水线未物化。
3. 发现阶段：本次D1探索预检与预测锁后的补充质量复查。
4. 事实：OBSERVED为三原件/57项核对、预备126OOF已隔离和Final72身份不适用；
   SOURCE_DERIVED为48/144/13及暂存40/120；INFERENCE为S1分母风险；UNKNOWN为实际检测能力。
5. 约束：仅非阻断探索标签、同类同标准、构造role隔离、不改真实题/规则/原件。
6. 时效：在重新接受准入总体或报告性能前必须解决，不能再先拟合后补质量门。
7. 风险：错误分母/shortcut、未绑定流水线、不完整复现、无依据的能力/长上下文论文结论和返工成本。
8. 方案：优先有界同源语义核查并物化D1；优点是可测/可回溯，代价是暂不能给率。
   若需同源补材料或版本化修题另获Owner批准；可能需定向复核，旧版保留，可逆但涉及机制/S须停。
9. LOCAL推荐：先统一处理新增同类0093/0098，再闭合其余HOLD与D1 B/C适配。
10. 依据/把握：结构风险和身份不匹配可直接复验；最终语义值/性能未知，不编数值置信度。
11. Owner需决定：是否把0093/0098纳入原0078/0116有界门；0028/0038范围及0051/0121材料
    是否需要另批同源修复/定向复核。不能直接选择YES/ZERO或按构造role反推。
12. 决定前：仅核验、证据/上下文保全、治理/Git；不再实样拟合、指标、改题/Guide/加源。

精确推荐下一任务：`P1-D1-QUALITY-HOLD-CLOSURE-AND-D1-SEPT-MATERIALIZATION-01`，未自动启动。
验证与收口见[检查记录](PAPER1_D1_EXPLORATORY_DOCUMENTATION_CLOSEOUT_V1.md)。

`D1_EXPLORATORY_DEV_DIAGNOSTIC / D1_DEV_EXPOSED / D2_D3_CONSTRUCTION_DATA_UNCHANGED /
CORE_FORMAL_SPLIT_NOT_EXECUTED / CORE_FORMAL_GT_NOT_FROZEN`。
