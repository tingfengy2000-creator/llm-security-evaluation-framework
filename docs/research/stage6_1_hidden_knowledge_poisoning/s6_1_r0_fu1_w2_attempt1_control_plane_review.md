# S6.1-R0-FU1-W2 Attempt 1 Control Plane Evidence Review

> Review machine: `LOCAL / CONTROL_PLANE`
> Worker task: `S6.1-R0-FU1-W2 / GMTP Detection-Only Minimal Smoke`
> Review status: `W2_ATTEMPT1_EVIDENCE_BLOCKER`
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
