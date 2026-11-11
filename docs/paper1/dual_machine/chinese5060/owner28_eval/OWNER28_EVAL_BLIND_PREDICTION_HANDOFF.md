# Owner28｜5060 独立评价盲预测交接

2026-11-11 JST。状态为 PREDICTION_READY_FOR_INDEPENDENT_5090_EVAL / SCORING_PENDING。

| 阶段 | 实际状态与证据 |
| --- | --- |
| G0 | 5060 执行 HEAD ba00a195eee55a2b3f6ad02a5d18854d308ce0ce。冻结代码提交 8d879235874ee91a2462cfbaa04c2e3e8cb36ae8，源码 blob、MiniLM 缓存、依赖和上游身份核验通过。 |
| G1 | 5090 兼容提交 0a4fde3966d9eefd3562f4d552f12090c7632ac9 的三件套哈希与交接回执一致。原角色盲包及原清单的 Git blob 一致。桥接审计记录 32 条问句和 352 段文本按原序保留，4 组、3 谱系、2 类签发机构。专利法 HTTPS 转载等价性依据 5090 审计。 |
| G2 | 冻结 check 退出 0，32 个主世界通过。7 个原始镜像单列 MIRROR7_NOT_RUN_NOT_IN_HEADLINE。 |
| G3 | 一次性 predict 退出 0。检索 32/32，32 个索引重开复核，160 个 TopK 槽，NONE、RD_B2、RD_ZH、DATE_ONLY 各 32 个掩码。封存完整 TopK 与盲预测。 |
| G4 | 等待 5090 独立评分，当前核验到评分 0/32，Human Gold 0。 |
| G5 | 5060 推送仅含不透明编号、秩、掩码与哈希的投影，以及运行证据和 Tracker。原始内容与完整 trace 留在 D 盘私有归档。 |

5090 在确认 5060 交接 Git 提交后，只读获取本目录的角色盲投影与原 runner 公开收据。投影 SHA256 为 5c9874bd6bb3252a2685e8481b92ea979dc1e842b5f3250a798e2bb7f03d21bb。每行 world_id 对应一个主世界，topk 逐条给出一基 rank、document_id 和 chunk_id。keep_ranks 中每臂保存要保留的一基原秩。由 5090 用其私有新旧编号映射核对世界及文档，再在本机打开托管标签一次评分。若编号不能核对，按协调规程停止。只回传聚合统计、匿名失效类型、分母与评分封存 SHA。

完整预测 SHA256 为 46979484afcc0708c104c98b72461bab2bf168127febf627c01c8e30a2d9258a，预测封存 SHA256 为 aeb47a49f915c55fd2c7e5679de63cfce664282667f9a818ed27b9dfc7b1205e。TopK 封存 SHA256 为 31ce5b1acfbfb0d6ceebe4acedda0f482ca506462baf48dd9f4ff36a37e4bd45。私有归档 244 个索引成员逐件回读，SHA256 为 c8c1f23308959b68ba70010d0096b8543e99132fdbd755b1d101ab0210b3206c。

本地执行 34.281 秒，CPU 限额 2，商业调用、下载和费用均为 0。检索中位/P95 为 286.56/610.04 ms。RD_B2 与 RD_ZH 的每臂逻辑过滤时延含共同编码，中位/P95 分别为 201.49/225.55 与 204.61/227.58 ms。候选级有效性指标待 5090 回执，正式 ASR 和答案准确率未测。

[角色盲预测投影](EVAL_PREDICTIONS_5060_ROLE_FREE.json) · [公开收据](PREDICTION_PUBLIC_RECEIPT.json) · [Run Manifest](OWNER28_EVAL_RUN_MANIFEST.json) · [协调规程](../../OWNER28_5090_TO_5060_SCHEMA_BRIDGE_AND_ONE_SHOT_HANDOFF_20261111.md)
