# Paper 1 Baseline Matrix V1

Status = `PLANNED / NOT EXECUTED`

| Baseline | 角色 | 主要输入 | 输出 | 公平性与失败边界 |
| --- | --- | --- | --- | --- |
| Random | sanity baseline | 无 | random score | 不形成方法结论 |
| PPL | lexical-naturalness baseline | Candidate text | naturalness score | 固定模型/revision；不是事实核验 |
| MLM naturalness | lexical-naturalness baseline / Semantic signal | Candidate text | masked-token score | 固定 mask/config/model；不是 proposed core method |
| GMTP | strong external poisoning-defense baseline | Candidate/query/retriever-compatible inputs | detection score | 独立复现记录、配置、模型、retriever compatibility、token-gradient availability；不兼容时如实 fail closed |
| Semantic similarity | Semantic baseline | Candidate + Evidence | similarity score | 固定 embedding/revision/normalization |
| Semantic + NLI | conditional comparison | Candidate + Evidence | contradiction score | 仅在理论合理且可复现时启用 |
| S/E/P/T/R only | single-view baselines | 各自 view contract | per-view detection score | 每个 view 独立报告 applicability/missingness |

GMTP 不是 Paper 1 proposed core method，也不得被并入 Temporal View。公开代码或单次工程 smoke 不等于论文级复现。
任何 baseline 进入实际执行前都必须冻结数据/模型/配置/retriever/Top-K/metrics/seeds 和严格或非严格可比类别。
