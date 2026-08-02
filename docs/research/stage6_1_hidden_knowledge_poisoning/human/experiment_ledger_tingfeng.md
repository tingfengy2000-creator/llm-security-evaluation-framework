# Paper 1 实验总账 — tingfeng

> 文档职责：项目需求提出人日常查看 Paper 1 的唯一总入口。需求原文、研究方案和阶段细节分别链接到其唯一权威文件；本页只提供可在 5–10 分钟内恢复进度的中文总览。

## 一分钟项目状态

Paper 1 研究中文版本化知识库中的隐蔽事实污染。Option B 已冻结，P1-R1 已作为协议框架验收；P1 只批准 PILOT0 基础设施。PILOT0 已实现 schema、标签隔离、group/split、leakage、attack contract、轻量 intervention、manifest 与 24 条纯合成 fixture，当前 `COMPLETED_PENDING_REVIEW`。这不是 Benchmark、Detector、真实 Pilot 或论文结果；真实数据、训练与 Formal Experiment 均未开始。

## 1. 论文与项目基本信息

| 项目 | 当前内容 |
| --- | --- |
| 中文题目 | 《面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法》；`TITLE_INTENT = CONFIRMED` |
| 英文题目 | *Stealthy Factual Poisoning in Versioned RAG Knowledge Bases: A Benchmark and Multi-View Detection Framework* |
| 研究目标 | 建立中文版本感知隐蔽知识污染 Benchmark，并研究多视角检测与轻量检索干预的安全—效用权衡 |
| 当前研究边界 | `OPTION_B_CONFIRMED`：Benchmark、Detection、Risk Score、Signals、Explanation、hard filtering / soft downweighting |
| 当前分支 | `research/stage6-1-hidden-poisoning` |
| 当前提交 | 本轮验收基础 `b19fc59cc5ba771fd547430f6096403720ef1a7d`；本页提交由 Git 动态解析 |
| 当前阶段 | S6.1-P1 PILOT0 工程证据审查门 |
| 当前任务 | `S6.1-P1-PILOT0 = COMPLETED_PENDING_REVIEW`；等待项目负责人审查工程证据 |
| 上下文恢复治理 | `HUMAN_ACCEPTED（人工验收通过）` |
| 正式实验状态 | `NOT STARTED（尚未开始）` |
| 我们的方法结果 | `NONE（尚无正式方法结果）` |

范围警戒：Option B 只允许 hard filtering 或 soft downweighting。trusted context package、完整上下文构造、多证据可信上下文生成、复杂端到端 Agent 防御、生产级 RAG 平台和完整可信检索链均排除并保留给 Paper 2 或后续研究。

## 2. 整体实验路线

| 阶段 | 研究目标 | 当前状态 | 主要产出 | 关键结论 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| S6.1-LR1 | 论文路线与外部基线对齐 | `HUMAN_ACCEPTED` | 路线、对齐矩阵、协议、工件登记 | 外部项目角色已区分，尚非统一严格比较 | 作为方案与后续协议输入 |
| S6.1-R0 | 复现环境与可行性预检 | `HUMAN_ACCEPTED_WITH_BLOCKERS` | 环境、源码、数据工件与证据合同 | 工程可行性已识别，目标阻塞仍存在 | 由 FU1 定向处理 |
| S6.1-R0-FU1 | 定向解除基线阻塞 | `HUMAN_ACCEPTED / CLOSED` | P0、L1、W2 证据、H1 模型包、resume_01 历史与 resume_02 `25/25` evidence | 仅关闭单样本 detection-core 工程可行性 | 历史冻结；不自动进入 P1 |
| S6.1-P1-R1 | 协议强化与 Option B 范围冻结 | `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK` | [审批级强化候选](../s6_1_p1_r1_protocol_review_candidate.md) | 框架已接受；数值参数待 Pilot 证据 | 保持 formal protocol 未冻结 |
| S6.1-P1-PILOT0 | Benchmark 与轻量解毒基础设施 | `COMPLETED_PENDING_REVIEW` | [P1 工作过程](../stage_process/S6.1-P1_work_process.md)与纯合成工程测试 | 工程合同可行；不是 Benchmark 或方法结果 | owner 审查后决定是否批准真实数据与标注 Pilot |
| S6.1-P1 | 正式实验协议批准 | `APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT` | 唯一 [canonical stage process](../stage_process/S6.1-P1_work_process.md) | 只批准基础设施 | 不自动进入真实 Pilot |
| Pilot | 样本规模、标注与资源可行性验证 | `NOT APPROVED / NOT STARTED` | 无 | 尚未执行 | 需独立批准 |
| 中文 Benchmark 构建 | 版本链与隐蔽污染数据 | `NOT STARTED / DATASET NOT FROZEN` | 预期为冻结数据快照 | 尚未构建 | 先完成协议审批 |
| 多视角 Detector 实现 | 五视角检测与风险评分 | `PLANNED / NOT IMPLEMENTED` | 预期为检测器实现 | 无实现结果 | 等待数据与协议 |
| Retrieval Intervention | hard filtering / soft downweighting | `PLANNED / NOT IMPLEMENTED` | 预期为轻量干预实现 | 无实现结果 | 等待协议、数据与 Detector |
| Formal Evaluation | 正式主实验 | `NOT STARTED` | 预期为可复现实验结果 | 无正式结果 | 等待全部准入条件 |
| Ablation | 视角与组件消融 | `PLANNED / NOT STARTED` | 预期为消融结果 | 无结果 | 正式方法实现后执行 |
| Generalization | 跨攻击、跨领域评估 | `PLANNED / NOT STARTED` | 预期为泛化结果 | 无结果 | 主实验后执行 |
| Paper Writing | 论文写作与证据绑定 | `OUTLINE-LEVEL / NOT STARTED` | 预期为论文稿 | 不得先写结果 | 以已验收证据为准 |

## 3. 总运行记录

### S6.1-LR1 — 论文路线与基线对齐

- 阶段目标：形成 Paper-first 研究路线并定位 PoisonedRAG、GMTP、SafeRAG。
- 当前状态：`HUMAN_ACCEPTED（人工验收通过）`。
- 进入条件：S6-T5 人工接受的工程基线可供引用，但不构成安全或论文实验结果。
- 执行机器：本机。
- 关键输入：三项外部工作、中文版本化隐蔽知识污染目标、既有治理边界。
- 数据、模型与源码身份：见对齐矩阵、外部工件登记与阶段过程。
- 核心执行步骤：文献和仓库证据核对、角色划分、实验 Track 与声明边界设计。
- 关键运行命令：Git 身份核对；架构测试入口。
- 输出文件：研究路线、Benchmark 对齐矩阵、复现协议、工件登记。
- 实验或工程结果：研究规划与工件身份核对；不是正式复现结果。
- 证据位置：[LR1 工作过程](../stage_process/S6.1-LR1_work_process.md)。
- 关键结论：PoisonedRAG 是攻击基线，GMTP 是检测基线，SafeRAG 是 Benchmark 参考。
- 不能得出的结论：不能声称三者已完成严格统一比较或本项目方法有效。
- 失败和 blocker：外部仓库、数据、依赖和论文目标并非同一评测链。
- 解决情况：通过非严格角色对齐保留可比边界。
- 当前下一步：作为 R0/P1 方案输入。
- 详细过程链接：[S6.1-LR1_work_process.md](../stage_process/S6.1-LR1_work_process.md)。

### S6.1-R0 — 外部基线工程预检

- 阶段目标：验证外部源码、公开工件、环境合同和可复现入口。
- 当前状态：`HUMAN_ACCEPTED_WITH_BLOCKERS（带阻塞项验收）`。
- 进入条件：LR1 已验收，R0 获得启动批准。
- 执行机器：5090 执行工程检查，本机复核证据。
- 关键输入：固定外部提交、公开数据工件和预检协议。
- 数据、模型与源码身份：PoisonedRAG `f660d721…`、GMTP `15b48d15…`、SafeRAG `e8f57974…`。
- 核心执行步骤：源码身份、数据 schema、环境与最小调用链检查；纠正第一版证据不足。
- 关键运行命令：环境启动；预检入口；证据索引验证。
- 输出文件：R0 evidence archive、修正矩阵、Control Plane Review。
- 实验或工程结果：工程可行性与目标阻塞识别；不是完整 baseline reproduction。
- 证据位置：[R0 工作过程](../stage_process/S6.1-R0_work_process.md)。
- 关键结论：R0 可以验收，但遗留阻塞必须由 FU1 解决。
- 不能得出的结论：不能声称外部基线结果已复现或 S6.1-P1 已获批准。
- 失败和 blocker：第一次 evidence archive 宣称与实际成员不一致。
- 解决情况：修正包 12/12 核验后，以追加记录关闭。
- 当前下一步：保持 R0 历史，转入 FU1 定向处理。
- 详细过程链接：[S6.1-R0_work_process.md](../stage_process/S6.1-R0_work_process.md)。

### S6.1-R0-FU1 — 定向外部基线可行性处理

- 阶段目标：以本机优先、5090 门控方式处理 P0、L1 和 W2。
- 当前状态：P0/L1/W2 `HUMAN_ACCEPTED`；W2 为 `ENGINEERING_FEASIBILITY_ONLY / CLOSED`；FU1 为 `HUMAN_ACCEPTED / CLOSED`。
- 证据状态：`W2_ATTEMPT1_EVIDENCE_BLOCKER = RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW`；`BLK-S6.1-FU1-W2-001 = RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE`。
- H1 状态：`OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090 / COMPLETED`。
- H2 状态：`ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS / HUMAN_ACCEPTED_AS_W2_EVIDENCE`；`resume_01 = VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0`；`resume_02 = CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED / call_count=1`。
- 进入条件：R0 带阻塞项验收并批准 FU1。
- 执行机器：本机负责规划、证据闭环和离线资产准备；5090负责受控运行与独立验证。
- 关键输入：PoisonedRAG 发布攻击文本、GMTP 检测输入、固定模型 revision。
- 数据、模型与源码身份：完整身份见阶段过程；模型 revision 为 `abe8c149…` 与 `86b5e093…`。
- 核心执行步骤：P0 工件验证、L1 静态调用链、W2 Attempt 1、Correction 01/02、H1 离线模型包、H2 resume_01 fail-closed 证据，以及 resume_02 的 H2-A `18/18`、本地 CUDA 模型加载、唯一一次 H2-B 与本机证据复核。
- 关键运行命令：环境启动；GMTP detection-core 入口；证据索引验证；结果生成入口。
- 输出文件：Correction 02 archive、H1 model bundle 与 resume02 15,625-byte evidence archive；均未进入 Git。
- 实验或工程结果：W2 Attempt 1 为 `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`；resume_02 为本机已接受的双文档工程 smoke 证据。
- 证据位置：[FU1 工作过程](../stage_process/S6.1-R0-FU1_work_process.md)、[Attempt 1 证据复核](../s6_1_r0_fu1_w2_attempt1_control_plane_review.md)与[H2 resume02 证据复核](../s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md)。
- 关键结论：最小 detector-core feasibility gate 已闭合并获项目需求提出人验收；`W2_ENGINEERING_OBJECTIVE = SATISFIED`，`W2_RUNTIME_GATE = CLOSED`。
- 不能得出的结论：不能把一次双文档调用写成 GMTP 复现、有效性、安全性、泛化、正式指标或论文结果。
- 失败和 blocker：Attempt 1 模型下载阻塞作为历史保留；W2 blocker 已由 resume_02 与 owner acceptance 关闭，后续 P1 协议、解毒范围与 formal-environment 仍是独立门。
- 解决情况：Correction 02 关闭 evidence blocker；resume02 本机复核关闭冻结的最小 Worker feasibility blocker。
- 当时下一步：审查 [P1-R1 协议强化候选](../s6_1_p1_r1_protocol_review_candidate.md)及其四项高层决定；该门现已由 OR-022 的框架验收与 PILOT0 批准替代。
- 详细过程链接：[S6.1-R0-FU1_work_process.md](../stage_process/S6.1-R0-FU1_work_process.md)。

## 4. 结果分类

### 4.1 已发表结果（Published Results）

仅引用 PoisonedRAG、GMTP、SafeRAG 原论文公开结论；本项目尚未把这些公开数字验证为本地复现结果。

### 4.2 已复现结果（Reproduced Results）

尚无完整严格的外部 baseline reproduction。

### 4.3 工程验证结果（Engineering Validation Results）

已形成外部工件身份与 schema 核对、固定输入、环境合同、Correction 02 evidence closure、本机离线模型 bundle 及受阻 smoke 记录。这些均为工程证据。

### 4.4 我们的正式实验结果（Our Formal Results）

`NONE（尚无正式方法结果）`；`FORMAL_EXPERIMENT = NOT STARTED（正式实验尚未开始）`。

## 5. 实验证据总表

| Evidence ID | 阶段 | 证明内容 | Commit / Artifact | SHA256 / Revision | 验收状态 |
| --- | --- | --- | --- | --- | --- |
| E-S6T5 | 前置基线 | 受控检索到上下文工程基线 | `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1` | Git commit | `HUMAN_ACCEPTED BASELINE`，非安全结果 |
| E-R0-CORRECTED | R0 | 修正工程预检证据与 12/12 索引 | corrected evidence archive | `904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b` | `HUMAN_ACCEPTED_WITH_BLOCKERS` |
| E-W2-C02 | FU1/W2 | Correction 02 完整性与命令证据闭环 | correction02 archive | `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622`；17/17 PASS | evidence blocker 已解除 |
| E-H1-BUNDLE | FU1/H1 | 本机准备并由 5090 在 H2-A 验证的离线模型包 | `s6_1_r0_fu1_w2_models_20260801.tar.gz`，1222137698 bytes | `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`；19/19 PASS | 5090 验证通过 |
| E-H1-ENC | FU1/H1 | Encoder 固定身份，8 files / 438708922 bytes | `facebook/contriever-msmarco` | `abe8c1493371369031bcb1e02acb754cf4e162fa` | 5090 本地 CUDA 加载通过 |
| E-H1-MLM | FU1/H1 | MLM 固定身份，9 files / 881643453 bytes | `google-bert/bert-base-uncased` | `86b5e0934494bd15c9632b12f734a8a67f723594` | 5090 本地 CUDA 加载通过 |
| E-H2-APPROVAL | FU1/H2 | 项目需求提出人批准条件式 H2；尚未发送或执行 | 审批基础 `212911a21dc35bef05b15fb840542403c415dd13` | H2 合同见 FU1 工作过程 | `APPROVED_TO_START / NOT SENT / NOT EXECUTED` |
| E-H2-R01 | FU1/H2 | resume_01 因 bundle/sidecar 缺失合规停止；H2-B 未执行 | 4,570-byte archive | `941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`；19/19 PASS | `OFFLINE_BUNDLE_SHA_BLOCKER`；本机复核通过 |
| E-H2-R02-APPROVAL | FU1/H2 | bundle/sidecar 已到 5090；项目需求提出人批准新证据命名空间 | `resume_02`；不可覆盖 resume_01 | 新 resume02 archive 待生成 | `APPROVED_TO_START / NOT EXECUTED` |
| E-H2-R02-REVIEW | FU1/H2 | H2-A `18/18`、唯一一次 H2-B、模型/环境/资源与 resume_01 不变证据 | 15,625-byte resume02 archive | `58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`；25/25 PASS | `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED` |
| E-W2-OWNER-ACCEPTANCE | FU1/W2 | 接受冻结单样本 detection-core 工程目标并关闭 W2/FU1 | acceptance base `b19fc59cc5ba771fd547430f6096403720ef1a7d` | PODR-061 / OR-020 | `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED` |

模型总字节数为 `1320352375`。完整细节见对应阶段过程、证据复核、项目实验主记录与 Git 外部私有归档；私有绝对路径不写入 Git。

## 6. 有研究价值的失败

| 失败 | 发生与原因 | 研究价值与后续影响 | 当前状态 |
| --- | --- | --- | --- |
| R0 第一次证据不足 | archive 对已包含成员的声明不充分 | 促成 evidence index 与实际成员绑定、控制面 fail-closed | 已由修正证据解决，历史保留 |
| W2 第一次模型下载阻塞 | 5090 无法在线取得固定模型 | 证明模型供应链必须与 detection-core 分层；促成 H1 离线包 | 运行仍受阻；证据缺口已解决 |
| Correction 01/02 | Correction 01 缺少具体 `du` 命令证据，Correction 02 补齐 | 形成测量命令、输出和索引共同闭环规则 | Correction 02 已解决证据 blocker |
| PoisonedRAG 工件复用边界 | 发布攻击文本可复用，但不等于重新生成攻击 | 避免把 artifact reuse 写成 generation reproduction | 边界已固定 |
| 攻击链不等价 | GMTP packaged HotFlip 与 PoisonedRAG LM-targeted 来源、目标和调用链不同 | 后续需明确非严格比较或重新冻结统一协议 | 尚未形成正式统一比较 |

## 7. 当前风险

- 工程风险：一次双文档 smoke 不能覆盖 full-corpus/indexing、阈值校准、批量稳定性或更广依赖；禁止把已关闭的最小 feasibility gate 外推。
- 架构风险：外部代码的隐藏依赖可能在受控 smoke 中再次暴露。
- 实验风险：P1-R1 框架已接受，但数据、参数、种子、指标和统计候选值尚未冻结；样本量与资源预算仍须后续获批 Pilot 校准。
- 论文风险：工程可行性、公开论文结论、复现结果和本项目结果若混写会导致不可支持的主张。
- 许可证与可发布风险：代码访问和内部复现不等于数据再分发许可，发布前仍须逐项复核。

## 8. 下一步

- P0：W2/FU1 已按工程 feasibility 范围接受并关闭；无需向 5090 发送 prompt，也不得重复 H2-B。
- P1-R1：`HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`；数值参数仍为 `PENDING_PILOT_EVIDENCE`。
- PILOT0：`COMPLETED_PENDING_REVIEW`；项目负责人审查工程证据后，决定是否批准真实数据与标注 Pilot。
- P1：`APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT`；真实数据 Pilot 与 240-group Pilot 均 `NOT APPROVED / NOT STARTED`。
- Dataset `NOT FROZEN`；Detector 与 Retrieval Intervention 均 `NOT IMPLEMENTED`；Training、Formal Experiment 均 `NOT STARTED`。
- P2：协议获批后才讨论中文 Benchmark 构建、多视角 Detector、Formal Evaluation、消融和泛化。

## 9. 需要项目需求提出人确认

- 审查 PILOT0 工程证据，并决定是否批准真实数据与标注 Pilot。
- 正式指标、统计协议、样本量、数据冻结与统一比较方案仍须后续独立确认。

## 10. 关键 Git 提交

| Commit | 恢复用途 |
| --- | --- |
| `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1` | S6-T5 人工接受工程基线 |
| `1294632ca0501e7b999a29383780bec49eaa6b04` | Paper 1 基线对齐初始材料 |
| `347dc2bfff2256a7ad6c0c6ab8c468e9f3f833d9` | S6.1-LR1 人工验收 |
| `2762ae90ccb739892a58f1684248cf777d2b24ed` | 修正 R0 证据验收 |
| `0e66047021a6e950c93419e0daa9178e72e04551` | P0/L1 验收与 W2 合同冻结 |
| `b922fb9091159a01bd5baad8ee1224d36a665e0d` | Correction 02 关闭与 H1 上下文 |
| `b19fc59cc5ba771fd547430f6096403720ef1a7d` | H2 resume_02 evidence accepted；父 W2 最终验收基础 |
