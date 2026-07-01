# 指标方法

## 本阶段目标

输出 ASR、Raw ASR、DMR、Detector Coverage、GBR、输入/输出拦截率、上游调用率、
Over-block 和延迟分布。

## 为什么这样设计

所有 rate 同时记录 numerator、denominator 和 percentage，防止分母不透明。

## 和上一阶段的关系

修正 DMR 与 GBR 分母，并增加 median、p95 与跨层 coverage。

## 当前结论边界

mock 延迟只用于测试；真实网络延迟必须由 live measurements 单独分析。

## 面试时怎么讲

安全性、可用性、成本和 detector coverage 必须联合解释。

## 不能夸大的地方

小样本百分比没有统计置信区间，不能作为生产 SLA。
