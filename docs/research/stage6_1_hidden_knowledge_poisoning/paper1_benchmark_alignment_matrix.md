# Paper 1 Literature / Benchmark Alignment Matrix

## 使用说明

- `Published Result` 只转录论文作者报告结果；本轮没有 `Reproduced Result` 或 `Our Method Result`。
- `Published Result ≠ Reproduced Result ≠ Our Method Result`；三者必须物理分栏并绑定各自证据。
- Strict comparison 需要尽可能一致的 dataset/split、attack samples/budget、retriever/embedding、Top-K、generator、
  metric definition、seed protocol 和 environment assumptions；不一致时必须标记 `NON_STRICT_COMPARISON`，不得
  声称 “outperforms SOTA by X%”。
- `required RAM` 与 `disk estimate` 若论文未报告，明确写成控制面规划估计，不冒充作者环境。
- `strict-comparison eligibility` 是当前资格，不是对论文质量的评价。

## License / Access / Comparison Governance

`Public Repository` 不等于 `Unrestricted Redistribution License`。以下六个字段必须分开，不得用一个模糊的
`BLOCKED` 同时代表源码访问、内部研究、严格比较与再分发：

- `SOURCE_ACCESS`：官方源码是否可公开访问；
- `INTERNAL_REPRODUCTION`：未来获批后是否存在当前技术/治理访问阻断；
- `STRICT_COMPARISON_ELIGIBILITY`：是否已完成 commit、环境、数据、预算和指标复现验证；
- `REDISTRIBUTION_ELIGIBILITY`：是否有明确许可再发布源码、修改代码、数据或 artifact；
- `CODE_LICENSE`：仓库代码许可；
- `DATASET_LICENSE`：每个数据集独立许可或使用条款。

这不是法律结论；明确的 upstream 条款始终优先。

| baseline | SOURCE_ACCESS | CODE_LICENSE | INTERNAL_REPRODUCTION | STRICT_COMPARISON_ELIGIBILITY | REDISTRIBUTION_ELIGIBILITY | DATASET_LICENSE |
| --- | --- | --- | --- | --- | --- | --- |
| PoisonedRAG | `AVAILABLE` | `MIT` | `AVAILABLE` for a future approved workflow | `PENDING_REPRODUCTION_VALIDATION` | `PERMITTED_SUBJECT_TO_MIT_CONDITIONS` for code | NQ / HotpotQA / MS MARCO separately governed |
| GMTP | `AVAILABLE` | `UNCONFIRMED` | `NOT_BLOCKED_BY_CURRENT_RESEARCH_PLAN` | `PENDING_REPRODUCTION_VALIDATION` | `TO_VERIFY / LICENSE_NOT_CONFIRMED` | upstream datasets and poisoned samples separately governed |
| SafeRAG | `AVAILABLE` | `UNCONFIRMED` | `NOT_BLOCKED_BY_CURRENT_RESEARCH_PLAN` | `PENDING_REPRODUCTION_VALIDATION` | `TO_VERIFY / LICENSE_NOT_CONFIRMED` | SafeRAG corpus terms separately governed |

## S6.1-R0-I Superseding Feasibility Qualification

The detailed matrix below remains the accepted LR1 alignment snapshot. Current R0-I review state supersedes only its
`reproduction status` and `strict-comparison eligibility` cells:

| baseline | R0-I review status | evidence-qualified outcome | strict comparison |
| --- | --- | --- | --- |
| PoisonedRAG | `HUMAN_ACCEPTED_WITH_BLOCKERS` | `ENGINEERING_FEASIBILITY_IDENTIFIED / P1_PROTOCOL_BLOCKED`；one selected dataset possible；`API_FREE_ATTACK_GENERATION = NOT ESTABLISHED` | `NOT_STRICT_COMPARISON_READY` |
| GMTP | `HUMAN_ACCEPTED_WITH_BLOCKERS` | `ENGINEERING_FEASIBILITY_IDENTIFIED / TARGETED_EXECUTION_BLOCKERS_REMAIN`；`GMTP_200_SAMPLE_ARTIFACTS_PRESENT = TRUE`（18 artifacts `AVAILABLE`）；modified `beir gitlink`/detection-only path unresolved；Docker `NOT MANDATORY` | `NOT_STRICT_COMPARISON_READY` |
| SafeRAG | `HUMAN_ACCEPTED_WITH_BLOCKERS` | `PARTIAL_REPRODUCTION_READY / DATASET_ARTIFACT_ONLY`；SN/ICC `BENCHMARK_ARTIFACT_AVAILABLE`；full pipeline not reproduced | `NOT_STRICT_COMPARISON_READY` for full pipeline |

Roles remain PRIMARY_ATTACK_BASELINE、PRIMARY_DETECTION_BASELINE and PRIMARY_BENCHMARK_REFERENCE respectively. See
[R0-I review](s6_1_r0_i_control_plane_review.md). The historical first-review `RETURNED_FOR_WORKER_CORRECTION` snapshot remains
in that record and is superseded only for current status.

## S6.1-R0-FU1-P0/L1 Superseding Targeted Resolution

P0 supersedes the unresolved *planning facts* above, not the LR1 published-result transcription and not runtime readiness:

| baseline | selected candidate / contract | identity result | current comparability | next evidence gate |
| --- | --- | --- | --- | --- |
| PoisonedRAG | NQ primary；HotpotQA fallback；official NQ released attack-text artifact | L1 `IDENTITY_VERIFIED`；100x5 schema and official `question + "." + adv_text` assembly deterministically verified；API-free reuse yes；generation identity still partial | `PARTIALLY_COMPARABLE / TRANSFER_EVALUATION_ONLY` | L1 `HUMAN_ACCEPTED`；former W1 superseded |
| GMTP | Contriever+BERT detection-only core on exact GMTP-packaged NQ HotFlip/Contriever record | BEIR gitlink verified；W2 input/source/model/parameter/environment/resource contract frozen；this input is not L1's LM-targeted artifact | `PARTIALLY_COMPARABLE` only after later protocol；W2 alone does not unify the artifacts | W2 approved but not completed/accepted；Attempt 1 `W2_ATTEMPT1_EVIDENCE_BLOCKER` |
| SafeRAG | SN 100 + ICC 93 artifact contract | exact repository commit, dataset/KB Git blobs and executed-script hash frozen | `BENCHMARK_REFERENCE_ONLY` | no further Worker task by default |

The exact dataset matrix, attack/API boundary, call graph, model revisions, resource ceilings and W1/W2 contracts are canonical in
[FU1 Targeted Resolution](s6_1_r0_fu1_targeted_resolution.md). `FU1-P0 = HUMAN_ACCEPTED` and `FU1-L1 = HUMAN_ACCEPTED`；
former W1 is `SUPERSEDED_BY_LOCAL_L1 / NOT FAILED`；W2, P1 and formal experiment have not run/started.

## LR1 External Benchmark Matrix

| paper | venue | year | role_in_our_paper | official_paper_url | official_repo | verified_commit/tag | license | datasets | dataset_license | attack | defense | retriever | generator | embedding model | Top-K | attack budget | metrics | published main results | required GPU | required RAM | disk estimate | original environment | 5090 compatibility issue | reproduction status | strict-comparison eligibility | gap relative to our method | unresolved questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PoisonedRAG | USENIX Security | 2025 | Primary Attack Baseline | [paper](https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag) | [repo](https://github.com/sleeepeer/PoisonedRAG) | `f660d72174f06b13fae5163ce656e7b235db858f` current HEAD; paper-result commit `TO_VERIFY` | MIT code | NQ; HotpotQA; MS MARCO | NQ CC BY-SA 3.0; HotpotQA CC BY-SA 4.0; MS MARCO non-commercial research terms | black-box LM-targeted; white-box HotFlip; 5 comparison attacks | paper evaluates perplexity, duplicate removal, isolation forest and other defenses; this row is attack baseline | Contriever; Contriever-ms; ANCE | PaLM 2; GPT-3.5; GPT-4; Llama-2 7B/13B; Vicuna 7B/13B/33B | retriever encoders above | 5 | 5 malicious texts per target question; 100 targets from 10x10 sampling | ASR; retrieval Precision/Recall/F1; #Queries; runtime | Table 1 ASR spans 0.88-0.99 for most black/white-box dataset-model cells; NQ black-box PaLM2 ASR 0.97/F1 0.96; HotpotQA 0.99/1.0; MS MARCO 0.91/0.89 | `NOT REPORTED` | `NOT REPORTED`; planning 32-64 GB | planning 150-300 GB for corpora, indexes, models and logs; worker must measure | repo: Python 3.10, torch 1.13.0 + cu117; paper uses APIs and local Llama/Vicuna; hardware unreported | cu117/torch1.13 binaries are pre-Blackwell; APIs/model availability drifted; compatibility patch required and must not alter algorithm | `NOT_STARTED`; source and paper verified | `NOT_ELIGIBLE`: paper-result commit, model snapshots and worker environment unresolved | no version/provenance modeling; target-query attack focus; lacks legitimate-evolution hard negatives and multi-view explanation | exact historical commit; API snapshots; data/index hashes; GPU/RAM/disk |
| GMTP | Findings of ACL | 2025 | Primary Detection / Defense Baseline | [paper](https://aclanthology.org/2025.findings-acl.1263/) | [repo](https://github.com/mountinyy/GMTP) | `15b48d150f93711371eb8da22c211cd84a0cf4df` | `CODE_LICENSE=UNCONFIRMED` | BEIR NQ; HotpotQA; MS MARCO; 200 queries each | upstream dataset terms above; supplied poisoned samples license `UNKNOWN` | PoisonedRAG; Phantom; AdvDecoding | GMTP; PPL; L2; generation comparison with TrustRAG/RobustRAG | DPR; Contriever; ColBERT generalization | Llama2-7B-Chat | DPR NQ; Contriever-msmarco; BERT or RoBERTa MLM | paper final 10; repo candidate 20 -> final 10 | PoisonedRAG 5/query = 1000 docs; Phantom/AdvDecoding 5 trigger docs | nDCG@10; Filtering Rate; CACC; ACC; ASR; cheating-token precision; latency | DPR Table 1: GMTP FR 0.999-1.0; PoisonedRAG generation ASR 3.5/7.5/4.5% on NQ/HotpotQA/MS MARCO; cheating-token precision mostly >0.8 | single NVIDIA A6000 | `NOT REPORTED`; planning 64 GB | planning 250-500 GB for three corpora, clean/attacked indexes, two retrievers and models | paper: single A6000; repo Docker PyTorch 2.5.1 CUDA 12.4, Java 21, Pyserini 0.43.0 | CUDA12.4/PyTorch2.5.1 is pre-native Blackwell; faiss-gpu wheel and Java/Pyserini on Windows need WSL/Linux validation; 32 GB VRAM vs A6000 48 GB | `NOT_STARTED`; source available; future internal research not blocked by current plan | `PENDING_REPRODUCTION_VALIDATION`: commit/revision/environment proof incomplete | detects optimization-token unnaturalness but does not model legitimate version evolution, provenance camouflage or semantic factual mutation without cheating tokens | redistribution license; paper-result commit; threshold artifacts; model revisions; exact RAM/disk; 5090 peak VRAM |
| SafeRAG | ACL Long Paper | 2025 | Primary Benchmark / Evaluation Reference | [paper](https://aclanthology.org/2025.acl-long.230/) | [repo](https://github.com/IAAR-Shanghai/SafeRAG) | `e8f579743b23e0a3937076dcc0792fe29027cba3` | `CODE_LICENSE=UNCONFIRMED` | Chinese SafeRAG tasks: Silver Noise; Inter-context Conflict; Soft Ad; White DoS | `UNKNOWN`; repository has no LICENSE | indexing/retrieval/generation injection for four tasks | OFF; NLI filter; SKR compressor | DPR; BM25; Hybrid; Hybrid-Rerank | DeepSeek; GPT-3.5; GPT-4; GPT-4o; Qwen 7B/14B; Baichuan 13B; ChatGLM 6B | bge-base-zh-v1.5; bge-reranker-base | Silver Noise 6; others 2 | Silver Noise 3/6 default; others 1/2 | Retrieval Accuracy; F1 variants; ASR/AFR; BLEU/ROUGE/BERTScore/QuestEval tracks | 14 components show vulnerability; noise lowers F1(avg); attack effectiveness by injection stage is filtered context > retrieved context > knowledge base; retriever vulnerabilities differ | NVIDIA H800 | `NOT REPORTED`; planning 64-128 GB | planning 30-100 GB for repo data, Milvus, embeddings and selected local models; full model matrix requires more | H800; sentence chunking; GPT-3.5 evaluator; requirements leave torch unpinned | 32 GB cannot assume FP16 14B + overhead fits; Milvus-lite/old dependencies and API snapshots require WSL/Linux and compatibility checks | `NOT_STARTED`; source available; future internal research not blocked by current plan | `PENDING_REPRODUCTION_VALIDATION`: revision/dependency/environment proof incomplete | strong Chinese pipeline benchmark, but no explicit version lineage; Paper 1 focuses Silver Noise/Conflict and adds hard negatives plus version/provenance views | redistribution/data license; exact dataset version/hash; H800 VRAM use; prompt/API snapshots; paper-result commit |

## EcoSafeRAG Deferred Record

`EcoSafeRAG` 当前为 `DEFERRED`。本轮没有确认可用官方源码，且前三项 artifact 已足以建立第一版对齐链。
不得在当前阶段投入主要算力复现，也不得把二手实现登记为官方 artifact。
