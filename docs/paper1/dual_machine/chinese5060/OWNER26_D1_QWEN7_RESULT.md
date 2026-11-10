# Paper 1｜Owner26 中文 D1 七臂可行性裁决

2026-11-10 JST · `W1-5060-OWNER26-D1-RD7-DEV-20261110-01` · `W1-OD-20261110-5060-D1-QWEN-NOANCHOR-26`

**`BLOCKED`。** 原 Pilot12 的两条 RD 基线完成新跑与独立候选级评分。84 世界评估输入未具备冻结条件，本轮真实 Qwen 请求为 0。没有可用的七臂评估支持 GO、PARTIAL 或 NO_GO。

[执行合同](W1_5060_OWNER26_D1_QWEN_RD7_FASTTRACK_EXECUTION_PROMPT_V1.md) · [Owner 授权](../owner_approvals/W1_5060_OWNER26_D1_QWEN_NOANCHOR_CHINESE_DEFENSE_COMPARE_20261110.md) · [脱敏 Run Manifest](OWNER26_D1_QWEN7_RUN_MANIFEST.json)

## 新运行证据与分母

签署 D1 数据清单为 40 组、120 候选、13 家族。Pilot12 原选择 SHA256 `2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689` 已核，不重新抽样。两臂共享原 query、36 个隔离世界、180 个有序 TopK 片段、缓存多语种 MiniLM 的一次世界级编码、RAGDefender 固定上游 `ba2a17efba165d45409114df2d70b030ade1e1b8`，以及 p=2、m=5 和原 Stage 2 相似度与并列规则。RD‑zh 仅替换 Stage 1 为字符 bigram、无停用词。新编码 36 次，两臂删留集合均逐世界对齐历史基线。先封存 72 个角色盲输出，再以单独进程和固定评价标签评分。未重检索。

Pilot12 各角色 12 个世界。Poison、Clean、HN 候选分别召回 10、10、9，漏召回 2、2、3。漏召回从过滤分母排除。其他 TopK 片段只报告删留数量，背景内容没有统一 Clean 标签。

| 臂 | DEV 世界 / 计划 | Eval 世界 / 计划 | DEV Poison 保留 | DEV Clean 误删 | DEV HN 误删 | DEV 其他片段删减 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| RD_B2 | 36/36 | 0/84 | 8/10 | 4/10 | 2/9 | 73/151 |
| RD_ZH | 36/36 | 0/84 | 6/10 | 5/10 | 4/9 | 99/151 |
| QWEN_VERIFY | 0/36 | 0/84 | 未测 | 未测 | 未测 | 未测 |
| RD_ZH+M1_SAFE | 0/36 | 0/84 | 未测 | 未测 | 未测 | 未测 |
| RD_ZH+M2_VOTE | 0/36 | 0/84 | 未测 | 未测 | 未测 | 未测 |
| M2_VOTE_ALONE | 0/36 | 0/84 | 未测 | 未测 | 未测 | 未测 |
| RD_ZH+M1_SAFE+M2_VOTE | 0/36 | 0/84 | 未测 | 未测 | 未测 | 未测 |

本地单臂成本含一次共同编码与该臂过滤。RD_B2 中位数/P95 为 137.55/148.01 ms，RD_ZH 为 138.69/149.48 ms。共 21/36 世界删留集合改变。七臂完整 DEV 为 0/36，D1‑28 冻结、预测、评分各 0/84，无主臂择优或冻结。正式 Targeted ASR、答案准确率和生成拒答均未测，Human Gold 为 0。

## 三项实际硬门

| 硬门 | 可核事实与剩余缺口 |
| --- | --- |
| `RETRIEVAL_IDENTITY_BLOCKED` | P1/P2 原协议和 36 个实际 TopK 均核实。白名单固定的无答案 V2 查询文件有 12 项，对应 Pilot12。其余 28 组没有找到与此协议绑定的独立查询和候选注入映射，0/28 可冻结。原 F5 的候选驱动查询仅用于旧审计，不能充当新评估的独立查询。已核候选包身份，未对额外 28 组构造或读取逐格标签。 |
| `D1_API_EXFIL_GATE_BLOCKED` | 历史 46 个源身份已知，15 个法规/规范来源、2 个官方解释或其他网页、29 个 D1 候选当时归于来源权利未知/受限。Owner12 的 108 格用途冻结为一次生成，不能替代本轮抽取、整世界核验及未来 84 世界的逐片段授权。本轮权限无合并签发清单，未外传任何内容。 [来源追溯](fast_unblock/evidence_recovery/SOURCE_ORIGIN_RECONCILIATION_SUMMARY.md) · [Owner12 原运行范围](pilot_rapid_live/RAPID_LIVE_OWNER12_EXECUTION_RESULT.md) |
| `BUDGET_GATE_BLOCKED` | 已重核历史北京 Workspace 回执字节和本进程凭据存在状态。当前 Workspace 归属和资金/在途、统一累计账本及适用美元换算上界仍未绑定。官方文档可证模型、北京服务和公开价，不能证明当前账户实际准入。原 Owner12 的 4096 后置风险放行仅限该批。本轮未获得实际 wire 输入 Token 硬上界，未做付费探测或替换地域。 [百炼模型与北京公开价](https://help.aliyun.com/zh/model-studio/qwen3-7-plus) · [Workspace 端点](https://help.aliyun.com/zh/model-studio/base-url) · [总输出上限语义](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions) |

### 请求和费用上界

逐段抽取最多 600 个逻辑请求，直接核验最多 120 个，再加至多 2 个虚构握手。DEV 上界为 216，Eval 上界为 504，合计 722 含握手。物理发送可严格按相同请求 SHA 去重，独立部署的 M1/M2 四臂各自计入每世界完整五段逻辑抽取，QWEN_VERIFY 各自计入一次完整 TopK。共享抽取不减免独立部署账。

固定快照北京公开价每百万输入/输出 Token 在 ≤256K 档为 CNY 2/8，较大输入档为 CNY 6/24。假定逐请求输入能在发送前证明 ≤4,096，且输出总上限拟用 512 并额外预留 10 Token，722 请求无折扣估算 **CNY 8.929696**。这是条件化预算，当前不得用于放行。若只依赖官方非思考最大输入 991,808，即使假定相同输出上限，722 个全按高档估算达 **CNY 4,305.557472**。当前缺精确输入上界、账户可用额度、结算/在途及适用 FX。历史 CNY 7.611826 和 Owner12 CNY 0.130084 都是各自封存的估算，未用作当前统一余额。[固定快照上下文限制和价格](https://help.aliyun.com/zh/model-studio/qwen3-7-plus) · [历史账本](fast_unblock/evidence_recovery/ACCOUNT_AND_LEDGER_RECOVERY.md)

本轮实际请求、探测、输入/输出/reasoning Token、新增费用均为 **0**，API 延迟未测。USD3 硬限和原 USD25/28/30 政策有效。

## 方法图与离线反例

```text
固定 query + 有序 TopK5
  ├─ 共享向量 ── B2 / RD-zh
  ├─ Qwen 逐段 ── 原文 span 验证 ── M1 / M2 / 联合（先 M1 后 M2）
  └─ Qwen 同世界核验 ── 原 rank + 逐字证据 ── 直接核验
各臂只输出有序原片段子集 → 角色盲封存 → 独立评价
```

- M1 草案只允许在保留段有唯一相同 scope、条件和值单位时恢复同一可比事实，遇版本声称不由文本提权。**虚构单测有 1 段污染被放回**，因为保留段与被删段共享同一个错值。此结果是机制反例，D1 的 M1 放毒分母未测。
- M2 草案对已绑定、可比范围的值去重。缺独立来源身份返回 `SOURCE_CORRELATION_UNKNOWN`，保持父集合。虚构 3/5、4/5、5/5 无来源证明时各保留全部毒段。即使五个来源身份都真实，3/5、4/5 的已攻陷多数也会删去正确少数，5/5 无正确证据可恢复。D1 原场景只注入一份候选文档，背景角色未审定，实际 3/5、4/5、5/5 和同义改写协同污染的覆盖无法证明。本轮未新建这些真实场景，也未测自相矛盾毒段或跨版本误绑率。
- v0 提示、严格字符/UTF‑8 逐字引用校验、原 rank 核验和保守回退单测通过。还需要本轮配置的实际无敏感握手、服务端 Token 语义、完整七臂封存及真实评价，当前未进入科学 DEV 调参。

## 裁决与下一路线

**先完成有权来源的中文版本敏感污染基准与 RD 中文迁移失效分析。** 优先为独立选择的查询冻结有效日期、适用对象、历史版、伪造更新和可传播范围，再在同一 TopK 上拆出 RD‑zh 的污染过滤收益与 Clean/HN 代价。只有独立查询、合法外传和可执行预算三项闭合后，才恢复 Owner26 七臂验证。现有结果证明词项迁移存在可复测的安全与可用性权衡。M1/M2 尚未取得论文方法增益或创新性证据。

## PO-MHEP 十二字段

1. **Issue ID** W1-5060-OWNER26-RD7-ADMISSION-20261110。
2. **问题** D1-28 检索身份、本轮逐段外传许可及费用硬上界未闭合。
3. **发现阶段** Owner26 DEV，两个 RD 臂已完成。
4. **事实与未知** OBSERVED 为 12 项固定查询、两臂复跑、0 次真实请求和 0 个 Eval 世界。SOURCE_DERIVED 为 84 世界同协议、逐段授权与预留硬门。INFERENCE 为历史生成许可与历史费用不足以放行。UNKNOWN 为 28 组查询绑定、当前统一账本及用途许可。
5. **约束** 原 Pilot12 和 B2/R2 保持原样，D1 只作内部开发，固定模型与地区，单次无重试，新增 USD3，原 25/28/30 门。
6. **为何现在处理** 三项均为真实发送或一次性冻结前置，事后修补会损失许可、预算和可比性。
7. **下游风险** 越权外传、候选驱动查询泄漏、费用越限、主臂选择偏置和论文过度解释。
8. **选项** A 补齐独立查询、逐段用途授权和机器账本，保持同输入的七臂，但需额外采集与预注册。B 暂停七臂，先做公开有权基准与 RD 失效分析，成本为采集和独立审核，保留对照的复用价值。两者都保留已封存证据，可分别审批。
9. **建议** B，优先建立可独立验证的中文版本敏感污染基准。
10. **理由与信心** 已复跑的 RD-zh 在 29 个已召回候选上的得失可核，M1/M2 的实测 D1 净收益未知。对三项准入阻断信心高。
11. **后续决策** Owner 选择是否先立公开基准。恢复原七臂须同时给出 28 组无角色查询绑定、本批逐段用途与地域授权、以及带费用和 Token 上限的当前机器账本。
12. **停止期间** 只读核验、证据保全与治理收口。无真实模型请求、重检索、科学重复、改样或解封。

## 封存与治理

私有 ZIP `OWNER26_PRIVATE_EVIDENCE.zip` 共 31 件，逐件重读核验。SHA256 `7a37430612edd622bbecd679f34ea6d1ce19ec52cdb41567138a8f88c6ee3867`。新 RD 预测 SHA256 `fa7f674d2c0e6ca5114c0c4e219706ab57c1f6eb3ac3c1c8287135f388d7d6f7`。角色盲 Seal SHA256 `6fe54afea2ff3cf78707c6992f7835254ab10dc7be67b81cf719edbd7ab8a45f`。6 项单测、Ruff 和 MyPy 通过，早期类型检查失败日志与实际执行源码均保留。最终发布的 RD 源码只补了静态类型注解。

Human Ledger、Agent Ledger、Current Work State、Experiment Master、Research Execution Log、Project Master 和 Tracker 已更新。Owner 原批准记录保留。Stage Process、Canonical Lessons、Research Plan Authority、README 的更新条件已检查，本轮未开启新的正式阶段或改变原合同。工作停在 `AUTO_CONTINUE=NO`。

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
