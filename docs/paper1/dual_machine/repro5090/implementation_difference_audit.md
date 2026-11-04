# Implementation difference audit

| Comparison | Status | Result |
| --- | --- | --- |
| Local clone versus upstream HEAD | VERIFIED | empty diff |
| `main` versus tag `v0.2.0` commit | VERIFIED | only `.github/workflows/codeql.yml` |
| Research repo versus upstream package | VERIFIED | research `src/` does not contain RAGDefender |
| `ragdefender/` package versus `artifacts/` | VERIFIED | artifact scripts do not import the package. `artifacts/main.py` defines `find_num_adv` itself. CLI `reproduce` delegates to `run.sh` |
| v0.2.0 Stage 2 behavior | REPORTED | author changelog says the package fixed which indices Stage 2 drops. This audit did not execute either implementation |
| 8-bit flags | VERIFIED | `Llama.py` hardcodes `load_in_8bit=True`. Vicuna JSON says `load_8bit` false. `run.sh` comments say 8-bit. No file was edited |
| Paper equation versus code | REPORTED | author `docs/reproducing-paper.md` says expected numbers follow the legacy implementation |

No semantic patch was applied. No before-fix or after-fix experiment exists.
