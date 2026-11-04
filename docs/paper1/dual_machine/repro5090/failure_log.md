# Failure log

No claim command failed, because no claim command was started.

| id | status | what happened |
| --- | --- | --- |
| ENV-CONDA-PATH | VERIFIED | `conda` is not on PATH. A conda 26.1.1 binary exists off PATH |
| ENV-ARTIFACT-ABSENT | VERIFIED | `conda env list` has no `artifact_acsac` |
| ENV-LOCKFILE-OS | BLOCKED | `artifacts/env.yml` pins linux-64 packages. Native Windows create was not attempted |
| WEIGHT-LICENSE | BLOCKED | Llama and Vicuna configs were read. Weights were not downloaded. Llama key field is a placeholder |
| GOVERNANCE-SCOPE | BLOCKED | repository approval at `4dc9161` covers the L0 Oracle review, not these three artifact claims |
| CLAIM2-CLAIM3-EXPECTED | REPORTED | expected numeric rows match. Left unchanged |

No retry loop. No simulated data. No paid API.
