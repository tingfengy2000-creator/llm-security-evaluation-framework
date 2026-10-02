# Core144 D2/D3 Phase1 external reviewer send checklist

Status: `PREPARED_NOT_DISTRIBUTED / STOP_EXTERNAL_REVIEW_REQUIRED`.
The paths below are relative to the `stage6-rag` worktree root. The private
`experiments/` files are Git-ignored local research artifacts; a remote Git
checkout alone does not contain them. The Owner must verify the exact file
hashes in each domain's `reviewer/package_manifest.json` before sending.

Send **exactly three files per fresh, isolated reviewer conversation**: that
reviewer's prompt, that reviewer's 144-row candidate-only package, and the
same domain's Phase1 import schema. D2 and D3 require separate fresh
conversations. `R4_CODEX` is a stable reviewer code; the actual provider is
Doubao. Do not present the R4 code as evidence that Codex was used.

## D2 Finance — 144 rows each

### R3-GPT, new isolated GPT conversation

1. `experiments/core144_d2_d3_20260929/d2/domain_release_v1/reviewer/PAPER1_CORE144_D2_R3_GPT_PHASE1_PROMPT_V1.md`
2. `experiments/core144_d2_d3_20260929/d2/domain_release_v1/reviewer/PAPER1_CORE144_D2_R3_GPT_PHASE1_PACKAGE_V1.json`
3. `experiments/core144_d2_d3_20260929/d2/domain_release_v1/reviewer/PAPER1_CORE144_D2_PHASE1_IMPORT_SCHEMA_V1.json`

Expected raw filename: `PAPER1_CORE144_D2_R3_GPT_PHASE1_RAW_RETURN_V1.json`.

### R4-CODEX code, new isolated Doubao conversation

1. `experiments/core144_d2_d3_20260929/d2/domain_release_v1/reviewer/PAPER1_CORE144_D2_R4_CODEX_PHASE1_PROMPT_V1.md`
2. `experiments/core144_d2_d3_20260929/d2/domain_release_v1/reviewer/PAPER1_CORE144_D2_R4_CODEX_PHASE1_PACKAGE_V1.json`
3. `experiments/core144_d2_d3_20260929/d2/domain_release_v1/reviewer/PAPER1_CORE144_D2_PHASE1_IMPORT_SCHEMA_V1.json`

Expected raw filename: `PAPER1_CORE144_D2_R4_CODEX_PHASE1_RAW_RETURN_V1.json`.

## D3 Information Security — 144 rows each

### R3-GPT, a different new isolated GPT conversation

1. `experiments/core144_d2_d3_20260929/d3/domain_release_v1/reviewer/PAPER1_CORE144_D3_R3_GPT_PHASE1_PROMPT_V1.md`
2. `experiments/core144_d2_d3_20260929/d3/domain_release_v1/reviewer/PAPER1_CORE144_D3_R3_GPT_PHASE1_PACKAGE_V1.json`
3. `experiments/core144_d2_d3_20260929/d3/domain_release_v1/reviewer/PAPER1_CORE144_D3_PHASE1_IMPORT_SCHEMA_V1.json`

Expected raw filename: `PAPER1_CORE144_D3_R3_GPT_PHASE1_RAW_RETURN_V1.json`.

### R4-CODEX code, a different new isolated Doubao conversation

1. `experiments/core144_d2_d3_20260929/d3/domain_release_v1/reviewer/PAPER1_CORE144_D3_R4_CODEX_PHASE1_PROMPT_V1.md`
2. `experiments/core144_d2_d3_20260929/d3/domain_release_v1/reviewer/PAPER1_CORE144_D3_R4_CODEX_PHASE1_PACKAGE_V1.json`
3. `experiments/core144_d2_d3_20260929/d3/domain_release_v1/reviewer/PAPER1_CORE144_D3_PHASE1_IMPORT_SCHEMA_V1.json`

Expected raw filename: `PAPER1_CORE144_D3_R4_CODEX_PHASE1_RAW_RETURN_V1.json`.

## Isolation and return gate

Do not send the other reviewer's package or answer, the other domain, the
repository or handoff directory, Evidence/Phase2, construction records,
mapping, C/P/H, HKP, S, Expected, GT or Owner decisions. The fresh sessions
must not browse the web or use other AI. The reviewer should create one
downloadable strict UTF-8 JSON file containing 144 objects in package ID
order, and separately state the actual provider and session isolation.

The Owner returns the four untouched raw files to this task. First byte-lock
each original and verify SHA-256, schema, enums, 144 IDs, order and raw
provenance. Only then compare R3/R4 Phase1 fields; Phase2 remains withheld
until the relevant domain's Phase1 gate explicitly passes. Reviewer agreement
is construction QA, not GT. If a real upload/context/truncation/serialization
failure occurs, preserve the incident and request a versioned `96+48`
fallback. Do not pre-split either 144-row package.
