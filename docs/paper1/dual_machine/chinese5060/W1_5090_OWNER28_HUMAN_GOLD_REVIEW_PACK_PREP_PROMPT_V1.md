# 5090 Cursor｜Owner28独立评分后：独立人类Gold待审包准备（仅准备，不签Gold）

**本项为非科学准备**：遵守Owner28`AUTO_CONTINUE=NO`，**不**重复预测/评分，也不修改5090已封存的原角色盲包、兼容包、私有Gold、映射SHA或原汇总。新的人工审阅计划以及实际审阅者指定、样本传递和签署是Owner后续单独决定；当前仅允许生成可供Owner审阅的结构化模板与必要的本地私有材料，不将人工Gold0偷换成AgentGold或“人工完成”。

1. `git fetch`并在自身`research/paper1-ragdefender-repro-5090`分支继续，先读`AGENTS.md`及5090当前报告`OWNER28_EVAL_INDEPENDENT_SCORE_REPORT.md`和`OWNER28_EVAL_SCORE_MANIFEST.json`。**严格保持完整一轮已评分的封存状态，绝不重跑**。
2. 开发一个离线本地**双人独立审阅包**的只读导出程序：对32问、160个实际TopK段以只读role-free素材生成匿名随机顺序A/B两份相同审查任务，包含事实对象、查询时点/范围、相关官方版本的公开出处、每个片段的事实命题及引用位；**不**标原agent P/C/H/B角色、正确答案、模型过滤结果、RD臂编号或答题有利暗示。法律/时效来源引用应能帮助人类审阅者独立判真假与scope。若某段事实不能核到原句，则填`SOURCE_UNVERIFIED`，不得猜测。
3. 私有工作目录保存候选级编号映射与待审schema；公开Git只放`HUMAN_GOLD_DOUBLE_REVIEW_PROTOCOL_DRAFT.md`、`HUMAN_REVIEW_IMPORT_SCHEMA.json`、校验模板/脚本、SHA计数与数据隔离说明，不公开角色、私有标签、评估结果。审阅者须填写真伪、时效、是否同scope、原文出处位置、信心、问题及签名；两人独立提交后第三人裁决分歧，Gold签署由授权真人负责。**当前无人审，HUMAN_GOLD=0**。
4. 统计可供双人审核的实际主问题数、片段数、官方谱系和未核引文数；先抽查10份仅用于格式和判定规则的虚构案例，不阅读或复判正式Gold标签。不能从之前Agent标签推导审阅结果。给Owner一个“实际分配和预计人力”表作为签审决策依据。
5. 只能留在5090自身branch推送公开模板，不触碰5060私有源和研发，原Claim1–3 NOT_RUN、D2/D3/HOLD8锁、商业API0、权重下载0。STOP并回传HEAD与导出程序SHA，不自行启动人类标注。

备注：本批32世界是8场景×4事实，非32独立事实单位；真实评审前必须确认自写段落的私有使用范围和可传递给指定审阅者的授权。
