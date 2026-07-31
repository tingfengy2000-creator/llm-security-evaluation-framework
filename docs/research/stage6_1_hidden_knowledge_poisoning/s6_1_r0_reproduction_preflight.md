# S6.1-R0 Paper 1 Reproduction Environment and Baseline Feasibility Validation

## Governance Identity

- Task ID: `S6.1-R0`
- Task Name: `Paper 1 Reproduction Environment and Baseline Feasibility Validation`
- 中文名称：`Paper 1 外部基准复现环境与可行性验证`
- Task Type: `ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT`
- Status: `APPROVED_TO_START`
- Superseded snapshot: `DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL`
- Execution machine: `RTX5090 / COMPUTE_WORKER`
- Bootstrap task: `S6.1-R0-B0 RTX5090 Compute Worker Bootstrap Validation`
- Bootstrap status: `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`
- Formal experiment: `FORMAL_EXPERIMENT = NOT STARTED`
- Auto Continue = NO

项目负责人已批准 R0 在 RTX5090 Compute Worker 按本文顺序执行。该授权不允许 LOCAL Control Plane 运行 external
baseline，也不允许付费 API、全量大型数据/模型、正式实验或 S6.1-P1。R0 只产生 engineering feasibility evidence。

## Accepted RTX5090 Bootstrap Snapshot

以下是项目负责人依据 RTX5090 实机证据接受的 `S6.1-R0-B0` 快照；本机 Control Plane 本轮不重新执行这些命令。

| Field | Accepted worker evidence |
| --- | --- |
| Machine ID / Role | `RTX5090 / COMPUTE_WORKER` |
| Status | `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY` |
| Host OS | Windows 11 Pro 25H2, Build 26200 |
| CPU | Intel Core i9-14900；24 physical cores；32 logical processors |
| RAM | approximately 64 GiB |
| Primary research SSD | ADATA SX8200PNP NVMe, approximately 2 TB |
| Research WSL storage | E drive |
| GPU | NVIDIA GeForce RTX 5090；PyTorch-reported VRAM 31.84 GB |
| Windows NVIDIA KMD | 610.88 |
| WSL-visible NVIDIA-SMI / WSL KMD | 610.57.01 / 610.88 |
| Driver CUDA UMD capability | 13.3 |
| Linux | WSL2 available；Ubuntu 24.04 LTS；GPU passthrough PASS |
| Toolchain | Git 2.43.0；GCC 13.3.0；CMake 3.28.3；ripgrep 14.1.0 |
| Environment | Miniforge installed；Conda 26.3.2；`llmguard-paper1` Python 3.11 environment |
| PyTorch | PyTorch 2.13.0+cu130；PyTorch CUDA Runtime 13.0 |
| CUDA visibility | `torch.cuda.is_available() = True`；Compute Capability (12, 0)；architecture list includes `sm_120` |
| FP16 | 4096 x 4096 matrix PASS；`RTX5090_GPU_TEST_OK` |
| BF16 | supported；2048 x 2048 matrix PASS；`BF16_TEST_OK` |
| Git sync | branch `research/stage6-1-hidden-poisoning` at `347dc2bfff2256a7ad6c0c6ab8c468e9f3f833d9`；clean；remote same SHA |
| Baseline tag | `s6-t5-rag-baseline-v1` peeled to `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1` |

Driver CUDA UMD capability 13.3 不得写成 `CUDA Toolkit 13.3 installed`。当前没有要求安装 standalone CUDA Toolkit。
Python patch version 必须在 R0-A 动态 fingerprint，不得从设计文档猜测。

PyTorch smoke 出现 `Failed to initialize NumPy: No module named 'numpy'`，分类为
`NON_BLOCKING_ENVIRONMENT_COMPLETENESS_OBSERVATION`。它没有影响 CUDA availability、FP16 或 BF16 test，不能登记为
GPU/CUDA/PyTorch failure。R0-A 可安装 NumPy，但必须记录实际 resolved version，不能为清除 warning 批量安装依赖。

## Position in the Research Sequence

```text
S6.1-LR1 HUMAN_ACCEPTED
  -> S6.1-R0 ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT
  -> S6.1-P1 Formal Experiment Protocol Design Freeze
  -> Dataset / Detector / Formal Experiment
```

本顺序 supersede `LR1 -> P1 -> environment` 的临时规划。R0 只回答外部 baseline 在目标机器上是否具备可复现
条件，不产生论文实验结果，也不冻结 S6.1-P1 的数据、方法或指标协议。

## Objectives

获批的 RTX5090 R0 只能执行以下目标：

1. 建立并记录 RTX 5090 科研环境；
2. 验证 Blackwell / PyTorch / CUDA 基础兼容性；
3. 在独立 external research directory clone PoisonedRAG、GMTP、SafeRAG 官方仓库；
4. 验证每个 external repository commit；
5. 建立 `Original Paper Environment` 与 `RTX5090 Compatibility Environment` 映射；
6. 执行 PoisonedRAG minimal smoke test；
7. 执行 GMTP minimal smoke test；
8. 执行 SafeRAG selected-task minimal smoke test；
9. 记录 peak VRAM；
10. 记录 peak RAM；
11. 记录 disk before/after；
12. 记录 runtime；
13. 记录 compatibility patches 及其算法影响；
14. 识别 strict reproduction blocker；
15. 明确 R0 does not produce Paper Result。

## External Repository Boundary

第三方仓库必须位于 LLMGuard 主仓库之外的 `external research directory`，统一根目录为
`~/paper1_external/`，例如 `~/paper1_external/PoisonedRAG`、`~/paper1_external/GMTP`、
`~/paper1_external/SafeRAG`。不得 clone 到 LLMGuard repository。

允许 LLMGuard 保存：upstream URL、commit、hash、config、compatibility note、command、metric artifact、我们拥有
版权的 wrapper/adapter。禁止 vendor 大段 upstream code、把未知许可证写成 MIT/Apache/GPL，或把第三方修改版冒充
LLMGuard 自有 Artifact。

## License and Artifact Gate

每项 external artifact 必须分开记录：

- `SOURCE_ACCESS`
- `INTERNAL_REPRODUCTION`
- `STRICT_COMPARISON_ELIGIBILITY`
- `REDISTRIBUTION_ELIGIBILITY`
- `CODE_LICENSE`
- `DATASET_LICENSE`

公开仓库不等于拥有不受限再分发许可；缺少根 LICENSE 也不自动阻断项目负责人未来批准的内部研究 clone/inspect/
install/execute/evaluate。若 upstream 有明确条款，必须遵守。代码和数据许可证始终分别治理。

## Required Evidence

- worker branch、HEAD、clean-tree attestation；
- upstream URL 与 exact commit；
- Original/Compatibility environment fingerprints；
- dependency lock/config hash；
- compatibility patch inventory；
- exit code、redacted log hash；
- peak VRAM/RAM、disk、runtime；
- smoke status 与 strict-reproduction blocker；
- claims supported / claims prohibited。

## R0 Execution Order

RTX5090 必须严格串行执行，不得把三个仓库一次性装入同一个 Python 环境：

1. `R0-A` — Environment Fingerprint；
2. `R0-B` — PoisonedRAG Static Audit；
3. `R0-C` — PoisonedRAG Minimal Smoke Test；
4. `R0-D` — GMTP Static Audit；
5. `R0-E` — GMTP Minimal Smoke Test；
6. `R0-F` — SafeRAG Static Audit；
7. `R0-G` — SafeRAG Selected-Task Minimal Smoke Test；
8. `R0-H` — Reproduction Feasibility Matrix；
9. `R0-I` — Control Plane Review。

发现路线级问题时输出 `RESEARCH_ROUTE_REVIEW_REQUIRED`，由 LOCAL Control Plane 决策；Worker 不自行改变
PoisonedRAG/GMTP/SafeRAG/EcoSafeRAG 的既定角色。

## Environment Isolation

- `llmguard-paper1` 保持为 LLMGuard 主研究环境；
- external baseline 原则上分别使用 `poisonedrag-compat`、`gmtp-compat`、`saferag-compat`；
- 先 static audit，再决定 Python、PyTorch、Transformers、FAISS、Pyserini、Java 和其他依赖版本；
- 不得在 Control Plane 文档中猜测最终版本。

每项 baseline 分别记录 `ORIGINAL_PAPER_ENV` 与 `RTX5090_COMPAT_ENV`。任何差异创建
`COMPATIBILITY_PATCH RECORD`，至少包含 dependency、original/replacement version、reason、code changes、algorithmic
impact、expected result impact 和 validation evidence。不得为“能跑”静默改变算法。

## R0 Data and Model Policy

允许为 minimal smoke 下载必要的最小公开 artifact/sample，优先 repo-provided sample、small fixture 或 small subset。
当前不允许直接下载 full Natural Questions、full HotpotQA、full MS MARCO 或 production-sized indexes。如果最小路径
不能脱离公开数据，先报告 `MINIMUM_DATA_REQUIREMENT`，由 Control Plane 决定。

允许 smoke 必需的小型公开模型。大型模型下载前必须记录 model ID、revision、size、license/usage terms、disk 与
expected VRAM。禁止付费 API、API key 和未经批准的大型 LLM 全量下载。如果路径强制依赖 OpenAI、DeepSeek 或其他
付费 API，停止并登记 `EXTERNAL_API_REQUIRED`；寻找论文允许的 local alternative，但不得自行改变核心定义。

## Resource Measurement

每个 smoke 至少记录 wall-clock runtime、peak GPU VRAM、system RAM、disk footprint、GPU、PyTorch、CUDA runtime、
Python、environment package snapshot、dataset/sample identity、model revision、Git commit、command 和 status。不得只写
“跑通了”。

## R0 Result Classification

每项 baseline 最终只能分类为：

- `STRICT_REPRODUCTION_READY`
- `COMPATIBILITY_REPRODUCTION_READY`
- `PARTIAL_REPRODUCTION_READY`
- `BLOCKED_BY_EXTERNAL_DEPENDENCY`
- `BLOCKED_BY_HARDWARE`
- `BLOCKED_BY_MISSING_ARTIFACT`
- `BLOCKED_BY_API_DRIFT`
- `NOT_REPRODUCIBLE_WITH_AVAILABLE_EVIDENCE`

不得为了推进论文强制写 `READY`。研究复现与再分发继续分开；第三方源码留在 external directories，不进入 Git。

## Stop Conditions

- Worker 未 pull 包含本次批准记录的最新 Control Plane commit；
- worker identity、HEAD、manifest、config、model/dataset identity 不一致；
- compatibility patch 可能改变算法、预算、Retriever、Top-K 或指标；
- upstream 条款禁止计划动作；
- 资源超出批准预算；
- smoke 结果将被误写为 `Reproduced Result` 或 `Paper Result`。

任何停止条件触发后，只能返回 blocker/evidence 给 LOCAL Control Plane；不得自行改变研究路线或继续运行。

## Claims Boundary

Bootstrap acceptance 只证明 RTX5090 WSL GPU、PyTorch cu130、FP16/BF16 基础 tensor computation 和 Git context sync
可用。R0 通过后也最多证明特定 commit、环境与最小路径的 engineering feasibility；仍不证明外部论文数字、dataset、
Detector、Our Method、SOTA、统计结果、安全效果或生产能力。`FORMAL_EXPERIMENT = NOT STARTED`。

## Next Gate

RTX5090 pull 本次 Control Plane 治理提交后，从 `R0-A Environment Fingerprint` 开始，按顺序执行并 fail closed。
本机完成治理提交后停止。R0-I Control Plane Review 完成前，S6.1-P1 仍不得启动。Auto Continue = NO 表示不得从
R0 自动进入 P1 或 Formal Experiment；不撤销本次已批准的 R0-A 至 R0-I 顺序范围。
