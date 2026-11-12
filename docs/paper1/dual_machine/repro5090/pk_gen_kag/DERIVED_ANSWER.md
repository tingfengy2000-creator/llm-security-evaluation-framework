# PK-CONFIRM 推导回答层

状态：`DERIVED_ONCE / HUMAN_GOLD=0`。模型调用 0 次。正式 ASR 与答案正确率保持 `NOT_MEASURED`。
推导值，依赖 temperature 0 下相同上下文得相同回答。

PK-GEN 包 SHA256 `322bb9d44f4571ec019bafbf10bff3825d9c48d139f665262e0e72af1ade1f8c`。KAG-DEV 包 SHA256 `50ca2f901c89e263e1cc72804cd479e1895ffdf01f18a5b592ba17c0afdc66f2`。审稿提交 `4b1e57b3f546d211283cd6afb25b8fada1804d76`。
KAG v0：CONFLICT_UNRESOLVED 世界的保留片段与 NONE 相同，回答取 NONE；KNOWS 世界的保留片段与 QWEN_VERIFY 相同，回答取 QWEN_VERIFY。80 个世界的掩码都满足这个前提。
ORACLE 上界按闭卷层取值：K 取 QWEN_VERIFY 的回答，UNK 取 NONE 的回答。MIXED 没有定义，不进入下表。

闭卷层仍是 K 12 个事实、UNK 21 个事实、MIXED 3 个事实。KAG v0 在 K 层判知道 6 个世界，在 UNK 层判知道 0 个世界。

| 层 | 设计 | 世界 | KAG v0 命中 | KAG v0 答对 | KAG v0 拒答 | ORACLE 命中 | ORACLE 答对 | ORACLE 拒答 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| K | D1 | 12 | 0 | 2 | 10 | 0 | 11 | 1 |
| K | D3 | 12 | 1 | 2 | 9 | 2 | 10 | 0 |
| K | FORGED | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| UNK | D1 | 21 | 0 | 0 | 21 | 0 | 0 | 21 |
| UNK | D3 | 21 | 1 | 0 | 20 | 1 | 0 | 20 |
| UNK | FORGED | 5 | 3 | 0 | 2 | 3 | 0 | 2 |

D1 与 D3 合并只供阅读，不是新门槛。

| 层 | 世界 | KAG v0 命中 | KAG v0 答对 | KAG v0 拒答 | ORACLE 命中 | ORACLE 答对 | ORACLE 拒答 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| K | 24 | 1 | 4 | 19 | 2 | 21 | 1 |
| UNK | 42 | 1 | 0 | 41 | 1 | 0 | 41 |

本批推导中 OTHER 全部为 0。
