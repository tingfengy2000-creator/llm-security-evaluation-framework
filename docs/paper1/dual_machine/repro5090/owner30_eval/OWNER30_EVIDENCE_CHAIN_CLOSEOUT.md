# Owner30 证据链归档

状态 `EVIDENCE_INDEX_ARCHIVED / NO_NEW_SCORE / SCIENTIFIC_TRIALS_STOPPED / OWNER_ROUTE_DECISION_PENDING / HUMAN_GOLD=0 / FORMAL_ASR=NOT_MEASURED / FORMAL_ACCURACY=NOT_MEASURED`。
这是公开证据索引，不是新评分。Owner28、Owner29、Owner30 已封存结果都没有改。没有重新生成、重新检索，也没有调用模型或商业 API。Human Gold 仍是 0。Claim1–3 仍是 `NOT_RUN`。`AUTO_CONTINUE=NO`。

指令来自 5060 提交 `01d003309aeca67db232f39d31914efe3c3cd902` 的 `docs/paper1/dual_machine/chinese5060/W1_OWNER30_FEASIBILITY_CLOSEOUT_DUAL_MACHINE_PROMPTS_20261111.md`，blob `b0f1fb15c2108d7513b75298f788fe1549d8071b`，SHA256 `464ad35243c39af6522121a6c3b5c4480e928aa9f22d1398e154802522af3ecc`。只读取出，没有合并 5060。

## 本次核对

交接 ZIP SHA256 仍是 `9ae356d60a3ec62ab8fec1df732b9dc21a91f8694422e2ff1b0b56879271c6a4`。成员 SHA256 `55d981aa50e39eb45bb3ad45cb5e31d88e983ab5e6e6e9ea0d1c5a82a62e705e`。成员只有一个相对路径文件，没有绝对路径或目录穿越，没有执行，也没有解压进仓库。
6 条的世界集合等于已封存 RD_ZH 扣留格。每条原回答 SHA 等于该格 `response_sha256`，事件日等于评价前冻结的参考日期。6 条都不是参考值。
对照评价前封存的攻击目标，5 条恰好命中，1 条是数值错误但不是攻击目标。统一分母 22 上，NONE 0、RD_B2 0、RD_ZH 5。这与已封存的六条核验清单一致，所以没有另写一份评分。
两个纯范围攻击世界不在这个交接包里。范围主张 `UNKNOWN`，范围攻击命中 `UNKNOWN`。
封存攻击目标仍在私有托管文件里，容器 SHA256 `c4244e86fb2ecf1177cc3d2bb39b8791e1b789713fc3522bbfaa46b35b055595`。逐条命中标记的私有明细 SHA256 `d08a07828d18895b9404a373043faa5328b89c6298cf6b084a6546942256f947`。两份都不进入 Git。

## 公开证据索引

| 角色 | 引用 | SHA256 |
| --- | --- | --- |
| 只读收口指令 | 5060 `01d003309aeca67db232f39d31914efe3c3cd902` | `464ad35243c39af6522121a6c3b5c4480e928aa9f22d1398e154802522af3ecc` |
| 评价前参考原子 | `OWNER30_PUBLIC_REFERENCE_ATOMS_ONLY.json` | `8090432d51b3670108e5ce7bf18ca8ed76be45ec44ee64980def45429a61e6b9` |
| 参考原子清单 | `OWNER30_REFERENCE_FREEZE_MANIFEST.json` | `c1829ddc467db6e3138f94d2ad63625149a5251bae022f83447997137b0616ef` |
| 结构化回答 | 5060 `1760ca56dc87674c488fe1a197304dfbe4b4fc8e`，未复制到本分支 | `2a3e2f05cec1ffd1f2fba698546888ec105554da495e65706a8b0340426da0b3` |
| 短值区间报告 | `OWNER30_FAST_TARGET_BOUNDS_REPORT.md` | `bf622f8bb95b6ccefb77b0d8cf6c63bedfde294c9311bd8a4e982e1fd0232e32` |
| 短值区间清单 | `OWNER30_FAST_TARGET_BOUNDS_MANIFEST.json` | `0d2fbe7308218a7aa78962859a4800c4f438b1fa8f733b0f7f78a24cdb7f4b25` |
| 交接缺失补充 | `OWNER30_FAST_TARGET_BOUNDS_SUPPLEMENT_V2.md` | `e493565fefafa23eb9eca40c89c3e5edac579515afed0e06d1fc4856c9216e73` |
| 交接缺失清单 | `OWNER30_FAST_TARGET_BOUNDS_SUPPLEMENT_V2_MANIFEST.json` | `4e2ffc84315b578c38a068e661ef9824f49cb66889ec7e06f29c65532a71686e` |
| 六条目标核验 | `OWNER30_SIX_VALUE_TARGET_MATCH_REPORT.md` | `8de56c3b4bcc27891dda1abf47b802a00c3a44a79c36ced31018ae6ded08f9b9` |
| 六条目标清单 | `OWNER30_SIX_VALUE_TARGET_MATCH_MANIFEST.json` | `56179d1a244ed695a6cc8e91e920ec371c160a91162004ab99405d3105783473` |
| 六条核验脚本 | `scripts/research/score_owner30_six_value_handoff.py` | `4c47929eb98997e9c250325330224221911258b3fdc2a90a549e85ae625e50c4` |
| Owner28 评分 | `OWNER28_EVAL_INDEPENDENT_SCORE_REPORT.md` | `3c05598a6ec65a6f224549232703e03e1ec8fdcac52621698b8acd6aee420715` |

私有、不进 Git：交接 ZIP `9ae356d60a3ec62ab8fec1df732b9dc21a91f8694422e2ff1b0b56879271c6a4`，成员 `55d981aa50e39eb45bb3ad45cb5e31d88e983ab5e6e6e9ea0d1c5a82a62e705e`，攻击目标容器 `c4244e86fb2ecf1177cc3d2bb39b8791e1b789713fc3522bbfaa46b35b055595`，命中明细 `d08a07828d18895b9404a373043faa5328b89c6298cf6b084a6546942256f947`。
区间文件里的 `[0, 6]/22` 和 V2 的“当时未收到六条”都保持原样。闭合后的 5/22 只记在六条核验报告里。5/22 不是正式 ASR，也不能证明因果。

## 以后真人复核

1. 重算上表每个公开文件的 SHA256，必须与表内一致。
2. 在 5090 私有机上重算攻击目标容器和命中明细的 SHA256。两份文件都不复制进 Git。
3. 重算交接 ZIP 和成员 SHA256。只检查成员名：恰好一个相对路径，没有绝对路径，没有目录穿越。不执行归档内容。
4. 用 5060 `1760ca56dc87674c488fe1a197304dfbe4b4fc8e` 的结构化回答核对 6 条世界集合、原回答 SHA 和事件日。
5. 只在私有机上把 6 条数值与评价前攻击目标做完全匹配。期望是 5 条命中，1 条数值错误且不是攻击目标，6 条都不是参考值。
6. 两个纯范围世界不在交接包里。没有回答原文时，范围主张和范围命中保持 `UNKNOWN`。
7. 本索引不能当作 Human Gold，也不能据此填写正式 ASR 或准确率。

## 保留的边界

32 个世界来自 4 个事实组，不是 32 个独立事实。62 条公开短值是白名单筛选后的数值，不是准确率。68 条回答的范围和引用支持仍是 `UNRESOLVED`。缺失的 1 个 NONE 单元格仍是 `MISSING_INPUT`，不补算。
负责人是否把下一阶段改成中文隐蔽污染基准和失效分析，本归档不代签。`AUTO_CONTINUE=NO`。
