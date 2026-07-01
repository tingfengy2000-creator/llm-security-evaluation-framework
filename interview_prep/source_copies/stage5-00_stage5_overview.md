# Stage 5 总览：Attack Matrix + Failure Taxonomy

## 本阶段目标

Stage 5 把 Stage 4.1 的两个 smoke prompt 扩展为可复现的评测框架。核心实验张量是：

`Attack Category × Guard Mode × Metric × Failure Type`

攻击面包含 prompt injection、role confusion、encoding obfuscation、context injection、data exfiltration 和 tool injection；防护模式固定为 passthrough、input-only、output-only、full-guard。

## 为什么这样设计

只报告一个总 ASR 会掩盖差异：输入防护可能拦截某类攻击，却对另一类完全无效；输出防护可能降低最终风险，却仍让危险内容在上游生成。矩阵化结果能回答“哪里有效、哪里失效、代价是什么”。

完整链路：

```text
JSONL 样本 -> Prompt Renderer -> 四种 Guard Mode
-> OpenAI-compatible 模型调用 -> 风险判定
-> Detector Adapter -> T1-T9 -> 指标与报告
```

## 和 Stage 4.1 的关系

Stage 4.1 证明四模式消融能够运行，并验证 output-only 先调用上游再拦截。Stage 5 保留同样的模式语义与历史 `GuardEngine`，增加统一数据 schema、六类攻击、benign 对照、失败分类和科学不变量验证。

## 当前结论边界

当前数据每类只有 2 条，是 smoke set。离线 mock 用于验证框架，不代表真实模型表现；真实 provider 必须另行执行并保留 run_id。

## 面试时怎么讲

“我没有只扩大 prompt 数量，而是把攻击类别、消融模式、风险指标和失败原因统一进 Canonical AttemptRecord，使每次实验都能复跑、聚合和审计。”

## 不能夸大的地方

所有结论必须写成“当前攻击矩阵和当前规则基线下”。这不是生产防护率，也不能证明模型绝对安全。
