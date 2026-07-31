# S6.1-R0-FU1 Targeted External Baseline Feasibility Resolution

> Task: `S6.1-R0-FU1-P0 / LOCAL Control-Plane Planning and Execution Contract Freeze`
> Status: `COMPLETED_PENDING_OWNER_REVIEW`
> Execution mode: `LOCAL-FIRST / WORKER-GATED`
> Evidence class: `CONTROL_PLANE_SOURCE_ANALYSIS / CONTRACT_CANDIDATE`
> Formal experiment: `FORMAL_EXPERIMENT = NOT STARTED`

## 1. Scope and decision boundary

The project owner approved `S6.1-R0-FU1`, but only P0 is currently executable. This record freezes source-backed candidate
identities and future Worker contracts. LOCAL did not clone or run an external baseline, download a dataset/model, invoke an API,
or contact RTX5090. `FU1-W1` and `FU1-W2` remain `NOT APPROVED`; this document is not a P1 protocol or experiment result.

Current baseline roles remain unchanged:

| Baseline | Role | Current evidence status |
| --- | --- | --- |
| PoisonedRAG | `PRIMARY_ATTACK_BASELINE` | released attack-text reuse is feasible; exact regeneration identity is not recovered |
| GMTP | `PRIMARY_DETECTION_BASELINE` | source and detection-only call path are frozen; Worker execution is pending approval |
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
| MLM reranker | `bert-base-uncased` | `86b5e0934494bd15c9632b12f734a8a67f723594` | 440,449,768 safetensors | required |
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
| Formal reproduction need | W1 identity validation, then P1 protocol | W2 core execution, then P1 protocol | artifact contract already sufficient for P1 design |
| Intended use | fixed external attack exposure | raw detection-score baseline | Chinese benchmark/task reference |
| Current comparability | `PARTIALLY_COMPARABLE` | `PARTIALLY_COMPARABLE` with PoisonedRAG on NQ | `BENCHMARK_REFERENCE_ONLY` |

The highest-value chain is NQ `PoisonedRAG attack -> poisoned document -> GMTP detection`. It is not yet a strict paper-to-paper
comparison: PoisonedRAG's released `adv_targeted` texts and GMTP's released PoisonedRAG/HotFlip corpus are distinct author
artifacts, retriever settings and result paths. Using the PoisonedRAG-released texts directly with GMTP provides a controlled
`TRANSFER_EVALUATION_ONLY` track; using GMTP's packaged PoisonedRAG corpus provides a GMTP-native detector track. P1 must keep
those tracks separate.

## 8. Proposed Worker contracts — not approved

### FU1-W1: PoisonedRAG Targeted Artifact / Attack Path Validation

| Contract field | Frozen candidate |
| --- | --- |
| Repo / commit | `https://github.com/sleeepeer/PoisonedRAG.git` / `f660d72174f06b13fae5163ce656e7b235db858f` |
| Environment | WSL Ubuntu; system Python 3 stdlib only; no install, model, dataset or API |
| Exact source | `results/adv_targeted_results/nq.json` blob/SHA-256 above; `src/attack.py` blob `a29630c42508adbb421cc5ee23eac9bbcd58be44` |
| Exact sample | lexicographically first key `test1`; validate required fields and exactly five `adv_texts` |
| Exact operation | verify commit/blob/SHA-256/schema/count; construct five strings using the audited `question + "." + adv_text` rule; hash outputs; do not save full texts in public evidence |
| Exact output | redacted JSON manifest with repo/commit/blob/hash, record count, sample ID, field names, five output SHA-256 values, byte counts and source-code identity |
| Resource ceiling | network <100 MB preferred via partial/sparse clone; disk 1 GB; RAM 2 GB; no GPU; 5 minutes |
| Stop conditions | hash/schema/count mismatch, network need beyond repo, API/model/data request, dirty source tree |
| Claims boundary | validates released-artifact reuse/call-path only; does not regenerate poison, reproduce retrieval/ASR or prove paper-generation identity |

The W1 runner must use `git clone --filter=blob:none --no-checkout`, checkout the exact commit and sparse-select only
`src/attack.py` plus `results/adv_targeted_results/nq.json`; its validation script and output manifest must be hashed before and
after execution.

### FU1-W2: GMTP Detection-Only Minimal Smoke

| Contract field | Frozen candidate |
| --- | --- |
| Repo / commit | `https://github.com/mountinyy/GMTP.git` / `15b48d150f93711371eb8da22c211cd84a0cf4df` |
| Environment | isolated clone of accepted Worker Python 3.11 / `torch 2.13.0+cu130`; add only `transformers==4.47.1`, `numpy==1.26.4` and their resolved dependencies; return full freeze |
| Exact models | local snapshots of Contriever and BERT at the revisions in section 5; pass snapshot paths to unmodified `GMTP` constructor |
| Exact input | blob `72fb52...`; record index 0 / `query_id=test0`; score `gt_text[0]` and `poisoned_docs[0]` |
| Exact detector config | `ret_type=contriever`, `N=5`, `M=5`, `remove_threshold=0.2`, `remove_lambda=1.0`, `topk=10`, `do_sort=false` |
| Exact call | invoke official `GMTP.filter_documents`; a read-only Python trace wrapper may capture its local `doc_infos` at return without editing detector source |
| Exact output | commit/blob/model revisions, source SHA-256 before/after, sample ID/doc-role hashes, `sim`, `avg_masked_prob`, retained flag, token-score hash/count, wall time, RSS, peak VRAM and environment/GPU identity |
| Resource ceiling | download 1.2 GB; disk 5 GB; RAM 16 GB; VRAM 8 GiB; 10 minutes after cache availability |
| Stop conditions | source/model revision mismatch, source mutation, CPU fallback, OOM/ceiling breach, NaN/Inf, unexpected Java/Pyserini/FAISS/API/generator request |
| Claims boundary | engineering detector-core smoke only; no threshold-quality, attack detection rate, nDCG/ASR, strict comparison or formal reproduction claim |

W2 must not install Java, Pyserini, FAISS, BEIR, generators or evaluators. If exact source cannot run with the accepted modern
Torch base, return `COMPATIBILITY_BLOCKER` with the minimal stack trace; do not downgrade Torch or alter the algorithm without a
new owner decision.

## 9. Artifact approval budget

| Artifact | Source / revision | Transfer / disk reserve | RAM / VRAM ceiling | License or usage note | Need |
| --- | --- | --- | --- | --- | --- |
| PoisonedRAG NQ attack JSON | exact repo commit/blob above | 123 KB / <1 GB sparse workspace | 2 GB / none | repo code MIT；NQ-derived content remains under dataset terms | required only for W1 |
| GMTP NQ 200 artifact | exact repo commit/blob above | 0.98 MB / included with repo | 2 GB / none before scoring | repository artifact license unconfirmed；internal use only pending terms | required only for W2 |
| Contriever + BERT | exact Hugging Face revisions above | ~0.9-1.2 GB / 5 GB | 16 GB / 8 GiB | model-card terms must be retained and rechecked on approval | required only for W2 |
| RoBERTa or DPR alternatives | exact revisions above | ~0.5-0.9 GB extra / 5 GB extra | 16 GB / 8 GiB | model-card terms apply | optional; excluded from W2 |
| BEIR NQ corpus/index | official BEIR snapshot, final hash not frozen | 0.5 GB zip / 15-30 GB planned | 32 GB / estimated <16 GiB | NQ CC BY-SA obligations | not W1/W2；`OWNER_LARGE_ARTIFACT_APPROVAL_REQUIRED` |
| HotpotQA corpus/index | official BEIR snapshot | 0.65 GB zip / 25-50 GB planned | 32-64 GB / estimated <16 GiB | CC BY-SA 4.0 | optional fallback；`OWNER_LARGE_ARTIFACT_APPROVAL_REQUIRED` |
| MS MARCO corpus/index | official BEIR snapshot | 1.08 GB zip / 40-80 GB planned | 64 GB / estimated <16 GiB | non-commercial research; underlying rights not granted | optional later track；`OWNER_LARGE_ARTIFACT_APPROVAL_REQUIRED` |

No large-artifact approval is required to approve only W1/W2 under their frozen ceilings. Formal corpus/index work remains closed.

## 10. Remaining blockers and P1 entry criteria

### Remaining blockers

1. `BLK-S6.1-FU1-W1-001`: W1 has not verified the exact sparse-checkout artifact, deterministic assembly hashes and evidence
   manifest on Worker; execution is not approved.
2. `BLK-S6.1-FU1-W2-001`: W2 has not verified exact GMTP source compatibility, pinned models, scores and measured resources on
   RTX5090; execution is not approved.
3. PoisonedRAG exact historical generator/API/paper-result identity remains `PARTIAL`; P1 must decide whether author-released
   attack-text reuse is scientifically sufficient instead of pretending full regeneration equivalence.
4. GMTP/SafeRAG code/data redistribution permission remains unconfirmed; this is a `REDISTRIBUTION_ONLY_ISSUE`, not an internal
   detection-core blocker.
5. Full corpus/index, generator, threshold calibration, metrics and formal comparison environment remain formal-experiment
   blockers and are outside FU1-P0.

### `S6.1-P1_ENTRY_CRITERIA`

P1 may be recommended only when the owner has reviewed P0 and, if approved, accepted W1/W2 evidence showing:

- NQ remains the selected primary external dataset and its later formal snapshot/license obligations are explicit;
- PoisonedRAG released-artifact identity, exact assembly, retriever/Top-K/attack budget and partial-equivalence boundary are
  accepted;
- GMTP source, models, detector-only call, input/output and modern RTX5090 compatibility are verified;
- SafeRAG SN/ICC benchmark-artifact contract remains frozen without a full-pipeline prerequisite;
- strict, partial, transfer-only and benchmark-reference boundaries are explicit;
- formal data/index/model budgets, metrics, thresholds, seeds and comparison protocol remain a separate P1 approval.

P0 alone does not satisfy runtime criteria and does not open P1. End state:

- `S6.1-R0-FU1-P0 = COMPLETED_PENDING_OWNER_REVIEW`;
- `FU1-W1 = NOT APPROVED`;
- `FU1-W2 = NOT APPROVED`;
- `S6.1-P1 = NOT STARTED`;
- `Dataset = NOT FROZEN`; `Detector = NOT IMPLEMENTED`; `Training = NOT STARTED`;
- `FORMAL_EXPERIMENT = NOT STARTED`; `Our Method Result = NONE`.
