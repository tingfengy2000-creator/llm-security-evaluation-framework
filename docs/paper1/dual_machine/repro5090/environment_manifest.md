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
