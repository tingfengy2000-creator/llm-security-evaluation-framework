# Failure Taxonomy：T1-T9

## 本阶段目标

把“最终 FAIL”拆成可行动的失败原因，而不是只保留一个二元结果。

| 类型 | 名称 | 解释 |
|---|---|---|
| T1 | True Attack Success | 原始模型输出达成攻击目标 |
| T2 | Detector Miss | detector 判 PASS，但原始输出有风险 |
| T3 | Guard Bypass | 开启防护后最终输出仍有风险 |
| T4 | Partial Containment | 防护采取动作后仍残留风险模式 |
| T5 | Over-blocking | 正常请求被输入或输出防护拦截 |
| T6 | Context Accumulation Failure | 多轮上下文累积后出现风险 |
| T7 | Confidentiality Breach | 输出合成机密 canary |
| T8 | Unsafe Tool Intent | 模型表达危险工具调用意图 |
| T9 | Side-effect Risk | 工具意图若执行将产生副作用 |

## 为什么这样设计

同样的 ASR 可能来自 detector 漏检、规则绕过或上下文累积。分类后，团队才能选择补 detector、扩规则、隔离上下文或收紧工具权限。

## 和 Stage 4.1 的关系

Stage 4.1 主要解释 input block 与 output block；Stage 5 把这些事件与模型风险、detector 结果和 benign 误拦组合成 T1-T9。

## 当前结论边界

分类器依赖显式字段和合成 pattern。多标签允许一条 Attempt 同时属于多个类型，计数之和可能大于 Attempt 数。

## 面试时怎么讲

“我把成功攻击、检测器漏检、防护绕过和误拦分开，因为它们的根因和修复负责人不同。”

## 不能夸大的地方

自动 taxonomy 是规则化归因，不是人工安全审计的替代品。
