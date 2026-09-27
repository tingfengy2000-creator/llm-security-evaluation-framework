# D1 HKP2 remaining-batch internal gate (not external acceptance)

Status: `HKP2_INTERNAL_CONSTRUCTION_GATE_PASS / EXTERNAL_REVIEW_PENDING / MEGAWAVE_NOT_RELEASED`.

This additive record covers the ten frozen HKP2 slots (`S1/S2/S3 = 3/3/4`) and 30 internal C/P/H draft candidates. It does **not** accept these candidates as Formal Ground Truth or authorize a 30-row reviewer release. The Owner-approved routing remains one combined 90-row R3/R4 Phase1 MegaWave after HKP3 and HKP4 independently pass their internal gates.

## Evidence-first lineage

- The [preconstruction evidence contract](PAPER1_FORMAL_D1_HKP2_EVIDENCE_PRECONTRACT_V1.json) was authored before candidates. Fourteen raw official documents were referenced across ten distinct within-batch family clusters. Their byte hashes, official HTTPS hosts, and frozen-slot allocation passed `PAPER1_FORMAL_D1_HKP2_PRECONSTRUCTION_EVIDENCE_IDENTITY_AUDIT_V1.json` in the private handoff namespace.
- The 1988 historical regulation is the unchanged Hubei official gazette PDF (`www.hubei.gov.cn`, 10,698,755 bytes, SHA256 `0e019dba4f9a32c142612bd36a1051821dfd89c228cfe1092f16b30b9b22d30a`). A short [Article 8 derived transcription](PAPER1_FORMAL_D1_HKP2_ML1988_ARTICLE8_DERIVED_TEXT_V1.txt) was visually checked against PDF page 6 for retrieval indexing. It is explicitly **not** the raw official PDF; its [provenance record](PAPER1_FORMAL_D1_HKP2_ML1988_ARTICLE8_DERIVED_TEXT_PROVENANCE_V1.json) keeps that distinction.
- An official Shanghai historical Q&A cites a separate contemporaneous notice with a four-month miscarriage-leave threshold. Therefore the original S3-C4 draft's broad claim about the entire 1988 regime was too strong. [Additive scope repair](PAPER1_FORMAL_D1_HKP2_S3C4_SCOPE_REPAIR_OVERLAY_V1.json) limits the comparison to the two named regulation clauses. V1–V7 private drafts remain retained and unreleased; S3-C4 receives new candidate IDs in V8.
- [S3 temporal metadata](PAPER1_FORMAL_D1_HKP2_S3_TEMPORAL_METADATA_OVERLAY_V1.json) records four version families and explicit source refs. Host, page publisher, original issuer and version role are kept separate; unobserved interval ends are not guessed.

## Construction-side results

Current private draft in the Owner handoff namespace `paper1_formal240_d1_remaining90_hkp2_20260927`: `PAPER1_FORMAL_D1_HKP2_CANDIDATE_DRAFT_V8_NOT_RELEASED.jsonl`, SHA256 `49ab68b61214d0e8a14d7b102c11be75f84609035dd23d7072dcfeae9e4ba24f`.

The linked atom audit (`...CONSTRUCTION_SIDE_QA_V5.json`) records 43 supported and 10 deliberately corrupted atoms, no *identified* accidental or ambiguous atom. This is construction-side inspection, not independent reviewer confirmation. Each triplet has one shared neutral query and the intended S1/S2/S3 path; target S was not used to alter a reviewer judgment. Character max/min ratio is 1.28. An expanded surface audit found no remaining numeric-surface attention flag after V8 repair. It does not assert perfect naturalness.

The private `PAPER1_FORMAL_D1_HKP2_INTERNAL_MECHANICAL_QA_V5.json` (SHA256 `57789396e0a35dffe8125dffe2b0d42a9818b41633e729a48f4fee07a2e661dd1`) reports 10/10 group queries executed against 14 frozen-source documents with fixed character-bigram BM25 (`k1=1.2`, `b=0.75`). Its top-k trace is an engineering smoke test, **not** candidate selection or a retrieval effectiveness claim. S/E inputs are present for 30/30; T applies to 12/30; P is not applicable because this HKP2 draft does not assert an issuing/publishing authority; R has shared neutral query and corpus membership. Input-missingness states are symmetric across C/P/H. The 1988 PDF excerpt's second-person transcription check remains for later independent blind inspection.

## Boundary and next gate

No R3/R4 package, reviewer raw return, Phase2 bundle, Human A/B package, GT, split, or model run was produced for HKP2. The next authorized internal unit is HKP3 Evidence-first construction. If HKP3 or HKP4 reveals a real hard blocker, stop without assembling the 90-row reviewer package. If both pass, create the single cross-group-shuffled MegaWave and only then ask the Owner to route it to new isolated R3/R4 environments.
