# Core144 并行状态 V21 — D1首轮四条件开发检测已执行

2026-10-28；PODR-146 / OR-100 / REL-2026-0115；Run D1-FIRST-DETECTION-20261028-R01。
[结果记录](PAPER1_D1_FIRST_DETECTION_RESULTS_RECORD_V1.md)，[协议](PAPER1_D1_FIRST_DETECTION_PROTOCOL_V1.md)。
V20是拟合前快照，V19与未签表停止记录保留为历史。

| 轨道 | 当前真实状态 | 下一门 |
| --- | --- | --- |
| D1 qualification | 40组120条13family已签D1_DEV；8组24 HOLD | 不提升Core正式GT |
| D1 detection | A/B1/B2/C各13折120 OOF，共480；预测seal先于角色/S评价关联 | 本轮完成收口后STOP，不追分 |
| D1主报告B1 | S1=2/12、S2=8/15、S3=10/13；总20/40，HN15/40，AUROC0.5306 | 尚未展示可信实用区分度 |
| D1同列B2/C | Recall21/40→23/40，AUROC0.5366→0.5872；S3不改善 | 先审事实/版本表示，不把Oracle当部署效果 |
| D1 original Oracle21 | 三项T全空训练折，仍BLOCKED | 不临时填0/删列 |
| D1 uncertainty | Wilson及2000家族bootstrap；13独立家族/小样本 | 非总体泛化结论 |
| D2 | 两条修复HN原会话定向复审门 | 未推进/数据不变 |
| D3 | 两S3原证据路径门 | 未推进/数据不变 |
| Core formal | GT/2/1/1未执行；D1_DEV_EXPOSED | D1不得再称untouched test |

推荐原子对齐claim/版本关系失效审计，仅推荐未启动；不进行校准/Stage B/新模型下载。
`D1_EXPLORATORY_DEV_DIAGNOSTIC / D1_DEV_EXPOSED / D2_D3_CONSTRUCTION_DATA_UNCHANGED /
CORE_FORMAL_SPLIT_NOT_EXECUTED / CORE_FORMAL_GT_NOT_FROZEN`。
