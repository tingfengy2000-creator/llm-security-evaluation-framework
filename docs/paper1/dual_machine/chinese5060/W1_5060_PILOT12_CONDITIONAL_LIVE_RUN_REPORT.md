# 5060 Pilot12 有条件真实执行与准入结果

2026-11-05 JST · `W1-5060-PILOTLIVE-20261105-01` · **`LIVE_GATE_BLOCKED_NO_REQUESTS`**

Owner 10 已批准证据齐备后的一次性 3+105 Pilot。独立离线预检退出码 3，A–E 全门未通过。真实 HTTPS POST 0、成功 0、失败 0、未运行 108，首 3 格均为 `NOT_RUN`。真实输入和输出用量各 0，本任务新增费用及新增在途 USD 0，既有累计费用仍待对账。无真实 Run ID、响应或首 3 格工程通过记录。

## 上下文恢复和风险审查

仓库是 LLMGuard Research Framework，优先进行 RAG 安全研究，其后是安全评测、AI Guard 和 Agent 安全。Paper 1 继续阶段 6.1 的中文隐蔽事实污染 D1 开发验证，前一轮完成的是离线 Runner 验收。专用工作树 `.worktrees/paper1-chinese-defense-5060`。本地和上游 `research/paper1-chinese-defense-5060` 经已审查的五个治理提交，从 `ce90a34348dff093e132e6f9823ad9b84e4f67d9` 安全快进到 `312f9b17dba2a20c142507ce7df5ec7ae203642d`。启动时无未提交和未推送变更，ahead/behind 为 0/0。基线 tag `s6-t5-rag-baseline-v1` 指向 `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。

已核对 AGENTS、权威映射、PO-MHEP、Owner 原件、当前状态、长期需求、实验总表、研究路线、执行日志和离线证据。授权与 Git 一致。仅开放真实传输候选、离线检查，以及 A–E 齐备后的单次固定序列。剩余 105 格的唯一阶段门是首 3 格工程通过，已包含在同一授权。旧样本、检索、过滤、提示词、参数和评价边界均受冻结合同约束。[Owner 10 原件](../owner_approvals/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_AUTHORIZATION_20261105.md) · [固定合同](W1_5060_PILOT12_CONDITIONAL_LIVE_3PLUS105_EXECUTION_PROMPT_V1.md)

**Forward Risk Review** 核对官方地域端点、TLS、超时、单发、代理/重定向、授权绑定、失败计费、D/E 资源和评价隔离。**Paper Risk Review** 核对 12 个事实组、36 世界、三臂共 108 格，80 个唯一提示词仍逐格保留。29 个候选命中和 7 个漏召回是检索分母，0 个空上下文、3 格单 chunk 是生成输入特征。首 3 格只检查传输和计费等工程指标。历史 Fast C 根因未识别及 B2 Clean 误删升高保留，Pilot12 不能验收 2.5 pp 保护门。

## 准入判定

| 门 | 已核验 | 未闭合条件 |
| --- | --- | --- |
| A 输入与外传 | 原 P2、PAIR01 封存、Fast C 归档哈希一致；108 格从原角色盲输入重新投影，wire 字节完全一致。四类敏感信息模式均 0 命中 | 缺逐来源可复核使用权、敏感信息裁决和获准处理方/地域范围，模式扫描覆盖有限 |
| B 模型与传输 | 固定请求 wire 与 HTTPS 候选在模拟端通过。固定模型保持 `qwen3.7-plus-2026-05-26` | 缺绑定账户的唯一官方地域 host 和旧 `max_tokens=256` 涵盖隐藏费用的总计费硬上限 |
| C 输入 Token | 全 108 格静态代理最大 2956 | 缺已核身份的本地同模型 tokenizer 和聊天模板，或严格保守上界证明 |
| D 账本与资源 | D 盘余量超过 20 GiB。历史差额和 USD 25/28/30 阈值保留 | 固定私有入口无数值账本，缺可核全线已结算、未结算、失败在途、费率/FX、资金和整批预留 |
| E 授权和封存 | Owner Git 原件、候选源码、离线测试和全部 108 格拒绝状态均按 SHA 绑定 | 无 A–D 通过证明，独立检查器没有签发运行权限或全 PASS manifest |

官方文档对旧 `max_tokens` 的通用说明限定答案长度，`max_completion_tokens` 语义涵盖推理与答案，且文档提到后者可能偏差 10 tokens。旧字段在目标账户/模型上的严格总计费上限仍缺证据。保持原字段并停发。[百炼接口文档](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions)

## 工程验收和结论

候选源码提交 `4826ddbf5721e748c499198af931be984807a0db`。标准库 HTTPS 候选和首 3 格推进逻辑经模拟测试。独立 CLI 在阻断状态拒绝 `--live` 及调用方提供的 manifest 摘要。当前构建只实现拒绝路径，尚未接入通过全部机器证据后的放行、真实逐格账本和发送意图编排。实际 TLS/端点行为无实测。46 项测试通过，包含原 29 项回归及 17 项新增，Ruff 和 MyPy 通过。首轮第 1 格超时测试错误地把缺省零计数与显式零键比较，修正断言后重跑通过，原失败留档。

私有预检归档 `W1-5060-PILOTLIVE-20261105-01-PREFLIGHT.zip` SHA256 `f0be558ace3258cc14ef017e57fc8102cc03b946854fd02cd18b6c3b97fba831`，共 34 项，逐项校验通过。全 108 格状态 SHA256 `b349c7ab65cccbf9765d4439f9fa8dd6060fc2812a94630e697929d4d0bdf0d1`。[门矩阵](pilot_live/ADMISSION_GATE_MATRIX.json) · [状态汇总](pilot_live/LIVE_3PLUS105_EXECUTION_SUMMARY.json) · [封存索引](pilot_live/FINAL_LIVE_RUN_AUTHORITY_AND_MANIFEST_INDEX.json) · [PO-MHEP 记录](pilot_live/FAILURES_AND_PO_MHEP.json)

独立暂定评价 `NOT_RUN`，Human Gold 0，攻击目标未知。C3、Targeted ASR 和正式问答准确率均 `NOT_MEASURED`。本轮完成阻断收口并停止。

额外治理与架构测试 8 项通过、1 项历史便携性失败。实施前后均匹配同样 5 行历史 Windows 绝对路径，本轮新匹配 0 行。 [QA](pilot_live/FINAL_QA.json)
