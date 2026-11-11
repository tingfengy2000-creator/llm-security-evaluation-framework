# 给5060 Codex｜Owner32 V-CARE：先验证独立来源是否存在，再开展有条件算法实验

**Authority currently: DESIGN_DRAFT / OWNER_APPROVAL_PENDING.** 请先读取 docs/paper1/dual_machine/chinese5060/W1_OWNER32_VERIFIED_EVIDENCE_FAST_METHOD_PROPOSAL_20261111.md；若Owner尚未明确批准Owner32，**仅可做静态只读来源可用性检查、代码草案和虚构fixture，不得开新的科学试次、发商业API、下载新模型或读取5090未见Gold**。获批后方可按提案G0→G1顺序执行，失败STOP，不请求重复的微观审批。

0. 保持 research/paper1-chinese-defense-5060 独立分支、先检查AGENTS、当前HEAD/dirty工作树；原Owner27/28/30/31数据、掩码、程序、结果不改；Owner31已 NO_GO，未获授权不得重用5090已冻结的虚构holdout来验证独立真实来源。
1. G0优先判别一个事实：外部版本化事实证据是否能提供Q-CER缺少的可信时间/范围信息。Owner31记录B2已删71片段中50段缺可核时间、9段缺scope；按预封存种子只抽10条角色盲B2被删片段与query，不看P/C/H/N角色，验证已有真实可信source index能否独立找到版本化官方证据。每次输出 source URI、TLS与独立读取依据、doc sha、版本有效窗、scope可用性和访问状态；不要从造数者Gold/receipt给出正确事实。官方文本使用权未知则仅查metadata/允许的短片段，不爬全文。>=3/10可用候选才建议进入G1；否则SOURCE_GATE_NO_GO。
2. G0通过且Owner确已批准后，写一个独立模块，输入只限query+TopK文本/B2 mask+从冻结独立官方索引返回的候选；核心输出 TRIGGER/EXTERNAL_EVIDENCE_ID/VALID_AT_QUERY/KEEP/DROP/REPLACE/UNRESOLVED。建立source pool冻结SHA和查询消耗日志，真正来源核查不靠自称机构和来源ID。
3. 先固定公平比较场景：同 TopK5；B2+等量可访问补充检索、B2+always-verify、V-CARE、V-CARE no-scope、V-CARE no-rescue，统计每个查询的检索次数、证据token预算、总证据槽与延迟；若V-CARE比只做相同额外检索的B2好，才算方法效益。不得把多拿到正确答案的收益写成算法创新。
4. DEV仅Owner27 32已揭示主世界；Owner28和Owner30是已暴露资料不叫EVAL，不能读取5090私有Gold。一次DEV v0最多有因据的v1；条件P、C、HN均不劣B2，C至少净保5或P至少多滤3，且相比B2+同预算补检仍分别净保>=3C或净滤>=2P。若全部靠Oracle或无法公平配置 STOP。CPU2、D盘增量<=2GiB、运行45min内；无法达标直接METHOD_NO_GO，不请求解封5090私有新事实。
5. 向Owner回传真正的G0统计或G1实测指标：Gold来源、代码/参数/数据快照SHA、分母、P/C/HN误删/保留、触发与额外检索率、matched budget baseline、成本、失败与NEXT_GATE。仅当前阶段的事实报告；不预言一定GO。只在5060分支推送。D2/D3/HOLD8及5090 Claim1–3仍锁，API默认0，Human Gold0。
