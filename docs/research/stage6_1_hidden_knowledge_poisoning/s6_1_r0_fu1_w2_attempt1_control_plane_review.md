# S6.1-R0-FU1-W2 Attempt 1 Control Plane Evidence Review

> Review machine: `LOCAL / CONTROL_PLANE`
> Worker task: `S6.1-R0-FU1-W2 / GMTP Detection-Only Minimal Smoke`
> Historical initial review status: `W2_ATTEMPT1_EVIDENCE_BLOCKER`
> Current superseding status: `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER` after Correction 02 final closure
> Parent W2 status: `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`
> Formal experiment: `FORMAL_EXPERIMENT = NOT STARTED`

## 1. Review boundary

LOCAL performed only archive integrity, safe-member, indexed-file and redacted evidence review. It did not load a model, run
GMTP, use a GPU, contact RTX5090 or enter S6.1-P1. The raw Worker archive remains outside Git.

## 2. Archive integrity

| Evidence | Verified result |
| --- | --- |
| Archive | `s6_1_r0_fu1_w2_evidence_20260801.tar.gz` |
| Sidecar / recomputed SHA-256 | both `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f` |
| Safe members | `18/18`；one directory and 17 regular files；no absolute/traversal path, symlink or unsupported member type |
| `evidence_index.sha256` | `16/16` indexed payload files verified；no unindexed payload file |
| Harness identity | SHA-256 `8411af2042774f1a18eec95e97a14ade088acbc35f09942ae9ffea4e8ea5fc06` verified |
| Secret/raw-input boundary | no credential-shaped value；no raw NQ artifact or full question/benign/poisoned text member；identity JSON contains hashes and lengths only |

## 3. Evidence-supported facts

- GMTP HEAD is `15b48d150f93711371eb8da22c211cd84a0cf4df`; the empty delimited `git status --short` block supports a clean GMTP tree.
- `src/defenses/method.py` blob is `84e69b3eadeb8adc0ce521501f8b560d6377b489`; source SHA-256 is
  `83531fe0e4933074c0a710f3dc07bb260b5d638d3cd4c8c317a353de135e00f6`.
- Python `3.11.15`, NumPy `1.26.4`, Torch `2.13.0+cu130`, CUDA runtime `13.0`, Transformers `4.47.1`, CUDA available,
  RTX 5090 and capability `[12, 0]` match the frozen environment evidence.
- The fixed NQ artifact SHA-256/size, record index `0`, `query_id=test0`, and question/benign/poisoned lengths and SHA-256 values
  match the frozen W2 contract.
- Encoder acquisition stopped with `MODEL_DOWNLOAD_BLOCKER`: exact revision absent locally and the Hugging Face request reported
  network unreachable. MLM acquisition is `NOT_ATTEMPTED_AFTER_ENCODER_BLOCKER`.
- `result_redacted.json`, stdout/stderr, run command and resource evidence consistently state `smoke_executed=false`,
  `Smoke execution: NOT_RUN`, no model load, no detector-core score and no runtime/RAM/VRAM result.

These individual facts passed byte-level review, but they are not accepted as a complete reusable preflight evidence set because
the mandatory repository-integrity evidence below is missing.

## 4. Material evidence gaps

1. The archive contains no main LLMGuard repository HEAD evidence. The claimed
   `457458cbc484c7a187c1b0b812c414280f4b837a` does not occur in any indexed payload.
2. The archive contains no delimited main-repository `git status --short` output or equivalent clean-tree evidence.
3. `resource_measurement.txt` says `Disk/resource smoke limits: NOT_EVALUATED`; therefore the reported approximately 5.2 GB
   `gmtp-compat` footprint is not evidenced by this archive.
4. `finalize_blocker.sh` prints main-repository status and HEAD only after creating the archive. That terminal output is not an
   archive member and cannot be reconstructed from the script itself.

Because the Worker summary asserts main-repository HEAD/clean success but the submitted archive does not carry that evidence,
the summary is not fully supported. Chat text or the presence of a command in a script cannot substitute for captured output.

## 5. Classification and stop

- `S6.1-R0-FU1-W2-ATTEMPT1 = EVIDENCE_REVIEW_BLOCKED`.
- Blocker: `W2_ATTEMPT1_EVIDENCE_BLOCKER`.
- Do not classify Attempt 1 as `VALID_BLOCKED_ENGINEERING_RUN`, `FAILED_ALGORITHM`, `GMTP_INCOMPATIBLE`, `W2_ACCEPTED` or
  `W2_COMPLETED`.
- Do not promote the partial checks to `REUSABLE_W2_PREFLIGHT_EVIDENCE` until corrected evidence binds the main repository
  HEAD/clean state and the claimed environment disk measurement.
- W2-H1 owner approval and the corrected future 10 GiB task-owned ceiling are preserved as governance decisions, but offline
  artifact preparation is `NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER` in this review.
- No model download or offline bundle was performed. `S6.1-P1 = NOT STARTED`; `FORMAL_EXPERIMENT = NOT STARTED`.

Required correction is additive: return a small corrected evidence archive/index containing captured main-repository HEAD and
delimited clean status plus an explicit byte-count measurement for `gmtp-compat`. Do not rerun GMTP, download models or rebuild the
environment merely to correct this evidence gap.

## 6. Correction 01 review

The submitted correction archive was reviewed on LOCAL without contacting the Worker or starting H1:

| Evidence | Result |
| --- | --- |
| Archive SHA-256 | sidecar, recomputation and Worker-reported value all equal `d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e` |
| Safe members | `6/6`；one directory and five regular files；no absolute/traversal path, symlink, hardlink, unsafe type or large member |
| Correction index | `4/4` for `original_attempt_reference.txt`, `main_repo_integrity.txt`, `gmtp_compat_disk_measurement.txt` and `correction_manifest.json` |
| Original binding | exact task ID, original archive SHA, `MODEL_DOWNLOAD_BLOCKER` and `smoke_executed=false` passed |
| Main repository | branch, Attempt 1 HEAD `457458cbc484c7a187c1b0b812c414280f4b837a`, upstream `0/0`, delimited empty porcelain status, staged/unstaged diff exits and baseline peeled tag passed |
| Disk fields | apparent `5399301224`, allocated `5492817920`, file count `33556`, directory count `3194` and ceiling `6442450944` match the manifest；both byte totals are below the ceiling |

Correction 01 does **not** capture either concrete `du` command or the flags/raw outputs that distinguish apparent bytes from
allocated bytes. `MEASUREMENT_TOOL=du` is a tool label, not command-derived provenance. The review therefore cannot verify that
the two fields were not confused, even though the values are internally consistent and under the ceiling.

Fail-closed result:

- `W2_ATTEMPT1_EVIDENCE_BLOCKER` remains open;
- Attempt 1 remains `EVIDENCE_REVIEW_BLOCKED`, not `VALID_BLOCKED_ENGINEERING_RUN`;
- no evidence is promoted to `REUSABLE_W2_PREFLIGHT_EVIDENCE`;
- H1 remains `APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS / NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER`;
- no model download, model load, bundle, GMTP, GPU, Worker contact, P1 or formal experiment occurred.

The next correction needs only the exact apparent-size and allocated-size `du` command lines with their captured outputs and an
updated index/manifest binding. It does not require a GMTP rerun, environment rebuild or model download. The temporary extracted
review copy was deleted after review；the original private correction archive remains outside Git.

## 7. Correction 02 final review and superseding closure

This section is the additive superseding result for the historical fail-closed sections above. LOCAL reviewed the private
Correction 02 archive without executing GMTP, loading models, using a GPU or contacting RTX5090.

| Evidence | Verified result |
| --- | --- |
| Archive | `s6_1_r0_fu1_w2_attempt1_correction02_20260801.tar.gz`；4367 bytes |
| Archive identity | sidecar, recomputation and Worker report all equal `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622` |
| Archive safety | one root directory, 17 indexed payload files and one index；no absolute/traversal path, symlink, hardlink, device, unexpected member or unexpected large file |
| Evidence index | sorted `17/17` payload hashes passed；no missing or unindexed payload；the index does not self-index |
| Attempt binding | original SHA `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`；Correction 01 SHA `d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e`；approval commit `b185b8fca74c68ef75a6150b62551f84759c0304`；exact task ID and `EVIDENCE_PACKAGING_CORRECTION_ONLY` |
| GNU provenance | GNU coreutils `du 9.4`；`command -V du` = `/usr/bin/du`；`type -a du` = `/usr/bin/du`, `/bin/du` |
| Apparent measurement | exact command `LC_ALL=C du -sb -- "$CONDA_PREFIX"`；raw value `5399301224`；exit `0`；explicit apparent-size semantics and complete UTC/raw-stream capture |
| Allocated measurement | exact command `LC_ALL=C du -sB1 -- "$CONDA_PREFIX"`；raw value `5492817920`；exit `0`；explicit allocated-block semantics and complete UTC/raw-stream capture |
| Resource and counts | both byte values below `6442450944`；Correction 01 deltas are zero；files `33556`；directories `3194` |
| Mutation boundary | pre/post explicit-spec SHA both `62981f4747156189f7870958da8ea7bc2fc0ead49c78bb6463e9fd284bb65961`；main HEAD `b185b8fca74c68ef75a6150b62551f84759c0304` and GMTP HEAD `15b48d150f93711371eb8da22c211cd84a0cf4df` clean；no install/uninstall/download/load/smoke/GPU/repository mutation |
| Materiality | `11/11 PASS`；formatting/repeated-field preferences are non-material and all identity, truth, reproducibility, safety and resource facts pass |

The manifest's non-repeated `final_status`, formatting of a summarized command string and inactive flag in `conda env list --json`
do not contradict the indexed raw command, registered path, environment variables, exact disk measurements or no-execution
boundary. Under the frozen `MATERIALITY_AND_FINAL_CLOSURE_RULE`, these are derivable or non-material packaging details and cannot
create another evidence blocker.

Final closure:

- `W2_ATTEMPT1_EVIDENCE_BLOCKER = RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW`;
- `S6.1-R0-FU1-W2-ATTEMPT1 = VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`;
- `smoke_executed=false`, `algorithm_failure=false`, `GMTP_incompatibility=not established`;
- `REUSABLE_W2_PREFLIGHT_EVIDENCE` is accepted only for main-repository identity, GMTP source/commit, fixed input identity,
  Python/Torch/CUDA/Transformers/NumPy environment, RTX5090 CUDA availability, `gmtp-compat` identity/disk measurement, encoder
  download blocker and the fact that smoke was not executed;
- model loading, detector output/scores, runtime/RSS/VRAM, compatibility and security effectiveness remain unobserved and are not
  reusable evidence;
- parent W2 remains `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`；S6.1-P1 and Formal Experiment remain not started.

## 8. H1 offline artifact result

After the passing closure, LOCAL used the existing owner approval to run only `huggingface_hub.snapshot_download` in the isolated
`w2-h1-download` environment with `token=False`, `max_workers=1` and frozen revisions. Cross-framework download artifacts and
local cache metadata were excluded. No model class or weight loader was invoked.

| Role | Exact identity | Files | Bytes |
| --- | --- | ---: | ---: |
| Encoder | `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` | 8 | 438708922 |
| MLM | `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594` | 9 | 881643453 |
| Total model artifacts | exact snapshots above | 17 | 1320352375 |

The sorted index covers all 17 model files plus `model_manifest.json` and `README.txt` (`19/19`) and excludes itself, download
script/log/environment, caches and credentials. The bundle contains 20 regular files plus three directories, has source bytes
`1320359518`, compressed size `1222137698`, and SHA-256
`aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`. Sidecar, member safety and archived-file hash
reverification pass. Raw models, logs, manifest, archive and sidecar remain Git-external.

H1 status is `OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`. This is transfer preparation, not Worker verification,
model loading, GMTP compatibility, W2 completion/acceptance, a security result or a formal experiment.
