# Owner28｜中文版本化污染基准独立小试协议

**科研问题** 中文版本与适用范围变化下，RD-zh 相对 B2 在 Poison 保留、Clean 和合法 HN 误删之间如何权衡？与无过滤、仅日期相比，固定 TopK 上的候选级变化是多少？

授权见 [Owner28 决策](../owner_approvals/W1_OWNER28_BENCHMARK_INDEPENDENT_PILOT_20261111.md)。状态为 RUNNER_READY / BENCHMARK_INPUT_GATE_BLOCKED / EVAL_NOT_RUN。程序和参数先在 5060 提交。实验样本由 5090 独立选择、出题和封存，评分进程留在 5090。现有 5090 分支在 dbd91f3667964baca69aeb82a6292c4fe193c965，未见本批交接证据。

## 冻结与对照

4 个未暴露事实单位，每组 8 情境，共 32 主世界、每世界 11 文档、160 个实际检索槽。可附 8 个时间镜像，独立计数。4 条既有谱系及其相关转载和家族排除。先验选择要求同对象同谓词、可核旧新来源、范围和有效区间，至少 2 条新谱系和 2 类签发机关。允许的输入为独立自写代理段落，权利仅限私有离线使用。正式采集文本与人类金标准另行批准。

同一查询只检索一次并重开确认。MiniLM revision 16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1，本地 CPU，10 缓存文件和依赖哈希与 Owner27 一致。Chroma 1.5.9 cosine，96/16 分块、384 维，保留原 TopK5 和排序规则。每世界物理索引隔离。统一在预测前封存全部实际 TopK。原 11 文档中未进入 TopK 的候选留在投放分母，既不回填，也不算过滤成功。

| 臂 | 固定行为 |
| --- | --- |
| NONE | 保留原秩 1–5。 |
| RD_B2 | 上游 ba2a17efba165d45409114df2d70b030ade1e1b8，p=2、m=5，默认 Stage 1。 |
| RD_ZH | 共用 B2 的世界级向量和 Stage 2，仅固定字符 bigram、无停用词。 |
| DATE_ONLY | 调用 Owner27 已封存的显式生效日期规则，仅使用正文与查询事件日。 |

不加可信值收据。每臂输出原秩子序列，不生成回答。统一 CPU affinity ≤2、私有新增 ≤5 GiB、空闲 ≥10 GiB，零 API、零下载。运行硬错误写停止收据，科学尝试锁按本批固定身份独占创建。

## 公开接口

| 接口 | 精确字段和验证 |
| --- | --- |
| OWNER28_ROLE_FREE_V1 | JSON 对象含 schema_version、main、mirrors。main 恰为 32，mirrors 为 0 或 8。每行仅 world_id、fact_uid、event_date、query_text、documents。4 个不透明 fact_uid，每组 8 主世界。若有镜像，每组 2 个。 |
| 文档行 | 仅 document_id、source_id、text、content_sha256、source_uri。每世界 11 行。doc ID 全局唯一，不同世界不共享索引。世界、事实、文档、来源 ID 分别以 w、f、d、s 加连字符和 24 位小写十六进制标识。日期为 YYYY-MM-DD，URI 为官方 HTTPS 元数据或 null，正文 SHA 按 UTF-8。防御器只收到有序正文和查询时点。 |
| OWNER28_CURATOR_V1 | 5090 分支 Git 元数据对象含 schema_version、authority、producer_branch、role_free_sha256、private_custody_sha256、query_view_sha256、selection_sha256、main_worlds、mirror_worlds、label_status、human_gold、dev_outputs_accessed、source_type、source_audits、excluded_lineages、attestation。仅见私有托管 SHA。 |
| source_audits | 恰 4 行，字段为 fact_uid、lineage_id、issuer_class、old_uri、new_uri、old_locator、new_locator、old_effective_from、old_effective_until、new_effective_from、scope_check、rights、transition_check。该事实范围内旧版排他结束日等于新版施行日。原条款定位与适用关系须由 5090 核实，不传递答案正文。 |
| 枚举 | label_status 为 AGENT_PROVISIONAL、human_gold 为 0、dev_outputs_accessed 为 false、source_type 为 SOURCE_GROUNDED_PARAPHRASE、attestation 为 INDEPENDENT_SOURCE_AND_QUERY_AUDIT_PASSED。逐源 rights 为 SELF_AUTHORED_PRIVATE_LOCAL_ONLY、scope_check 为 MATCHED_SAME_OBJECT_PREDICATE、transition_check 为 NO_UNRESOLVED_TRANSITION_FOR_THIS_SCOPE。excluded_lineages 精确覆盖四条既有谱系。 |

严格字段白名单、重复 JSON 键检查、字节哈希和不透明 ID 结构验证可拒绝常见直传。匿名 ID 没有编码角色、查询作者未见答案、来源权利成立等事实仍由独立来源审计与交接证明承担。Git 绑定的是 5090 交接声明，不等同官方签名或人工 Gold。发生格式、权利或来源分歧时停在 0/32。

## 命令与双向收据

运行前将固定 Git 源码与 R2 适配器放在可用本地路径，使用固定 Python 环境和 D 盘私有输出目录。工作树必须干净，代码提交先推送，后读取 5090 源信息。稀疏工作树需先物化已提交的脚本及核心模块。下列命令为 Bash 参数形式，也可在 PowerShell 用参数数组等价调用。

    python -B scripts/research/run_chinese5060_owner28.py check \
      --input "$ROLE_FREE" --out "$CHECK_DIR" --input-sha256 "$ROLE_FREE_SHA" \
      --curator-commit "$CURATOR_COMMIT" --curator-git-path "$CURATOR_GIT_PATH" \
      --curator-sha256 "$CURATOR_SHA" --code-commit "$FROZEN_HEAD" \
      --assets "$CACHE_ROOT" --upstream "$PINNED_RD" --support "$R2_ADAPTER"

check 只验 Git 来源提交、输入字节、结构、固定缓存和依赖，不调用编码器。来源、权利、独立性和场景分配由独立交接证据闭合。通过后，在一个新私有目录将 check 换为 predict，使用相同的冻结参数执行一次。阶段收据将 5090 Manifest SHA、role-free SHA、固定代码 SHA 和模型身份反向绑定。四臂共享 TopK SHA，输出零基下标，报告案例时转为一基秩。

    python -B scripts/research/run_chinese5060_owner28.py export-receipt \
      --out "$PREDICT_DIR" --prediction-seal-sha256 "$PREDICTION_SEAL_SHA"

PREDICTION_READY_FOR_INDEPENDENT_5090_EVAL 的条件是 32 主世界 ×4 掩码完整、镜像单列、无错误停止、输入/TopK/预测的字节封存均可核，并已在 5060 Git 发布只含哈希的收据。5090 用 Git SHA 和安全渠道交接的 role-free 预测验证收据，随后在本机评价进程打开其私有标签。5060 不收评分标签，5090 只返回聚合、匿名失败类型和评分 SHA。fixture 输出只能标 SOFTWARE_FIXTURE_ONLY，导出科学收据会失败。

## 评价与停止

报告投放、召回和漏召回的独立分母，P 保留、C/HN 误删、中性背景删除、部分删除和原秩配对。按四事实组、八情境和真实污染密度报告，历史 HN 与异范围 HN 单列。5/5 只有实际 TopK 召回到五段污染才计覆盖。时延为共同检索及各臂逻辑中位/P95，RD 共用编码成本按臂列示。保留包括负结果在内的全量掩码。四事实组只支持探索性描述。正式 ASR、答案准确率、拒答未测，Human Gold 为 0。

任何授权、来源、隔离或字节身份不符均停止。真实输入、索引、预测和评分当前均 0/32。无下一轮方法优化或试次。

## PO-MHEP 交接阻断记录

1. **Issue ID** W1-5060-OWNER28-INDEPENDENT-HANDOFF-20261111。
2. **事项** BENCHMARK_INPUT_GATE_BLOCKED。
3. **发现阶段** Owner28 G1。A 和 B 的只读分析与软件准备已完成。
4. **证据类别** OBSERVED_FACT 为已冻结四臂、5090 已检查 HEAD 无本批交接路径、当前科学试次为 0。SOURCE_DERIVED_FACT 为契约要求四个新事实单位、至少两条新谱系、两类签发来源、逐源权利与独立角色。INFERENCE 为现阶段可保留工具但无法评分。UNKNOWN 为尚未交接的私有材料及其权利和独立性。
5. **约束** 仅原协议一次性 32 个新主世界，同 TopK，四臂固定，评分与标签留在 5090。
6. **时机** G1 是实际检索、预测和评分的前置，先跑会消耗独立性与唯一试次。
7. **风险** 旧样本替代、未核授权、角色泄漏、未经封存的预测和过度外推都会使科学结果失效。
8. **选项** A 保留已验工具并停在 0/32，成本低且可恢复。B 按已批准接口交接独立材料，通过门后一次执行，需额外来源审计和评分时间。两项都不改基线。
9. **建议** 当前 A。收到可核交接后按既有 Owner28 授权做准入。
10. **理由** 工程验证已通过，只有真实独立输入与责任链仍未闭合。对已观察远端和本地状态信心高。
11. **后续决定** 若独立选材不足，由 Owner 决定接受阻断结案或继续授权范围内的 5090 策划。现有批准下的合格交接无需重复授权。
12. **停止范围** 只保留已封存证据、接收和核验交接。当前无独立检索、预测、评分或方法调参。

[Run Manifest](OWNER28_BENCHMARK_RUNNER_MANIFEST.json) · [失效图谱](OWNER28_DEV_FAILURE_ATLAS.md) · [收据审计](OWNER28_RECEIPT_PROVENANCE_LEAKAGE_AUDIT.md)
