# D1首轮开发检测结果记录 V1

2026-10-28；PODR-146 / OR-100 / REL-2026-0115。
Task `P1-D1-DEVELOPMENT-DETECTION-FIRST-RESULTS-01`；Run `D1-FIRST-DETECTION-20261028-R01`。
[拟合前冻结协议](PAPER1_D1_FIRST_DETECTION_PROTOCOL_V1.md)，[最新状态V21](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V21.md)。

## 准入与科学角色

Owner已真实完成三项“确认”、署名、日期；对未签模板仅五格逻辑值变化，其余三页不变。
实际更新原文件名而非先报的另存名，路径识别差异已记录；原件未由Agent重存。
只接受D1_DEV：40完整组/120条/13事实家族，8组24条继续HOLD。
有效Poison S1/S2/S3=12/15/13，各有相同数量Clean/HN；总三类各40。
二元标签119 Human一致+1签署规则QA；独立S路径已核，不以构造角色训练。
构造角色/S只在新预测锁后关联评价。没有Core144正式GT、正式测试或2/1/1切分。

## 固定阈值0.5的开发OOF

| 条件 | S1 TP/N（Recall） | S2 TP/N（Recall） | S3 TP/N（Recall） | 总Recall | Clean-FPR | HN-FPR | AUROC | AUPRC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A 文本TF-IDF+LR | 6/12（50.00%） | 2/15（13.33%） | 4/13（30.77%） | 12/40（30.00%） | 3/40（7.50%） | 7/40（17.50%） | 0.6836 | 0.5398 |
| B1 非Oracle SEPT21 | 2/12（16.67%） | 8/15（53.33%） | 10/13（76.92%） | 20/40（50.00%） | 18/40（45.00%） | 15/40（37.50%） | 0.5306 | 0.3814 |
| B2 非Oracle SEP18 | 3/12（25.00%） | 7/15（46.67%） | 11/13（84.62%） | 21/40（52.50%） | 15/40（37.50%） | 18/40（45.00%） | 0.5366 | 0.3669 |
| C Oracle SEP18 ONLY | 6/12（50.00%） | 7/15（46.67%） | 10/13（76.92%） | 23/40（57.50%） | 15/40（37.50%） | 16/40（40.00%） | 0.5872 | 0.4364 |

B1是事前指定主报告，不是按最好分选模。四条件各13折/120新OOF，合计480条；
全部预处理仅fit训练家族，LR参数/seed/阈值固定，不校准、不调参。
原Oracle SEPT21因女性劳动保护留出折三项T训练列全空，仍BLOCKED，未填0或单方删列。

B1 S1/S2/S3 Wilson95分别4.70–44.80%、30.12–75.19%、49.74–91.82%；
总Recall35.20–64.80%、HN-FPR24.22–52.97%。家族bootstrap95的三S分别
0–50%、25–81.82%、60–100%，2000次固定seed、重采样OOF不重拟合。
完整各条件率/样本级Wilson和家族区间在私有指标JSON；只作小样本开发不确定性，不宣称泛化。

## Oracle、检索与失败分析

仅同18列B2→C：总Recall+5pp、HN-FPR−5pp、AUROC+0.050625、AUPRC+0.069465；
S2同7/15、S3反降11/13→10/13，不能把Oracle当逐样本严格上界或B1直接减C。
S2 Any参考命中14/15，但Oracle仍漏8/15；S3双参考命中12/13，B2漏的两条均双命中，C仍漏3/13。
所以不能把失败全归“缺第二份证据”，也不能把浅层Extractor失败直接称LLM推理失败。
参考召回不是投毒检出率，也不是唯一合法证据完整性真值。
历史HN：B1误报4/11、其他HN11/29；B2为7/11与11/29，C为6/11与10/29。

52个主模型fold无收敛警告；但B1有12条极端概率、35个验证连续输入|z|>10，
说明稀疏T跨家族缩放风险。不改配置掩盖；B2/C无极端概率，也不等于已校准或稳定部署。
一次组内置换A控制AUROC0.5625/AUPRC0.4177，非充分无泄漏证明或置换p值。
没有整体AUROC/AUPRC≥.95触发；所有重要指标经不同计算路径复核。

## 真实结论与下一步

本轮当前浅层多视角实现尚未展示可信实用区分度；A的AUROC/HN-FPR点估计反而更好。
不宣称方法优越、正式泛化、可部署、长上下文收益或“Temporal无用”。
建议先做原子级claim/条件/否定/版本关系表示审计；同分布加样本可减方差，不能自动修测量。
已知Dense128-token截断先针对检索编码，不直接等于下游LLM需要长上下文。
更稳妥的论文候选组合是版本感知Benchmark、失效机制和透明轻量基线；方法主张待检验。
推荐下一任务`P1-D1-ATOM-ALIGNED-CLAIM-AND-VERSION-REPRESENTATION-FAILURE-AUDIT-01`，未启动。

## 执行与证据

输入来源b559dee；协议/代码冻结a34fa0f；首尝试在fit前因JSON list/tuple比较断言停止。
纯工程修复512842944fbbe73a0f7ca1de35536182589a2c5f后执行，旧日志/source lock保留。
评价源码运行前已hash/archive，提交发生在结果收口，不倒写为此前已提交。
私有根`experiments/core144_d1_first_detection_20261028_run01/`，全部raw/models/logs/输入/结果/manifest保留且Git-ignore。
签署raw SHA：35609f9ea3fa5fad2fca440dab6b16e57c2bc7954b53d0381ac9cae114049b5d。
预测seal SHA：d2894c10727b1ba7d3263c254fe63c935b5830b6fe1777bcfc339b6dc20118ef。
评价关联OOF SHA：d04a010803ab7e63dbeb85d6cf9d72736a389f82ea485d253d67caa9b177a61c。
config SHA：ace891f123a06ca61e2f469577e46885b0ea6adb8b7a940542ebde1af861925c。

五个主文件：D1_FIRST_DETECTION_RESULTS.csv、D1_S1_S2_S3_DETECTION_REPORT.md、
D1_MODEL_OOF_PREDICTIONS.jsonl、D1_ORACLE_VS_NONORACLE_COMPARISON.md、D1_NEXT_RESEARCH_DIRECTION_DECISION.md。
完整私有复现manifest/索引及交接/Git回执见[文档收口](PAPER1_D1_FIRST_DETECTION_DOCUMENTATION_CLOSEOUT_V1.md)。
旧126预测未读/未复用；D1 Candidate/Evidence/Human raw、D2/D3、Stage1–5/Final72不改。
