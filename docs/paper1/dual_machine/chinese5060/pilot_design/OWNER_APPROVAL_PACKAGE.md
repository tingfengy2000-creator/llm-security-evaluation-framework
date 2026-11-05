# 下一Owner Gate审批清单（本次不申请即时调用）

状态：DESIGN_ONLY_NOT_RUN；设计可审阅，执行DESIGN_GATE_BLOCKED。HumanGold不是此D1可行性设计的前提，也不因暂定参考获批就自动获得执行许可。

| 必需确认 | 已准备/待确认 |
|---|---|
| 固定12组/36世界、G0/G1/G2 | 已物化108格哈希，原TopK/过滤不重跑 |
| 参考 | 固定SHA JSON已收到、12题精确映射；仅评价侧，Gold0 |
| 生成模型/账户/区域 | 字面ID qwen3.7-plus-2026-05-26；当前可用性待Owner/正式账户材料确认，无本轮探测 |
| 共同prompt与参数 | 完整模板/system哈希及每格prompt哈希已提供；4096输入/256输出、temperature0、一次一请求、无重试为待审值 |
| 精确token与adapter | 未运行Tokenizer；需获准的精确计数/聊天模板版本、所有108格证明及厂商wire字段/usage/非Thinking契约 |
| 最大费用 | 当前价格、余额、统一累计账单/FX待核；公式及20%候选预留已提供，无实价不能签数值报价 |
| 评价与风险 | 暂定一致性/UNKNOWN/拒答/故障政策待接受；无judge API、无ASR/正式QA/C3，保留2.5pp门但不能证明满足 |
| 执行授权 | 需新的Owner SHA明确输入/配置/proposal SHA、最多108物理请求及已核USD ceiling；本08授权不能填此项 |

建议一次批准范围仅限三臂108格，不添加探测/judge/retry。实际API runner当前未实现，候选命令仅文本；实现与静态验收不能被这次设计冒充已完成。
本轮先停止，Owner可在价格/账户与token/adapter证据闭合后单独审执行；不反复要求提供密钥或先完成Human Gold。

## PO-MHEP十二字段（执行预算/计数门未闭合）

1. Issue ID：W1-5060-PILOTDESIGN-GATE-01。
2. 名称：设计完成但精确token、provider适配与实时预算准入未知。
3. 阶段：最小端到端Pilot设计，尚未获执行许可。
4. OBSERVED_FACT：108格和参考SHA/映射已核、实际调用0；SOURCE_DERIVED_FACT：08仅设计授权与USD30/25/28门；
   INFERENCE：只能给条件式预算表达式，不能开始模型探测；UNKNOWN：当前价格/账单/余额/FX/精确token与model可用性。
5. 约束：AGENTS/PO-MHEP、08、数据隔离、累计费用与不可变输入/参考。
6. 原因：先启动再核价/usage将绕过费用及模型身份硬门。
7. 风险：费用超限、隐藏重试/Thinking计费、上下文截断、角色/答案泄漏、把暂定一致性当正式QA；继续设计不产生这些调用风险。
8. 选项A：按本包交付并STOP，费用0、可逆，等待准入材料；选项B：Owner后续补齐证据并新SHA批准有界执行；
   未批准选项C是为了核可用性先发API或静默改预算/模型，不执行。
9. LOCAL建议：A，本轮不请求立即执行。
10. 理由/置信度：输入/参考和静态长度高可追溯，实时价格/可用性和精确token未知；不把代理量当计费tokens。
11. 待Owner：审核共同模板/256输出与暂定评分边界，并在未来执行审批前补齐账户价格/预算及计数/adapter证据。
12. 决定前：只保存脱敏设计、证据与Git后STOP；禁止任何模型/API/过滤/检索/重选组/答案修订/新机制或阶段。

待审proposal原字节SHA256：`0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`；共同system hash：`b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1`。这两个hash不产生执行许可；未来新增Owner决定必须再绑定所有准入证据。
