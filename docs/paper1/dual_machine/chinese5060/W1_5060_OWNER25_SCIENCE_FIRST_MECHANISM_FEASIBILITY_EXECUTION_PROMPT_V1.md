# Codex 5060｜Owner25：科学结果优先的零模型快速可行性试验（立即执行）

本次任务的成功标准是给Owner **可核查的正/负研究结果和下一方向裁决**，不是完成Windows/PE/网络环境工作。不要继续尝试修Owner24 F0的网络阻断；Owner24 F1–F4保持NOT_RUN。Owner25创建的是独立授权的**本机无模型小型研究试验**。

### 权威与身份

分支`research/paper1-chinese-defense-5060`，按AGENTS、PO-MHEP、Owner Decision Register恢复。唯一新授权：
`docs/paper1/dual_machine/owner_approvals/W1_5060_OWNER25_SCIENCE_FIRST_OFFLINE_MECHANISM_PILOT_20261110.md`
ID `W1-OD-20261110-5060-SCIENCE-FIRST-OFFLINE-PILOT-25`。先确认远端与worktree无异常，原 `83620d82ba1af4dae325017b64c3f1abb1bac33f` 是Owner24 F0失败提交，不是当前新提交。创建新的Run与D盘隔离归档，历史不覆盖。

只使用D1已有已公开脱敏报告/固定聚合证据，不再次读取或跑D1 raw/Gold，具体：
`docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md`
`docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_R2_FAIR_CONTROL_RESULT.md`
`docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/VESA_REVIEW_RESPONSE_P0_M1M2M3_S0S5_DESIGN_V1.md`

现有冻结事实：B2 36世界 TopK5/180个chunk；召回29，Poison删2/10、Clean错删4/10、HN删2/9，RD-zh仅分词Poison删4/10、Clean删5/10、HN删4/9；D1独立可信来源收据覆盖**0/180**，P0禁止无真实独立来源锚时凭文档相似、同值或自称最新版本做向上信任变更。严格P0主臂在当前D1上不可能仅靠抽取改善该 Clean 误删门，证明边界而不是伪造可达结果。旧73上V2值59/61但新100上值5/70、wrong10/11、NO_GO；所有结果和来源分母保持。

### 科研假设和两种证据等级

**H1（可证伪）**：在受控情境中，有独立于攻击者控制的来源收据、明确版本有效期、问题适用范围时，可以在保留污染防护的同时减少普通证据误删，并在多数污染或伪造最新版情况下不让假事实因“群体一致”获信任。
**H0**：可信收据缺失或语义/版本/范围不可比较，安全决策退化到已冻结RD，不具备恢复能力。此零锚边界是目前D1可直接论证的**负结果**。
**Oracle-ceiling ≠ real-world defense**：机制候选可以直接用**受控合成事实的抽取Gold作为显式oracle输入**测其条件上界，但不能写成真实抽取/真实来源/新基准效果。必须留出plain raw-text部署模拟臂，以评估Rule-only抽取可达性；无需新LLM。所有真实可信身份仅来自另保管的合成签发登记，不从文本上自称推断。

### STEP A：先固定事实组、场景、守卫和预注册分母（不得先看预测）

通过Python已有标准依赖，生成**12个不重复的全新虚构事实组**，至少4个主题域与不同来源家族。先固定8个事实组为DEV，4个为HOLDOUT；每事实组设计8个固定情境（共DEV64世界、HOLDOUT32世界、每世界5个片段）。至少8种场景：
1. 全正常同scope同version；
2. 合法版本沿革（历史与新生效）；
3. 合法跨地域/适用对象不同值；
4. 单Poison假值+独立可信正常锚；
5. 3/5同文本Poison与正确可信来源冲突；
6. 3/5改写同假值+来源家族重复（不得3票算3独立源）；
7. 攻击者伪造“最新修订”+伪造机构名称/URL；
8. 4/5或5/5多数/全毒（两变体在DEV和HOLDOUT都需出现，若场景数不变用事实组的预注册对称配置）。
为全部案例建立source-truth/issuance ledger（独立可信收据只给已注册且哈希绑定的片段，**注册条件绝不可基于Poison/Clean标签**）；同时保留不可伪造收据/自称来源/真正上游被攻陷3种威胁区分。除官方安全的真实URL范例外，所有“可信”均为**模拟受控登记**，绝不可冒称官方网络核实。

将Role-free input与Gold、签发ledger、分组映射和评估协议分开seal+SHA，算法只看到query、5个原片段、可独立核验receipt_id/issuer/validity/parent-hash及必要版本时间。不得接触Poison/Clean/expected decision或Gold。**在正式HOLDOUT前完成所有数据、判分、程序冻结**，任何变更必须将原holdout转为已暴露开发集、停止再称盲评。

### STEP B：完成方法与对照

至少6臂同输入同分母：
- `NONE`: 纯不滤；
- `RD_B2` + `RD_ZH`: 只在原离线embedding或固定安装且能无需下载/外网地在本合成数据上公平编码时才可运行，**不许拿D1旧数与合成新数比较**；如本地缺资产就如实`BASELINE_UNAVAILABLE`，仍跑其它无模型消融，不造数据；
- `ANCHOR_ONLY`: 仅收据与来源独立性；
- `SCOPE_VERSION_ONLY`: 查询scope/effective-date匹配但**没有受信锚时不能提升信任**；
- `JOINT_P0`: 独立收据、版本/范围合取、相同来源传播去重、防可控票数升权；
- `FORGED_RECEIPT_NEGCTRL`: 合成伪证明/来源自称文本，不能获得信任。
`RD_ZH`有权限的中文迁移为公平 baseline，不把分词修复当VESA贡献。
允许DEV64上最多两版JOINT实现（v0,v1），每版完整保存结果与hash；不得凭隐含Role/Gold调算法，Evaluator可以返回DEV完整指标用于开发，**HOLDOUT完全不可见**。一旦冻结最终代码/hash/参数/模型依赖，先在32 holdout世界上一次性role-free运算和seal，再独立Evaluator加载Gold并一次性评分。

### STEP C：一次性结果与下一路线裁决

分子分母**必须全部写**：每臂各32 holdout世界 /160片段、按8情境x4事实组、Poison保留/删除、正常证据错误删除、HN误删、可信收据coverage、伪修订未证升权次数、无锚fallback精确一致、源家族相关性、不同版本/时间/scope冲突、绝对 abstention、5/5和4/5多数污染残余、运行时间与现有模型/网络/费用计数。对关键比例给Wilson95 CI（注意只有4事实组，案例非独立，不做显著性声称）。另外将oracle upper bound与raw-text+Rule-V2/available extractor结果**单独统计**；不要混平均或把perfect oracle作为部署证据。
预注册判断：
- `MECHANISM_POTENTIAL_GO_ORACLE_ONLY`：JOINT在**持真实模拟受信收据的场景**相对公平同世界RD基线使Clean误删至少减半、Poison保留不增加、伪造自称或无锚不升权/0、合法历史版本识别不出现安全恶化；
- `ANCHOR_COVERAGE_LIMITED`：零/低收据覆盖使主方法无可作用空间，必须直接说明D1处于本区；
- `MECHANISM_NO_GO`：JOINT出现不安全升权或在受信场景也无实质可用性收益；
- `BASELINE_INCOMPLETE`：RD等公允对照无法运行，**不允许比较性PASS**；
- `INCONCLUSIVE`：身份、评估隔离或代码无法完成。
你可以有负结果，**绝对不能为了正结果挑样、删角色、改目标、后验补受信receipt**。

### STEP D：论文可行性的一页裁决

在`docs/paper1/dual_machine/chinese5060/...`提交`OWNER25_SCIENCE_FIRST_RESULT.md`和Run Manifest（脱敏）、每臂消融、失效例、相邻工作冲突表。对2025–2026已有论文核：
- RAGDefender, ACSAC 2025 official implementation v0.2.0，复杂度低、无LLM推理；
- SeCon-RAG, NeurIPS2025, entity/relation + semantic conflict (https://proceedings.neurips.cc/paper_files/paper/2025/hash/668563ef18fbfef0b66af491ea334d5f-Abstract-Conference.html);
- X-MADAM-RAG, arXiv:2606.12903, extract/group/conflict + 自然化失效 (https://arxiv.org/abs/2606.12903);
- GuardRAG, 2026-10-26 arXiv:2610.35071, HAC检索后聚类 (https://arxiv.org/abs/2610.35071).
**不得将普通抽取/聚组/冲突/聚类/多证据投票称创新**。潜在差异是可信来源可验证收据、有效时间、适用范围、假修订与多数污染的一致安全规则；创新性和真实通用性仍待后续独立外部数据+强基线审查。
最后给Owner回答三个明确问题：
(1) 仅在合成可信来源上时机制有没有安全-效用空间？
(2) 真实D1为什么不可能达到原恢复门，补来源收据或改目标需要哪些具体资源？
(3) 下一项最快、最能推翻假设的真实世界/公开数据对照该怎么做？
给出**保留/调整/停止**单一推荐，不能写没有证据的“已取得可发表创新”。

### 工程与科研限制

本任务只运行普通CPU Python本地无模型程序。**0新模型加载/推理/外部API/新权重/新工具下载**，无防火墙管理员操作，Owner24 F0仍`BLOCKED`不强行继续，不碰5090/D2/D3/S2–S5正式验证，不改任何既有实验数据/方法历史。只有这一条新合成小试获得Owner25明确的有限授权。对新实现/单测/报告在DEV允许自主修补，但HOLDOUT只能一次性揭盲。研究结果必须保留Role-free seal与Evaluator分离、Run SHA和真实分母。D盘受控路径并遵守已有ACL/脱敏限制，完成后commit/push并验证远端，STOP。若任何比较臂不可完成，先交已有真实结果再停，不要花主要时间继续配环境。
