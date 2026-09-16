# Paper 1 Two-stage Risk Architecture V1

Status: `FROZEN_METHOD_BOUNDARY / NO_DETECTOR_TRAINING`

## 两个不同问题

Stage A 是 document-level poison risk。它只回答“这份文档本身是否像被投毒”，输入为离线或文档条件化的
Semantic、Entity-Claim、Provenance、Temporal-Version，即 `S+E+P+T`，输出为 `document_poison_risk`。

Stage B 是 query-conditioned retrieval exposure risk。它回答“在这个 query 下，这份文档以当前 rank/score 进入
Top-K 后会带来多大暴露风险”，输入为 Stage A 的文档风险、Retrieval-Behavior 与 query context，输出为
`retrieval_exposure_risk`，可用于 reranking、downweighting、filtering 与检索时解释。

## 为什么 R 不等于 Poison

一个合法的 2021 年历史文件，在“当前规定是什么？”下可能排在第一名。它可能让回答错误地采用旧制度，所以 Stage B
风险可以较高；但文档仍是真实合法的历史材料，document poison label 仍为 negative。不能把高 rank、历史文档或
Hard Negative 直接解释成 Poison，也不能把这类情况计成 Stage A 的 detector false positive。

Paper 1 仍使用 Five-view Security Signals，但 `SEPT` 是 document-level 候选架构，`SEPTR` 是 query-conditioned
风险架构。二者不得混写成同一个分类任务。

## 当前门

- Stage A：`NOT_READY`。当前 S/E/P/T 中 29 个 signal 仍依赖人工预匹配 E1/E2，属于 oracle diagnostic。
- Stage B：`READY_WITH_LIMITATIONS`。Sparse 与 frozen-offline Dense 已提供 rank、score、stability；7 个版本构成类 R
  signals 等待 Trusted Version Registry。
- 本轮没有训练 detector、调阈值、校准 risk 或生成正式 test result。
