# D1 Human Phase2 — 原件锁定与单份回收检查 V1

2026-10-16；`P1-CORE144-D1-HUMAN-DUAL-PHASE2-RAW-LOCK-AND-COMPARISON-01`。
Source HEAD `5d66be1c55c46621ce8ea3a50d6cdc96a08ae824`；PODR-139 / OR-093 / REL-2026-0108。
分类：`HUMAN_RETURN_RECEIPT / READ_ONLY_DIAGNOSTIC / OWNER_GATE_PENDING`，不是仲裁或GT。

## 原件与单份检查

两份XLSX先原字节复制、锁只读属性/清单，再解析。原文件未重存、改写、排序或清洗。
Owner直接确认同一位A/B独立完成各自两阶段、仅用获准冻结材料、未看对方答案/新增搜索/AI，
接收后未改原件。记为 `OWNER_ATTESTED`，非机器证明。收到文件名含 `(1)`，保留名称偏差，身份依内容核验。

| 检查 | HUMAN-A01 | HUMAN-B01 |
| --- | --- | --- |
| 原始字节数 | 200781 | 217867 |
| SHA256 | `75b444a135c9b7df01a494912047ec2a2513f8552befaecc572a91760c5ca45e` | `b66984a7247d7dff86492cef48549506bd743a511710fd0dfcab9c348d648052` |
| 记录/唯一ID | 144/144 | 144/144 |
| 本人题号/题序/题文/表头/已锁Phase1身份 | 精确一致 | 精确一致 |
| 合法分类格/非空必填理由 | 1152/1152；144/144 | 1152/1152；144/144 |
| minimum等机械跨字段违规 | 0 | 0 |
| 固定单元格实质文字变化 | 0 | 0 |
| 固定单元格首尾空白变化 | 123 | 0 |
| None/空字符串存储差异 | 0 | 315 |
| 严格只读回收门 | 暂扣 | PASS |

十个sheet、144×20填写区、下拉值覆盖一致；ZIP CRC通过、无宏/嵌入对象/外部工作簿链接。
原有公式/原生超链接相同，标注区没有隐藏行列。未打开URL，未加载mapping、Expected、GT、
构造角色或其他Reviewer答案。阶段判定只是本人独立的回收诊断，不是事实准确性验收。

## 文件边界与待批准事项

A01的123格逐格核实为首尾空格/换行变化，标注表60格涉及48行，冻结证据全文63格，
全部满足 `before.strip() == after.strip()`。这是诊断分类，不是清洗、改值或自动接受等价。
依据PO-MHEP，A01精确只读门仍暂扣；未做A/B对齐、比较、共识或仲裁。
建议Owner仅接受本次123格呈现等价，原件不动，完整before/after/坐标/哈希保留；
不要求真人为此重标144条。批准文件例外不等于接受答案或关闭证据充分性问题。

A01两行、B01一行报告 `INSUFFICIENT_EVIDENCE / EVIDENCE_MISSING`；B01另24行理由中的E1/E2
编号与 `evidence_selection` 需结合上下文核对。它们是独立复核线索，不是已证实题目缺陷；
引用提及可能是否定或说明，无自动修selection/minimum。未跨人合并或计算问题并集。

## 证据恢复与实现

私有命名空间 `experiments/core144_d1_human_phase2_raw_lock_20261016/`（Git ignored）；
Owner-only镜像 `E:/LLMGuard-Handoff/paper1_core144_d1_human_phase2_raw_lock_owner_only_20261016/`。
不得向Annotator或外部Reviewer分发。

- `raw/PAPER1_CORE144_D1_HUMAN_A01_PHASE2_RAW_RETURN_V1.xlsx`；B01对应文件。
- `DUAL_PHASE2_RAW_LOCK_MANIFEST_V1.json`、`OWNER_REQUEST_AND_ATTESTATION_V1.json`。
- `HUMAN_A01_...`/`HUMAN_B01_...`：独立validation、readonly逐格差异、诊断答案、flags、leads。
- `DUAL_PHASE2_RECEIPT_GATE_V1.json`、`NATIVE_WORKBOOK_SAFETY_AUDIT_V1.json`。
- `OWNER_PRESENTATION_EXCEPTION_DECISION_PACKET_V1.md`：PO-MHEP十二字段与有界选项。
- `COMMAND_RECEIPT_V1.json`、`TASK_QA_V1.json`、`EVIDENCE_INDEX_V1.json`。

封存索引50份文件，SHA256 `6ee7a95a0bf200255c9afc3a38ddb08c82f05ff0f68fa7c6da4113c55fbafb36`。
13项合成测试、45项审计检查、Ruff、MyPy、UTF-8、secret/private-path检查及diff检查通过；
10份逐人诊断JSON独立命名空间重跑字节一致。后续Git/镜像回执为独立post-seal记录，
不改已封索引。源代码/文档快照是封存时版本；本索引标识段是随后追加的公开恢复指针。

只读复算笔记 `D1_PHASE2_READONLY_AUDIT_COMPANION_V1.ipynb` 已用捆绑Python按顺序执行全部代码单元；
环境无nbformat/nbclient，未安装依赖，未作Jupyter内核/官方格式验证或GUI验版。结果文本已检查；
该笔记只是可选伴随件，不取代原件、验证脚本、JSON与逐格审计。

只读实现 `scripts/research/validate_core144_d1_human_phase2_returns.py`；合成测试
`tests/research/test_core144_d1_human_phase2_returns.py`。新建输出、拒绝覆盖；独立命名空间复跑逐树核对。
没有A/B比较实现或答案改写代码。原件与发放版在读取后复哈希不变。

## Documentation closeout与限制

Human/Agent Ledger、Current State、Owner Register、Execution Log、Master Record、Stage Process、两层README、
Project Master Context与[状态V14](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V14.md)同步。
Research Plan Authority/长期要求/Guide/canonical lessons不改：没有新接受规则、方法、研究目标或可晋升结论。
测试/文档PASS只验收审计实现，不代表Owner文件例外/标注验收通过。Git以实际HEAD与封存回执为准。

D2载体/范围Owner门、D3两项S3门与两域Human禁发保持。Stage1–5、Final72、D1题文/ID/顺序、
发放Excel/原快照/Guide/两阶段原答均未修改；无Expected/GT、切分训练。原无关design/PDF不纳入提交。

`HUMAN_DECISION_REQUIRED / AUTO_CONTINUE=NO`。
`D1_HUMAN_PHASE2_RAW_LOCKED / A01_READONLY_PRESENTATION_EXCEPTION_PENDING / AB_COMPARISON_WITHHELD / NO_GT`。
