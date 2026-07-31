# Dual-Machine Research Execution and Context Sync Policy

## Canonical Roles

- `LOCAL = CONTROL_PLANE`
- `RTX5090 = COMPUTE_WORKER`
- `Context Sync = Git`
- `Codex memory is not a context authority`

本政策定义长期机器职责和上下文同步；Paper 1 的具体硬件兼容细节由
[stage-specific hardware policy](../research/stage6_1_hidden_knowledge_poisoning/hardware_execution_policy.md) 补充。
两者职责不同，不是竞争性副本。

## LOCAL / CONTROL_PLANE

本机负责：研究决策、Git 主控、代码与协议、governance、source/benchmark review、审批门、result
integration、claims review 和最终提交。Control Plane 必须保存 canonical route、Owner Decision、Current Work
State、Experiment Master Record 和 Research Execution Log 的一致引用。

## RTX5090 / COMPUTE_WORKER

5090 worker 负责未来获批的 GPU、reproduction、embedding、model execution、benchmark execution 和 formal
computation。计划硬件身份为 RTX 5090 32 GB + 64 GB RAM；在实测前只能标记为 planning information。

Compute Worker 不得自行改变重大研究路线、attack taxonomy、dataset protocol、metric definition、baseline 角色或
claims boundary。发现设计问题时停止运行，标记 `RESEARCH_ROUTE_REVIEW_REQUIRED`，把证据返回 Control Plane。

## Git-Native Context Sync

两台机器只通过 Git commit、branch、tag、manifest 和明确的 artifact hash 同步研究上下文，不通过 Thread history、
聊天摘要、剪贴板记忆或“另一台机器应该已经改过”同步。

每个任务启动时：

```powershell
git fetch --prune --tags origin
git status --short --branch
git branch --show-current
git rev-parse HEAD
git log -15 --oneline
```

存在 upstream 且工作树 clean 时才执行 `git pull --ff-only`。缺少 upstream、分叉、未知修改或预期 HEAD 不存在时
fail closed，并返回 Control Plane。

## Compute Worker Additional Gate

未来任何 formal/smoke/reproduction 执行前必须核对：

| Identity | Required check |
| --- | --- |
| branch | equals the approved expected branch |
| HEAD | equals `RunManifest.git_commit` |
| working tree | clean |
| dataset snapshot | matching approved ID/version/hash/license |
| config hash | matching approved manifest |
| model revision | exact matching revision or explicitly approved compatibility track |
| environment fingerprint | recorded before execution |

任一不匹配必须 **fail closed**。不得“先跑再补 manifest”，不得将 uncommitted patch 的结果并入正式比较。

## Original vs Compatibility Environment

1. Original Environment 逐字记录论文/官方仓库依赖，不保证能在 Blackwell 运行。
2. Compatibility Environment 单独记录为现代 CUDA/PyTorch/driver 兼容轨道。
3. 每个 patch 绑定 old/new version、原因、算法影响、validation 和 local patch commit。
4. 兼容环境只证明可运行时，Blocker 状态写 `MITIGATED` 或 `MITIGATED_BY_COMPATIBILITY_ENV`；WORKAROUND
   不得直接写 `RESOLVED`。
5. 只有算法级等价和正式关闭证据齐备后，才能由 Control Plane 把 Blocker 改为 `RESOLVED`。

## Artifact Transfer

- Git 只保存源码、协议、配置、轻量 manifest、hash、脱敏指标和报告。
- dataset、model、index、raw log 和大型输出不进 Git；用批准的 artifact store/transfer 方法并保存 hash。
- API key、Authorization、完整污染正文、Ground Truth 和 evaluator labels 不同步到运行时链路或普通日志。
- Compute Worker 返回的结果必须含 run ID、exit code、command、environment fingerprint、raw artifact hash 和
  `RunManifest.git_commit`。

## Result Integration

Control Plane 在接受 worker 结果前核对：

1. manifest 与 worker HEAD；
2. clean-tree attestation；
3. dataset/config/model/environment identity；
4. raw log/result hash；
5. status 是 `FORMAL_EXPERIMENT`、`ENGINEERING_VALIDATION`、`FAILED_RUN` 或 `INVALID_RUN`；
6. Published/Reproduced/Our Method 分栏与 strict-comparison eligibility；
7. claims 不超过证据。

验证失败的结果保留为 FAILED/INVALID 记录，不删除、不挑选性隐藏。

## Current Gate

`S6.1-LR1` 与 Context Recovery Governance 已人工接受；下一任务 `S6.1-R0` 仅为
`DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL`。`FORMAL_EXPERIMENT = NOT STARTED`。当前未批准
Worker 环境安装、external repository clone、数据/模型下载、PoisonedRAG/GMTP/SafeRAG smoke/reproduction、
Detector、training 或 S6.1-P1。取得 R0 execution 单独批准前，两台机器均停止在 planning/control-plane 边界。

## Baseline Integrity

- S6-T5 governance baseline：`18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。
- Accepted baseline content：`4ecf73a`。
- Last accepted implementation：`b136ee2`。
- Accepted integration evidence：`b6cedf3`。
- Stage 1–5 remain immutable historical assets。

这些身份用于核验，不授权改写 baseline、历史 artifact 或 tag。
