# Claim 1 run report

- claim_id: `claim1_poisonedrag`
- status: `NOT_RUN` / `BLOCKED`
- entry: `claims/claim1_poisonedrag/run.sh` and `ragdefender reproduce claim1`
- run.sh SHA-256: `f1d42d574b1c522ef4546494373ae6dd33d1d04f1d97fd9e913a8d20f93dddb1`
- expected SHA-256: `5124ea6f5c01e3a163f60ae57aabed42e113eb8eaaf7c18f7133a21220005864`
- sample_n: `UNKNOWN`
- undefended ASR: `NOT_MEASURED`
- RAGDefender ASR: `NOT_MEASURED`
- QA accuracy: `NOT_MEASURED`
- reason: `artifact_acsac` does not exist and generator weights were not verified. The author expected file was hashed only.
