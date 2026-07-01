# T1-T9 Failure Taxonomy

## 本阶段目标

自动归因真实攻击成功、Detector Miss、Guard Bypass、部分遏制、误拦、上下文累积、
机密泄露、危险工具意图和副作用风险。

## 为什么这样设计

相同 ASR 可能对应不同根因，taxonomy 决定应修改 detector、Guard、上下文还是工具权限。

## 和上一阶段的关系

保留 T1-T9，强化 T2 必须有官方 detector coverage。

## 当前结论边界

一条 Attempt 可以有多个标签，计数之和可大于 Attempt 数。

## 面试时怎么讲

Failure Taxonomy 把“失败了”转成可分派给不同团队的修复任务。

## 不能夸大的地方

规则化归因不能替代人工安全审计。
