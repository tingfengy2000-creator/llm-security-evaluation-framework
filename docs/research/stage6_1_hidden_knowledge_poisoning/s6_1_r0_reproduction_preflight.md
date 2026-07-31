# S6.1-R0 Paper 1 Reproduction Environment and Baseline Feasibility Validation

## Governance Identity

- Task ID: `S6.1-R0`
- Task Name: `Paper 1 Reproduction Environment and Baseline Feasibility Validation`
- 中文名称：`Paper 1 外部基准复现环境与可行性验证`
- Task Type: `ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT`
- Status: `DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL`
- Future execution machine: `RTX5090 / COMPUTE_WORKER`
- Formal experiment: `FORMAL_EXPERIMENT = NOT STARTED`
- Auto Continue = NO

本文只冻结下一任务的目标、边界、工件和停止条件，不批准环境安装、源码 clone、数据/模型下载、API、smoke、
reproduction 或任何 5090 计算。执行必须取得项目负责人新的明确批准。

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

未来获批后，R0 只能执行以下目标：

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

第三方仓库必须位于 LLMGuard 主仓库之外的 `external research directory`。具体机器路径由后续执行批准确定，不在
Git 治理文件中写死本机绝对路径。

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

## Stop Conditions

- 没有新的 S6.1-R0 execution approval；
- worker identity、HEAD、manifest、config、model/dataset identity 不一致；
- compatibility patch 可能改变算法、预算、Retriever、Top-K 或指标；
- upstream 条款禁止计划动作；
- 资源超出批准预算；
- smoke 结果将被误写为 `Reproduced Result` 或 `Paper Result`。

任何停止条件触发后，只能返回 blocker/evidence 给 LOCAL Control Plane；不得自行改变研究路线或继续运行。

## Claims Boundary

R0 未来通过后最多证明特定 commit、环境与最小路径的 engineering feasibility。它仍不证明外部论文数字已复现，
也不证明 dataset、Detector、Our Method、SOTA、统计结果、安全效果或生产能力。当前 R0 尚未开始，不能宣称 RTX5090
ready 或任何 baseline 已可运行。

## Next Gate

项目负责人单独批准或拒绝 `S6.1-R0 EXECUTION`。在批准前停止；R0 完成并经独立审核前，S6.1-P1 仍不得启动。
