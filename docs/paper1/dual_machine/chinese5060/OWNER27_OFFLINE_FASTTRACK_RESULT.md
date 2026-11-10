# Paper 1｜Owner27 中文版本化来源离线验证

2026-11-11 JST · `W1-5060-OWNER27-PUBLIC-VERSION-20261111-DEV-V0`
`DEV_COMPLETE_DIRECTIONAL_FAIL / EVAL_BLOCKED_INDEPENDENT_INPUTS / AUTO_CONTINUE=NO`

**裁决为只保留基准。** 32 个主世界完成同 TopK5 七臂比较。与同凭据简单规则相比，联合门控的 Clean 误删均为 29/63，相对降幅 0%，未达到预注册 50% 主门。联合臂多保留 2 段合法 HN，但去 scope 臂得到完全相同的 32 个主世界掩码。EVAL 为 0/32，尚无独立评价或正式泛化证据。

[正式授权](../owner_approvals/W1_5060_OWNER27_PUBLIC_VERSION_OFFLINE_FASTTRACK_20261111.md) · [执行合同](W1_5060_OWNER27_PUBLIC_VERSION_OFFLINE_FASTTRACK_EXECUTION_PROMPT_V1.md) · [Run Manifest](OWNER27_OFFLINE_FASTTRACK_RUN_MANIFEST.json) · [来源登记](PUBLIC_VERSION_SOURCE_REGISTER_DRAFT.json) · [阶段记录](../../../research/stage6_1_hidden_knowledge_poisoning/stage_process/W1_5060_OWNER27_PUBLIC_VERSION_work_process.md)

## 数据、权限与公平性

按 SHA256(`20261111|lineage_id|fact_id`) 升序冻结 `HOL-SPRING`、`HOL-LABOR`、`HY-ISSUER`、`DRV-HEAVY-AGE` 四组，涵盖国务院和公安部两类签发机构、三条文档谱系。第五项和仅闭合目录过渡的医保均未入样。使用登记中的真实生效切点和适用范围，在 D 盘自写事实等价中文、污染和背景文本。原始网页、官方原句和附件入库均为 0，原始来源再使用权仍未知。语料标记为 `SOURCE_GROUNDED_PARAPHRASE / NOT_NATURAL_ORIGINAL_DOCUMENT`。 [国务院令第795号](https://app.www.gov.cn/govdata/gov/202411/12/521605/article.html) · [国务院令第797号](https://app.www.gov.cn/govdata/gov/202412/13/522682/articleNew.html) · [公安部令第172号](https://jtgl.beijing.gov.cn/jgj/jgxx/flfg/gabgz/543498902/index.html)

每世界 5 个情境候选和 6 个自写中性背景文档，物理索引互斥。查询进程只读取对象、时点、适用范围和所问属性。不同进程生成和封存 TopK 与预测，评价进程在完整预测封存后读取暂定标签。编制者为同一 5060 研发工作线，查询视图与评价进程隔离，人工独立选材和双评未发生。所有评价为 `DEV_AGENT_PROVISIONAL`，Human Gold 为 0。

使用 Chroma 1.5.9 cosine、固定本地 multilingual-MiniLM revision `16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`、96/16 分块和 TopK5。40 个索引全部关闭重开后复现相同 rank、score 和成员，主世界 32 个，S2 的 8 个时间镜像单列。B2 与 RD‑zh 共用每世界一次编码和固定上游 `ba2a17efba165d45409114df2d70b030ade1e1b8` 的 Stage 2，p=2、m=5。RD‑zh 只替换 Stage 1 中文字符 bigram、无停用词。DATE_ONLY 只读正文的显式生效日期。

T1 三臂共享同一份收据字节和 RD‑zh 父掩码。收据以代理文档 UID 和正文 SHA 绑定到版本、谱系、有效区间和范围。简单规则保留有有效且无冲突的同范围收据的证据。联合臂在已有同范围锚、时间有效及同谱系范围内无冲突时，额外保护另一个合法范围的证据。消融仅忽略范围条件。无适用锚或冲突回退到父掩码。未验证文本及其来源自称不能产生收据或获得放回资格。三臂只恢复有收据的原 TopK 项，不凭同值投票，也不另设 Poison 删除规则。这里的收据是本地代理绑定，没有外部签章。

## DEV 七臂实测

| 臂 | 主世界 | Poison 保留 / 召回 | Clean 误删 / 召回 | HN 误删 / 召回 | 中性背景删除 / 召回 | 本地中位 / P95 ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NONE | 32/32 | 45/45 | 0/63 | 0/33 | 0/19 | 0.00 / 0.00 |
| RD_B2 | 32/32 | 20/45 | 40/63 | 4/33 | 2/19 | 115.93 / 141.04 |
| RD_ZH | 32/32 | 6/45 | 54/63 | 13/33 | 6/19 | 119.12 / 141.58 |
| DATE_ONLY | 32/32 | 45/45 | 0/63 | 11/33 | 0/19 | 0.02 / 0.03 |
| RD_ZH + SIMPLE_RECEIPT_RULE | 32/32 | 6/45 | 29/63 | 13/33 | 6/19 | 119.14 / 141.60 |
| RD_ZH + SOURCE_TIME_SCOPE_JOINT | 32/32 | 6/45 | 29/63 | 11/33 | 6/19 | 119.14 / 141.59 |
| RD_ZH + JOINT_NO_SCOPE | 32/32 | 6/45 | 29/63 | 11/33 | 6/19 | 119.13 / 141.59 |

每臂 160 个主 TopK 槽。Poison 召回 45/50，Clean 63/70，HN 33/40，中性背景 19/192。漏召回不计作过滤成功。各臂均无空集合。表内是单臂逻辑开销，RD 轨道含共同编码和过滤，T1 另含凭据规则执行但不含凭据编制人工时。共同检索中位 197.22 ms，P95 472.25 ms。32 主世界中 55/160 槽有本地收据，分布在 30/32 世界，联合臂 2/32 无适用锚且精确回退。镜像 8 世界、40 槽只作时间诊断，Clean 召回 16，HN 召回 17。三条 T1 在镜像均误删 Clean 6/16、HN 14/17。

## 配对翻转与失败归因

| 配对 | 掩码变化世界 | Poison 保留→删除 | Clean 删除→保留 | HN 删除→保留 | 其他关键变化 |
| --- | ---: | ---: | ---: | ---: | --- |
| B2 → RD‑zh | 21/32 | 14 | 0 | 0 | 多删 Clean 14、HN 9、中性背景 4 |
| RD‑zh → 简单收据规则 | 25/32 | 0 | 25 | 0 | 四组分别放回 6、5、7、7 段 Clean，组序见来源小节 |
| 简单收据规则 → 联合门控 | 2/32 | 0 | 0 | 2 | 均在卫生许可组，S3 与 S7 各 1 |
| 联合门控 → 去 scope | 0/32 | 0 | 0 | 0 | 当前 DEV 无可归因的 scope 增益 |

- 两种规则各恢复 25 段 Clean，解释为可验证代理收据带来的共同收益。联合臂对同证据简单规则未改善 Clean。所有 T1 错误放回 Poison 为 0，伪造新版自称获收据或提权为 0。这个结果不代表自动拒绝伪造新版，联合臂仍保留 2/4 已召回伪造新版。
- 联合臂在单段、近重复、改写协同、伪造新版、极端场景分别保留 **0/3、0/12、2/12、2/4、2/14** 段已召回 Poison。DATE_ONLY 保留伪造新版 4/4。RD_B2 和 RD_ZH 分别有 9 和 4 个主世界只删掉部分已召回 Poison。联合臂与 RD‑zh 的 4 个残留世界相同。M1 放回算法、M2 多数投票算法均 `NOT_IN_ARM`，上述数字衡量相应压力下的候选残留。
- S8 投放计划为两个 4/5 和两个 5/5，实际 TopK 为两个 3/5、两个 4/5。保留全部漏召回，实际 5/5 缺失正确证据时的行为仍未测。S4 另有 1 个单污染候选未进入 TopK。
- 汇总与 Run Manifest 保留 21 对臂的配对结果、八情境与四组分层、每臂分母和时延。研究分母只有 4 个事实单位，无法把 32 个世界当作独立事实样本。

## EVAL 停止与证据

EVAL 冻结、检索、预测和评分均为 **0/32**。准入核对仅发现已暴露的预检池，4 条预检谱系全部排除。绑定的新独立事实 0/4，新谱系 0/2，缺少独立无答案查询和逐源权限证据。Agent 暂定评分仅可替代评价标签来源，独立选材和使用权仍为硬门。本次未启动 v1 或 EVAL。Owner26 的 D1‑28 维持 0/84，D2/D3/HOLD8、5090、主线未进入本次执行。

科学 v0 单次，三阶段退出码均 0。12 项测试、Ruff、MyPy 和独立掩码重算通过。保留两次虚构工程 smoke 的原始失败及复查，一次因测试引用格式无效，一次因用候选向量自身作为查询触发 Chroma 距离校验。独立虚构查询 smoke 通过，科学协议未变。另保留一条 Chroma API 类型桩不含 `close` 的 MyPy 失败，类型注解修正后通过。科学阶段合计 59.797 s、CPU affinity 2、D 盘新增留存 130,032,279 B，盘剩余 355,692,040,192 B。新增下载、安装、商业 API、API Token 和费用均为 0。正式 ASR、答案正确率和生成拒答均未测。

| 封存项 | 标识 |
| --- | --- |
| 科学执行代码 Git SHA | `6c851ea5ad4b33afdb3494267177cfedd66222a6` |
| 代理语料 SHA256 | `32232dbbe4eeb48365ce65a60d262658a95e9880ec3a106868c77a3d7ca6c98b` |
| 独立查询视图 SHA256 | `705159cc4295478d257de383232517e9ce4e9b8d63687bcaa62faaaf20645544` |
| 运行冻结 SHA256 | `8a2d1ce24d518107fbaa2b8a25d77c3c3de97c2ec3349afd66ebd27ac5b6643f` |
| TopK 封存 SHA256 | `c65c9e1e811a524fcafa35cec9e642aa91da8733c63c349745d53d642741f03f` |
| 预测封存 SHA256 | `b4cae321ef438a84f60c6239c327e8b68541a002cf298b6dbd24c688ce32cbcd` |
| 评分汇总 SHA256 | `d151488e5a6763abee73871a9966c8dccf30147edd65cdd884db87f63aabccd8` |
| 私有归档 SHA256 | `cc9051b64dccb5b9bcf57495ebfdf370d99c859708fe0b833707be5a65825d92` |

`OWNER27_OFFLINE_FASTTRACK_PRIVATE.zip` 含 363 个逐项索引成员，回读全部 SHA 一致。角色标签、查询正文、输入文本、索引、原始掩码和运行日志留在私有归档。

## PO-MHEP 决策材料

1. **Issue ID** `W1-5060-OWNER27-G3-INDEPENDENCE-20261111`。
2. **问题** 预注册的 EVAL 来源和独立输入未交接，联合方法的 DEV 主门未通过。
3. **发现阶段** Owner27 G3 检查与 DEV v0 G4 评分。
4. **事实状态** `OBSERVED_FACT` 为 DEV 32/32、同 T1 主指标均 29/63、EVAL 0/32。`SOURCE_DERIVED_FACT` 为新 EVAL 必须有至少 4 组、2 条新谱系、2 类签发组合及逐源权利。`INFERENCE` 为现有证据只支持基准路线。`UNKNOWN` 为未见语料上的联合效果、权利和未来独立策划人员。
5. **受影响约束** 冻结分母、预检谱系排除、独立选材、最小授权与单次盲评。原 Owner26 及禁止范围仍按原合同执行。
6. **为何现在处理** 任何新 EVAL 查询或世界先于准入都会破坏真正独立的验证。
7. **下游风险** 同作者偏置、受限文本入库、把代理收据当真实可信来源、把过滤结果外推成答案正确率，以及为补结果消耗单次试次。
8. **选项** A 保留基准和中文迁移负结果，暂不投入新方法运行，成本低且可逆。B 先交接独立策划者与合规材料，再按原冻结门执行一次 EVAL，需新增人工选材和审核成本，可能仍失败，但可补独立描述证据。
9. **建议** A，只保留版本敏感污染基准和 RD 中文迁移分析。
10. **理由与信心** 对同证据 DEV 主门失败与 scope 消融相同有高信心。独立表现未知，未据此裁决整个机制类别。
11. **Owner 决定** 仅当 Owner 仍要执行条件 EVAL 时，指定独立策划者，交接未见事实、无答案查询与逐源权利材料。
12. **停止期间** 仅保全证据、核验及归档。任何新科学运行、用开发谱系补 EVAL、调参及商业调用停止。

文档收口已核 Human Ledger、Agent Ledger、Current Work State、Execution Log、Experiment Master、Project Master、Tracker 和阶段记录。Owner Decision 原批准已登记，本次无新增 Owner 决定。Canonical Lessons 仍待独立证据及 Owner 验收，Research Plan Authority 与 README 的合同和入口条件未改变。


    human_ledger_checked = true
    human_ledger_updated_if_required = true
    agent_ledger_checked = true
    agent_ledger_updated = true
    current_work_state_updated = true
    execution_log_appended = true
    experiment_master_condition_evaluated = true
    owner_decision_condition_evaluated = true
    stage_process_condition_evaluated = true
    lessons_condition_evaluated = true
    research_authority_condition_evaluated = true
    README_condition_evaluated = true
    cross_document_current_task_consistent = true
    cross_document_status_consistent = true
    cross_document_next_action_consistent = true
    cross_document_blocker_consistent = true
    markdown_links_valid = true
