# 四模式结果对比

## 本阶段目标

比较 passthrough、input-only、output-only、full-guard 在每类攻击上的 ASR、拦截率、上游调用率、漏检率、绕过率和延迟。

## 为什么这样设计

总表回答整体变化，`attack_coverage_heatmap.csv` 回答哪一类攻击导致变化。分析时先确认 `run_status` 和 parity，再读取指标，不能把无效 run 纳入结论。

## 和 Stage 4.1 的关系

Stage 4.1 只有两个 probe；Stage 5 使用同样的四模式，但将结果展开到六类 attack category，并加入 10 条 benign 请求。

## 当前结论边界

当前仓库中的最新结果由离线 mock 回归生成，用于证明数据流、validator 和报告完整。真实模型结果尚未在 Stage 5 自动执行。

最新离线 run：`20260701T030819Z-05703f`，22 个样本、88 个 Attempt，`run_status=completed`，prompt hash parity 与 raw output hash parity 均通过。

| Guard Mode | ASR | Input Block | Output Block | Upstream | Guard Bypass | Over-block |
|---|---:|---:|---:|---:|---:|---:|
| passthrough | 100.00% | 0.00% | 0.00% | 100.00% | 0.00% | 0.00% |
| input-only | 91.67% | 8.33% | 0.00% | 91.67% | 91.67% | 0.00% |
| output-only | 100.00% | 0.00% | 0.00% | 100.00% | 100.00% | 0.00% |
| full-guard | 91.67% | 8.33% | 0.00% | 91.67% | 91.67% | 0.00% |

这组故意可攻击的 mock 结果说明：历史输入规则只覆盖 12 条攻击中的 1 条，历史输出规则没有覆盖本矩阵的合成风险标记。它验证了框架能暴露规则边界，不代表防护“退化”，也不能与 Stage 4.1 的两条专门规则样本直接比较。

## 面试时怎么讲

“我先做离线 88-Attempt 回归，保证报告链可靠，再运行真实接口。这样真实调用的每一笔额度都用于模型实验，而不是调试文件路径。”

## 不能夸大的地方

离线 mock 的 ASR 不能作为模型安全结论；只有标记为真实 provider 且验证通过的 run 才能用于真实模型对比。
