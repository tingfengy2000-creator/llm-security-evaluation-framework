# Detector Miss 分析

## 本阶段目标

识别“detector 判定通过，但原始模型输出已经出现风险”的 T2 情况，并输出 Detector Miss Rate。

## 为什么这样设计

PASS 只表示某个 detector 没有命中。把原始风险标签与 detector verdict 交叉，才能发现 detector coverage gap，而不是把 PASS 误读为绝对安全。

`detector_source=stage5_pattern` 表示 Stage 5 的回退适配层；只有明确标记 `garak_official` 的记录才是官方 garak verdict。

## 和 Stage 4.1 的关系

Stage 4.1 主要使用 garak 自带 detector；Stage 5 增加 adapter，使外部 verdict 和本地 pattern verdict 进入同一 AttemptRecord，但保留来源字段避免混淆。

## 当前结论边界

pattern detector 与风险标签相关，离线回归中的漏检率主要验证计算逻辑，不能代表官方 detector 的真实召回率。

最新离线 mock run 中 T2 为 0，原因是回退 detector 与合成 risk pattern 使用相同的显式标记。这是一个“测试链一致”的结果，不是 detector 泛化能力证据。T2 的代码路径由独立单元测试覆盖。

## 面试时怎么讲

“我显式记录 detector source。否则把本地正则的 PASS 写成 garak PASS，会造成方法学错误。”

## 不能夸大的地方

低 Detector Miss Rate 可能只是测试 pattern 简单，不代表对语义变体、隐喻或多语言攻击具有高召回。
