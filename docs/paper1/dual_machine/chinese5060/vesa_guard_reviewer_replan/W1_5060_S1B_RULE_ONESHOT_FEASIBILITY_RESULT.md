# 5060｜Owner20 S1-B 单次规则可行性结果

2026-11-10 JST · **`FEASIBILITY_NO_GO / S2_S5_LOCKED / AUTO_CONTINUE=NO`**。Run `W1-5060-S1B-RULE-ONESHOT-20261110-01`。两臂各完成 120/120 条冻结输入，只消耗一次主集对照。两个规则的值命中均低于 63/70，已决定错抽率均高于 2%。这些是合成可行性证据，标记 `AGENT_GENERATED_PROVISIONAL_FEASIBILITY / NOT_INDEPENDENT_AUTHOR / NOT_HUMAN_GOLD`。

## 主 100 个语义案例

| 预注册指标 | Rule-V1 | Rule-V2 |
| --- | ---: | ---: |
| 完整正确 / 错误 / UNKNOWN / ERROR | 0 / 2 / 98 / 0 | 1 / 10 / 89 / 0 |
| 值和单位命中（95% Wilson） | 0/70（0.00%–5.20%） | 5/70（3.09%–15.66%） |
| 错抽 / 已决定（95% Wilson） | 2/2（34.24%–100.00%） | 10/11（62.26%–98.38%） |
| 错抽 / 主集（95% Wilson） | 2/100（0.55%–7.00%） | 10/100（5.52%–17.44%） |
| 覆盖 / 拒识 | 2/100 / 98/100 | 11/100 / 89/100 |
| 可答而 UNKNOWN | 70/70 | 64/70 |
| 应拒识而给答 | 2/30 | 5/30 |
| 严格 scope / span 支持 | 0/100 / 0/100 | 1/100 / 1/100 |

Rule-V2 多命中 5 个值，只有 1 个达到严格正确。V1→V2 配对为 UNKNOWN→正确 1、UNKNOWN→错误 8、UNKNOWN→UNKNOWN 89、错误→错误 2。决定数由 2 增至 11，主集错误由 2 增至 10。V1 决定分母很小，不能用两者决定后错抽率的点估计声称 V2 更安全。

| 主集分层（每类 10，7 可答） | V1 完整状态四元组 · 值命中 | V2 完整状态四元组 · 值命中 |
| --- | ---: | ---: |
| 时效 | 0 / 1 / 9 / 0 · 0/7 | 0 / 1 / 9 / 0 · 0/7 |
| 跨范围同值 | 0 / 0 / 10 / 0 · 0/7 | 0 / 1 / 9 / 0 · 1/7 |
| 等价证据 | 0 / 1 / 9 / 0 · 0/7 | 0 / 1 / 9 / 0 · 0/7 |
| 多段绑定 | 0 / 0 / 10 / 0 · 0/7 | 0 / 3 / 7 / 0 · 3/7 |
| 网页导航 | 0 / 0 / 10 / 0 · 0/7 | 0 / 0 / 10 / 0 · 0/7 |
| 否定例外 | 0 / 0 / 10 / 0 · 0/7 | 1 / 1 / 8 / 0 · 1/7 |
| 重复与冲突 | 0 / 0 / 10 / 0 · 0/7 | 0 / 0 / 10 / 0 · 0/7 |
| 标量 | 0 / 0 / 10 / 0 · 0/7 | 0 / 0 / 10 / 0 · 0/7 |
| 适用范围 | 0 / 0 / 10 / 0 · 0/7 | 0 / 2 / 8 / 0 · 0/7 |
| 未证修订 | 0 / 0 / 10 / 0 · 0/7 | 0 / 1 / 9 / 0 · 0/7 |

10 类中 V1 的值命中均为 0。V2 七类为 0，跨范围同值 1/7、否定例外 1/7、多段绑定 3/7。多段绑定的 3 次值命中均缺完整支持，因此严格正确为 0。4 主题域、10 来源家族（匿名编码）、全部率的 Wilson 区间见[脱敏 Run Manifest](W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_RUN_MANIFEST.json)。

- **标题压力测试。** 30 条无标题主案例中有 21 条可答，两臂 30/30 均 UNKNOWN、0/21 值命中。70 条有标题主案例中有 49 条可答，V1 值命中 0/49、2 次错误决定，V2 值命中 5/49、1 完整正确、10 错误。V2 的 70 次查询识别类 UNKNOWN 含 30 条无标题和 40 条有标题，标题风险无法解释全部漏答。
- **20 条从属视图。** V1 为 0 正确、0 错误、20 UNKNOWN，配对均 UNKNOWN→UNKNOWN。V2 为 0 正确、1 错误、19 UNKNOWN，19 对 UNKNOWN→UNKNOWN，1 对错误→错误且两边值均命中。改写仅换问句，证据固定，全部从属例都可回答。
- **完整错误归因。** V1 两次错误都是在应拒识例给答，其中一条跨范围，一条目标日期范围未绑定。V2 的 10 次错误包含 5 次应拒识误答（缺支持 3、目标日期未绑定 1、未证修订 1）及 5 次可答例严格失败。5 个可答失败均未满足支持集合，其中 1 个值或单位错误、其余 4 个值命中。归因维度可重叠。保守追溯识别出 V1 与 V2 跨范围误答分别 1 次和 5 次，未证修订误答分别 0 次和 1 次，未把无法定位的输出归为已证实来源。逐视图原始输出、缺字段与失败标签保留在私有归档。
- **拒识归因。** V1 的 98 个主 UNKNOWN 分为查询主体或属性未识别 93、多个范围事实 4、未抽出标量 1。V2 的 89 个主 UNKNOWN 分为查询主体或属性歧义 70、多个不可比候选 11、没有绑定的有效候选 8。额外视图逐类原因见 Manifest。

## 预检、执行和时序

Context Recovery / FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW。Paper 1 优先验证中文 RAG 隐蔽事实投毒研究的可行性，RAG Security 优先于评估平台、Guard 与 Agent Security。复核 AGENTS、权威地图、PO-MHEP、R1/R2、治理及冻结证据。5060 独立发布检出在干净状态快进到 `1d6b1ab89dbc3e3f9e902259b7451167fea5950a`，与远端一致。原检出分叉且保持原状。Owner20 只放行本次冻结规则对照，S1 原失败、R2 K1-C、Owner19 封存、D1 开发定位及 P0 不升权保留。前置风险为同作者、标题依赖、词面和合成来源偏差，以及两臂原生证据粒度不同。 [Owner20 授权](../../owner_approvals/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_AUTHORIZATION_20261110.md)

独立保管进程只返回哈希，核对五档 ZIP、11 个成员和封存回执。预检两臂各读旧开发 73 条角色盲输入，无技术错误；用合成单测验证等价窗口、跨范围同值、跨段、无跨度和宽跨度拒绝。统一适配器只转发原生字段、主跨度和唯一匹配的已选候选所提供的范围跨度。没有联合相邻跨度、扩窗或从暂定标签回填。两臂统一按支持集合间 OR、集合内 AND 严格判分。V1 的原生单跨度和 V2 的额外候选范围跨度如实保留。早期预检保留了控制包顺序检查误写和 MyPy 类型问题，均在冻结代码与主样本运行前处理，历史包未改动。最终 4 项单测、Ruff、MyPy 通过。

- 冻结代码 `c31e696f1a9432f6264f4fb8e4b26cab8e933ac5` 在试验前已推送核验。固定 Rule-V1 `68d34a5d877206f4e6d7d9e2bdda16784145a76a`，Rule-V2 `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`。适配器、评分器、依赖源码、运行参数和 Python 3.12.14 二进制 SHA 见 release。
- 预测封存 10:25:16.592 JST，独立只读确认 10:25:16.842，Gold 揭盲 10:25:17.507。四个角色进程 PID 分离，预测与确认阶段 Gold 读取均为 0。执行命令、退出码、stdout/stderr 及时间戳均封存。
- 原数据 Seal `531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`。双臂预测封存 SHA256 `a6b84efd8dff172732e4503ffb3c93aca64ec2ed034060a883017e14056ca4e7`。
- 私有归档 SHA256 `f991e6e2fd3379c66412b061a2f9377b92f720783041c2253bd8374b59d65110`，私有 Run Manifest SHA256 `c0f8e7e6d806177dbab9d8ab01cde488f36598d773dcfe0f28a8b2d36586f17c`。D 盘 `experiments/paper1_chinese5060/W1-5060-S1B-RULE-ONESHOT-20261110-01`，归档 47 件。公开 Git 只发布实现、普通测试、脱敏结果及哈希。
- 科学试次 1，重试 0，下载、依赖安装、模型推理、模型 API、实验联网与费用均为 0。正式 ASR / Answer Accuracy 未测，Human Gold 为 0。本批未重跑 D1 或历史生成。

Current Work State、Project Master、Experiment Master、Execution Log、Week 1 Tracker 与 Human/Agent Ledger 已同步。没有新 Owner 决策、阶段转换、正式方法验收或研究路线变化，Owner Register、Stage Process、Lessons、Plan、README 保持历史。下一步只等待 Owner 决策，S2–S5、模型、5090 Claims 保持锁定。

## DOCUMENTATION_CLOSEOUT_CHECKLIST

```text
human_ledger_checked=true
human_ledger_updated_if_required=true
agent_ledger_checked=true
agent_ledger_updated=true
current_work_state_updated=true
execution_log_appended=true
experiment_master_condition_evaluated=true
owner_decision_condition_evaluated=true
stage_process_condition_evaluated=true
lessons_condition_evaluated=true
research_authority_condition_evaluated=true
README_condition_evaluated=true
cross_document_current_task_consistent=true
cross_document_status_consistent=true
cross_document_next_action_consistent=true
cross_document_blocker_consistent=true
markdown_links_valid=true
```
