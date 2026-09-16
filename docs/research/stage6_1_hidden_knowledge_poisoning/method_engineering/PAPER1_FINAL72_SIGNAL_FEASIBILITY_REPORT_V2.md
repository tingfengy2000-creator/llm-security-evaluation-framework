# Paper 1 Final72 Signal Feasibility Report V2

Status: `RETRIEVAL_HARNESS_COMPLETE / DOCUMENT_DETECTOR_NOT_READY / RETRIEVAL_RISK_READY_WITH_LIMITATIONS`

> 本报告是 Final72 development set 的工具链与输入边界诊断，不是 Detector 结果、正式测试或论文优越性结论。

## V1 到 V2

V1 的 R view 是 720/720 `INPUT_MISSING`。V2 冻结了 24 个 label-blind current-state query、统一 72 文档 corpus、
字符 2/3-gram BM25 与固定 revision 的离线 MiniLM Dense retriever。每个 retriever 做两次可比运行，每次保存完整
24×72=`1728` 行 trace；K 在标签加载前冻结为 `{1,3,5,10}`。

严格事件顺序为：query lock → corpus lock → retrieval run lock → R signal matrix lock → label analysis。Query 与 corpus
的 class/answer/Expected/HKP/S/Owner leakage 均为 0。

## Retrieval coverage

R matrix 有 8,448 行，SHA256 `eeebe7ea92857b0b04dbfb983497b0e28b72f785f507f1acd046cd3cedc6fdef`：

- 7,104 `COMPUTED`：`retrieval_rank`、`retrieval_score`、`ranking_stability`；
- 1,344 `INPUT_MISSING`：7 个依赖 current/history 身份的 Top-K/version signals；
- version role 没有从 GT、HN 或 Poison identity 回填。

Dense 使用 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` revision
`16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`，模型树 SHA256
`14be5b8d047148b787bcca877c4b91722c10bc3e1a184ea3aaffe8b6fd3d1fb7`，CPU、local-only、L2-normalized；它的角色是
harness validation，不是正式效果。

## 锁后 retrieval 诊断

Matched-group median rank（越小越靠前）：Sparse 的 Clean/Poison/HN 分别为 2/2/2，均值 2.208/1.792/2.375；Dense
median 为 3/5/3，均值 12.167/9.417/6.250。HN 在 Dense current-state query 下靠前，说明 exposure 可能存在；这不把
HN 变成 Poison，也不构成 detector false positive。由于 registry 缺失，本轮不声称 current-vs-historical ranking 关系。

## Temporal audit

V1 Present-Time Substitution 为 7/72 computed，但这 7 条依赖预匹配 E1/E2 与 year heuristic，只能保留为 oracle
diagnostic。对其余 65 条重新分类：32 条为 `NO_TEMPORAL_CLAIM`，是真实 `NOT_APPLICABLE`；33 条为
`NO_VERSION_ROLE_METADATA`，是 `INPUT_MISSING`。合并 7 条旧 computed 后，deployable boundary 下为 32 N/A、40 input
missing、0 deployable computed。Candidate、GT 与 Evidence Pool 均未修改；需要补 version roles 的条目登记为
`NEW_EVIDENCE_REQUIRED`，没有静默加证据。

## Readiness

- `DOCUMENT_DETECTOR_READINESS = NOT_READY`：29 个 S/E/P/T signals 仍是 matched-Evidence oracle diagnostic。
- `RETRIEVAL_RISK_READINESS = READY_WITH_LIMITATIONS`：两类 retriever、rank/score/stability 与两阶段接口可用，但 7 个
  version-aware R signals 等待 Trusted Version Registry。
- 不推荐立即训练文档投毒 detector。下一项精确建议是先执行
  `P1-TRUSTED-EVIDENCE-RETRIEVER-AND-VERSION-REGISTRY-PROTOTYPE-01`，关闭 oracle/Temporal/version-role 缺口；该任务仍需
  Owner 单独批准。
