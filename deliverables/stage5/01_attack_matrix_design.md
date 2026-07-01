# 攻击矩阵设计

## 本阶段目标

用统一 JSONL schema 表达六类攻击和正常请求，使每条样本可定位、可分组、可哈希和可复跑。

## 为什么这样设计

每条样本包含 `id`、`category`、`variant`、`risk_goal`、`prompt`、`expected_risk_patterns`、`expected_guard`、`severity` 和 `notes`。`risk_goal` 描述安全目标，`expected_risk_patterns` 是评测标签，`expected_guard` 是预期规则，不应被误当成模型输入。

多轮样本使用受限 DSL：

```text
[[TURN:user]]...
[[TURN:assistant]]...
[[TURN:user]]...
```

Renderer 将它转换为 messages，并对规范化结果计算 SHA-256。四模式哈希一致，才能证明输入公平。

## 和 Stage 4.1 的关系

Stage 4.1 的 prompt 由 garak probe 产生；Stage 5 把样本作为一等数据资产，允许按 category 和 variant 解释结果，同时延续 prompt hash parity。

## 当前结论边界

每类 2 条只覆盖代表性机制，不覆盖语言变体、长上下文、多轮自适应攻击和真实业务数据。

## 面试时怎么讲

“矩阵不是 prompt 列表，而是带风险目标、期望检测信号、严重度和版本语义的数据集。统一 schema 让指标分母和失败归因可审计。”

## 不能夸大的地方

`expected_risk_patterns` 是合成标签，不是通用安全判定器；命中率不能外推到未覆盖攻击。
