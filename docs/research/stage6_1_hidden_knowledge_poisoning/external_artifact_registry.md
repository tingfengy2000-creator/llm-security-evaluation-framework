# Paper 1 外部 Artifact 登记册

> 未关闭的 license、paper-result commit、revision、API snapshot 与 hardware facts 统一登记为 canonical blocker
> `BLK-S6.1-LR1-001`，见 [Experiment Master Record](../../governance/experiment_master_record.md)。

## 核验口径

- 核验日期：`2026-07-31`。
- commit 来自对官方 GitHub 仓库默认分支执行 `git ls-remote` 后的 HEAD。
- “官方”由论文正文/脚注或论文官方页面的代码链接支持。
- 当前 HEAD 只是本轮准备快照；它不自动等于作者生成论文结果时使用的 commit。
- 未发现根目录 `LICENSE` 时记录 `CODE_LICENSE=UNCONFIRMED` 和 `REDISTRIBUTION_ELIGIBILITY=TO_VERIFY`，不推定
  默认开源许可，也不自动解释为内部研究工作流的技术访问阻断。

`SOURCE_ACCESS`、`INTERNAL_REPRODUCTION`、`STRICT_COMPARISON_ELIGIBILITY`、
`REDISTRIBUTION_ELIGIBILITY`、`CODE_LICENSE` 与 `DATASET_LICENSE` 必须独立判断。这不是法律结论；明确的
upstream 条款必须遵守。

## LR1 Artifact Snapshot

正式论文入口：

- PoisonedRAG: [USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag)
- GMTP: [Findings of ACL 2025](https://aclanthology.org/2025.findings-acl.1263/)
- SafeRAG: [ACL 2025 Long Paper](https://aclanthology.org/2025.acl-long.230/)

| ID | SOURCE_ACCESS | CODE_LICENSE | INTERNAL_REPRODUCTION | STRICT_COMPARISON_ELIGIBILITY | REDISTRIBUTION_ELIGIBILITY | 当前运行状态 |
| --- | --- | --- | --- | --- | --- | --- |
| `EXT-P1-POISONEDRAG` | `AVAILABLE`：[official repo](https://github.com/sleeepeer/PoisonedRAG)，HEAD `f660d72174f06b13fae5163ce656e7b235db858f` | `MIT` | `AVAILABLE` for a future approved research workflow | `PENDING_REPRODUCTION_VALIDATION` | `PERMITTED_SUBJECT_TO_MIT_CONDITIONS` for code | `NOT_RUN` |
| `EXT-P1-GMTP` | `AVAILABLE`：[official repo](https://github.com/mountinyy/GMTP)，HEAD `15b48d150f93711371eb8da22c211cd84a0cf4df` | `UNCONFIRMED` | `NOT_BLOCKED_BY_CURRENT_RESEARCH_PLAN` | `PENDING_REPRODUCTION_VALIDATION` | `TO_VERIFY / LICENSE_NOT_CONFIRMED` | `NOT_RUN` |
| `EXT-P1-SAFERAG` | `AVAILABLE`：[official repo](https://github.com/IAAR-Shanghai/SafeRAG)，HEAD `e8f579743b23e0a3937076dcc0792fe29027cba3` | `UNCONFIRMED` | `NOT_BLOCKED_BY_CURRENT_RESEARCH_PLAN` | `PENDING_REPRODUCTION_VALIDATION` | `TO_VERIFY / LICENSE_NOT_CONFIRMED` | `NOT_RUN` |
| `EXT-P1-ECOSAFERAG` | `OFFICIAL_REPOSITORY_NOT_VERIFIED` | `UNKNOWN` | `NOT_EVALUATED` | `NOT_EVALUATED` | `UNKNOWN` | `DEFERRED` |

## S6.1-R0-I Current Qualification

| ID | R0-I status | Verified/current qualification |
| --- | --- | --- |
| `EXT-P1-POISONEDRAG` | `HUMAN_ACCEPTED_WITH_BLOCKERS` | `ENGINEERING_FEASIBILITY_IDENTIFIED / P1_PROTOCOL_BLOCKED`；one selected NQ/HotpotQA/MS MARCO dataset is possible；attack-generation identity unresolved；`NOT_STRICT_COMPARISON_READY` |
| `EXT-P1-GMTP` | `HUMAN_ACCEPTED_WITH_BLOCKERS` | `ENGINEERING_FEASIBILITY_IDENTIFIED / TARGETED_EXECUTION_BLOCKERS_REMAIN`；`GMTP_200_SAMPLE_ARTIFACTS_PRESENT = TRUE`（18 artifacts `AVAILABLE`）；modified `beir gitlink` source/detection-only path unresolved；Docker `NOT MANDATORY`；`NOT_STRICT_COMPARISON_READY` |
| `EXT-P1-SAFERAG` | `HUMAN_ACCEPTED_WITH_BLOCKERS` | `PARTIAL_REPRODUCTION_READY / DATASET_ARTIFACT_ONLY`；SN/ICC `BENCHMARK_ARTIFACT_AVAILABLE`；full pipeline `NOT_STRICT_COMPARISON_READY` |

Corrected private-evidence identity: archive SHA-256
`904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b`；inner index `12/12`；corrected matrix
SHA-256 `fd7617eca689fa46fc6908f94aa4fa158aaae4d277bb17943bbcc1baf74db9bc`。

The absence of a GMTP/SafeRAG root license remains a `REDISTRIBUTION_ONLY_ISSUE`, not an internal research blocker. The
private Worker archives are not stored in Git；only their SHA-256 values, the corrected matrix SHA and the
[redacted R0-I review](s6_1_r0_i_control_plane_review.md) are persisted。Historical first-review return remains preserved there。

## S6.1-R0-FU1-P0/L1 Exact Artifact Addendum

P0 is accepted source planning. L1 validated the released PoisonedRAG artifact and deterministic assembly locally in memory;
no model, retrieval, API, NQ corpus or external baseline was executed:

| Artifact | Exact identity | Current decision |
| --- | --- | --- |
| PoisonedRAG NQ released attack text | commit `f660d72174f06b13fae5163ce656e7b235db858f`；`results/adv_targeted_results/nq.json` blob `d1da818b28da7013864ea465ff88ad4c3ca29562`；SHA-256 `44df711454a9bada08e72e9e4a003a2cc845c43707ac93a3493e5168ec415cf2`；123,089 B；100 targets x 5 texts | `IDENTITY_VERIFIED / L1 HUMAN_ACCEPTED`；API-free reuse yes；generation identity unresolved |
| PoisonedRAG official assembly source | same commit；`src/attack.py` blob `a29630c42508adbb421cc5ee23eac9bbcd58be44`；source SHA-256 `31fb59905812e7656f7206f416dc53228a3089390b0ecd9f0c9e9575dbfc250b` | exact semantics `question + "." + adv_text`；no inserted space/strip/normalization/suffix；source order preserved |
| PoisonedRAG NQ/Contriever retrieval result | same commit；`results/beir_results/nq-contriever.json` blob `bb5c039b172e11b6a4750fb7928c9ffb921be576`；SHA-256 `a5e9d9ca8e65b61e2fa34428e154a55c2e97c2064c97af09bf87822a61995fa5` | `AUTHOR_RELEASED_RESULT_ARTIFACT`；not attack corpus |
| GMTP BEIR gitlink | GMTP commit `15b48d150f93711371eb8da22c211cd84a0cf4df` -> `beir-cellar/beir@f062f038c4bfd19a8ca942a9910b1e0d218759d4` | source identity `VERIFIED`；not a private fork |
| GMTP NQ detector-core sample | `data/poisoned_documents/poisonedrag/hotflip/contriever/nq-200.json` blob `72fb52cda9ea794bafb5c114ee937a00f4d1728a`；SHA-256 `0233a26ecc56d7baf1448b86a114e328beece60624aa88304fa3553e90421e44`；975,113 B；200 records | W2 input frozen；GMTP-packaged HotFlip/Contriever, not L1 LM-targeted artifact；W2 not executed |
| SafeRAG dataset | commit `e8f579743b23e0a3937076dcc0792fe29027cba3`；`nctd_datasets/nctd.json` blob `6508f154817910e1f55926c1fee22bca411255df` | SN/ICC `DATASET_ARTIFACT_ONLY` contract |
| SafeRAG SN KB | `knowledge_base/SN/db.txt` blob `f8ee557c9cb0649f0d8f00569cfdb90cb3eb9e8b` | benchmark artifact；license unconfirmed |
| SafeRAG ICC KB | `knowledge_base/ICC/db.txt` blob `d831977cd3320ba32af2da129ce710d83d5e4e8c` | benchmark artifact；license unconfirmed |

For fixed L1 target `test1`, the five ordered assembled-document SHA-256 values are `0bb73269...14ac`,
`2f891304...f1c7`, `3449b7d5...ffdf`, `c8224391...641b` and `ef79bbb3...474d`; the canonical full values and aggregate
`f22b7576c27926a07a7138e952cf3ee6b86c982b584a3078f3364577d32c60a7` are in the FU1 resolution.

Exact W2 model revisions are `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` and canonical
`google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`. Model acquisition remains pending separate W2
approval. See
[FU1 Targeted Resolution](s6_1_r0_fu1_targeted_resolution.md) for dependency classes and resource ceilings.

## DATASET_LICENSE 治理

| 数据 | 一手许可记录 | 当前使用结论 |
| --- | --- | --- |
| Natural Questions | [Google NQ 页面](https://ai.google.com/research/NaturalQuestions/download)记录 CC BY-SA 3.0 | 研究使用前仍需保存具体下载版本和派生语料义务 |
| HotpotQA | [HotpotQA 官方页面](https://hotpotqa.github.io/)记录数据/处理 Wikipedia 为 CC BY-SA 4.0 | 允许研究准备；派生发布必须保留署名和 share-alike 审查 |
| MS MARCO | [Microsoft 官方条款](https://microsoft.github.io/msmarco/)限定 non-commercial research，并不授予底层文档权利 | 只允许非商业研究；公开 Artifact 前独立 legal/license review |
| GMTP 提供的 200 poisoned samples | 仓库未发现 LICENSE | 只做来源核验；复制、修改、再分发前必须取得明确许可 |
| SafeRAG 数据与知识库 | 仓库未发现 LICENSE；README 仍列出未来 Hugging Face release TODO | 只做来源核验；复制、修改、再分发前必须取得明确许可 |

`CODE_LICENSE` 不能外推为 `DATASET_LICENSE`。PoisonedRAG code 的 MIT 不表示 NQ、HotpotQA 或 MS MARCO 是
MIT；GMTP/SafeRAG 仓库许可状态也不能替代其 corpus、poisoned samples 或底层公开数据条款。

未来 Public Artifact 优先发布 LLMGuard 自有 source、configs、download/preprocessing scripts、dataset hashes 与
official links，而不是直接重新托管全部第三方原始数据。

## 源码与论文差异提醒

### PoisonedRAG

- 官方 README 环境为 Python 3.10、PyTorch 1.13.0 + CUDA 11.7。
- 当前 HEAD `f660d72...` 是 2026 年的 results loading bug fix，晚于论文；必须向作者材料或历史 commit
  追溯 paper-result commit，才能建立严格复现身份。
- README 默认 `top_k=5`、`adv_per_query=5`、10 次重复，每次 10 个 target questions。

### GMTP

- 论文脚注明确给出 `mountinyy/GMTP`。
- README 的下载命令拼写为 `donwload_datasets.py`，实际根文件名是 `download_datasets.py`；复现清单必须记录此
  documentation patch，不能静默更改。
- 论文定义 final `k=10`；仓库脚本先 retrieve 20，再 rerank/filter 到 10。两者可以兼容，但 manifest 必须同时记录
  candidate K 与 final K。
- Dockerfile 使用 PyTorch 2.5.1 + CUDA 12.4 + Java 21；requirements 同时列出 GPU/CPU FAISS 变体，依赖并非完整锁文件。
- 根目录未发现 LICENSE。

### SafeRAG

- README quick start 默认 BM25、Top-K 6、Silver Noise、indexing injection，并依赖 API evaluator/generator。
- 论文还覆盖 DPR、Hybrid、Hybrid-Rerank、NLI、SKR 以及 8 个 generator。
- requirements 的 `torch` 未锁版本，模型 revision、API snapshot 和若干依赖未冻结。
- 根目录未发现 LICENSE。

## 仍需向作者或 artifact 补齐

1. PoisonedRAG paper-result commit/tag、exact generator/API snapshot 和完整依赖锁；released attack-text reuse remains partial。
2. GMTP、SafeRAG 代码与数据的明确许可证。
3. Formal-run data snapshot/preprocessing hashes；GMTP W2 source/input/model/config identities are frozen but not executed。
4. PoisonedRAG 的作者运行 GPU/RAM/disk；GMTP/SafeRAG 的 RAM/disk。
5. API 模型的可复现实验 snapshot 或等价的本地模型轨道。
