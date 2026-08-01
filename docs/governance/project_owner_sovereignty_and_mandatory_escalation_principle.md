# Project Owner Sovereignty, Mandatory Human Escalation, and Physical Context Preservation Principle

## 1. Identity and status

| Field | Value |
| --- | --- |
| Principle ID | `PO-MHEP` |
| Chinese name | 项目负责人主权、强制人工升级与物理上下文保全原则 |
| English name | Project Owner Sovereignty, Mandatory Human Escalation, and Physical Context Preservation Principle |
| Status | `HUMAN_ACCEPTED` |
| Authority | `HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY` |
| Scope | entire LLMGuard Research Framework；Stage 1–7 and future stages；LOCAL/CONTROL_PLANE；RTX5090/COMPUTE_WORKER；all agents and automation；all current/future research branches |
| Permanent | `YES` |
| Auto expiry | `NO` |
| Owner decision | `PODR-056` |

This is the highest internal rule governing whether project execution may continue after facts are discovered. It applies to
research design, engineering, experiments, papers, data, environments, models, APIs, governance and handoff.

## 2. Authority hierarchy and non-override boundary

The hierarchy is:

1. **L0 — Dynamic Git Facts and Immutable Raw Evidence.** Branch, commit, tag, diff, raw artifact, hash, Run Manifest, exact
   source/input/model/config identity and captured execution evidence decide what objectively exists or ran.
2. **L0.5 — PO-MHEP.** The project owner decides whether work may continue after L0 facts are known. PO-MHEP is the highest
   internal project execution authority.
3. **L1 and below — Operational governance and project documents.** `AGENTS.md`, long-term requirements, Owner Decision Register,
   Project Master Context, Current Work State, experiment/execution ledgers, accepted specs, protocols, plans and learning material.

PO-MHEP supersedes conflicting task prompts, implementation plans, accepted specs, Worker contracts, Token Economy rules,
auto-continue defaults, schedule/performance goals and agent-inferred defaults. It does **not** authorize anyone to alter L0 facts,
rewrite immutable history, fabricate results, weaken evidence, bypass safety/law/privacy/license, cancel label isolation or override
the project owner's latest explicit decision.

## 3. Machine roles and decision sovereignty

`LOCAL / CONTROL_PLANE` is:

- `PRIMARY_CONTROL_PLANE`;
- `PROJECT_EXECUTION_LEAD`;
- `RESEARCH_GOVERNANCE_LEAD`;
- `5090_APPROVAL_AUTHORITY`;
- `PAPER_RISK_REVIEWER`;
- `CONTEXT_PRESERVATION_OWNER`.

LOCAL owns project orchestration, stage order, contract freeze, Worker evidence review, research-route consistency, paper risk,
architecture/technical-debt risk, data/model/API/license/resource risk, evidence completeness, physical context preservation and
Git/remote verification.

`RTX5090 / COMPUTE_WORKER` is compute-only. It has `NO_SELF_APPROVAL_AUTHORITY` and may not independently change research
questions, data, models, parameters, metrics, seeds, budgets, resource ceilings, algorithm semantics, compatibility patches,
stage gates, evidence classification, paper comparison boundaries or result acceptance.

## 4. Mandatory escalation state

Discovery of any trigger in section 5 changes the affected work to:

```text
HUMAN_DECISION_REQUIRED
Auto Continue = NO
```

The affected work must stop. The agent must not choose a plausible default, apply a silent workaround, continue the Worker,
resolve the blocker automatically, download/install/mutate/call external services or enter the next task. It may continue only:

- read-only evidence collection;
- non-mutating fact verification;
- decision-focused risk analysis;
- context/evidence preservation;
- Git state verification and governance persistence.

Uncertainty is itself an escalation reason when alternative choices could materially affect research, architecture, resources,
reproducibility, licensing or paper conclusions.

## 5. HUMAN_DECISION_REQUIRED triggers

### A. Accepted-boundary conflict

- conflict with an accepted spec, owner decision, branch policy, claims boundary or fail-closed rule;
- Worker deviation from a frozen contract;
- change to frozen data, model, parameter, metric, seed, Top-K or attack budget;
- history rewrite, approval-gate bypass, safety weakening or unresolved disagreement among canonical current-state documents.

### B. API, service and external dependency

- any real API/model service, API key, token, login, paid service or project-data transfer;
- provider/model/API version change affecting reproducibility;
- unapproved mirror, proxy or third-party download source;
- network behavior that leaves artifact identity uncertain.

### C. Human cost, resource and irreversible operation

- system-level installation, administrator privilege, driver/CUDA/WSL/Docker/system-environment change;
- large model/data/index download or budget exceedance in disk/RAM/VRAM/time/cost;
- deletion, overwrite, migration, irreversible mutation, reusable-environment pollution or credible data-loss risk.

### D. Architecture and engineering risk

- a shortcut likely to force later Stage redesign or block Paper 2, Agent Security or education-project extension;
- unclear boundaries, cycles, hard coupling, non-replaceable implementation or unreasonable compatibility/history edits;
- label/evaluator/Ground Truth leakage, mock evidence likely to be overclaimed, algorithm-semantic patch, machine-bound design or
  insufficient logs/cache/manifest for reconstruction.

### E. Paper and research risk

- weak novelty/scientific gap, unfair or incomplete baselines, protocol misalignment or strict/transfer comparison confusion;
- engineering evidence being promoted to paper evidence, single-run statistical claims or missing seed/CI/significance/effect size;
- inadequate hard negatives, legitimate updates, version cases, exception samples or external-benchmark validation;
- released-artifact reuse being described as reproduction, unisolated contribution, reviewer-visible confounder, likely late
  dataset/experiment rebuild, license/redistribution risk or Published/Reproduced/Our Result confusion.

### F. Evidence and governance risk

- missing commands, flags, stdout/stderr or exit code；summary without raw evidence；estimate without measurement;
- unbound hash/commit/revision/path/sample identity, inconsistent HEAD/worktree/Run Manifest, incomplete index or unsafe archive;
- result not traceable to exact source/input/model, raw-summary conflict, fact/inference ambiguity, unsupported conclusion or state
  that cannot be recovered from Git plus private evidence.

### G. Material choice or uncertainty

- two or more options materially affecting paper, architecture, resource, reproducibility or later stages;
- low-confidence judgment, rigor-versus-speed tradeoff, original-paper-versus-modern-environment tradeoff, released-artifact-versus-
  regeneration decision, internal-use-versus-redistribution choice or any decision with broad downstream impact.

## 6. Mandatory human feedback contract

Every escalation must provide a decision-ready record with exactly these semantic fields:

1. Issue ID;
2. issue name;
3. discovery stage/task;
4. current facts separated into `OBSERVED_FACT`, `SOURCE_DERIVED_FACT`, `INFERENCE` and `UNKNOWN`;
5. affected existing constraints;
6. why the issue must be handled now;
7. downstream risks across engineering, architecture, experiment, paper, reproducibility, time/resource and safety/license;
8. options, each with action, advantages, disadvantages, cost, risk, later-Stage impact, paper impact and reversibility;
9. LOCAL recommendation;
10. rationale and confidence;
11. explicit questions requiring owner decision;
12. allowed and prohibited work before that decision.

A message such as “manual handling required” is not sufficient.

## 7. Forward risk and paper risk review

Before each stage, spec, Worker contract and experiment, LOCAL performs `FORWARD_RISK_REVIEW` for future redesign, Paper 1/Paper 2/
Agent Security/education-project extensibility, baseline fairness, dataset/metric reuse, label leakage, train-test contamination,
version traceability, reproducibility, claims wording, reviewer attack surface and cheaper early mitigation. A foreseeable material
risk is reported before execution.

`PAPER_RISK_REVIEW` is mandatory at research-route, baseline, dataset, attack-taxonomy, detector, metric and formal-protocol freeze;
first formal run；ablation；generalization；conclusion drafting；SOTA comparison；and pre-submission. It covers novelty, gap,
fairness, validity, hard negatives, confounders, reproducibility, statistics/effect size, claims, artifact availability, reviewer
attack surface, licensing and contribution coherence.

## 8. RTX5090 approval chain

Every Worker task requires, in order:

1. research necessity;
2. input identity freeze;
3. source commit/blob freeze;
4. model ID/revision freeze;
5. parameter freeze;
6. environment freeze;
7. resource ceilings;
8. stop conditions;
9. claims boundary;
10. project-owner approval;
11. LOCAL governance commit and push;
12. Worker pull of the exact approval commit;
13. Worker execution;
14. LOCAL raw-evidence review;
15. project-owner final acceptance.

Any new dependency, patch, input/model/network substitution, resource exceedance, algorithm anomaly, environment deviation,
evidence gap, unfrozen parameter or manual-install need requires:

```text
STOP
RETURN_TO_CONTROL_PLANE
```

## 9. Physical context preservation

Project context must not exist only in chat, temporary memory, an IDE/session, terminal history or a one-time prompt. Even if all
chat is lost, Git repository + private evidence archive + hash/index + Current Work State must recover goals, stage/task, approvals,
completed evidence, evidence location, blockers, next gate, claims boundary, machine roles, decisions and their rationale.

Every task ending in `PASS`, `FAIL`, `BLOCKED`, `RETURNED`, `CANCELLED`, `SUPERSEDED` or `NOT STARTED` persists:

1. Task ID and Task Name;
2. Task Type;
3. execution machine and role;
4. approval/status classification;
5. exact branch, HEAD and upstream;
6. exact source commit/blob and model revision;
7. input identity and hash;
8. environment identity;
9. actual execution commands;
10. parameters and resource contract;
11. output/result;
12. test/validation result;
13. failure or blocker;
14. private evidence archive, SHA-256 and evidence index;
15. claims boundary;
16. allowed and prohibited claims;
17. paper impact;
18. later-architecture impact;
19. next approval gate;
20. human decision;
21. Git commit and remote synchronization.

## 10. Canonical and private-evidence rules

Canonical responsibilities remain singular:

- `AGENTS.md`: repository entry, startup/escalation/completion obligations;
- `context_authority_map.md`: L0/L0.5/L1-and-below hierarchy and conflicts;
- this PO-MHEP file: one permanent highest execution principle;
- `long_term_research_requirements.md`: durable research and governance requirements;
- `current_work_state.md`: only dynamic task-state entry;
- `research_execution_log.md`: append-only chronology;
- Owner Decision Register: all owner decisions;
- Experiment Master Record: experiments, engineering validations, invalid/failed runs and evidence indexes;
- Project Master Context: global architecture/history/claim boundary;
- current Stage/Paper canonical document and task review/completion record: task-specific contract/evidence.

History is superseded additively, never overwritten. Important context must be navigable by valid relative links.

Raw logs, models, datasets, full inputs/attack text, API responses, large archives, external repositories and credentials remain in
Git-external private evidence. Git records only safe abstractions: evidence type, archive filename/SHA/index/time, task/run and
claims boundary. Public Git must not contain usernames, user-absolute paths, tokens, keys, cookies or full sensitive content.

## 11. Startup and completion protocols

Every LOCAL session/task starts with:

1. read `AGENTS.md`;
2. read the Authority Map;
3. read PO-MHEP;
4. read Current Work State;
5. read Project Master Context;
6. read the latest relevant Owner Decision;
7. read the Experiment Master Record and relevant append-only execution entries;
8. read the current Stage canonical document and applicable protocol/spec;
9. verify Git branch, HEAD, status, tag and upstream;
10. check canonical context conflicts;
11. verify that the exact current task is approved;
12. evaluate `HUMAN_DECISION_REQUIRED` triggers.

Unrecoverable context produces `CONTEXT_RECOVERY_BLOCKER` and STOP. Chat memory cannot fill missing facts.

Before completion, `CONTEXT_PERSISTENCE_CHECK` must answer the unique task/status, approved/unapproved work, blocker, decision
owner, allowed/prohibited claims, Formal Experiment status, Git sync, private evidence hash/index and whether a new session can
recover from the repository. If any answer is unavailable, completion cannot be claimed.

The minimum explicit completion checklist is:

1. What is the unique current task?
2. What is its current status?
3. What work is approved?
4. What work is unapproved/prohibited?
5. What blocker remains?
6. Who decides the next step?
7. What may and may not be claimed?
8. Has Formal Experiment started?
9. Is Git synchronized and clean?
10. Does private evidence have a safe archive identity, hash and index when applicable?
11. Can a new session recover the decision and rationale from repository plus private evidence?

Every material plan, approval, execution, review, blocker, owner decision, acceptance or protocol freeze must update canonical
documents, then:

1. run governance and architecture tests;
2. run `git diff --check` and scoped secret/path/protected-history checks;
3. create a semantically accurate commit;
4. push to the active research branch;
5. confirm `HEAD = upstream = remote`;
6. confirm ahead/behind `0/0`;
7. confirm working tree clean;
8. report the commit SHA;
9. stop without auto-starting the next task.

## 12. No progress-based downgrade

Prior effort, smoke scope, “run first”, probability, Worker cost, time pressure, later documentation, default parameters, a small
evidence gap, model executability or agent confidence never override escalation, evidence, persistence, paper rigor, approval gates
or reproducibility. Token Economy may reduce waste only after these requirements remain satisfied.

## 13. Preserved Stage 6.1 registration-time snapshot

Registration of PO-MHEP does not change execution state:

- P0/L1: `HUMAN_ACCEPTED`;
- W2: `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`;
- Attempt 1: `EVIDENCE_REVIEW_BLOCKED`;
- `W2_ATTEMPT1_EVIDENCE_BLOCKER = OPEN`;
- Correction 01: archive/index/original binding/main repository passed；exact apparent/allocated `du` command provenance incomplete;
- H1: `APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS / NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER`;
- S6.1-P1 and `FORMAL_EXPERIMENT`: `NOT STARTED`.

At PO-MHEP registration time, the only next candidate was an unapproved, unsent, unexecuted Correction 02 evidence-only Worker
contract. That approval-state snapshot is preserved as history. `PODR-057` subsequently supersedes only the approval field to
`APPROVED_TO_START / NOT SENT / NOT EXECUTED`; the canonical approved contract is recorded in the
[FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md). PO-MHEP itself and all
W2/H1/P1/Formal Experiment execution boundaries remain unchanged.
