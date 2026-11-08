# W1-OD-20261108-5060-S1B-RULEV2-DEV-18｜Owner 有界许可：Rule-V2 旧样本开发 + UIE 只读许可/依赖核查

**日期**：2026-11-08 JST  
**状态**：`OWNER_EXPLICITLY_APPROVED / RULE_V2_DEVELOPMENT_ONLY / UIE_READONLY_AUDIT_ONLY`  
**唯一工作分支**：`research/paper1-chinese-defense-5060`  
**控制面前置 HEAD**：`ae9f978ea5eb739ec30a677618d17c0c126470f6`  
**Owner 原话**：“批准”。所指内容为紧邻的唯一提议：“是否批准 5060 进入仅限 Rule-V2 的开发修复阶段？……使用已暴露的旧 73 条 S1 样本及普通本地单测，开发和诊断 Rule-V2；同时继续只读核实 UIE 许可与依赖。不下载、不加载或调用新模型，不接触新独立验证集，不运行 S2–S5。”  
**约束继承**：2026-11-04 双机研究合同、AGENTS.md、PO-MHEP、Owner16、Owner17、R1/R2、R2 K1-C、S1 `S1_FAIL_STOP`。  
**注意**：这不是 S1-B 模型资产、开发模型推理或独立验证批准。旧 S1 测试集已暴露，所有 Rule-V2 再试结果均属于 `EXPOSED_DEVELOPMENT`。

## PO-MHEP 十二字段

1. **Issue ID**：`W1-OD-20261108-5060-S1B-RULEV2-DEV-18`。
2. **Issue name**：5060 S1-B 仅 Rule-V2 规则抽取器受限开发与 UIE Nano 许可/依赖只读核查。
3. **Discovery stage**：S1 `W1-5060-S1-CHINESE-EXTRACTION-20261108-01` 已封存失败；Owner17 B 方案设计/只读资产审计已完成，下一道完整模型资产门不满足。
4. **Facts, derived and unknown**：`OBSERVED` S1 73条（61不同语义事实、12对配对视图），30完整正确、4错、39 UNKNOWN，值命中31/61、错抽4/34；R2 K1-C；UIE官方5项资产71,847,290字节但发布者权重/分词器许可、不可变revision、SHA256仍UNKNOWN；Qwen2.5-1.5B固定权重约3.10GB且当前5060可用内存8.73GiB低于先验12GiB CPU门；5090 Meta Llama 2申请等待；新模型下载/推理0。 `INFERENCE` Rule-V2优先修复查询主体属性、数值、多事实与时间/版本错误可改善使能模块，但不能预测独立泛化收益。 `UNKNOWN` Rule-V2改善幅度、UIE许可闭合情况、下一次验证结果、独立人审。
5. **Affected constraints**：历史R2/旧S1/旧108不可改；D1 `DEV_EXPOSED`、D2/D3严格隔离；P0无可信来源不升权；S2–S5需新Owner批准；S1-B三道审批门仍关闭模型资产/模型试验/新独立验证；5090 Claims不得改动。
6. **Why now**：UIE权重许可未闭合，Qwen内存/运行后端未闭合；可先零新模型成本定位已实测的查询槽位与scope/span错误，减少模型许可等待造成的空转。
7. **Downstream risks**：在已暴露73样本上后验调规则将高估泛化；提高召回可能引入未证修订/跨scope错误；Rule-V2仅抽取不提供来源真伪证明；暗中安装/下载、D2/D3数据污染或5090借用资源破坏合同；UIE代码许可证≠权重及分词器许可证。
8. **Options with tradeoffs**：A 保持停滞（成本低、研究进度停）；B **Owner批准**：Rule-V2 old73开发+只读UIE资产身份追溯（无新模型成本、可逆、结果仅开发级）；C 直接下载UIE或Qwen（许可证/资源/权限未闭合，拒绝）。B 的性能与论文价值仍须后续独立验证确认，不能由旧73推断。
9. **LOCAL recommendation**：执行 B；将旧73视为有标签开发集，保留原版 Rule-V1 锁，新增分阶段解析 Rule-V2，并共享未来所有臂的确定性源span/scope安全验证接口；程序性失败与语义误答分离，特别保留12应拒识中2条误答案例。UIE追溯限官方公开文档、许可和依赖元数据，证据不足如实UNKNOWN。
10. **Rationale and confidence**：Owner语境对本次明确“批准”的指向唯一，授权范围判断置信高；Rule-V2新方法收益、后续独立表现与模型可用性未知。若与上一Owner17及冻结文件冲突，按更窄的明确许可执行并上报。
11. **Owner decision**：`RULE_V2_DEVELOPMENT_ON_OLD73=APPROVED`；`UIE_LICENSE_DEPENDENCY_READONLY_AUDIT=APPROVED`；`NEW_MODEL_ASSET_DOWNLOAD=NOT_APPROVED`、`NEW_MODEL_INSTALL/LOAD/INFERENCE=NOT_APPROVED`、`S1B_INDEPENDENT_VALIDATION=NOT_APPROVED`、`S2_S5=NOT_APPROVED`；`5090_CLAIMS=NOT_APPROVED`；`S3_INDEPENDENT_CUSTODIAN=UNASSIGNED`。
12. **Allowed/prohibited**：
    - **允许**：以旧73已暴露的输入和标注做离线 Rule-V2 开发、规则迭代、失败归因（含必要的子集回放），用既有本地Python依赖开展无模型的普通合成unit tests；版本、输入SHA、参数、开发分母和全部迭代留痕；新代码先不覆盖旧V1。可设计 query槽位→多候选证据→实体/属性/值/单位→时间/版本/条件/否定例外→严格span→UNKNOWN。允许只读查询UIE官方资产/许可、tokenizer与CPU依赖元数据、列完整可核源/缺口。
    - **禁止**：任何新模型权重或依赖下载安装/模型加载/推理（包括使用已缓存但未授权权重）、外部或免费模型 API、在线模型推理、改写旧73原样本/Gold/失败结果、将旧73作为`INDEPENDENT_TEST`、新独立主样本/20配对视图生成或打开、接触D1/D2/D3私有样本或Reviewer/GT、旧B2/R2/108重跑、S1-B Gate1/2/3自动解封、S2–S5、5090任一操作或Llama2下载、主研究分支merge/cherry-pick。公开只读文献检索不等于获取权重许可，不请求在线权重文件体、tokenizer体、wheel体或模型端点。
    - **STOP**：出现独立验证标签泄漏、模型出站/依赖准备、使用未授权source、损坏旧不可变证据、资源门不合、对原P0语义修改、Git工作树冲突或需要新的算法科学测试即`HUMAN_DECISION_REQUIRED / Auto Continue=NO`。

## 完成条件与证据

单次有限开发闭环，交付 Rule-V2 源码与单测、源/规则SHA、old73开发评价及相对 Rule-V1 的同分母变化（包括改善和新误答）、UNKNOWN与错误类型、覆盖/拒识、原span位置信息、至少一个未证修订/跨scope不放行安全断言、UIE许可与依赖证据追溯/剩余UNKNOWN、无新模型与API的守卫报告、PO-MHEP前向/论文风险复核、Git新提交及远端SHA。
不得将 `DEVELOPMENT_ONLY` 写为S1 PASS。完成后STOP，将下一资产、开发模型推理与新独立验证门留给Owner。
