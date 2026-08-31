# S6.1-P1-PILOT2 Adjudication Closure Attempt

## 1. Scope and owner authority

- Task: `S6.1-P1-PILOT2-ADJUDICATION-CLOSURE-AND-PILOT3-ENTRY`.
- Date: `2026-08-31`.
- Machine: `LOCAL / CONTROL_PLANE`.
- Owner approval: validate the completed owner packet, construct a Pilot-only Ground Truth candidate only after validation passes,
  close Pilot2 only after its quality gate passes, and then run a local small-scale Pilot3 signal diagnostic.
- Prohibited: rewriting the owner workbook, automatic conflict resolution, A/B relabeling, 5090 contact, 240-group data,
  Dataset freeze, large-model training, Formal Experiment, Paper Result or SOTA claim.

## 2. Dynamic Git and owner evidence binding

- Unique worktree resolved by `git worktree list --porcelain` for
  `refs/heads/research/stage6-1-hidden-poisoning`; no checkout path was assumed.
- Execution base: `54481eb740cab09c559524623b022385cd0f8c3b`; upstream ahead/behind `0/0`; worktree clean.
- Owner workbook:
  `LLMGuard-Handoff/paper1_pilot2_post_annotation_20260831/minimal_owner_adjudication_packet.xlsx`.
- `OWNER_ADJUDICATION_INPUT_SHA256 = cf47a6c3ffada717a2a0dee2b67d6b92ebfb6236d599fb8a4daf2957e292dcb1`;
  size `42,081` bytes.
- The distributed blank packet SHA256 remains historical identity
  `67081c0e3f7c32d42041ccc736316ed2f42fa979d417a76f577b4e90418d363a`.
- The workbook was read and rendered without saving; formula-error scan found zero matches. LOCAL did not change owner values.

## 3. Completion and consistency validation

- Issue rows: `84/84` have owner final value, rationale and inclusion decision.
- Candidate rows: `26/26` are marked `RESOLVED` and have inclusion decisions.
- Residual `PENDING`: `0`.
- Completion therefore passes, but executable cross-row consistency fails for four candidates:

| Candidate | Issue rows | Field | Blocker |
| --- | --- | --- | --- |
| `C-3ed6b082e98ee91e` | `D-007 / L-081` | `locally_detectable` | owner values are both `NO` and `YES` |
| `C-6fe04fe29567e9d9` | `D-032` | `version_relation_present` | `YES;` is not an exact frozen enum member |
| `C-f73d03e9cfdf6e64` | `D-023 / L-057 / L-076 / L-077 / L-078` | `assigned_stealth_level` | `S2` conflicts with `NOT_APPLICABLE`; two rows use the invalid stealth value `LEGITIMATE_VERSION_OR_HISTORY` |
| `C-fda2135153cc6c96` | `L-049` | `assigned_stealth_level` | `LEGITIMATE_VERSION_OR_HISTORY` is not a stealth enum |

The minimal reconfirmation table records exact candidate text, evidence, observed cells and LOCAL recommendations. It does not ask
A/B to annotate again and does not silently replace an owner value.

## 4. Evidence and stop status

Git-external blocker evidence root:

`LLMGuard-Handoff/paper1_pilot2_closure_20260831`

The root contains the four-candidate CSV/JSON, owner workbook binding, blocker manifest, human summary and a `5/5` SHA256 index.

```text
OWNER_ADJUDICATION_COMPLETION = PASS_84_OF_84_ISSUES_AND_26_OF_26_CANDIDATES
OWNER_ADJUDICATION_CONSISTENCY = FAIL
BLOCKER = OWNER_ADJUDICATION_CONSISTENCY_BLOCKER
OWNER_RECONFIRMATION = REQUIRED_FOR_4_CANDIDATES
GROUND_TRUTH_CANDIDATE = NOT_GENERATED
PILOT2_CLOSURE = BLOCKED
PILOT3_ENTRY = NOT_STARTED
DATASET = NOT_FROZEN
FORMAL_EXPERIMENT = NOT_STARTED
AUTO_CONTINUE = NO
```

Next gate: the project owner confirms only the four rows in the minimal blocker table and returns a corrected owner workbook or an
explicit issue-ID-to-final-value decision. LOCAL then rebinds the new evidence identity and repeats validation before Ground Truth.
