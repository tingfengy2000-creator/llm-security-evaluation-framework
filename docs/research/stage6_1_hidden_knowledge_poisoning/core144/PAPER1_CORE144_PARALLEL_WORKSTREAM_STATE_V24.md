# Core144状态V24 — VACE-F5真实开发诊断完成，低覆盖待Owner审阅

2026-10-28；PODR-149 / OR-103 / REL-2026-0118。
Task `P1-VACE-LITE-V03-F5-IMPLEMENTATION-AND-D1-DIAGNOSTIC-01`。
[实测](vace_lite/VACE_V03_IMPLEMENTATION_AND_TEST_RECORD.md)、[决策](vace_lite/VACE_V03_NEXT_RESEARCH_DECISION.md)。

| 轨道 | 真实状态 | 下一门 |
| --- | --- | --- |
| V03-F5 / V02-NA-F5 | 同120新预测各一次，240条先封存再评分；同证据/规则最终逐条一致 | OWNER_REVIEW_REQUIRED |
| 分层效果 | 两者S1=1/12、S2=4/15、S3=1/13，总6/40；C/HN误报均0/40 | 不能据零误报称有效 |
| 弃权/组内 | 114/120弃权，80/80负例弃权；严格成功0/40 | 科学覆盖不足，不是正常知识已放行 |
| 证书/路由 | I早退1，公布机关反证4，版本方向反证1；V03正文消费595份/NA600 | 仅小额调度差异，非泛化/生产加速 |
| 数据 | 签署40组120条13家族，8组24条HOLD；D1_DEV_EXPOSED | 原数据/人工/GT/Guide不变 |
| 检索/元数据 | 原33文档Corpus/Registry V2/Hybrid Top5；120/120身份一致 | 不扩池/不新增来源 |
| D2/D3 | 独立质量/GT/来源家族门保持 | 本轮不运行、不改构造数据 |
| L0 / L0-Oracle | NOT_EXECUTED | 仅建议独立preflight，需Owner批准 |
| 正式研究 | 无Core正式GT/split/训练/校准/Stage B | 无任何正式测试/方法优越性结论 |

源码冻结559ff45321dcb5d28c750afc69758ee45a9c099d；协议/输入/预测/模型SHA、命令/日志、
逐样本slots/证书/模块/证据/cost与复现工件在`experiments/vace_v03_f5_20261028_run01/`。
50项边界/既有合同测试通过，原始/历史不可变；当前低检出是实测，不再补规则追分。
`VACE_V03_F5_DEV_DIAGNOSTIC_COMPLETE / OWNER_REVIEW_REQUIRED`，STOP；V23及以下为历史。
