# Detector 方法

## 本阶段目标

严格区分 `garak` 官方 detector 和 `stage5_pattern` 自定义 detector。

## 为什么这样设计

来源混淆会把本地规则的结果错误包装成官方 garak 结论，破坏方法可信度。

## 和上一阶段的关系

旧 adapter 只规范化布尔值；新 adapter 直接构造 garak Attempt 并调用 Detector API，
不使用 probe、harness 或 scheduler。

## 当前结论边界

没有适用官方 detector 时记录 not applicable，不计入 DMR 分母。

## 面试时怎么讲

Detector Coverage 与 Detector Miss 必须一起报告，否则低漏检可能只是覆盖不足。

## 不能夸大的地方

pattern detector 的高召回不能外推到语义改写和未知攻击。
