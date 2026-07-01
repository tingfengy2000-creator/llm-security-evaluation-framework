# A1-A6 攻击矩阵

## 本阶段目标

使用统一 JSONL schema 管理 12 条攻击和 10 条 benign 请求。

## 为什么这样设计

每条数据都包含 sample ID、threat layer、risk goal、expected patterns、官方 detector
配置、严重度和证据范围，便于审计分母。

## 和上一阶段的关系

保留多轮 `[[TURN:*]]` DSL 和 prompt hash parity，并增加 schema version 与 evidence scope。

## 当前结论边界

每个 Attack ID 仅 2 条 smoke，主要验证方法与链路。

## 面试时怎么讲

统一 schema 让 Dataset Runner 不依赖 garak scheduler，也能稳定复跑。

## 不能夸大的地方

expected pattern 是合成 oracle，不是通用语义安全分类器。
