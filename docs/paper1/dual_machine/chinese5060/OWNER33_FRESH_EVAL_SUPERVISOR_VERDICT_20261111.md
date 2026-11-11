# Paper1｜Owner33 V-CARE 新中文事实盲评：监督复核与研究路线裁决

日期：2026-11-11 JST。状态：`SUPERVISOR_VERIFIED_PUBLIC_EVIDENCE / OWNER33_METHOD_EVAL_NO_GO / AGENT_PROVISIONAL / HUMAN_GOLD_0 / NO_NEW_SCIENCE_AUTH`。

## 核实的来源链
- 5060 SCIENCE `research/paper1-chinese-defense-5060@108b35c9239ad113c50f7d84daf9b84f361b37d6`，方法冻结 `11880c5be71e22d73217c32e0c779fbf8b117741`；`docs/paper1/dual_machine/chinese5060/OWNER33_VCARE_DEV_RESULT.md`和`owner33_eval/OWNER33_EVAL_PREDICTION_HANDOFF.md`。
- 5090独立一次评分 `research/paper1-ragdefender-repro-5090@d7d28cc7cab25b1ade04fcb8b0678bd369c3b558`，`docs/paper1/dual_machine/repro5090/owner33_eval/OWNER33_EVAL_SCORE_REPORT.md`和`OWNER33_EVAL_SCORE_MANIFEST.json`。输入rolefree SHA `fccae2a0967b7bcefe051849c5b8d65d930e8954abe3c4ffb1b4a53daf03cf0c`，5060 prediction `7082eba17608c8d8ee6d93a591b4c74fdb017e295558e76f1b1867e712a8ccd8`，TopK `861cb132b70b133bda4db3e493a11cecf07be4cd75f3cf3ebcce2c70d5174205`；由报告中的SHA链相互核对，不代表监督者读取5090本机private Gold。私有Gold始终0人签。
- 5060最初回传认为5090远端仍在11242...，这是时间上的旧HEAD；已核5090最新为d7d...并完成评分，不能在Tracker写“SCORE_PENDING”。

## 真实对照指标

| 批次 | 指标 | RD_B2 | V-CARE | B2+同预算补检/强消融 |
| --- | --- | ---: | ---: | ---: |
| 旧Owner27 DEV | P保留/已召回 | 20/45 | 7/45 | ALWAYS_VERIFY 7/45；RETRIEVAL_ONLY 20/45 |
| 旧Owner27 DEV | Clean误删/已召回 | 40/63 | 10/63 | ALWAYS_VERIFY 40/63；RETRIEVAL_ONLY 40/63 |
| 旧Owner27 DEV | HN误删/已召回 | 4/33 | 4/33 | 两臂均4/33 |
| 全新5090 EVAL | P保留/已召回 | 11/34 | 11/34 | 11/34 |
| 全新5090 EVAL | Clean误删/已召回 | 35/59 | 35/59 | 35/59 |
| 全新5090 EVAL | H历史误删/已召回 | 0/1 | 0/1 | 0/1 |
| 全新5090 EVAL | O其他scope删除/已召回 | 8/8 | 8/8 | 8/8 |
| 全新5090 EVAL | B背景删除/已召回 | 4/58 | 4/58 | 4/58 |
| 全新5090 EVAL | B2掩码差异世界 | — | 0/32 | 0/32 |
| 全新5090 EVAL | 逻辑补检/命中 | 0/0 | 32/0 | 32/0 |

两批各32个世界但各自只包含4个事实组；不能把世界/槽位当独立统计单位。EVAL投放P48/C84/H12/O16/B192，实际进入TopK5 P34/C59/H1/O8/B58。不能只报告H=0/1而隐藏O=8/8被删；合法其他scope是本研究的重要误删类型，但报告单列并严谨区分定义。EVAL 32world均触发了逻辑补检，0次查到可用来源，算法同B2且不产生额外答案支持。没有新的Qwen回答层调用，formal ASR/Accuracy NOT_MEASURED。

## 科学判读：不是方法裁决证明正确，而是前端覆盖失效
- 冻结源码 `src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner33_vcare.py` 的 `intent()` **实际写死**三个属性族：statutory_days（节日）、permit_issuer（旅馆卫生许可签发主体）、application_age_max（大型客车申请年龄）。而新EVAL四事实族为 `CONSUMER_DISTANCE_RETURN`、`ENV_DAILY_PENALTY_START`、`OGI_APPLICATION_REPLY`、`PIT_COMPREHENSIVE_BASIC`，均不属于这三个分支。508/5090独立报告相互吻合地给出`recognized_intents=0/32`。所以更精确的诊断是**跨领域查询意图覆盖缺失导致系统零启动**，而不只是版本判断能力差。现有代码对陌生领域`intent=None`即无anchor回退B2。
- DEV相对B2减少的P13 **并非完全属于V-CARE独有贡献**，因为DEV的同预算`B2_ALWAYS_VERIFY`也将P保留降到7/45。V-CARE在DEV上的可区分贡献主要是同样P和H下，Clean误删40/63→10/63的有限证据恢复；这还依赖旧DEV官方来源索引，**不能算独立事实泛化**。No-rescue消融也为Clean40/63，说明保全分支在旧领域有效；no-scope误删HN3/33略低于FULL4/33，说明scope消融没有额外HN保护收益。该结果不是“完整V-CARE机制已证明”。
- 本次EVAL给出`METHOD_EVAL_NO_GO`的充分证据（完全同B2、来源0/32、消融无差异），但没有实验识别该方法在其他新领域具备通用证据入库时的有效性。这不是推广成功的借口，也不能把当前测试集再改为未见测试重跑。
- 失败归因应登记为`CROSS_DOMAIN_INTENT_COVERAGE_FAILURE`、`NO_EXTERNAL_REFERENCE_HIT`、`NO_MASK_DELTA`、`EQUAL_BUDGET_B2_NOT_BEATEN`；不是`SCIENCE_NOT_RUN`、`HUMAN_GOLD_AVAILABLE`或`QWEN_ASR_IMPROVED`。

## 下一步：有限、非科学分析优先；新研究需要Owner一次新授权
1. **今天先做只读工程根因审计**：在不改5090 EVAL和不重新执行科学预测的条件下，用已公开rolefree的query和独立source index，仅统计解析失败类型、规范字段命名/字段缺失、索引通用字段覆盖率、按事实组的O/H分布，归档静态审计。不得依据看到Gold调整旧V-CARE源码再用这批EVAL称holdout。
2. 若Owner仍决定创新，将原EVAL视为**已曝光诊断数据**；为下一批设计通用、无Gold的`entity/property/time/scope`映射，必须通过新领域无标签单测与source覆盖率门（至少80%可解析，至少50%有非Oracle独立source候选才允许一轮离线DEV），再用**真正新的**来源谱系独立blind EVAL一次。不能套壳修这四个领域的正则后冒充通用方法。
3. **高价值但不构成完整GO**：保留跨域覆盖失效这个机制负结果；反复更换regex/数据对照无法建立可发表防御算法。考虑是否限时转成“跨域适用性检测+可审计外证更新”的系统性研究，但需预算、文献新颖性、公平比较、独立样本。
4. 未来真正正式实验仍需独立HumanGold、可信来源权利核验、同预算检索强基线、生成答案ASR/正确率/拒答、聚类抽样。当前未进行这些步骤时只使用`AGENT_PROVISIONAL`。

**治理**：本文件是监督复审的只读记录，**不**自动解封新科学试次，不改Owner33 DEV/预测/评分任何一字节。Owner33 STOP，AUTO_CONTINUE=NO，D2/D3/HOLD8、5090 Claims1–3、main merge继续禁止。
