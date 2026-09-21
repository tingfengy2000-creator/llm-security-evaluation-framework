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
