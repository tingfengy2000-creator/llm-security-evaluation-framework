# Artifact claim matrix

Measured ASR and accuracy are `NOT_MEASURED` for every row.

| Unit | Dataset | Model | Attack | Script | Expected file | Paper map | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| claim1 | NQ, HotpotQA, MS MARCO | Contriever/DPR/ANCE in expected file; LLaMA-7B; Vicuna-7B | PoisonedRAG | `claims/claim1_poisonedrag/run.sh` | `5124ea6f5c01e3a163f60ae57aabed42e113eb8eaaf7c18f7133a21220005864` | REPORTED Figure 4 open-model rows | NOT_RUN / BLOCKED |
| claim2 | same three datasets; expected file is Contriever at 100% only | LLaMA-7B; Vicuna-7B | Tan et al. | `claims/claim2_tan/run.sh` | `56433fd30ad76f5e56fdcb46c2fd3e55fa568175757c29da26e76731c8645b94` | REPORTED Figure 4 | NOT_RUN / BLOCKED |
| claim3 | same as claim2 expected shape | LLaMA-7B; Vicuna-7B | GARAG | `claims/claim3_garag/run.sh` | `7cb98b139bab9ba0fa2c9aff8a48aad76a443b045521d6fe25c0770dbd409a8d` | REPORTED Figure 4 | NOT_RUN / BLOCKED |
| GPT-4o / Gemini rows | paper figures | commercial APIs | several | not shipped as runnable configs | none | REPORTED not automated | OUT_OF_SCOPE |
| 13B rows | paper Figure 5 | LLaMA-13B / Vicuna-13B | PoisonedRAG | configs not shipped | none | REPORTED not automated | NOT_AUTOMATED |
| Table 4 other RAG stacks | paper | external repos | n/a | no glue shipped | none | REPORTED | NOT_AUTOMATED |

Claim 2 and claim 3 expected numeric rows are identical. That is an upstream file fact, not a measured result.
