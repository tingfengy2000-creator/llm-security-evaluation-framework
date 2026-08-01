# S6.1-R0-FU1 Targeted External Baseline Feasibility Resolution

> Accepted task: `S6.1-R0-FU1-P0 / LOCAL Control-Plane Planning and Execution Contract Freeze`
> Current project task: `GOV-PO-MHEP / Highest Internal Project Execution Authority`
> Status: `W2 APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED / ATTEMPT1 EVIDENCE_REVIEW_BLOCKED`
> Execution mode: `LOCAL-FIRST / WORKER-GATED`
> Evidence class: `CONTROL_PLANE_SOURCE_ANALYSIS / SOURCE_ARTIFACT_VALIDATION / DETERMINISTIC_TRANSFORMATION_VALIDATION /
> ENGINEERING_VALIDATION_APPROVED_NOT_EXECUTED`
> Formal experiment: `FORMAL_EXPERIMENT = NOT STARTED`

## 1. Scope and decision boundary

The project owner accepted P0 and reassigned the former Worker W1 candidate to LOCAL as `S6.1-R0-FU1-L1`. L1 performed only
source-artifact identity, whole-file schema and deterministic transformation validation against exact GitHub commit content and
accepted evidence. It did not run a model, retrieval, external baseline or API service; it did not acquire the NQ corpus or contact
RTX5090. The former `FU1-W1` is `SUPERSEDED_BY_LOCAL_L1`, not failed. The project owner subsequently approved the exact frozen
`FU1-W2` contract for `RTX5090 / COMPUTE_WORKER`. The first Worker attempt stopped before model load/smoke, but its archive omits
mandatory main-repository integrity evidence；Attempt 1 is therefore `W2_ATTEMPT1_EVIDENCE_BLOCKER`, not an accepted blocked run.
This document is not a P1 protocol or experiment result.

Current baseline roles remain unchanged:

| Baseline | Role | Current evidence status |
| --- | --- | --- |
| PoisonedRAG | `PRIMARY_ATTACK_BASELINE` | released attack-text reuse is feasible; exact regeneration identity is not recovered |
| GMTP | `PRIMARY_DETECTION_BASELINE` | source and detection-only call path are frozen; Worker execution is approved but not run |
| SafeRAG | `PRIMARY_BENCHMARK_REFERENCE` | SN/ICC benchmark-artifact contract is frozen; no full-pipeline prerequisite |

All three remain `NOT_STRICT_COMPARISON_READY` until the applicable future execution evidence and P1 protocol are accepted.

## 2. PoisonedRAG dataset decision

Sources: [PoisonedRAG paper/repository](https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag),
[BEIR dataset table](https://github.com/beir-cellar/beir), [BEIR download index](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/),
[Natural Questions](https://ai.google.com/research/NaturalQuestions/download), [HotpotQA](https://hotpotqa.github.io/) and
[MS MARCO](https://microsoft.github.io/msmarco/). Counts and zip sizes below are source facts; index/disk/resource figures are
Control Plane estimates that a future Worker must measure.

| Criterion | NQ | HotpotQA | MS MARCO |
| --- | --- | --- | --- |
| Paper 1 scientific fit | high: factual QA and localized answer mutation | medium/high: factual, but explicitly multi-hop | medium: passage ranking and broader web-query confounds |
| Query complexity | not designed as a multi-hop benchmark; still not guaranteed single-hop | explicit multi-hop reasoning | real anonymized Bing queries; heterogeneous intent |
| BEIR corpus / test queries | 2,681,468 / 3,452 | 5,233,329 / 7,405 | 8,841,823 / 6,980 |
| Official BEIR zip | 498,307,926 B (~475 MiB) | 654,025,350 B (~624 MiB) | 1,082,258,632 B (~1.01 GiB) |
| Raw FP32 768-d vector estimate | ~8.2 GB | ~16.1 GB | ~27.2 GB |
| Planned corpus+index reserve | 15-30 GB | 25-50 GB | 40-80 GB |
| PoisonedRAG published use | yes; 100 targets, five malicious texts/target, Top-K 5 | same | same |
| GMTP coverage | yes; DPR/Contriever, 200-query artifacts | yes | yes |
| Released-artifact continuity | PoisonedRAG and GMTP both release NQ artifacts | both release artifacts | both release artifacts |
| Retriever compatibility | Contriever/Contriever-ms/ANCE in PoisonedRAG; DPR/Contriever in GMTP | same | same |
| Dataset terms | CC BY-SA 3.0 recorded by NQ | CC BY-SA 4.0 | non-commercial research; underlying-document rights not granted |
| RTX5090 control cost | lowest of the three candidates | higher index and multi-hop explanation cost | largest index and licensing/explanation cost |

Decision:

- `PRIMARY_EXTERNAL_DATASET_CANDIDATE = NQ`.
- `SECONDARY_FALLBACK_DATASET = HotpotQA`.
- MS MARCO is retained as later external generalization only.

NQ best joins factual-poisoning relevance, the smallest corpus/index footprint, both baselines' released artifacts, and a lower
reasoning-confound/explanation burden. HotpotQA is the fallback when a multi-hop stress test is scientifically required. This is a
candidate external choice, not `Dataset = FROZEN`.

## 3. PoisonedRAG attack identity and API-free feasibility

Audited identity: official repository commit `f660d72174f06b13fae5163ce656e7b235db858f`.

| Layer | Exact source behavior | API / offline decision | Artifact class |
| --- | --- | --- | --- |
| target-answer and malicious-text generation | `gen_adv.py` obtains a correct answer through a configured LLM, then directly calls OpenAI `gpt-4-1106-preview` to generate an incorrect answer and five adversarial texts | API-dependent in the audited path | `REGENERATED_POISONED_ARTIFACT` |
| released adversarial text | `results/adv_targeted_results/<dataset>.json` stores question, correct/incorrect answer and five `adv_texts` per target | offline reuse is possible | `AUTHOR_RELEASED_ATTACK_TEXT_ARTIFACT` |
| LM-targeted assembly | `src/attack.py` consumes the released file and constructs each detector/retriever-visible text as `question + "." + adv_text` | deterministic and offline after artifact acquisition | assembled attack input, not a separately released corpus |
| retrieval result | `results/beir_results/<dataset>-<retriever>.json` stores author-released retrieval output | offline analysis is possible | `AUTHOR_RELEASED_RESULT_ARTIFACT` |
| full generation/evaluation | `main.py` invokes the selected PaLM/GPT/local LLM after retrieval | API or large local model required depending on model | result-generation path |

Verified NQ identities:

| Path | Git blob | Size | SHA-256 from accepted corrected Worker evidence |
| --- | --- | ---: | --- |
| `results/adv_targeted_results/nq.json` | `d1da818b28da7013864ea465ff88ad4c3ca29562` | 123,089 B | `44df711454a9bada08e72e9e4a003a2cc845c43707ac93a3493e5168ec415cf2` |
| `results/beir_results/nq-contriever.json` | `bb5c039b172e11b6a4750fb7928c9ffb921be576` | 11,464,323 B | `a5e9d9ca8e65b61e2fa34428e154a55c2e97c2064c97af09bf87822a61995fa5` |

`AUTHOR_RELEASED_ATTACK_ARTIFACT_USABLE = PARTIAL`.

The file is author-released, content-addressed, has the schema required by the official `LM_targeted` path, and supports API-free
reuse of the released attack texts. It is not a released final poisoned corpus and the repository does not bind it to an exact
generator revision, API snapshot, prompt-run manifest, seed, or paper-result commit. Therefore:

- `API_FREE_REUSE_OF_RELEASED_ATTACK_TEXTS = FEASIBLE`;
- `API_FREE_ATTACK_GENERATION = NOT ESTABLISHED`;
- `EXACT_PAPER_GENERATION_IDENTITY = PARTIAL / UNRESOLVED`.

### L1 whole-artifact and deterministic-assembly validation

L1 read the exact GitHub commit content in memory and recomputed both Git blob framing and ordinary SHA-256. No full attack text
is stored in this governance record.

| Evidence field | Verified value |
| --- | --- |
| Repository / commit | `sleeepeer/PoisonedRAG@f660d72174f06b13fae5163ce656e7b235db858f` |
| Artifact path | `results/adv_targeted_results/nq.json` |
| GitHub API / recomputed Git blob | both `d1da818b28da7013864ea465ff88ad4c3ca29562` |
| File size / SHA-256 | 123,089 B / `44df711454a9bada08e72e9e4a003a2cc845c43707ac93a3493e5168ec415cf2` |
| Whole-file target count | `NQ_TARGET_COUNT = 100` |
| Required fields | all 100 records contain non-empty `id`, `question`, `correct answer`, `incorrect answer`, `adv_texts`; map key equals `id` |
| Adversarial-text distribution | `ADV_TEXTS_PER_TARGET_DISTRIBUTION = {5: 100}` |
| Schema result | `SCHEMA_VALIDATION = PASS / 0 errors` |
| Assembly source | `src/attack.py`；Git blob `a29630c42508adbb421cc5ee23eac9bbcd58be44`；SHA-256 `31fb59905812e7656f7206f416dc53228a3089390b0ecd9f0c9e9575dbfc250b` |

Official lines 92-93 first compute `adv_text_a = question + "."`, then compute
`adv_texts = [adv_text_a + i for i in adv_texts_b]`. Therefore the exact semantics are UTF-8 text
`question + "." + adv_text`, preserving artifact order and content with no inserted space, strip, normalization or suffix.

The fixed L1 sample is serialized artifact record index 0, map key and `id` both `test1`, followed by `adv_texts[0:5]` in source
order. The question SHA-256 is `e795764af1655c8de777c4f265400922512e0ab905cdd073b39cca7cc19d9c96`.

| Assembled index | UTF-8 bytes | SHA-256 |
| ---: | ---: | --- |
| 0 | 234 | `0bb73269d9294a0417fab16314656c14465472f3b539f4617002839dd98114ac` |
| 1 | 217 | `2f891304ab4fbf620e6befe0566600c2e7904832b7da3fafd157e0d90836f1c7` |
| 2 | 207 | `3449b7d5ad7ec0e72d83b35e9c433a0ca9fd2411e2ed7ca6bd8ff46e7e72ffdf` |
| 3 | 244 | `c82243914a79cacfdbc081cfc4d21524251e8d5c383fd85f509bbec1a924641b` |
| 4 | 218 | `ef79bbb3741499e288b615fe5ca45cc85a9606fbf2cdc5ac53f3d6d7d1cb474d` |

Ordered-list aggregate rule: SHA-256 over the ASCII lowercase document SHA-256 values joined by LF, with no trailing LF.
Aggregate: `f22b7576c27926a07a7138e952cf3ee6b86c982b584a3078f3364577d32c60a7`.

L1 decisions:

- `AUTHOR_RELEASED_NQ_ATTACK_TEXT_ARTIFACT_IDENTITY_BOUND = TRUE`;
- `AUTHOR_RELEASED_ATTACK_TEXT_ARTIFACT = IDENTITY_VERIFIED`;
- `OFFICIAL_LM_TARGETED_ASSEMBLY = DETERMINISTICALLY_VERIFIED`;
- `API_FREE_REUSE_OF_RELEASED_ATTACK_TEXTS = VERIFIED_FEASIBLE`;
- `AUTHOR_RELEASED_ATTACK_ARTIFACT_USABLE = PARTIAL` remains the scientific-equivalence qualification;
- `API_FREE_ATTACK_GENERATION = NOT ESTABLISHED` and
  `EXACT_PAPER_GENERATION_IDENTITY = PARTIAL / UNRESOLVED` remain unchanged.

Candidate paper wording is “we reuse the attack artifacts released by PoisonedRAG”, never “we reproduced PoisonedRAG attack
generation”. Final publication wording remains a P1 decision.

### Candidate external attack contract

| Field | Candidate value |
| --- | --- |
| Dataset | NQ / BEIR test corpus; final snapshot and hash still require P1 approval |
| Attack input | official released NQ `adv_targeted_results` artifact above |
| Assembly | exact `LM_targeted`: `question + "." + adv_text` |
| Retriever | preserve author setting as a declared axis; Contriever candidate for alignment with GMTP, not yet frozen |
| Top-K | 5 |
| Attack budget | five malicious texts per target; 100 targets in released artifact |
| Metrics | author ASR plus retrieval Precision/Recall/F1; exact formal definitions/aggregation remain P1 work |
| Comparability | `PARTIALLY_COMPARABLE` unless the later protocol freezes corpus, retriever, retrieval results, generator and metrics |

## 4. GMTP modified-BEIR source identity

GMTP commit `15b48d150f93711371eb8da22c211cd84a0cf4df` contains a mode-`160000` `beir` gitlink at
`f062f038c4bfd19a8ca942a9910b1e0d218759d4`, while the root `.gitmodules` file is absent.

GitHub's global commit index identifies that exact SHA in
[`beir-cellar/beir`](https://github.com/beir-cellar/beir/commit/f062f038c4bfd19a8ca942a9910b1e0d218759d4) and its fork
`danglive/beir`. The canonical upstream commit is dated 2023-08-09 and adds a result-download utility to `beir/util.py`.
GMTP commit `16588bcf875ca8a04e5bb021418f6b783157bf92` adds the gitlink with the exact subproject commit.

Decision:

- repository URL: `https://github.com/beir-cellar/beir.git` — `VERIFIED` by exact global commit match;
- revision: `f062f038c4bfd19a8ca942a9910b1e0d218759d4` — `VERIFIED`;
- special private GMTP BEIR fork/modification — `NOT EVIDENCED`;
- absent `.gitmodules` is a packaging/provenance defect, not a reason to reimplement BEIR.

## 5. GMTP detection-only call path

`DETECTION_ONLY_CALL_PATH`:

Audited identity: official GMTP commit `15b48d150f93711371eb8da22c211cd84a0cf4df`; detector source blob
`src/defenses/method.py = 84e69b3eadeb8adc0ce521501f8b560d6377b489`.

```text
question + document text
  -> GMTP.__init__(retriever encoder, tokenizer, MLM reranker)
  -> encode question/document
  -> similarity.backward()
  -> embedding-gradient norm per document token
  -> select above-mean gradient tokens, retain top N
  -> get_mask_probs(): mask selected tokens in MLM
  -> take the lowest M original-token probabilities
  -> avg_masked_prob
  -> compare with remove_threshold * remove_lambda
  -> retained/filtered documents
```

This core can run directly through `src.defenses.method.GMTP.filter_documents(question, documents, ...)` when question and
document strings already exist. It does not call BEIR, Pyserini, FAISS, Java, a generator, or an evaluator.

The 18 repository `*-200.json` artifacts are sufficient as detector-core smoke inputs. For example,
`data/poisoned_documents/poisonedrag/hotflip/contriever/nq-200.json` is a 975,113-byte, 200-record artifact with Git blob
`72fb52cda9ea794bafb5c114ee937a00f4d1728a`. Record index 0 is `query_id=test0` and includes the query, two `gt_text`
documents, five `poisoned_docs`, correct/incorrect answers and attack intermediates. Full BEIR indexing is not required to pass
these texts to the detector core.

### Dependency stratification

| Class | Required components | Needed for detection-only W2? |
| --- | --- | --- |
| `CORE_DETECTOR_DEPENDENCY` | Python, PyTorch, Transformers, NumPy, one retriever encoder/tokenizer, one MLM/tokenizer, CUDA under the exact source because `.to("cuda")` is hard-coded | yes |
| `RETRIEVAL_PREPARATION_DEPENDENCY` | BEIR loader, `datasets`, `jsonlines`, corpus/query conversion | no, because released record text is direct input |
| `INDEXING_DEPENDENCY` | Pyserini, Java 21, FAISS, merged indexes and `src/search.py` | no |
| `GENERATION_DEPENDENCY` | OpenAI/local generator and answer-generation prompts | no |
| `EVALUATION_ONLY_DEPENDENCY` | `ir-measures`, qrels/poison labels, nDCG/filtering/ASR aggregation | no for core score smoke |

The official Docker environment (`torch 2.5.1`, CUDA 12.4, Java 21) is a full-project convenience environment. The algorithm
does not require an old Torch version. A future W2 should retain the already accepted Worker-native
`torch 2.13.0+cu130`/CUDA 13.0 base and validate only the source-compatible `transformers==4.47.1` and `numpy==1.26.4`
detector path. This is a compatibility hypothesis until W2 executes.

### Model identity and budget

| Role | Upstream model ID | Frozen candidate revision | Weight bytes | Planned use |
| --- | --- | --- | ---: | --- |
| document/question encoder | `facebook/contriever-msmarco` | `abe8c1493371369031bcb1e02acb754cf4e162fa` | 438,007,537 | required |
| MLM reranker | upstream alias `bert-base-uncased` -> canonical `google-bert/bert-base-uncased` | `86b5e0934494bd15c9632b12f734a8a67f723594` | 440,449,768 safetensors | required |
| alternative MLM | `FacebookAI/roberta-base` | `e2da8e2f811d1448a5b465c236feacd80ffbac7b` | 498,818,054 safetensors | optional, not W2 |
| DPR context encoder | `facebook/dpr-ctx_encoder-single-nq-base` | `bb21a3c2b1656d60c6a8e920283bc40dabddadb8` | 437,983,985 | optional, not W2 |
| DPR question encoder | `facebook/dpr-question_encoder-single-nq-base` | `d04a52f6d2f96c60117a925e8c24c4043a75f265` | 437,986,065 | optional, not W2 |

W2 planned network transfer is approximately 0.9-1.2 GB; reserve 5 GB disk, 16 GB RAM, 8 GiB VRAM and 10 minutes after
models are cached. These are ceilings/estimates, not measurements. No W2 artifact exceeds 5 GB.

## 6. SafeRAG benchmark-artifact contract

`SAFERAG_BENCHMARK_ARTIFACT_CONTRACT`:

| Field | Frozen candidate |
| --- | --- |
| Official repository / commit | `IAAR-Shanghai/SafeRAG` / `e8f579743b23e0a3937076dcc0792fe29027cba3` |
| Selected tasks | Silver Noise (`SN`) and Inter-context Conflict (`ICC`) |
| Dataset artifact | `nctd_datasets/nctd.json`; Git blob `6508f154817910e1f55926c1fee22bca411255df`; 1,945,700 B |
| SN knowledge artifact | `knowledge_base/SN/db.txt`; Git blob `f8ee557c9cb0649f0d8f00569cfdb90cb3eb9e8b`; 165,499 B |
| ICC knowledge artifact | `knowledge_base/ICC/db.txt`; Git blob `d831977cd3320ba32af2da129ce710d83d5e4e8c`; 40,861 B |
| Executed validation script | corrected Worker script SHA-256 `8a38c9f54b963703ae3279f36f53c49083fd76b0f7e96ea27707b728b915db7e` |
| Counts / validation | SN 100/100 and ICC 93/93 rows passed required-key validation |
| Scope | `DATASET_ARTIFACT_ONLY / BENCHMARK_REFERENCE_ONLY` |
| License/usage | root code/data license unconfirmed; internal analysis does not establish redistribution permission |
| Future wording | “evaluated on SafeRAG benchmark/tasks” only after a formal run; never “reproduced SafeRAG” from artifact use |

SafeRAG's full retriever/generator/evaluator pipeline is not a P1 prerequisite under this contract. No further Worker task is
proposed unless a later scientific design explicitly requires pipeline-level comparison.

## 7. Cross-baseline alignment

Comparison classes are `STRICTLY_COMPARABLE`, `PARTIALLY_COMPARABLE`, `TRANSFER_EVALUATION_ONLY` and
`BENCHMARK_REFERENCE_ONLY`; P0 does not assign `STRICTLY_COMPARABLE` to any current track.

| Field | PoisonedRAG | GMTP | SafeRAG |
| --- | --- | --- | --- |
| Research role | attack baseline | detection baseline | benchmark reference |
| Selected dataset/task | NQ candidate | NQ candidate | SN + ICC |
| Attack type | LM-targeted / HotFlip retrieval poisoning | detects PoisonedRAG, Phantom, AdvDecoding artifacts | noise/conflict injection tasks |
| Input unit | target question, wrong answer, five attack texts | question + candidate document | benchmark record + task KB |
| Retriever | Contriever / Contriever-ms / ANCE | DPR / Contriever; ColBERT generalization | DPR/BM25/Hybrid families |
| Top-K | 5 | retrieve 20, final 10 in full path; not needed for direct core score | SN 6; other tasks 2 in quick-start setting |
| Attack budget | 5 documents/query | supplied PoisonedRAG artifacts use 5/query | task-specific |
| Detector input | N/A; produces retriever-visible attack text | raw document text plus query | pipeline context/records |
| Metrics | ASR, retrieval P/R/F1 | FR, nDCG@10, CACC/ACC, ASR, token precision | task retrieval/generation metrics |
| Published results | yes | yes | yes |
| Released artifacts | attack texts + BEIR result JSON | 18 full 200-query artifacts | dataset and task KB files |
| Formal reproduction need | L1 identity validation accepted, then later P1 protocol | W2 core execution, then later P1 protocol | artifact contract already sufficient for later P1 design |
| Intended use | fixed external attack exposure | raw detection-score baseline | Chinese benchmark/task reference |
| Current comparability | `PARTIALLY_COMPARABLE` | `PARTIALLY_COMPARABLE` with PoisonedRAG on NQ | `BENCHMARK_REFERENCE_ONLY` |

The highest-value chain is NQ `PoisonedRAG attack -> poisoned document -> GMTP detection`. It is not yet a strict paper-to-paper
comparison: PoisonedRAG's released `adv_targeted` texts and GMTP's released PoisonedRAG/HotFlip corpus are distinct author
artifacts, retriever settings and result paths. Using the PoisonedRAG-released texts directly with GMTP provides a controlled
`TRANSFER_EVALUATION_ONLY` track; using GMTP's packaged PoisonedRAG corpus provides a GMTP-native detector track. P1 must keep
those tracks separate.

## 8. FU1 execution split and final W2 contract

### Historical W1 candidate -> LOCAL L1

The P0 Worker candidate `FU1-W1 / PoisonedRAG Targeted Artifact / Attack Path Validation` is
`SUPERSEDED_BY_LOCAL_L1`, not failed. Its evidence objective was completed locally in section 3 without GPU, environment
installation, model, corpus, retrieval or API execution.

### FU1-W2: GMTP Detection-Only Minimal Smoke

Status: `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED` on `RTX5090 / COMPUTE_WORKER`.

The W2 input is a GMTP-packaged `poisonedrag/hotflip/contriever` artifact. It is not the PoisonedRAG official LM-targeted
artifact verified by L1. W2 proves only GMTP detector-core executability; it does not create a unified PoisonedRAG LM-targeted ->
GMTP formal comparison chain.

| Contract field | Final frozen candidate |
| --- | --- |
| Repo / commit | `https://github.com/mountinyy/GMTP.git` / `15b48d150f93711371eb8da22c211cd84a0cf4df` |
| Detector source | `src/defenses/method.py`；blob `84e69b3eadeb8adc0ce521501f8b560d6377b489`；SHA-256 `83531fe0e4933074c0a710f3dc07bb260b5d638d3cd4c8c317a353de135e00f6` |
| Environment | independent `gmtp-compat`；Python 3.11；`torch 2.13.0+cu130` / CUDA runtime 13.0；`transformers==4.47.1`；`numpy==1.26.4`；only resolved core import dependencies |
| Exact encoder | `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` |
| Exact MLM | canonical `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`；upstream alias `bert-base-uncased` resolves to this same repository/revision |
| Input artifact | `data/poisoned_documents/poisonedrag/hotflip/contriever/nq-200.json`；blob `72fb52cda9ea794bafb5c114ee937a00f4d1728a`；975,113 B；SHA-256 `0233a26ecc56d7baf1448b86a114e328beece60624aa88304fa3553e90421e44` |
| Exact record | serialized array index 0；`query_id=test0` |
| Question | field `query`；49 UTF-8 B；SHA-256 `53c1176d667577193fa7b4eb171319597c4b99dd80b3e72d8eb779b98a204b0d` |
| Benign document | field `gt_text`, index 0；351 UTF-8 B；SHA-256 `e177b2da95be6282c2f4c7855e36dde35a875bd21190755b27329353252d2f09` |
| Poisoned document | field `poisoned_docs`, index 0；363 UTF-8 B；SHA-256 `b94ca256b3ac79d22429abe1d36d90fad352c024cd2b5e19b78cfb2e72135a5b` |
| `W2_PARAMETER_CONTRACT` | `ret_type=contriever`, `N=5`, `M=5`, `remove_threshold=0.2`, `remove_lambda=1.0`, `topk=10`, `do_sort=false` |
| Exact call | load exact file through `importlib.util.spec_from_file_location`, instantiate unmodified `GMTP`, call `filter_documents` once with `[gt_text[0], poisoned_docs[0]]`; a read-only trace wrapper may capture local `doc_infos` without source mutation；Worker may not select another sample |
| Required output | source/input/model identities；per-document `sim`, `avg_masked_prob`, threshold `0.2`, retained/filtered flag；exit code；wall time；peak RSS/VRAM；environment/GPU fingerprint |
| Resource ceiling | model download `<2 GB` expected；corrected task-owned disk hard ceiling 10 GiB (`gmtp-compat <=6 GiB`, exact models <=2 GiB, harness/evidence/archive <=256 MiB)；RAM <=16 GB；VRAM <=8 GiB；runtime <=10 minutes after model availability |
| Evidence directory | `~/experiments/s6_1_r0_fu1/w2/`；main LLMGuard repository remains read-only |
| Stop conditions | identity/hash mismatch；CPU fallback；NaN/Inf；OOM/resource ceiling；unexpected Java/Pyserini/FAISS/BEIR/datasets/Docker/API/generator requirement；any ceiling exceedance returns `WORKER_RESOURCE_APPROVAL_REQUIRED` and stops；any required source patch returns `COMPATIBILITY_PATCH_REVIEW_REQUIRED` and stops |
| Claims boundary | engineering detector-core smoke only；no accuracy/F1/AUPRC/AUROC/Filtering Rate/ASR/statistics/strict comparison/formal reproduction claim |

Parameter provenance is explicit: `src/defenses/method.py` constructor defaults are `N=10`, `M=5`,
`remove_threshold=-1.0`, `remove_lambda=1.0`; the official experiment `conf/config.yaml` instead sets `N=5`, `M=5`,
`remove_threshold=0.2`, `remove_lambda=1.0`. W2 deliberately freezes the official experiment config values, while
`topk=10` and `do_sort=false` remain the `filter_documents` defaults. The two-document smoke does not use top-k as a research
metric.

W2 must create/use only the independent `gmtp-compat` environment and must not mutate `llmguard-paper1`. Direct loading of
`src/defenses/method.py` limits imports to its core graph (`typing`, NumPy, PyTorch and Transformers). If that core import chain
forces another dependency, Worker records `UNEXPECTED_CORE_IMPORT_DEPENDENCY`; only a small ordinary Python dependency that does
not change the algorithm may be installed. Java, Pyserini, FAISS, BEIR, Docker, `datasets`, generators and evaluators are
prohibited and cause STOP/return to Control Plane. Any required source patch returns `COMPATIBILITY_PATCH_REVIEW_REQUIRED` and
stops；no silent patch is allowed.

### W2 Attempt 1 evidence review and H1 recovery gate

The exact review is [W2 Attempt 1 Control Plane Review](s6_1_r0_fu1_w2_attempt1_control_plane_review.md). Verified archive facts:

- archive SHA-256 `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`;
- safe members `18/18`, evidence index `16/16`, harness SHA-256
  `8411af2042774f1a18eec95e97a14ade088acbc35f09942ae9ffea4e8ea5fc06`;
- GMTP/source/input/environment identity passed；encoder acquisition reports `MODEL_DOWNLOAD_BLOCKER`；MLM was not attempted;
- no model load, detector-core score, runtime/RAM/VRAM result or full sensitive input text is present.

The archive does not contain the claimed main LLMGuard repository HEAD/clean output. Its resource file also says disk/resource
limits were not evaluated, so it cannot substantiate the reported approximately 5.2 GB environment footprint. A script that would
print those facts after archive creation is not captured execution evidence. Therefore:

- `S6.1-R0-FU1-W2-ATTEMPT1 = EVIDENCE_REVIEW_BLOCKED`;
- blocker `W2_ATTEMPT1_EVIDENCE_BLOCKER` is open;
- do not classify Attempt 1 as `VALID_BLOCKED_ENGINEERING_RUN` or `REUSABLE_W2_PREFLIGHT_EVIDENCE`;
- do not classify the result as `FAILED_ALGORITHM`, `GMTP_INCOMPATIBLE`, `W2_COMPLETED` or `W2_ACCEPTED`.

The owner-approved `RESOURCE_CONTRACT_CORRECTION` raises future resumed W2 task-owned disk ceiling from the historical 5 GB plan
to 10 GiB without changing algorithm, data, parameters or models. `S6.1-R0-FU1-W2-H1 / Offline Model Artifact Provisioning and
W2 Resume` is owner-approved as `APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS`, but execution is
`NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER`. LOCAL did not download models or create a bundle.

Correction 01 later supplied archive SHA-256
`d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e`, safe members `6/6`, index `4/4`, exact original-attempt
binding and complete main-repository integrity fields. Its manifest and measurement text agree on apparent bytes `5399301224`,
allocated bytes `5492817920` and ceiling `6442450944`. However, it records only `MEASUREMENT_TOOL=du`; it does not capture the
concrete apparent-size/allocated-size commands, flags or raw outputs. The Control Plane therefore cannot prove that the two
measurement semantics were not confused. `W2_ATTEMPT1_EVIDENCE_BLOCKER` remains open and H1 remains blocked/not started.

### Correction 02 Worker Contract Candidate

Governance status:

```text
Task ID = S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02
Task Type = EVIDENCE_PACKAGING_CORRECTION_ONLY
Machine = RTX5090 / COMPUTE_WORKER
Status = CONTRACT_CANDIDATE / NOT APPROVED / NOT SENT / NOT EXECUTED
Approval blocker = CORRECTION02_OWNER_APPROVAL_REQUIRED
Auto Continue = NO
```

This candidate is prepared under [PO-MHEP](../../governance/project_owner_sovereignty_and_mandatory_escalation_principle.md).
It is not authority to contact or execute the Worker. Owner approval is required before transmission.

#### Candidate objective and immutable scope

Capture only command-derived provenance for the existing `gmtp-compat` environment measurement. Do not run/import GMTP；do not
install, update, repair or activate a different environment；do not download/load models；do not use GPU；do not mutate the LLMGuard
or GMTP repositories；do not enter H1/P1/Formal Experiment.

Bind the candidate to:

- original Attempt 1 archive SHA-256 `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`;
- Correction 01 archive SHA-256 `d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e`;
- environment name/basename `gmtp-compat`;
- original main-repository Attempt 1 HEAD `457458cbc484c7a187c1b0b812c414280f4b837a` as historical binding only；no new repository
  state claim is required.

#### Candidate exact commands

The approved Worker, if later authorized, must execute on GNU/Linux with the existing `gmtp-compat` environment already active:

```bash
set -o nounset
set -o pipefail
test "${CONDA_DEFAULT_ENV:-}" = "gmtp-compat"
test "$(basename -- "${CONDA_PREFIX:?}")" = "gmtp-compat"
date -u +%Y-%m-%dT%H:%M:%SZ
LC_ALL=C du --version
LC_ALL=C du --apparent-size --block-size=1 --summarize -- "$CONDA_PREFIX"
LC_ALL=C du --block-size=1 --summarize -- "$CONDA_PREFIX"
```

The apparent command explicitly sets `--apparent-size --block-size=1 --summarize`. The allocated command deliberately omits
`--apparent-size` and uses GNU `du` default allocated-block semantics with `--block-size=1 --summarize`. `LC_ALL=C` freezes parseable
output. `$CONDA_PREFIX` is permitted only inside private Worker evidence；public Git records environment basename, not its absolute
path.

Each of the three evidence-producing commands (`du --version`, apparent, allocated) must be invoked separately with raw stdout,
raw stderr and exit code captured without piping or rewriting the streams. The private evidence must also preserve the literal
command template above and measurement timestamp. A summary field may be parsed only after exit code `0` and exactly one
`<non-negative integer><whitespace><path>` stdout record.

#### Candidate evidence set and index

Private directory candidate: `correction_02/`. Required indexed payloads are:

1. `original_attempt_reference.txt`;
2. `correction_01_reference.txt`;
3. `measurement_commands.txt`;
4. `environment_identity.txt`;
5. `measurement_timestamp.txt`;
6. `du_version.stdout`;
7. `du_version.stderr`;
8. `du_version.exit_code`;
9. `apparent_size.stdout`;
10. `apparent_size.stderr`;
11. `apparent_size.exit_code`;
12. `allocated_size.stdout`;
13. `allocated_size.stderr`;
14. `allocated_size.exit_code`;
15. `correction_manifest.json`.

`correction_index.sha256` must contain a normalized, lexicographically sorted SHA-256 entry for all `15/15` payloads and must be
reverified before packaging. The index does not self-index. Proposed private archive name is
`s6_1_r0_fu1_w2_attempt1_correction_02_20260801.tar.gz` plus `.sha256` sidecar. Candidate evidence/archive ceiling is `1 MiB`；
no repository, environment, cache, model, input text, credential or unrelated evidence may be included.

The manifest must bind schema/task/correction IDs, both earlier archive hashes, UTC timestamp, environment basename, literal
commands/flags, GNU `du` version evidence hashes, each raw-stream/exit-code hash, parsed apparent/allocated bytes, file count/index
status, `no_environment_mutation=true`, `no_model_download=true`, `no_smoke_execution=true` and
`claims_boundary=EVIDENCE_PACKAGING_CORRECTION_ONLY`. Public governance must not persist the Worker absolute path or username.

#### Candidate stop codes and claims

Return immediately to Control Plane with one of:

- `CORRECTION02_CONTEXT_MISMATCH` for missing/wrong environment identity;
- `CORRECTION02_DU_UNAVAILABLE` for absent/non-GNU or unsupported `du` flags;
- `CORRECTION02_MEASUREMENT_COMMAND_FAILED` for non-zero exit;
- `CORRECTION02_OUTPUT_SCHEMA_MISMATCH` for ambiguous/multiple/non-integer output;
- `CORRECTION02_EVIDENCE_INTEGRITY_BLOCKER` for manifest/index/archive mismatch or unsafe member.

Do not substitute another command/tool, estimate a value, suppress stderr, normalize raw streams, repair the environment or rerun
GMTP. A later passing Control Plane review could establish command provenance only；it would not by itself establish model load,
detector score, runtime, peak VRAM, GMTP compatibility, W2 completion/acceptance, P1 or a formal result.

## 9. Artifact approval budget

| Artifact | Source / revision | Transfer / disk reserve | RAM / VRAM ceiling | License or usage note | Need |
| --- | --- | --- | --- | --- | --- |
| PoisonedRAG NQ attack JSON | exact repo commit/blob above | 123 KB / in-memory LOCAL validation | 2 GB / none | repo code MIT；NQ-derived content remains under dataset terms | L1 completed |
| GMTP NQ 200 artifact | exact repo commit/blob above | 0.98 MB / included with repo | 2 GB / none before scoring | repository artifact license unconfirmed；internal use only pending terms | required only for W2 |
| Contriever + BERT | exact Hugging Face revisions above | ~0.9-1.2 GB / <=2 GiB model sub-budget within 10 GiB task-owned ceiling | 16 GB / 8 GiB | model-card terms must be retained and rechecked on approval | H1 approved but blocked/not started |
| RoBERTa or DPR alternatives | exact revisions above | ~0.5-0.9 GB extra / 5 GB extra | 16 GB / 8 GiB | model-card terms apply | optional; excluded from W2 |
| BEIR NQ corpus/index | official BEIR snapshot, final hash not frozen | 0.5 GB zip / 15-30 GB planned | 32 GB / estimated <16 GiB | NQ CC BY-SA obligations | not L1/W2；`OWNER_LARGE_ARTIFACT_APPROVAL_REQUIRED` |
| HotpotQA corpus/index | official BEIR snapshot | 0.65 GB zip / 25-50 GB planned | 32-64 GB / estimated <16 GiB | CC BY-SA 4.0 | optional fallback；`OWNER_LARGE_ARTIFACT_APPROVAL_REQUIRED` |
| MS MARCO corpus/index | official BEIR snapshot | 1.08 GB zip / 40-80 GB planned | 64 GB / estimated <16 GiB | non-commercial research; underlying rights not granted | optional later track；`OWNER_LARGE_ARTIFACT_APPROVAL_REQUIRED` |

The historical 5 GB W2 disk plan is superseded only by the owner-approved 10 GiB task-owned correction above. No model bundle was
created in this review. Formal corpus/index work remains closed.

## 10. Remaining blockers and P1 entry criteria

### Remaining blockers

1. `BLK-S6.1-FU1-W1-001` is `RESOLVED_BY_LOCAL_L1 / SUPERSEDED_BY_LOCAL_L1`; no Worker W1 remains.
2. `BLK-S6.1-FU1-W2-001`: W2 has not verified exact GMTP model loading, detector scores or measured runtime resources.
3. `W2_ATTEMPT1_EVIDENCE_BLOCKER`: Correction 01 resolves the main-repository capture gap and supplies internally consistent disk
   values, but omits the exact `du` commands/flags/raw outputs required to distinguish apparent from allocated bytes；H1 preparation
   remains stopped pending a minimal additive correction.
4. PoisonedRAG exact historical generator/API/paper-result identity remains `PARTIAL`; P1 must decide whether author-released
   attack-text reuse is scientifically sufficient instead of pretending full regeneration equivalence.
5. GMTP/SafeRAG code/data redistribution permission remains unconfirmed; this is a `REDISTRIBUTION_ONLY_ISSUE`, not an internal
   detection-core blocker.
6. Full corpus/index, generator, threshold calibration, metrics and formal comparison environment remain formal-experiment
   blockers and are outside FU1-P0.

### `S6.1-P1_ENTRY_CRITERIA`

P1 may be recommended only after the accepted P0/L1 and, if separately approved, accepted W2 evidence showing:

- NQ remains the selected primary external dataset and its later formal snapshot/license obligations are explicit;
- PoisonedRAG released-artifact identity, exact assembly, retriever/Top-K/attack budget and partial-equivalence boundary are
  accepted;
- GMTP source, models, detector-only call, input/output and modern RTX5090 compatibility are verified;
- SafeRAG SN/ICC benchmark-artifact contract remains frozen without a full-pipeline prerequisite;
- strict, partial, transfer-only and benchmark-reference boundaries are explicit;
- formal data/index/model budgets, metrics, thresholds, seeds and comparison protocol remain a separate P1 approval.

P0/L1 do not satisfy runtime or formal-protocol criteria and do not open P1. End state:

- historical `S6.1-R0-FU1-P0 = COMPLETED_PENDING_OWNER_REVIEW` remains preserved;
- `S6.1-R0-FU1-P0 = HUMAN_ACCEPTED`;
- `S6.1-R0-FU1-L1 = HUMAN_ACCEPTED`;
- former `FU1-W1 RTX5090 = SUPERSEDED_BY_LOCAL_L1`;
- historical `S6.1-R0-FU1-W2 = READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED` is preserved;
- `S6.1-R0-FU1-W2 = APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`;
- `S6.1-R0-FU1-W2-ATTEMPT1 = EVIDENCE_REVIEW_BLOCKED / W2_ATTEMPT1_EVIDENCE_BLOCKER`;
- `S6.1-R0-FU1-W2-H1 = APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS / NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER`;
- `S6.1-P1 = NOT STARTED`;
- `Dataset = NOT FROZEN`; `Detector = NOT IMPLEMENTED`; `Training = NOT STARTED`;
- `FORMAL_EXPERIMENT = NOT STARTED`; `Our Method Result = NONE`.
