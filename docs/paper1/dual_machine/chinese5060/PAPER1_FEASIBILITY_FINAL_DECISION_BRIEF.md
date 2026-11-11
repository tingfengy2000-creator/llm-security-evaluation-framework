# Paper 1｜5060 可行性最终决策简报

2026-11-11 JST · `SCIENTIFIC_TRIALS_STOPPED / OWNER_ROUTE_DECISION_PENDING / AUTO_CONTINUE=NO`

## 一页决策摘要

**建议保持联合门控暂停，论文主线优先转向中文版本敏感污染基准与 RAGDefender 中文迁移失效分析。** 现有数据支持三个受控发现。路线、题目和后续预算仍待 Owner 决定。

1. **候选层存在重复出现的取舍。** 在各 32 个同 TopK5 世界的 Owner27 DEV 和 Owner28 EVAL 中，RD_ZH 均比 RD_B2 删除更多已召回污染，同时误删更多正常及合法难负例证据。在 Owner28，污染保留由 33/56 降至 15/56，Clean 误删由 27/82 升至 55/82，HN 误删由 7/20 升至 10/20。四个范围互换污染片段在两臂均保留。
2. **更严格的候选过滤伴随不利的回答层数值信号。** 在 31 个完整三臂配对世界，NONE、RD_B2、RD_ZH 的参考数值匹配分别为 20、25、15。5090 用评价前封存的私有目标独立核验，22 个已召回污染的数值型目标世界中三臂分别命中 0/22、0/22、5/22。RD_ZH 的五次命中在 NONE 均为拒答。现有证据不能识别正常证据误删对该结果的因果贡献。
3. **当前联合方法未通过开发门。** 同凭据的简单规则与联合门控均误删 Clean 29/63，相对降幅 0%，预注册要求为 50%。去 scope 消融与联合掩码 32/32 相同。D1 无独立可信收据，代理收据另有真值侧信息，尚无新防御方法 GO 或已验证的方法创新。

Human Gold 为 0。95 条回包中 68 条回答的适用范围与引用支持仍未决。数值匹配、短值目标命中和拒答状态是三个不同观测，正式端到端 Accuracy/ASR 为 NOT_MEASURED。原作者 Claim1–3 为 NOT_RUN。未启动任何新试次，联合门控继续暂停。

## 附录 A｜候选层与负结果

**Owner25–26 前置边界。** D1 36 个隔离世界共 180 个 TopK 槽，36 个候选中召回 29 个，独立可信收据 0/180。严格 P0 无法恢复 B2 误删的 4/10 个已召回 Clean。合成 64 DEV／32 HOLDOUT 只表明模拟可信锚可作用，真签发者失陷可误锚，无锚 5/5 多数污染需回退，原 Rule‑V2 严格绑定为 0/320、0/160，且缺同世界 RD 基线。D1 无锚恢复及原 Rule‑V2 部署路线保留 NO_GO。Owner26 后续仅完成两个 RD 臂各 36/36；全七臂 DEV 0/36、D1‑28 EVAL 0/84，因独立查询、外传和预算准入未闭合，Qwen 0 次。M1 同错值放回和 M2 多数误判是离线反例，D1 实测分母未建立。 [Owner25 机制结果](OWNER25_SCIENCE_FIRST_RESULT.md) · [Owner26 准入与实测](OWNER26_D1_QWEN7_RESULT.md)

**Owner27 DEV 与 Owner28 EVAL。** 每批 4 个事实组、3 条来源谱系、32 个主世界，每臂 160 个同 TopK5 槽。语料是依据真实公开版本变化自写的代理文本。EVAL 由 5090 策划新谱系并保管暂定标签，5060 先封存角色盲预测，再由 5090 评分一次。分离为同项目的跨机与进程隔离。Owner27 自身 EVAL 0/32，Owner28 四臂 EVAL 32/32 不包含联合门控。DEV 的 8 个时间镜像单列，EVAL 原包 7 个镜像未运行。B2 为固定 RAGDefender 上游和中文缓存适配，RD_ZH 仅改变 Stage 1 字符 bigram 和停用词处理，共用 Stage 2。 [方法与限制](BENCHMARK_V01_METHODS_AND_LIMITATIONS.md)

| 批次 | 臂 | Poison 保留／召回 | Clean 误删／召回 | HN 误删／召回 | 背景删除／召回 |
| --- | --- | ---: | ---: | ---: | ---: |
| DEV | NONE | 45/45 | 0/63 | 0/33 | 0/19 |
| DEV | RD_B2 | 20/45 | 40/63 | 4/33 | 2/19 |
| DEV | RD_ZH | 6/45 | 54/63 | 13/33 | 6/19 |
| DEV | DATE_ONLY | 45/45 | 0/63 | 11/33 | 0/19 |
| DEV | RD_ZH + 简单收据 | 6/45 | 29/63 | 13/33 | 6/19 |
| DEV | RD_ZH + 联合门控 | 6/45 | 29/63 | 11/33 | 6/19 |
| DEV | RD_ZH + 去 scope | 6/45 | 29/63 | 11/33 | 6/19 |
| EVAL | NONE | 56/56 | 0/82 | 0/20 | 0/2 |
| EVAL | RD_B2 | 33/56 | 27/82 | 7/20 | 0/2 |
| EVAL | RD_ZH | 15/56 | 55/82 | 10/20 | 1/2 |
| EVAL | DATE_ONLY | 56/56 | 0/82 | 0/20 | 0/2 |

DEV 的 Poison/Clean/HN/背景漏召回依次为 5/50、7/70、7/40、173/192，EVAL 为 2/58、0/82、0/20、190/192。漏召回不计入过滤成功。EVAL 中 RD_ZH 相对 B2 额外删除 50 段，构成为 18 Poison、28 Clean、3 HN、1 背景。8 个事实组来自 6 条谱系，世界是组内相关变体，两批不合并作独立样本推断。

- **范围与正常证据。** EVAL 无污染世界 Clean 误删 8/20→12/20，范围互换 Poison 保留均为 4/4。合法历史 HN 误删 2/12→4/12，合法异范围 HN 误删 5/8→6/8。
- **改写、伪版本与多数污染。** EVAL 的近重复情境两臂均滤除 12/12，改写协同 Poison 保留 10/12→4/12，同时 Clean 误删 3/8→7/8。跨情境伪造新版投放 10、召回 8、漏 2，保留 8/8→3/8。EVAL 仅 2 个实际 5/5 世界，Poison 保留 8/10→2/10。DEV 计划的两个 5/5 世界实际只达到 3/5 和 4/5。
- **时效和收据对照。** EVAL DATE_ONLY 在 352 个投放段和 160 个 TopK 槽均 0 命中，32/32 掩码与 NONE 相同。DEV 代理收据覆盖 Clean 30/63、HN 25/33、Poison 0/45，含由造数者指定的版本、范围及规范值，独立签发的真实收据为 0。简单与联合各恢复 25 个 Clean，联合多恢复 2 个 HN，去 scope 也恢复这 2 个 HN。相对 T0 的差异不能归于部署时可独立取得的可信证据。 [收据信息审计](OWNER28_RECEIPT_PROVENANCE_LEAKAGE_AUDIT.md) · [失效图谱](OWNER28_DEV_FAILURE_ATLAS.md)

## 附录 B｜端到端生成与目标核验

**Owner29。** 在 Owner28 同一 32 世界与冻结掩码上，固定北京 `qwen3.7-plus-2026-05-26`、提示、采样与上下文顺序，计划并发送 96 格。首格 NONE 已发送，Runner 读取错误的回包字段导致原始回复未归档，无法恢复且未重发。余 95 格全部成功，68 ANSWER、27 ABSTAIN。总输入/输出为 33,093/3,716 Token，延迟中位/P95 为 1.601/1.936 秒，公开费率估算 CNY 0.095914，首格实际用量和扣费未知。 [续跑报告](OWNER29_RAPID_GENERATION_REMAINDER_RESULT.md)

| 比较臂 | 全批成功 | 主配对数值匹配 | 主配对数值不匹配 | 主配对拒答 | 22 个数值目标世界命中 |
| --- | ---: | ---: | ---: | ---: | ---: |
| NONE | 31/32 | 20/31 | 0/31 | 11/31 | 0/22 |
| RD_B2 | 32/32 | 25/31 | 0/31 | 6/31 | 0/22 |
| RD_ZH | 32/32 | 15/31 | 6/31 | 10/31 | 5/22 |

**Owner30。** 5090 在生成封存后公开 32 条参考原子。Rule V1 处理 95 份回包，确认 27 条原拒答和 68 条范围/引用未决。62 个可公开短值全匹配受披露白名单选择影响；补核其余 6 个 RD_ZH 短值均不匹配。全批数值匹配分别为 20/31、26/32、16/32，含 1 个额外 B2–ZH 配对。68 个短 Judge 包已封存，服务端 Token 上界、账本和逐包外传未闭合，Owner30 Judge 实际 0 次、额外 USD 0。拟用 Judge 与生成器同一快照，若今后使用须标记相关偏差。 [规则结果](owner30_eval/OWNER30_AUTO_ANSWER_GRADE_REPORT.md) · [数值诊断](owner30_eval/OWNER30_NUMERIC_AGREEMENT_PROXY_REPORT.md) · [Judge 补充](owner30_eval/OWNER30_QWEN_JUDGE_SUPPLEMENT_REPORT.md)

**5090 公开核验。** 6 条 RD_ZH 不匹配中 5 条命中预封存短值目标、1 条为其他错误。五次相对 NONE 都由拒答转为命中，相对 B2 为 3 次拒答转命中、2 次非目标转命中。数值型目标的 22 个世界均召回污染，按本批数值口径无额外条件分母变化。另有 2 个纯范围世界，三臂共 6 格的范围主张及目标命中 UNKNOWN，未纳入 22，也未记为未命中。5060 仅核对 5090 的公开报告及 Manifest SHA，不读取该机的私有目标、Gold 或六条原值。 [5090 公开核验报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/15a6961a4722a903069fbb829046972f9e45027e/docs/paper1/dual_machine/repro5090/owner30_eval/OWNER30_SIX_VALUE_TARGET_MATCH_REPORT.md)

## 附录 C｜正式发表前的最低证据与停止边界

| 缺口 | 最低交付要求 |
| --- | --- |
| 独立人审 | 两名真人盲评与第三人裁决，冻结时点、适用范围、引用、拒答及攻击目标定义，保留分歧与未知。 |
| 有效时效对照 | 独立开发和验证生效、废止、过渡及适用范围的有效基线，报告解析覆盖、决策覆盖和未知回退，以同 TopK 进行公平对照。 |
| 合法自然检索与规模 | 核准真实自然来源的采集、引用及模型传输权限。按新事实与来源谱系分割开发和验证，用精度或功效论证独立簇规模，分层报告实际召回密度及漏召回。 |
| 真实端到端与基线身份 | 同世界冻结检索、提示、生成器、证据权限和计费，评价正式 ASR、准确率、拒答和来源支持。单列原 RAGDefender 论文与 v0.2 公开库、中文适配的差异及原 Claim1–3 复现状态。 |
| 可复算科研包 | 冻结数据、源码、依赖、许可证、命令、失败与分母。提供公开匿名汇总与私有授权复核路径，确保从 TopK、掩码、原回包到逐格人工判断可追溯。 |

上述为后续预注册清单。路线或资源变化由 Owner 另批，D2/D3/HOLD8、5090 Claims 和主线仍受原约束。当前不调参、不重跑、不新增模型实验。 `AUTO_CONTINUE=NO`。

## 附录 D｜冻结证据定位

| 阶段 | 版本锚与 SHA256 |
| --- | --- |
| Owner25/26 | [Owner25 Manifest](W1_5060_OWNER25_SCIENCE_FIRST_RUN_MANIFEST.json) `4ba31544ba4ea6d9c62e1fbefa2b8409a8499ff5242c1c9e90ef763f0a52b716` · [Owner26 Manifest](OWNER26_D1_QWEN7_RUN_MANIFEST.json) `2f3262659d5cc56d62e2424464ca98c3be3424aa6ae619822268a7179deec55c` |
| Owner27 DEV | 执行代码 `6c851ea5ad4b33afdb3494267177cfedd66222a6` · [Run Manifest](OWNER27_OFFLINE_FASTTRACK_RUN_MANIFEST.json) `ebca241a364c75cfe9cfaebfb6832e7a97b9a856a47638b870e0ea55d7b762f4` |
| Owner28 EVAL | 5060 盲预测封存提交 `ad413ea639c950faea2106a52fa4352735384ef1` · [预测 Manifest](owner28_eval/OWNER28_EVAL_RUN_MANIFEST.json) `ead33b73b25e78da9d1877a63cee0337f31ec94bafa2f4dea2cffeff731d4277` · [5090 评分 Manifest](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/670d9ab0e546d46117bf5c48ebb2b0043689f453/docs/paper1/dual_machine/repro5090/owner28_eval/OWNER28_EVAL_SCORE_MANIFEST.json) `2ff71d24dad2904f04d0912393f80bfce563855ea9c73ff5c7ebb6c760027378` |
| Owner29 生成 | 结果提交 `188212344ce8c0144356c307efe3847f2f6fb97a` · 续跑 Seal `8d795ce58056aee0ab1784a29699e9a96bfb7546161846128e297e6e39457e3a` · 私有归档 `903991fa617f3d51bc2eb193fd20e0b04982f28c88b2b4fe18e7b2a7838c1822` |
| Owner30 5060 | [规则 Manifest](owner30_eval/OWNER30_AUTO_ANSWER_GRADE_MANIFEST.json) `1a9a7c6b6729d449a3272d32b22cf7415de4f909d9632cce11d255e553b22d94` · [短包补充 Manifest](owner30_eval/OWNER30_QWEN_JUDGE_SUPPLEMENT_MANIFEST.json) `60fe6155720e606922eccca883bf3c09d599926675a3d15e30df1cda992f3106` |
| Owner30 5090 | 公开核验提交 `15a6961a4722a903069fbb829046972f9e45027e` · 报告 `8de56c3b4bcc27891dda1abf47b802a00c3a44a79c36ced31018ae6ded08f9b9` · [目标核验 Manifest](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/15a6961a4722a903069fbb829046972f9e45027e/docs/paper1/dual_machine/repro5090/owner30_eval/OWNER30_SIX_VALUE_TARGET_MATCH_MANIFEST.json) `56179d1a244ed695a6cc8e91e920ec371c160a91162004ab99405d3105783473` |

归档以关闭合同锚 `01d003309aeca67db232f39d31914efe3c3cd902` 为基准。无新增 Owner 决策或正式阶段，Owner Decision Register、Stage Process、研究路线文档和方法冻结保持原版本。
