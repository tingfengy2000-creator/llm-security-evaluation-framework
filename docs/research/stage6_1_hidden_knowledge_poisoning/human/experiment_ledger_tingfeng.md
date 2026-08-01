# Paper 1 实验总账 — tingfeng

> 文档职责：项目需求提出人日常查看 Paper 1 的唯一总入口。需求原文、研究方案和阶段细节分别链接到其唯一权威文件；本页只提供可在 5–10 分钟内恢复进度的中文总览。

## 一分钟项目状态

Paper 1 研究中文版本化知识库中的隐蔽事实污染，当前范围仍是 Benchmark、Detection、Risk Score、Signals 与 Explanation。LR1、P0、L1 已人工验收；R0 带 blocker 验收。H1 离线模型包已由本机准备并验证。H2 已批准，但尚未发送或执行：5090 必须先通过 H2-A 包完整性门，才可条件执行一次 H2-B 双文档 GMTP 工程 smoke；完成或遇到 blocker 后立即停止并返回本机复核。父 W2 仍未完成、未验收，P1 与正式实验未开始，也没有正式论文结果。最大工程风险是离线加载与 detection-core 尚未实证；最大论文风险仍是把单次工程 smoke 误写为检测效果或复现结果。

## 1. 论文与项目基本信息

| 项目 | 当前内容 |
| --- | --- |
| 中文题目 | 《面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法》；题目意图已确认，解毒技术范围待确认 |
| 英文题目 | *Stealthy Factual Poisoning in Versioned RAG Knowledge Bases: A Benchmark and Multi-View Detection Framework* |
| 研究目标 | 建立中文版本感知隐蔽知识污染 Benchmark，并研究多视角检测、风险评分、信号与解释 |
| 当前研究边界 | Benchmark、Detection、Risk Score、Signals、Explanation |
| 当前分支 | `research/stage6-1-hidden-poisoning` |
| 当前提交 | 文档来源提交 `b922fb9091159a01bd5baad8ee1224d36a665e0d` |
| 当前阶段 | S6.1-R0-FU1 |
| 当前任务 | `S6.1-R0-FU1-W2-H2` 已批准；等待项目需求提出人将批准提交与 Git-external bundle 交给 5090 |
| 上下文恢复治理 | `HUMAN_ACCEPTED（人工验收通过）` |
| 正式实验状态 | `NOT STARTED（尚未开始）` |
| 我们的方法结果 | `NONE（尚无正式方法结果）` |

范围警戒：自动过滤、自动重排、可信上下文包、运行时可信检索和完整解毒系统均为 `SCOPE_CONFIRMATION_REQUIRED（需要进一步确认范围）`，不得由题目措辞自动扩展。

## 2. 整体实验路线

| 阶段 | 研究目标 | 当前状态 | 主要产出 | 关键结论 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| S6.1-LR1 | 论文路线与外部基线对齐 | `HUMAN_ACCEPTED` | 路线、对齐矩阵、协议、工件登记 | 外部项目角色已区分，尚非统一严格比较 | 作为方案与后续协议输入 |
| S6.1-R0 | 复现环境与可行性预检 | `HUMAN_ACCEPTED_WITH_BLOCKERS` | 环境、源码、数据工件与证据合同 | 工程可行性已识别，目标阻塞仍存在 | 由 FU1 定向处理 |
| S6.1-R0-FU1 | 定向解除基线阻塞 | `H2 APPROVED / NOT SENT / NOT EXECUTED` | P0、L1、W2 证据、H1 模型包与 H2 冻结合同 | P0/L1 已验收；W2 未完成 | 5090 先 H2-A，通过后仅执行一次 H2-B |
| S6.1-P1 | 正式实验协议冻结 | `NOT STARTED` | 预期为冻结协议 | 尚无准入授权 | 等待前置门关闭与人工批准 |
| 中文 Benchmark 构建 | 版本链与隐蔽污染数据 | `NOT STARTED / DATASET NOT FROZEN` | 预期为冻结数据快照 | 尚未构建 | 先完成协议审批 |
| 多视角 Detector 实现 | 五视角检测与风险评分 | `PLANNED / NOT IMPLEMENTED` | 预期为检测器实现 | 无实现结果 | 等待数据与协议 |
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
- 当前状态：P0/L1 `HUMAN_ACCEPTED`；W2 `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`。
- 证据状态：`W2_ATTEMPT1_EVIDENCE_BLOCKER = RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW`；这只关闭证据缺口。
- H1 状态：`OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`。
- H2 状态：`APPROVED_TO_START / NOT SENT / NOT EXECUTED`；`Auto Continue = CONDITIONAL_WITHIN_H2_ONLY`。
- 进入条件：R0 带阻塞项验收并批准 FU1。
- 执行机器：本机负责规划、证据闭环和离线资产准备；5090负责受控运行与独立验证。
- 关键输入：PoisonedRAG 发布攻击文本、GMTP 检测输入、固定模型 revision。
- 数据、模型与源码身份：完整身份见阶段过程；模型 revision 为 `abe8c149…` 与 `86b5e093…`。
- 核心执行步骤：P0 工件验证、L1 静态调用链、W2 Attempt 1、Correction 01/02、H1 离线模型包；H2 已冻结但尚未执行。
- 关键运行命令：环境启动；GMTP detection-core 入口；证据索引验证；结果生成入口。
- 输出文件：Correction 02 archive 与 H1 model bundle；均未进入 Git。
- 实验或工程结果：W2 Attempt 1 为 `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`；H1 仅为本机已准备资产。
- 证据位置：[FU1 工作过程](../stage_process/S6.1-R0-FU1_work_process.md)与[证据复核](../s6_1_r0_fu1_w2_attempt1_control_plane_review.md)。
- 关键结论：Correction 02 解除了 evidence blocker，但没有完成 W2。
- 不能得出的结论：不能声称模型已在 5090 加载、GMTP 已跑通、W2 已验收或产生论文结果。
- 失败和 blocker：Attempt 1 模型下载阻塞；当前仍需 5090 验证 H1。
- 解决情况：Correction 02 已关闭证据缺口；计算执行仍待审批。
- 当前下一步：项目需求提出人把批准提交和 Git-external bundle 交给 5090；5090 先执行 H2-A，只有全部实质条件通过才可执行一次 H2-B，随后停止并返回本机复核。
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
| E-H1-BUNDLE | FU1/H1 | 本机准备并验证的离线模型包 | `s6_1_r0_fu1_w2_models_20260801.tar.gz`，1222137698 bytes | `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`；19/19 PASS | 等待 5090 验证 |
| E-H1-ENC | FU1/H1 | Encoder 固定身份，8 files / 438708922 bytes | `facebook/contriever-msmarco` | `abe8c1493371369031bcb1e02acb754cf4e162fa` | 本机已准备 |
| E-H1-MLM | FU1/H1 | MLM 固定身份，9 files / 881643453 bytes | `google-bert/bert-base-uncased` | `86b5e0934494bd15c9632b12f734a8a67f723594` | 本机已准备 |
| E-H2-APPROVAL | FU1/H2 | 项目需求提出人批准条件式 H2；尚未发送或执行 | 审批基础 `212911a21dc35bef05b15fb840542403c415dd13` | H2 合同见 FU1 工作过程 | `APPROVED_TO_START / NOT SENT / NOT EXECUTED` |

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

- 工程风险：H2 尚未发送或执行；H1 尚未由 5090 独立核验、离线加载，GMTP detection-core 未完成。
- 架构风险：外部代码的隐藏依赖可能在受控 smoke 中再次暴露。
- 实验风险：数据、参数、种子、正式指标和统计协议尚未冻结。
- 论文风险：工程可行性、公开论文结论、复现结果和本项目结果若混写会导致不可支持的主张。
- 许可证与可发布风险：代码访问和内部复现不等于数据再分发许可，发布前仍须逐项复核。

## 8. 下一步

- P0：执行已批准的 H2：5090 先完成 H2-A；只有 18 项 bundle 条件、冻结环境与离线条件全部通过，才执行一次 H2-B 双文档 smoke；随后返回本机复核。
- P1：仅在 W2 与前置门正式关闭后，提交 S6.1-P1 协议冻结申请；当前不得启动。
- P2：协议获批后才讨论中文 Benchmark 构建、多视角 Detector、Formal Evaluation、消融和泛化。

## 9. 需要项目需求提出人确认

- “多视角解毒方法”的技术定义是否只覆盖 Detection、Risk Score、Signals、Explanation。
- 自动过滤、自动重排、可信上下文包、运行时可信检索、完整解毒系统中哪些（如有）进入 Paper 1。
- 正式指标、统计协议、数据冻结与统一比较方案须在 S6.1-P1 单独确认。

## 10. 关键 Git 提交

| Commit | 恢复用途 |
| --- | --- |
| `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1` | S6-T5 人工接受工程基线 |
| `1294632ca0501e7b999a29383780bec49eaa6b04` | Paper 1 基线对齐初始材料 |
| `347dc2bfff2256a7ad6c0c6ab8c468e9f3f833d9` | S6.1-LR1 人工验收 |
| `2762ae90ccb739892a58f1684248cf777d2b24ed` | 修正 R0 证据验收 |
| `0e66047021a6e950c93419e0daa9178e72e04551` | P0/L1 验收与 W2 合同冻结 |
| `b922fb9091159a01bd5baad8ee1224d36a665e0d` | Correction 02 关闭与 H1 上下文 |
