# D2/D3数据与人工标注新对话交接 V1

2026-10-29（JST）；PODR-152 / OR-106 / REL-2026-0121。
Task `P1-CORE144-D2-D3-DATA-THREAD-HANDOFF-01`；base `a83437ab0a685d69114093fd4bd0e6ab22f354aa`。
Owner明确分工：**本机本项目的新Codex对话负责D2/D3数据准备和标注；原对话继续负责实验。**
本次仅准备上下文与分工，不创建新对话、不冒充外部Reviewer、不执行修题、标注或实验。

## 1. 两条工作线，审批门仍独立

| 工作线 | 负责 | 不负责 |
| --- | --- | --- |
| 新对话：D2/D3 DATA / ANNOTATION | 私有工件盘点、原件回收/锁定、既有质量门、Owner材料、获准后的Human材料准备与回收 | D1/L0/VACE实验、模型/依赖/下载、训练、阈值、测试或方法调参 |
| 原对话：EXPERIMENT | 既有D1_DEV/L0实验交接、Worker回包审计、开发性评分及方法实验治理 | 未获Owner单独批准的D2/D3数据修复、正式GT或Human验收 |

这是职责划分，不是新增科研授权。新对话可先恢复上下文和只读核查；后续操作逐门继承既有Owner决定。
不能因“负责数据”就关闭未解决质量问题、直接发Human Excel或冻结GT。
原实验5090 Cursor包仍固定源码`a83437a`，不要因本次纯文档提交要求Worker换源码或重跑。
控制端尚未核实5090执行状态或接收新L0结果；不把未收到结果写成模型失败/完成，也不臆测远端没在运行。

## 2. 正确仓库入口

使用已有唯一`research/stage6-1-hidden-poisoning`研究worktree，不在Stage1–5历史checkout上改文件。
本机绝对地址、原始证据目录、精确Reviewer六文件和可复制启动语位于独立的**Owner-only本机交接件**，不公开私有路径。
新对话先运行Git preflight，读取根AGENTS及权威恢复链；Git动态事实优先于本文固定base。
保留已知无关design修改及Master Guide PDF，禁止`git add .`、`reset --hard`、自动stash或混入其它对话变更。

## 3. D2 Finance真实起点

- 48组/144条；Human A/B尚未放行，未形成正式GT。
- [最新完成记录](PAPER1_CORE144_D2_OWNER_QA_AND_TWO_HN_REPAIR_RECORD_V1.md)：37项历史建议逐项独立审查，
  ACCEPT37 / REJECT0 / OWNER_DECISION_REQUIRED0，涉及42格；QA overlay不是GT，不覆盖R3/R4原值。
- 先封存Candidate-visible语义、再审计构造合同，确认两个原HN有非设计缺陷；仅这两条做additive最小修复。
  原题/raw/Evidence保留，其余142条未改。待复审lineage是当前候选视图，不是最终验收。
- `D2_FULL144_PREANNOTATION_ACCEPTANCE=PENDING_TARGETED_TWO_REVIEW`。
- 当前正确下一步：**原D2 R3-gpt与原D2 R4_CODEX/豆包，各仅2条Candidate-only Phase1**。
  本次核验相应归档及交接目录尚无新两条raw；不据此声称全机绝无未交回文件。
- Phase1两原件字节锁、结构及独立性门通过后，才准备正式targeted Phase2；现有Phase2仅含空Phase1值的暂扣草案。
  之后两条Phase2闭合并全144质量验收通过，才评估此前Owner的条件性Human工作簿授权，不跳门。
- 不重做37项/targeted6已完成审查，不让未改142条重复盲审；不能把旧targeted6返回当新targeted2返回。

私有命名空间标识：`core144_d2_owner_qa_contract_audit_20261016`。
原55文件封存索引SHA256：`12cf8d94b793ed4a2ca3436be8d56217c71f281d623e77e74c0b60d6995aa10c`。
新对话核验hash，不重写历史索引或因本机QA而标外部验收PASS。

## 4. D3 Information Security真实起点

- 48组/144条，Phase1已完成此前有界修复与回收；这不是Phase2/Human/数据集最终验收。
- [D3-PHASE2-S3-NECESSITY-01/-02](PAPER1_CORE144_D3_PHASE2_S3_NECESSITY_BLOCKER_V1.md)：
  两条拟S3机关比较命题含可由单份冻结官方证据独立反驳的绝对断言，导致设计的“两端必要性”不成立。
- 当前`D3_PHASE2_WITHHELD / HUMAN_DECISION_REQUIRED / AUTO_CONTINUE=NO`。
- Owner须决定两条有界最小修复、显式重分配/平衡修复或继续HOLD；本次分工不等于选择方案A。
- 获批修复也须保留旧题/新版本新ID、单源/联合必要性及定向复审链；不得裁掉反例条文或强改MULTI。
- D3全域Phase2、Human A/B与正式GT均不放行；D2通过也不会自动解锁D3。

私有冻结preflight命名空间标识：`core144_d2_d3_phase2_prep_20261007`。
原74文件索引SHA256：`2e92f682cbba6261381388f3c5b62b6cd5aa63e7c073609a4fc2ee581a03a4f9`。
`SEMANTIC_PREFLIGHT_WITNESSES_V1.json`是Owner-only反例见证，不给盲审者。

## 5. 关键阅读顺序

先读AGENTS→Authority Map→PO-MHEP→长期需求→最新Owner Register/总控/Current State→本页与下列领域记录。

1. [双轨状态V27](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V27.md)。
2. D2[语义与构造审计协议](PAPER1_CORE144_D2_OWNER_QA_AND_CONSTRUCTION_AUDIT_PROTOCOL_V1.md)、[完成记录](PAPER1_CORE144_D2_OWNER_QA_AND_TWO_HN_REPAIR_RECORD_V1.md)。
3. D3[两S3必要性阻断及Owner选项](PAPER1_CORE144_D3_PHASE2_S3_NECESSITY_BLOCKER_V1.md)。
4. [D2/D3既有Phase1闭合记录](PAPER1_CORE144_D2_D3_BOUNDED4_PHASE1_V2_RAW_LOCK_AND_QA_RECORD_V1.md)。
5. [Master Guide](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md)、[Phase2中文说明](PAPER1_CORE144_HUMAN_PHASE2_ANNOTATION_GUIDE_ZH_V1.md)。
6. [Human/Agent/Evidence文档分离与收口](../documentation_separation_contract.md)。

V4/V4.1/V4.2/V4.3、枚举和实际workbook合同不变。中文Master/Phase2手册语义可以复用，
但后者首页仍写D1答卷身份；不能因此声称D2/D3 Excel已生成、题序/证据已匹配或已批准发放。
将来放行时先核验领域自己的题文/ID/顺序/证据/字段与UX，再按Owner批准做最小适用范围说明，不重复发明语义Guide。
本轮不修改Guide、XLSX、Candidate或Evidence。

## 6. 不可丢失的语义和隔离边界

- version是否存在必须先Candidate-only判断；普通《某法》第X条规定不因证据页带版本信息而自动有version claim。
- substantive错误、version元数据、authority角色独立；host/page publisher/original issuer/adoption/revision/repost不自动等价。
- `self_containment`看对象有没有交代；`ambiguous_referent`看已有对象中的指代是否唯一，不机械联动。
- local冲突且overall事实冲突可走ZERO_EXTERNAL_EVIDENCE_REQUIRED；S3必须单份不足、联合充分，不能按target S强赋值。
- evidence_selection是实际证据使用过程，不归一为唯一GT值。
- R3-gpt实际GPT；`R4_CODEX`是保留代码，实际提供方**豆包**，不是Codex。不可再要求豆包执行Codex projectless条件。
- 仍用各领域原隔离Reviewer会话，互不可见；原会话不可用先交Owner决定，不自行新建或混用D1/D3会话。
- Reviewer/AI QA不等于Human GT；原件逐字节锁定、独立性可如实记OWNER_ATTESTED，不能写机器证明。
- Phase1不得提供证据/标签/Owner包；Phase2只在门后提供该条获准冻结证据。内部映射和修复意图不发Reviewer/Human。
- 不加载Expected评Candidate，不用D1模型输出/系数/召回率选择或修改D2/D3；保持未来独立验证的质量与家族隔离门。
- 各Human仅在自己Phase1原件验收后获自己的Phase2；A/B盲态、原答、Owner仲裁、GT冻结依次过门。

## 7. 同机并行的写入与Git约束

两对话当前可能共用同一研究checkout；**有工作分工不等于有文件系统隔离**。
新对话使用自己的新私有任务命名空间和D2/D3领域文件，不改`paper1_l0`配置/源码或D1/VACE运行/预测/评估封存。
原对话不替新对话做D2/D3裁决或修改其未提交文件。
共享Current State/Owner Register/Master/ledgers/README在提交窗口串行更新；始终保留另一工作线当前摘要。
读写前核对HEAD与dirty列表；显式逐文件stage，提交前复查diff不能混入另一线变更，不amend已推提交。
若共享文件正在被另一线改动、发现未知重叠或分叉，停止该共享文件的写入并由Owner协调，不覆盖/自动解决科研冲突。
不能自行发消息给另一对话或迁移工作树；必要时取得Owner明确授权。当前未创建新worktree/新对话或任务ID。
每次收口仍按AGENTS更新应更新的文档，不能以分工为由省略，但也不能为了文档收口抢写另一线的内容。

## 8. 新对话首轮交付与停止条件

首轮先报告：Git/worktree、两域各48/144身份与现有工件hash、D2 targeted2收件状态、D3未决选项、
当前可发/暂扣材料、哪些还需Owner决定。初始不执行修复或制作可发Human XLSX。
对D2可以给既有已批准Phase1两题的精确清单；无新raw时停外部回收门，不编造Reviewer返回。
对D3只提交既有阻断的决策材料，等Owner有界授权。
禁止正式split、GT冻结、Detector/LLM训练、L0/D1实验、模型下载、阈值调参或把D1已暴露集重称untouched test。

## 9. FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW与交接验证

主要风险是共享checkout同时写入、把旧QA误当验收、实验反馈污染待验证领域、把Reviewer身份或Phase1/2材料混发。
本交接以双线摘要、显式stage/串行提交、原会话/精确三文件清单、D2/D3各自硬门和独立原件索引降低风险。
若需要新的worktree、Reviewer会话、D3修复或科研协议选择，先按既有Owner门处理，本次不擅自增加方案。
旧治理测试初跑90通过/7失败；相同7项在不可变basea83437a均有相同失败，涉及旧文档约束、路径和词形扫描。
这些历史失败未获豁免、未改成PASS，也不通过重写历史消除；交接新增内容单独做范围内验证，并把旧技术债保留给新对话。
本轮不修改长期需求、Research Plan Authority、Guide、原数据或任何实验合同；没有新增科学结论或accepted lesson。

状态：`D2_D3_DATA_THREAD_HANDOFF_READY / WAITING_FOR_OWNER_TO_OPEN_THREAD`。
领域门仍为`D2_PENDING_TARGETED_TWO_REVIEW / D3_OWNER_DECISION_REQUIRED`；不是D2/D3验收PASS。
