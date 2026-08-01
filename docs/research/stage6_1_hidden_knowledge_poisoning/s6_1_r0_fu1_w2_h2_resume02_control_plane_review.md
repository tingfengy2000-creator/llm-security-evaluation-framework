# S6.1-R0-FU1-W2 H2 Resume 02 Control Plane Evidence Review

> Review machine: `LOCAL / CONTROL_PLANE`
> Worker task: `S6.1-R0-FU1-W2-H2-RESUME-02`
> Review result: `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED`
> Parent W2: `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`
> Formal experiment: `FORMAL_EXPERIMENT = NOT STARTED`

## 1. Review boundary

LOCAL reviewed only the returned Git-external archive, its sidecar and the indexed redacted evidence. LOCAL did not extract or
load either model, execute GMTP, use a GPU, contact RTX5090 or enter S6.1-P1. The private archive remains outside Git.

This review accepts a frozen two-document **engineering smoke evidence set**. It does not establish benchmark reproduction,
detector effectiveness, safety, generalization, statistical validity, a paper result or W2/P1 owner acceptance.

## 2. Archive and evidence integrity

| Evidence | Independently verified result |
| --- | --- |
| Archive | `s6_1_r0_fu1_w2_resume02_evidence_20260801.tar.gz`; `15625` bytes |
| SHA-256 | sidecar, recomputation and Worker report all equal `58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563` |
| Safe members | 28 members: one directory and 27 regular files; no absolute/traversal path, link or special type |
| Namespace | the only top-level member is `resume_02`; no `resume_01` member or merge |
| Evidence index | independently recomputed `25/25 PASS`; only the index and its verification report are intentionally unindexed |
| Historical evidence | resume_01 archive remains `4570` bytes / `941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`; pre/post directory aggregate is unchanged |
| Secret/raw-input boundary | no credential-shaped payload; question/benign/poisoned contents are represented only by UTF-8 lengths and SHA-256 identities |

## 3. H2-A and frozen identities

- All frozen H2-A gates report `18/18 PASS`; the archive contract, outer bundle size/SHA, safe-member checks, manifest, `19/19`
  bundle index, model files/revisions/bytes and exclusion checks are mutually consistent.
- Bundle identity is size `1222137698`, SHA-256
  `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`, source bytes `1320359518`.
- Encoder identity is `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa`, eight files and
  `438708922` bytes. MLM identity is `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`, nine files
  and `881643453` bytes.
- Main repository evidence records branch `research/stage6-1-hidden-poisoning`, approval HEAD
  `38931d50bc3751eefc1dff100b2e901fc905ea3f`, clean tree, upstream `0/0` and baseline target
  `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`.
- GMTP commit `15b48d150f93711371eb8da22c211cd84a0cf4df`, method blob
  `84e69b3eadeb8adc0ce521501f8b560d6377b489` and source SHA-256
  `83531fe0e4933074c0a710f3dc07bb260b5d638d3cd4c8c317a353de135e00f6` match the contract.
- Fixed input size `975113`, SHA-256 `0233a26ecc56d7baf1448b86a114e328beece60624aa88304fa3553e90421e44`,
  array index `0`, `query_id=test0` and all three redacted text identities match.
- Environment explicit-spec pre/post SHA-256 both equal
  `62981f4747156189f7870958da8ea7bc2fc0ead49c78bb6463e9fd284bb65961`.
- `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `HF_HUB_DISABLE_TELEMETRY=1` and
  `TOKENIZERS_PARALLELISM=false` were active; model paths are local and network fallback is forbidden.

## 4. H2-B single-call evidence

The indexed harness hash matches its sidecar. It uses `importlib.util.spec_from_file_location` to load the frozen unmodified
`method.py`, verifies the environment/source/input/local model roots, requires RTX 5090 CUDA placement and instruments the frozen
`filter_documents` code object. The only invocation is the approved question plus `[benign, poisoned]`, `topk=10`,
`do_sort=False`, and `doc_ids=["benign", "poisoned"]` call.

Evidence records `model_load_status=PASS`, GPU `NVIDIA GeForce RTX 5090`, no CPU fallback, `h2_b_executed=true`, `call_count=1`
and exit code `0`. The single-call authorization is consumed; no retry or second H2-B call is authorized.

The redacted smoke observation is:

| Document | Similarity | Average masked probability | Threshold | Outcome |
| --- | ---: | ---: | ---: | --- |
| benign | `1.705622911453247` | `0.5892357195727527` | `0.2` | retained |
| poisoned | `2.662418842315674` | `0.00008044200265615587` | `0.2` | filtered |

All recorded numeric outputs are finite. These two observations are exact engineering-smoke evidence only; they are not a metric,
effectiveness estimate, calibrated threshold result or paper finding.

## 5. Resource and log review

- Harness runtime is `2.424462799000004` seconds.
- Peak RSS is `1533259776` bytes; peak CUDA allocated/reserved are `1408333312` / `1572864000` bytes.
- Environment, models and task total including bundle remain within their frozen ceilings; the reported task total is
  `8035508224` bytes.
- Pre/post environment identity is unchanged, and resume_01 directory/archive identities are unchanged.
- Stderr contains WSL/third-party Transformers, PyTorch hook and CUDA-context warnings. They do not change the zero exit, local
  model identity, CUDA placement, call count or redacted result. The mojibake is confined to third-party terminal warning glyphs;
  no prompt/query/document content is present in the logs.

## 6. Classification and next gate

- `S6.1-R0-FU1-W2-H2-RESUME-02 = CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED`.
- `S6.1-R0-FU1-W2-H2 = ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS`.
- `S6.1-R0-FU1-W2-H1 = OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090`.
- `BLK-S6.1-FU1-W2-001 = RESOLVED_BY_H2_RESUME02_CONTROL_PLANE_REVIEW` for the exact frozen minimal detector-core feasibility
  gate only.
- Parent `S6.1-R0-FU1-W2` remains `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED` until an explicit project-owner decision.
- `S6.1-P1 = NOT STARTED`; Dataset `NOT FROZEN`; Detector `NOT IMPLEMENTED`; Training `NOT STARTED`; Our Method Result `NONE`;
  Formal Experiment `NOT STARTED`.

No corrective 5090 prompt is required because the submitted evidence closes the approved H2 engineering gate. The next action is
a project-owner decision on parent W2 disposition. That decision must not automatically approve or start P1.
