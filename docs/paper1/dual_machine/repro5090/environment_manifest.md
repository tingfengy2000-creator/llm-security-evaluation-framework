# Environment manifest

run_id: `W1-5090-R0-20261104`

| Item | Status | Value |
| --- | --- | --- |
| OS | VERIFIED | Windows 11 Pro 10.0.26200 |
| GPU | VERIFIED | RTX 5090, driver 610.88, CUDA UMD 13.3, 32607 MiB |
| Disk free | VERIFIED | C 98.7 GB, D 742.8 GB, E 748.2 GB at 2026-11-04 16:01 UTC+8 |
| conda on PATH | VERIFIED | absent |
| conda binary | VERIFIED | 26.1.1 in an Anaconda prefix on drive E |
| conda envs | VERIFIED | `base`, `pose_openmmlab`; `artifact_acsac` absent |
| author env.yml | VERIFIED | linux-64, Python 3.10.14, torch 2.4.0, transformers 4.41.2, bitsandbytes 0.43.1 |
| Windows native create | BLOCKED | lockfile is linux-64 |
| WSL Ubuntu-24.04 | REPORTED | installed, Stopped. Not booted this audit |
| prior L0 venv | VERIFIED | torch 2.8.0+cu128 sees RTX 5090 capability (12, 0). Not the author env |
| workspace .venv torch | VERIFIED | not installed |
| author env created | NOT_RUN | no install, no compatibility patch |

## Install — 2026-11-04 20:01 UTC+8

The R0 table above is the audit snapshot. This section is the later install.

| Item | Status | Value |
| --- | --- | --- |
| official env | VERIFIED | WSL Ubuntu 24.04, Miniforge, env `artifact_acsac`, Python 3.10.14, created from `artifacts/env.yml` |
| first create | BLOCKED | strict channel priority rejected the defaults build strings in the lockfile. User condarc was not edited |
| retry | VERIFIED | one isolated CONDARC, conda-forge plus defaults, flexible priority. Create EXIT 0 at 17:49 UTC+8 |
| official pins | VERIFIED | torch 2.4.0+cu121, transformers 4.41.2, bitsandbytes 0.43.1, triton 3.0.0, xformers 0.0.27.post2, faiss-gpu 1.7.2, faiss-cpu 1.8.0.post1, sentence-transformers 3.0.1, sympy 1.12 |
| official CUDA kernel | BLOCKED | RTX 5090 capability (12, 0) is visible. `torch.ones` raises no kernel image. That build lists sm_50 through sm_90. Env left at torch 2.4.0 |
| faiss import | VERIFIED | both wheels are installed. `import faiss` resolves to faiss-cpu 1.8.0. CPU `IndexFlatIP` works. `StandardGpuResources` is absent |
| compat env | VERIFIED | separate env `artifact_acsac_compat`. Not the author env |
| compat torch | VERIFIED | torch 2.8.0+cu128, CUDA 12.8. One-element CUDA sum is 1.0 on RTX 5090. Wheel sha256 `0c96999d15cf1f13dd7c913e0b21a9a355538e6cfc10861a17158320292f5954` |
| compat stack changes | VERIFIED | triton 3.4.0, sympy 1.14.0, bitsandbytes 0.45.5. Required for the cu128 torch and a working 8-bit linear. Official env still has 0.43.1 |
| 8-bit check | VERIFIED | `Linear8bitLt` forward on CUDA returned a finite value in the compat env only |
| xformers | REPORTED | 0.0.27.post2 stays installed. Its CUDA extension does not load on torch 2.8. Artifact Python files do not import it |
| package | VERIFIED | `ragdefender` 0.2.0 editable install in the compat env. Import succeeds. Official env does not have the package |
| weights | BLOCKED | Llama-2-7B-chat and Vicuna-7B were not downloaded |
| claims | NOT_RUN | no claim command, no ASR, no accuracy |
| compat env acceptance | VERIFIED | PODR-154 conditionally accepts `artifact_acsac_compat` for later reproduction and keeps the official kernel failure |
