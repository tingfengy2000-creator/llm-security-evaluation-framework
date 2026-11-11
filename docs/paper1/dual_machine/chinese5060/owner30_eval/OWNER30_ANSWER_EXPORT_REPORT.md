# Owner30｜封存回包只读核验与评分准备

状态 `G0_VERIFIED / G1_AWAITING_REFERENCE / RULE_SCORED_0 / JUDGE_SENT_0 / HUMAN_GOLD_0`。仅处理 Owner29 已封存的回包。本轮未重新生成、检索或运行任何过滤臂。

| 项目 | 核验结果 |
| --- | --- |
| 原计划格数 | 96，首格 NONE 原样保留为 UNRECOVERABLE_MISSING |
| 可核验回包 | NONE 31，RD_B2 32，RD_ZH 32，共 95 |
| 原始状态 | ANSWER 68，ABSTAIN 27 |
| 配对分母 | 主分析 31 个完整三臂世界，次分析 32 个 RD_B2/RD_ZH 配对 |
| 完整性 | 95 个响应 ID 唯一，全部回包 SHA 与 Seal、请求、引用编号及用量收据一致 |
| 评分规则 | 读取真实回包前冻结，虚构样本测试 4 项通过，Ruff 和 MyPy 通过 |
| 实际评分与调用 | 确定性真实评分 0、模型 Judge 0、新增费用 USD 0.00 |

私有回答保留原字符串和原状态。导出使用随机响应键，不含比较臂，臂映射和引用原文分文件放在 D 盘 Git 忽略目录。未进行外传内容批准或原文交接。Git 仅存封存哈希、聚合计数和规则源码。完整命令为 `python -B -m llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner30_auto_eval --owner29 <D盘Owner29归档目录> --private-out <D盘空的Owner30目录> --rubric <OWNER30_GRADE_RUBRIC_V1.json>`，退出码 0。另行重读三份私有导出，复核 SHA、95 个响应键和 96 格映射。

5090 已读取远端提交 `aed1f1b47256be6503d9f653aa04d09fffe0c3cd` 的两个白名单路径，均未找到。下一步需 5090 发布 `owner30_eval/OWNER30_PUBLIC_REFERENCE_ATOMS_ONLY.json` 与 `owner30_eval/OWNER30_REFERENCE_FREEZE_MANIFEST.json`。通过 32 世界、事件日期、范围和来源的准入校验后，使用当前冻结规则评分。当前正确、错误、无依据、未决和 Source-support 无真实计数，31 个配对没有暂定准确率。私有攻击目标命中由 5090 独立计算。

如后续启用 Judge，模型与生成器均为同一 Qwen 快照，存在同模型相关偏差。现未形成可发送 Judge 包，内容外传、当前账户及逐请求 Token 和 USD 0.50 上限仍需核验。正式准确率、正式 ASR 均为 NOT_MEASURED，Human Gold 为 0。停止于参考资料门。
