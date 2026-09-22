# Formal240 neutral query contract V1

Status: `FROZEN_DESIGN_ONLY / QUERY_TEXT_NOT_AUTHORED`. Every future group has exactly one neutral information need and one query ID/text, shared unchanged by Clean Current, Poison and Hard Negative. Construct from the information need, not from the candidate role or expected answer. No class-dependent date, institution, “false”, “poison”, version or target-S token. Predeclare query quality checks for answer leakage, ambiguity, realistic wording and lexical-style balance.

Before Oracle/GT loading, freeze unified corpus membership, query bytes/hash, candidate-to-query mapping, retriever config and full ranked traces. Audit that no candidate label, HKP, S, Owner/Expected decision, manual E1/E2 identity, group-ID encoding or split assignment enters query construction or ranking. Query identity is control-plane only; future retrieval outputs must retain query ID/config/hash but not expose labels as inference inputs.
