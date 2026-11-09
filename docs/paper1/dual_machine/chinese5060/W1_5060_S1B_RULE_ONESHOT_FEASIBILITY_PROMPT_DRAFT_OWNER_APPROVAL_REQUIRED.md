# 5060 Codex｜S1-B Rule-V1/Rule-V2 一次性可行性验证（**待 Owner20 明确批准，不得直接执行**）

**状态：`DRAFT / NOT_AUTHORIZED / NO_AUTO_CONTINUE`**。本文件仅是下一批的预注册执行草案，存档和阅读不能作为新样本评价许可；必须先由Owner在新会话明确表述“批准本一次性Rule-V1/V2可行性评价”，按PO-MHEP登记正式授权号、具体运行边界及文件路径，之后方可把本草案升级为生效执行合同。

## 0. 恢复与源码身份

唯一仓库 `tingfengy2000-creator/llm-security-evaluation-framework`；工作分支 `research/paper1-chinese-defense-5060`。读取AGENTS.md、PO-MHEP、Owner19、封存Manifest、质量报告和监督Gate审查：
`docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_ONE_SHOT_SUPERVISOR_GATE_REVIEW_20261109.md`。
封存 Run `W1-5060-S1B-FEAS-DATA-PREP-20261109-01`，数据seal SHA256 `531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`；输入 `bd2bc5e6586789070c20dde123bfe72843181aa861aca229fdb0c23091328dee`；Gold `8f745f921424c6e61357ec19800bc4a1f198e92a26d36377a3a238d634598371`；评分协议 `43d4d22770f5887058fabfc0162368e77cd36bd6c7d85d846417789515f5341e`。
冻结 Rule-V1 `68d34a5d877206f4e6d7d9e2bdda16784145a76a`，Rule-V2 `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`，参数与源不修改。开工必须完成Git preflight、工作树与私有数据身份核验、Env/资源/许可风险回顾、前向/论文风险复核。

## 1. 始终先做只读无Gold适配器预检

仅使用旧73暴露数据或全新普通合成unit fixtures（**不可使用封存的新120视图执行试预测**）验证共同 `id/query/evidence` 接口和输出字段映射。共同适配器必须对两臂保留原字段且不提供额外Oracle/query hint；V1/V2不支持的字段显式UNKNOWN/缺失，不能借Gold补齐。固定角色盲adapter源码、配置、hash、进程出站与D/E路径。对source span set必须支持字符及UTF8偏移的半开区间验证和明确的多证据窗口编码；不能通过无限扩大引用窗口覆盖全部事实来蒙混通过。无法设计无偏与可解释适配器则STOP，回Owner，不消耗主100。

特别预注册：数据生成器有70主案例带文档标题头、30无标题头；可回答70中有21条无标题头（由源码分配公式推得），Rule-V2依赖`《...》`书名抽取。此分层为**高风险压力测试**，但不能先读取新结果调代码。必须报告标题头有/无，不能删无标题数据或后验重权重。
评价器中同一值在多个不同位置的合法支持必须以冻结的`accepted_span_sets`（支持集合之间OR，集合内部AND）评分；段间关联必须包含每个必要原文键，不能仅数值相等就算支持。所有字段映射约束从公开schema和protocol推出，不能看Gold后改适配器。

## 2. 实验单次离线执行（只有下一批Owner明确签署后生效）

- `ONE_SHOT_FEASIBILITY / AGENT_GENERATED_PROVISIONAL_FEASIBILITY / NOT_INDEPENDENT_AUTHOR`。
- 同120行role-free输入，100主语义案例（70 ANSWER/30 UNKNOWN）+20从属改写视图；Rule-V1与Rule-V2在同代码/环境/输入顺序/共同Adapter下单次完整预测，禁止跑一半后修改模型/参数重新试。
- 两臂所有结果先不接触Gold写入私有角色盲结果、全120状态包括ERROR/UNKNOWN完整分母、输出archive hash与signed input/config SHA；Evaluator只在双臂都seal后读取Gold。
- 必须报告总100主分母的`correct/wrong/UNKNOWN`、值命中/70（至少63达90%）、已决定错抽/decided（点估计≤2%且decided>0）、错抽/100、coverage/abstain、30应拒识误答、strict scope/version/span错误及source proof fail、题型10组、标题有/无、20配对变化、95%Wilson区间。原打分协议不能为某臂修改；如发现语义/标注冲突，只能记录`EVALUATOR_AMBIGUITY`并不修改Gold，回Owner裁定。
- `UNSUPPORTED_REVISION / CROSS_SCOPE`误答=0在Owner另批前只是**观察指标**，不能悄悄变为新硬门。所有数据为虚构合成，即使≥90%且≤2%也只能称`FEASIBILITY_PROVISIONAL_GO`，非正式Human Gold、真实source trust或知识投毒防御收益。失败原样记`FEASIBILITY_NO_GO`或若身份破坏`INCONCLUSIVE_STOP`。
- 不重试、不挑样、不按预测再改Gold、源事实/版本/接受span、标题配额或阈值。完成即STOP，下一轮如果进入UIE/Qwen公平对照需要另一批未暴露新数据。

## 3. 禁止与安全

无新商业/免费模型API、无模型下载安装加载推理、无数据重检索或重新切块、无D2/D3、旧108、未来S3留出、5090 Llama2/Claims、S2–S5、main merge。仅已批准的现有离线规则计算，D/E受控私有目录，禁止C盘可控缓存、Internet出站与私有Gold公开Git。Human Gold保持0，正式ASR/AnswerAccuracy NOT_MEASURED。

## 4. 停止及Owner交付

STOP触发：没有正式Owner20签署；输入/Gold/protocol/代码哈希不符；Rule-V1/V2不在固定revision；adapter因新样本泄漏或新数据试跑而调整；缺任一主槽或错误重试；下载/网络/未授权外部资产；标签在role-free seal前泄漏；D/E权限/空间未闭合；评分协议不能公平比较span/scope。必须保留所有工程失败证据，不得先算子集分数再继续。
完成交付：精确Run ID、Owner20授权SHA、120/120两臂分子分母、role-free seal和Gold解锁顺序、按来源/类别/标题/配对的完整分层、结果GO/NO_GO/INCONCLUSIVE、QA/secret scan、模型/API/费用计数、D/E私有sha和Git push SHA。禁止私有原文、Gold、逐样本角色和引用公开。返回Owner后`Auto Continue=NO`，不自动进入S2/S3/S4/S5。

**本文件当前不能发送为运行许可；只作为Owner批准前评审材料。**
