# Paper1｜外部技术评审指令（直接粘贴评审对话）

你现在是独立评审人，研究方向为网络安全、RAG/LLM知识污染防御、中文多文档投毒。请对 Paper1 最新两机验证进行**严厉的可证伪方法评审**，不要替我们找理由调参成功。

项目研究分支：
- 5060 `research/paper1-chinese-defense-5060`：Owner33开发源 `11880c5be71e22d73217c32e0c779fbf8b117741`，实际DEV和EVAL交接 `108b35c9239ad113c50f7d84daf9b84f361b37d6`。
- 5090 `research/paper1-ragdefender-repro-5090`：独立一次性评分 `d7d28cc7cab25b1ade04fcb8b0678bd369c3b558`。
- 完整评审包位置：`docs/paper1/dual_machine/chinese5060/OWNER33_TO_EXTERNAL_REVIEWERS_CRITICAL_REVIEW_PACKET_20261111.md`。请先阅读该文件及文件内指定的源码、统计、来源快照、DEV/EVAL报告；可读公开Git，不要接触任何5090私有Gold。

必须注意的事实：DEV旧32世界中，B2的P保留20/45、C误删40/63，VCARE为P7/45、C10/63，但B2_ALWAYS_VERIFY的P也为7/45；独立32新世界中B2和VCARE P11/34、C误删35/59、H误删0/1、O误删8/8，所有mask一样；新EVAL Frozen Intent识别0/32、来源命中0/32；新方法源码仅有三个硬编码领域。HumanGold0，ASR/最终正确率未测，5090原论文Claims1–3未跑。

请完整回应评审包W1–W7，**特别审查新EVAL来源快照中 `short_fact`和`selection_status`造成的隐藏Oracle/选材泄漏**，同预算补检基线是否公平，以及这批失败究竟是否值得用通用实体-属性-时点-scope对齐修复。审查2026已有研究：RAGDefender、FRESCO、TCR、TRIS、RAGSentinel、CEG-RAG，避免建议已发表的简单方法作为论文创新。

你的目标不是写论文，也不是给工程机器执行代码。必须给出唯一总裁决 `A_GO_FOR_SMOKE_ONLY / B_BASELINE_FIRST / C_BENCHMARK_FIRST / ALL_NO_GO`，3条最严重缺陷，每条对应Git证据，1项最小且公平的可证伪实验，明确STOP/GO门。若确实缺乏值得尝试的方法，直接回答停止算法研究。每个没有核实的数字都标NOT_VERIFIABLE。写回评审意见让我转交Owner，不能自称HumanGold审阅。
