# Paper 1 240-Group Scale Readiness Spec V3

Status: `PLANNING_ONLY / NOT_EXECUTED / NOT_FROZEN_DATASET`

## Purpose

V3 carries the accepted five-domain, four-HKP, three-stealth, four-independent-chain target (`240` groups; approximately `720` Clean/Poison/Hard-Negative candidates) forward while adding the retrieval-validity requirements exposed by the Final72 prototype. It does not generate candidates or authorize a formal benchmark run.

## Required group isolation

- Split by complete version-chain group; no Clean/Poison/Hard-Negative sibling may cross train/dev/test.
- Keep candidate IDs, group IDs, HKP, stealth, labels, adjudication and repair history out of retrieval queries and inference features.
- Preserve an untouched group-aware test population before any Detector fitting or threshold selection.

## Evidence and registry requirements

Each group must bind a unified trusted-corpus membership, stable document/version identities, official snapshot hashes, publisher/issuer/authority provenance, effective intervals, current/history role and explicit predecessor/successor evidence when available. Missing metadata remains missing. Chronology alone must not be converted into supersession.

The formal corpus must not contain only the two evidence documents already known to answer each candidate. It must include frozen, label-independent distractors, including:

- lexically similar but irrelevant official documents;
- same-subject and same-version-family alternatives;
- same-authority documents with different predicates or time scopes;
- current and historical versions that require version-aware discrimination;
- multi-evidence cases whose components are individually insufficient.

## Query robustness gate

Before labels or Oracle mappings are loaded, freeze and run at least:

- `Q_FULL`;
- `Q_NO_TITLE`;
- `Q_TEXT_ONLY`;
- `Q_STRUCTURED`.

Report title-removal and lexical-overlap deltas under predeclared thresholds. A corpus with no lexically similar irrelevant distractors cannot support formal retrieval-effectiveness claims, even if reference Recall@K is high.

## Detector boundary

Stage A consumes only frozen, non-Oracle S/E/P/T inputs. Availability/missingness must be audited separately and may not become a class shortcut. Retrieval-Behavior R remains Stage B (`document risk + query context + R → exposure risk`). Feature selection, normalization, fitting, calibration and thresholds require separate approval and development-only procedures.

## Readiness gates before execution

1. Candidate-generation and annotation protocol separately approved.
2. Trusted corpus and Version Registry schema complete enough for planned Temporal/Provenance signals.
3. Distractor design and query-robustness thresholds frozen before label analysis.
4. Group-aware split manifest locked before model development.
5. No Oracle E1/E2 identity used in retrieval, aggregation or inference features.
6. Independent leakage audit passes for raw values, applicability, IDs, paths and annotation-process fields.
7. Formal run, Detector training and untouched-test evaluation each receive separate Owner approval.

Current Final72 outcome is only engineering feedback: `Q_NO_TITLE + HYBRID` is the frozen prototype setting, lexical-overlap risk is material, and the 57-document corpus is too easy for formal evaluation. None of these observations is a Paper result.

## 2026-09-21 detector-preflight feedback

Before any scaled Detector fit, every frozen feature must have either observable training values or an independently justified neutral/applicability representation. A feature that is globally `INPUT_MISSING` cannot be silently filled, dropped or converted into a missingness indicator. The scale corpus and Registry must therefore provide real host/publisher and publisher/issuer relations across train/dev/test, with missingness rates reported by class, domain and split before labels are used for model development. This requirement is added because Final72 Feature Set V1 contains two 72/72 all-missing Provenance columns; no model result was produced from them.

## 2026-09-22 observability gate for formal scale

Owner rejected constant/indicator repair and conditionally approved a 21-feature Final72 development-only V1.1 after a frozen-source metadata audit found no valid candidate-level representation for two relation features. The future 240-group construction must collect, before candidate labels and splits are consulted, `source_host`, `page_publisher`, `document_issuer`, authority role, document/version binding, official repost status, role-level provenance, and a source-backed host-to-institution mapping. It must predeclare the relation taxonomy and how multiple retrieved documents are aggregated into one candidate-level signal. A URL host is never silently equated with a publisher or issuer.

Before **any** proposed feature is frozen for formal scale, run an observability preflight: type/semantics, lawful source, representative observed count, applicability versus missingness, per-domain and per-group coverage, and train-fold preprocessing feasibility under the planned group-aware split. After the feature matrix is locked, check missingness by class for label shortcuts. The two deferred relations may return only through a separately versioned contract backed by actual data; Final72 V1.1 does not erase their scientific value or establish their future performance.

## 2026-09-22 first LOGO prototype feedback (development-only)

Final72 V1.1's 24-group LOGO pipeline runs reproducibly, but its nine fixed-view models show **mixed** rather than established multiview advantage. Full SEPT AUROC/AUPRC `.647/.496`; Full-P `.673/.571` and Full-T `.674/.536`. T-only has HN-FPR `.917` at the fixed `.5` threshold; Full has `.333`. The scaled set must challenge legal historical hard negatives across all version roles, not reward labeling every old text poison. It must capture temporal effective intervals/supersession/current-vs-history bindings and candidate-bound host/publisher/issuer lineage natively, before labels. Include difficult same-family/same-authority distractors and multi-evidence cases in a unified trusted corpus: the current 57-document evidence pool is too easy for formal retrieval evaluation. Audit constant/near-constant signal coverage, class/domain missingness, shortcut potential and group-level failures (`EDU-06`, `FIN-03`, `FIN-04`, `HR-03`, `INF-01`, `INF-04`, `INF-05`) as **construction hypotheses**, without copying their answers or tuning Final72. Formal test must be independent, untouched and version-chain group isolated; no model claim is transferred from this development diagnostic.

## 2026-09-22 failure-analysis and raw-prediction retention feedback

The validated one-time reconstruction supplied the eight model OOF vectors omitted from the original result serialization; the original Full OOF and summary metrics remain canonical. Final72 has seven observed-constant features, only 13 distinct varying feature vectors, T-only/P-only each with 20/24 Poison–HN ties, and PTS V3 computed for only 10/40 temporal-applicable candidates. These are development diagnostics, not a license to tune Final72. Before freezing any formal feature contract, the scale construction must preflight overall/domain/class variance, applicability versus missingness, and legal inference inputs. Planned temporal groups must natively retain version family/ID, current/history role, effective start/end, predecessor/successor/supersession, current/historical binding and metadata provenance. Provenance groups must retain host, page publisher, issuer, authority role, repost relation and candidate-to-document/version lineage; official-site membership alone is insufficient variation.

Formal hard negatives must stay factually valid and source-backed while approaching Poison in vocabulary, entity, claim shape, authority and version family. The unified frozen evidence corpus must contain same-domain, same-family different-version, same-authority unrelated and lexically similar irrelevant official distractors; difficulty/coverage gates must be defined before labels are used in method development. Preserve at least four independent chains per design cell, and keep version-chain siblings together across train/dev/test. The untouched group-aware test must remain unseen during feature, model, hyperparameter and threshold selection.

Every future single-view, ablation, baseline and formal model run must satisfy [Experiment Output Contract V1](../method_engineering/PAPER1_EXPERIMENT_OUTPUT_CONTRACT_V1.md): per-sample score/probability/model/fold/input-hash retention, plus per-fold trace and immutable index. `PER_SAMPLE_PREDICTION_RETENTION=TRUE / PER_FOLD_TRACE_RETENTION=TRUE / VIEW_ABLATION_RAW_SCORE_RETENTION=TRUE`. This rule prevents aggregate-only evidence from blocking later matched-group analysis. It does not itself approve the 240-group construction or formal experiment.
