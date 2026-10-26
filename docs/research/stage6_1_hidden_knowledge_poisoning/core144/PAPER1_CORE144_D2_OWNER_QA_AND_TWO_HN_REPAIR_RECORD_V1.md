# D2 Owner语义QA、构造合同审计与两条HN最小修复 V1

2026-10-16；任务 `P1-CORE144-D2-PHASE2-OWNER-SEMANTIC-ADJUDICATION-AND-CONSTRUCTION-CONTRACT-AUDIT-01`。
源HEAD `484b04bb6f59b1c7edbe4cb488019c94b774c95c`；PODR-142 / OR-096 / REL-2026-0111。
[执行前协议](PAPER1_CORE144_D2_OWNER_QA_AND_CONSTRUCTION_AUDIT_PROTOCOL_V1.md)。

## 已完成与未完成

37项历史作者建议独立核对后，ACCEPT37 / REJECT0 / OWNER_DECISION_REQUIRED0，涉及42格。
这不是按原建议或两模型多数自动接受：逐项保留原R3/R4值、题文命题、冻结证据原文span、
规则SHA、独立理由及disposition。字段QA overlay不覆盖原答，不是Human GT。
两份targeted6原字节SHA继续为
`e83c3b0d8abbd5a3e00f18e2b47a99591cdebde399259789660838daf2e711cb` /
`3085bdc7be45a061acef348d26baf0fbb0eeb1b3b9b4a7764c35cf1f12a829bf`。
旧79/18/74份及targeted6封存索引复验；25份官方快照、提取正文和V3摘录原文投影一致。

先封存可见语义，再加载两条指定题的私有构造合同。语义锁SHA
`814c92c25b9641244efd64f475ae4260b1c57b1e8fea7afa9475ec84ceddc3e7`。
先后时间和哈希均在新私有记录中，不能用后读的角色改变原事实判断。

## 六条Owner意见的执行

- 三条明示修改决定/修订身份/生效转换的版本字段均为PRESENT_CORRECT。
  已有V4.2/V4.3执行，不修Guide、不重审、不改三条题文。
- 银行业完整第二条已支持当前事实一致；E1或E1+E2是各自真实阅读过程，不归一为真值。
- 会议载体题：原题整体INSUFFICIENT_EVIDENCE、phase2_issue=EVIDENCE_MISSING；
  authority独立PRESENT_CORRECT。V4.1 B及对应一致性规则问向机关归属的角色/权限，
  Master Guide17同样问谁通过/公布，没有明确把所有载体存在/内容纳入该字段。
  令826号支持国务院通过/公布身份；未支持另一个独立会议记录载体，不等于该记录不存在。
- 其他服务题：原题整体FACTUAL_CONFLICT、ONE_OFFICIAL_EVIDENCE、phase2_issue=NONE，
  version/authority均NOT_PRESENT。第十条第一、二、五项另设服务类别税率，原字面范围过宽。
  多个服务反例是同一范围泛化问题，不自动算多个secondary errors。

`evidence_selection`始终保留双方过程差异；本轮没有生成唯一过程值或Human答案。

## 构造合同审计后才决定修题

两条原始角色都为Hard Negative，不是controlled Poison。
一条漏掉6%服务范围的法定排除，一条附加了未获支持的独立载体主张，均不满足HN fully-supported合同。
历史数值原子检查漏掉了完整句子的条件范围/附加事实，旧PASS记录保留但不能覆盖本次字面发现。

按Owner本次条件授权，仅两条HN分别最小补齐排除范围、把附加载体改为同一冻结令中可见的信息。
新V2与新opaque ID；原题、原raw、旧atoms和证据全保留。其余142条不变，Clean/Poison零修改，
源/版本/事实核心/三元组/中性查询/证据映射不变。两个组原Poison的S1/S3机制与路径仍独立成立。
修复后五个完整命题原子逐一有冻结原文见证；只是作者本地QA，不是外部验收。
两组字符长度最大比约1.146、1.014；两句结构保留，未引入全局固定角色模板。
自包含、指代与自然度本地检查完成，仍须原两会话复审，不以本机判断冒充Reviewer。

## 当前真实门控

`D2_FULL144_PREANNOTATION_ACCEPTANCE=PENDING_TARGETED_TWO_REVIEW`，不是PASS。
48组/144条及48/48/48角色规模保持；完整最终验收留到两条新题Phase1/2通过后。
37项处置已闭合，尚待：两条Phase1外部raw及锁定、两条Phase2外部raw及锁定、最终144验收。
本轮没有生成D2 Human A/B可发工作簿；Phase2仅生成含待填Phase1值的封存草案，绝不提前发送。
不改V4–V4.3/枚举、不补新源、不读Expected/Human标签，不切分/训练/调参，不推进D1/D3。

## 私有产物和发放方式

私有命名空间 `experiments/core144_d2_owner_qa_contract_audit_20261016/`：

- `semantic_lock_v1/HISTORICAL37_INDEPENDENT_DISPOSITIONS_V1.json`：37项逐条审查。
- `semantic_lock_v1/OWNER_QA_FIELD_OVERLAY_V1.json`：43条QA overlay，before/after/依据/Owner谱系完整。
- `construction_repair_v1/PRIVATE_TWO_CONSTRUCTION_CONTRACT_AUDIT_V1.json`：两条角色/atoms/三元组合同。
- `construction_repair_v1/ADDITIVE_TWO_HN_REPAIR_LEDGER_V1.json`：旧新版本与修复理由。
- `construction_repair_v1/CURRENT144_REPAIR_PENDING_LINEAGE_V2.json`：仅两条替换、142条不变，待复审。
- `construction_repair_v1/reviewer_release_phase1/`：R3_GPT/R4_CODEX各仅题包、Schema、提示词三件。
- `construction_repair_v1/withheld_phase2/`：不得发送的Phase2草案。
- `OWNER_ONLY_REVIEW_AND_REPAIR_REPORT_V1.md`：Owner完整审查/证据阅读入口。

Reviewer交接目录标识 `paper1_core144_d2_owner_targeted2_20261016`，R3_GPT/R4_CODEX各自子目录。
Owner私有目录另为 `paper1_core144_d2_owner_qa_contract_audit_20261016`，不得混发。
继续**原D2**独立GPT/豆包会话；R4_CODEX只是历史代码，实际提供方豆包。
若原会话不可用，先报告Owner，不擅自换会话，也不套用Codex projectless运行条件。
不用重审其余142条。三个文件逐一地址与回收文件名见私有中文发放清单。

## 本轮验证边界

2026-10-27续接交接/Git收口：55份工件封存索引SHA
`12cf8d94b793ed4a2ca3436be8d56217c71f281d623e77e74c0b60d6995aa10c`已复验。
旧封存内容不重算/覆盖；后续交接与Git回执独立post-seal保留，外部复审门不变。

41项实际工件检查及26项相关合成测试通过，任务Ruff/MyPy、UTF-8、
新增公开内容secret/private-path与链接、git diff --check通过。
首次合成测试遇隔离TEMP目录写权限错误，已记录并使用任务内临时目录重跑；不改系统配置。
没有跑全仓测试，也没有用本地QA代替两个外部复审或最终144验收。
Stage1–5/Final72/原Guide/旧证据/原raw不变；原有design修改/PDF保持原SHA且不提交。

[状态V17](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V17.md)，
[文档收口](PAPER1_CORE144_D2_OWNER_QA_DOCUMENTATION_CLOSEOUT_V1.md)。
`D2_OWNER_SEMANTIC_QA_COMPLETE / TWO_HN_MINIMAL_REPAIRS_PREPARED / STOP_EXTERNAL_TARGETED_REVIEW_REQUIRED / NO_HUMAN_RELEASE / NO_GT`。
