# Owner30｜短包 Qwen Judge 补充执行报告

`68_PACKETS_FROZEN / JUDGE_NOT_ADMITTED / 0_SENT / NUMERIC_PROXY_COMPLETE / STOP`。同步基线 `3756b240994f491b85d732e080fb29f2e7907f03`。先封存旧 95 条逐格判断、原报告和私有规则详情，逐字节验证后才建立 68 个短包。原报告和 68 条 UNRESOLVED 保持不变。无重新生成、检索、过滤或重试。 [数值代理报告](OWNER30_NUMERIC_AGREEMENT_PROXY_REPORT.md)

## 包与准入

- 北京固定 `qwen3.7-plus-2026-05-26`、temperature=0、非思考、非流式、无联网工具和缓存写入。每包只含原问题、原回答引述、事件日、公开参考短值、范围和保留引用，不传臂、世界 ID、标签或攻击目标。所有内容视为不可信资料。
- 固定提示、六字段响应 schema 和实际序列化 JSON。68 包长 1,357–2,563 字节，总计 122,474 字节。已证明的 4,096 总输入 Token 上界为 0/68，字节数无法替代服务端 Token 化及模板开销。
- 输出字段设 118，留出官方说明的最多 10 Token 偏差，以满足 128 上限。在 4,096 输入和 128 输出上界获得验证的前提下，68 条北京低档原价 CNY 0.626688，保守高档 CNY 1.880064，约 USD 0.28。尚无可执行的预留结论。 [北京固定快照费率](https://help.aliyun.com/zh/model-studio/qwen3-7-plus) · [输出偏差](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions) · [中国银行牌价](https://www.boc.cn/sourcedb/whpj/)
- 配置缓存未发现固定快照可核的 tokenizer 与 chat template；当前北京账户余额及在途费用无可核对账；通过字段和秘密模式筛查，逐包出站权利未闭合，放行 0/68。未发 Token 探测。

## 实际账本与结论

Judge 0 请求、0 返回、0 Token、0 重试，新增 **USD 0.00**，无请求 ID。原范围和引用未决为 **68/95（71.6%）**，占原 ANSWER 的 68/68。计划 Judge 与生成器是同一 Qwen 快照，任何后续模型结果仅能标记 LLM_JUDGED_PROVISIONAL。当前结论仍为 MIXED/INCONCLUSIVE，新增证据仅为数值代理差异。

执行 `python -B -m llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner30_small_packet --docs <旧Git受控副本> --custody <D盘回答导出> --grades <D盘规则结果> --out <D盘补充目录>`，退出码 0。虚构样本测试 7 项通过，Ruff 和 MyPy 通过，68 个请求哈希与 ZIP 成员独立复核。所有私有短包、原文、逐条扣留值判定均留 D 盘。 [补充 Run Manifest](OWNER30_QWEN_JUDGE_SUPPLEMENT_MANIFEST.json)
