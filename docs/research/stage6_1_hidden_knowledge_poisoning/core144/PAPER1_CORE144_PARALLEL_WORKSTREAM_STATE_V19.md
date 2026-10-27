# Core144 并行状态 V19 — D1特征已物化，等质量签署及Oracle工程门

2026-10-27；PODR-144 / OR-098 / REL-2026-0113；source HEAD2ce4b1c。
[本轮记录](PAPER1_D1_QUALITY_AND_SEPT_MATERIALIZATION_RECORD_V1.md)。
仅追加替代V18的D1质量/物化字段；不覆盖旧失败、raw、Guide或D2/D3审批。

| 轨道 | 当前真实状态 | 下一门 |
| --- | --- | --- |
| D1 Human/QA | 55非空/2null已核；33符合待签、21 HOLD-only、1范围未证；另18规范化建议 | Owner批量签署40组集合及适用QA，保留8组HOLD，不重标54条 |
| D1 qualification | 建议40组120条/13family；8组24条HOLD；有效评价0/0 | D1_DEV资格明确签署；不自动提升AI为GT |
| D1 retrieval | 33可信文档，144×3完整排名14,256条；固定配置精确重放PASS | 不按参考召回调query/模型/权重 |
| D1 features | B/C各144×21；非Oracle1991/3024、Oracle1642/3024 computed | 材料可比但不是检测效果；仍有启发式/元数据限制 |
| D1 Oracle | 13-family预检一折三T训练列全空，冻结imputation不能fit | Owner独立决定可比缺失策略；不单独删C列/填0 |
| D1 classifiers | 本轮A/B/C fit=0；无新OOF或性能；旧126隔离不复用 | 质量与工程门闭合后才允许新Run |
| D2 | 两条新HN待原会话定向Phase1/2；全144尚未最终验收 | 原外部复审门不变，未发Human Excel |
| D3 | 两S3原证据必要性门未变 | 原审批门，本轮未推进 |
| Core formal | D1_DEV_EXPOSED；GT/2/1/1未执行 | 不把D1当未来untouched test，不根据诊断改D2/D3 |

`D1_DATA_QUALITY_GATE_PENDING / D1_SEPT_MATERIALIZED / D1_PERFORMANCE_NOT_ESTIMATED`。
AUTO_CONTINUE=NO；S1/S2/S3 Recall、HN-FPR、AUC/CI与Oracle检测差距均未知。
