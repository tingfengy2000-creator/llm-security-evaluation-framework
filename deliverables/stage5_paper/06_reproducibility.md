# 可重复性设计

## 本阶段目标

相同 mock 输入生成相同 experiment fingerprint、attempt ID 和 canonical log。

## 为什么这样设计

时间戳、延迟和随机 request ID 会破坏字节级复现，因此放入 measurements sidecar。

## 和上一阶段的关系

保留 prompt hash parity，新增 canonical/measurement 双日志。

## 当前结论边界

远程模型可能因版本与路由变化产生不同输出，流程确定不等于供应商输出确定。

## 面试时怎么讲

我把可复现的实验事实与不可复现的运行测量分开保存。

## 不能夸大的地方

不能承诺真实 Groq 在相同 seed 下永远输出同一内容。
