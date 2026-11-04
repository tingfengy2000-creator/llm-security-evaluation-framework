# Failure log

No claim command failed, because no claim command was started. The R0 rows are the audit snapshot. Later rows are the environment install.

| id | status | what happened |
| --- | --- | --- |
| ENV-CONDA-PATH | VERIFIED | `conda` is not on PATH. A conda 26.1.1 binary exists off PATH |
| ENV-ARTIFACT-ABSENT | VERIFIED | `conda env list` has no `artifact_acsac` |
| ENV-LOCKFILE-OS | BLOCKED | `artifacts/env.yml` pins linux-64 packages. Native Windows create was not attempted |
| WEIGHT-LICENSE | BLOCKED | Llama and Vicuna configs were read. Weights were not downloaded. Llama key field is a placeholder |
| GOVERNANCE-SCOPE | BLOCKED | repository approval at `4dc9161` covers the L0 Oracle review, not these three artifact claims |
| CLAIM2-CLAIM3-EXPECTED | REPORTED | expected numeric rows match. Left unchanged |
| ENV-STRICT-CHANNEL | VERIFIED | first `conda env create` failed because strict priority excluded defaults build strings. Isolated CONDARC retry succeeded. User condarc was not edited |
| ENV-TORCH-SM120 | VERIFIED | official torch 2.4.0+cu121 sees the RTX 5090 and raises no kernel image. Official env was not upgraded |
| ENV-CUBLAS-HASH | VERIFIED | one cu128 dependency download failed sha256. The bad file was discarded. The installed wheel matches the published hash |
| ENV-BNB-043 | VERIFIED | bitsandbytes 0.43.1 has no CUDA 12.8 library and does not import against triton 3.4. Compat env uses 0.45.5. Official env still has 0.43.1 |
| ENV-XFORMERS | REPORTED | xformers 0.0.27.post2 does not load CUDA extensions on torch 2.8. Left installed. Artifact code does not import it |
| SMOKE-PYTEST-ABSENT | VERIFIED | `artifact_acsac_compat` has no pytest. The invocation exited 1 with `No module named pytest`. pytest was not installed |
| SMOKE-RUNNER-IMPORT | VERIFIED | The first direct runner imported a truncated name `Evaluato` and failed that one assertion. The library was not edited. A second import printed `Evaluator` and version 0.2.0 |
| PLAN-TAN-LOG-DIR | VERIFIED | `run_tan.py` creates `logs/main_tan_<seed>` but writes and `eval.py` reads `logs/main_logs_tan_<seed>`. Source was not patched |
| PLAN-TABLE7-FLAGS | VERIFIED | `reproducing-paper.md` tells the user to pass `--p` and `--m` to `main_abl.py`. That argparse does not define either flag |

No claim retry. No simulated paper data. No paid API. No model download.
