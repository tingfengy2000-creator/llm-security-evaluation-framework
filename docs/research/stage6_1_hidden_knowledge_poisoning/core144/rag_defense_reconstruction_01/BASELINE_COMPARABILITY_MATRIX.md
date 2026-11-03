# 防御对照与可比性门

2026-11-04 JST；STRICT_COMPARISON_ELIGIBILITY=NO；不存在新查询级性能表。

| 条件 | 冻结前候选定义 | 当前实物/执行状态 | 后续必要门 |
| --- | --- | --- | --- |
| B0 | 原检索上下文直接给共同 QA 生成器 | 仅 no_defense 上下文直通；未生成答案 | 独立查询/答案、共同 QA 合同 |
| B1 | 同一固定 Qwen 逐片段核验＋过滤→共同 QA | 未实现新场景调用；旧 E1 仅短候选核验 | 对照 prompt、过滤三态、费用、引用失败处理冻结 |
| B2 | 固定作者 v0.2 两阶段过滤→共同 QA | 非论文 embedding 的核心 API 离线可用 | embedding/中文 tokenization/长度/Top-K/单多跳身份决策 |
| B3 | B2→同一 B1 核验→共同 QA | 未实现；不可省略的简单串联对照 | 与 B4 配对时必须存在，累计调用如实计费 |
| B4 | Query-conditioned Version and Provenance Consistency Check | PROPOSED；未实现，NO_CONFIRMED_IMPROVEMENT_GAP | 真实 B1/B2 可复现错误及版本/来源归因，Owner 审阅 |
| B5 | B4 去掉版本/来源约束 | 未实现 | B4 获准后冻结同预算消融，不能换骨干/证据 |

原版 B2 严格复现应固定论文 embedding、数据/攻击/检索器/Top-K/模型/指标/seed/环境并解释论文与代码差异。本轮替代 embedding 不具严格比较资格；可在明示迁移后做同任务方法比较，名称必须带 transferred / cached multilingual embedding，不称原论文复现或 SOTA 超越。采用作者默认 embedding 也不自动等于论文 Stella。

三方法输入/信号/资源的横表见[发表方法审查](PUBLISHED_METHOD_REVIEW.md)。FaithfulRAG 目标是忠实生成，GMTP 面向梯度与异常 token；都不能用未运行的论文数字填本 D1 对照格。

共同约束：同一查询/场景/反事实世界、检索集合及顺序、来源字段、可信证据访问、输入/输出预算、最终生成器、QA prompt、评分与失败分母；过滤后不补检索。额外核验调用属方法成本，不要求所有方法调用数相等，但不得隐瞒。完整保留纯净集合、合法历史、来源角色、正常缺证与拒答效用。

旧 E1 的 37/40 与新 B1 的 ASR/QA 不是同一任务、同一分母；不能从旧 Recall 推断新环境的弱点。虚构 query-time 相同删除只是工程现象，不能作为允许 B4 的真实数据证据。下游答案、真实自然错误漏检、合法历史误删或来源/适用范围失效均尚 UNKNOWN。

不允许通过缩短 B1 证据、给 B4 答案/额外官方库、将不适用历史标 Poison、选择 E1 已错案例、修改 scorer 或跳过 B3 创造方法优势。
