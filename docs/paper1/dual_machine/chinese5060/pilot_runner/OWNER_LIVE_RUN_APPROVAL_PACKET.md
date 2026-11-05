# 5060 Pilot12 真实执行审批包

状态 `IMPLEMENTATION_READY_EXECUTION_BLOCKED`。Owner 09 授权代码和模拟验收。下次真实生成须单独登记审批编号，并绑定下表全部准入证据。

| 准入项目 | 当前状态 | 一次批准的绑定内容 |
| --- | --- | --- |
| 代码与冻结输入 | PASS | Runner 源码提交 `1a11fd2ef4802d5029619acb3e65c5ad09a4a57e`，源文件 SHA 与模拟证据见 QA。proposal `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`，私有计划 `7db82812f893fc0384b2896c98bb5c779504e19a5c45a097945962e840999c96`，共同 system `b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1` |
| 账户、地域、费率、可用额 | OWNER_ATTESTED | Owner 已核验。审批绑定受控本地证据摘要及端点身份，凭证只在未来经授权的进程通过环境变量读取 |
| 模型与 wire | WIRE_UNVERIFIED | 精确模型 `qwen3.7-plus-2026-05-26`，POST `/compatible-mode/v1/chat/completions`，候选 `max_tokens=256`、`enable_thinking=false`、`enable_search=false`、`stream=false`、`response_format={"type":"json_object"}`、temperature 0、top_p 1、无 tools。返回 model 必须精确匹配，响应和 usage 严格校验 |
| 精确 Token | TOKEN_GATE_BLOCKED | 绑定同模型离线 tokenizer 和聊天模板哈希，以及 108 个请求 ID、prompt SHA、完整 chat-template token 计数。任一格 >4096 时停发，保持输入字节 |
| 费用硬门 | BUDGET_GATE_BLOCKED | 本地 hash-pinned 费率、账本、未结算、余额、FX、覆盖全部调用的快照和 Owner 美元 ceiling，另做来源和时效核验 |
| 传输与运行权限 | LIVE_NOT_AUTHORIZED | 提交并审核真实传输实现、审批签名或不可变授权锚点及严格哈希核验，绑定最终可运行源码/环境和指定工作区。凭 CLI 或环境变量不能解锁 |
| 评价与结论边界 | PASS_OFFLINE_ISOLATION | 完整结果封存后，由独立开发评价进程按单独允许的输入做暂定一致性评价。Human Gold 0、target 未知、正式 ASR/QA 未测 |

接口候选依据百炼官方 Chat Completions 说明。该文档将 `max_tokens` 标为将弃用，且将 `max_completion_tokens` 定义为涵盖推理与答案的总输出上限，并说明实际值可能有最多 10 tokens 偏差。当前候选使用 `max_tokens` 配合显式关闭 thinking，仍须核对目标账号/区域能否保证 256 的实际计费硬上限。若需改字段、下调请求 cap 或提高预留上限，纳入 Owner 审定。 [百炼 Chat Completions](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions)

固定 36 世界 × 三臂，每格至多一次，108 个请求槽位。并发 1，SDK 重试、人工重试、Judge 和探测均 0。相同提示词跨格照常保留。空上下文本地拒答。连接/读取/总超时的候选为 10/60/90 秒。首个异常封存原始响应哈希、失败用量或未结算预留，其余记 `NOT_RUN`，留存后停止。

最大 token 预算为 442,368 输入和 27,648 输出。按每百万未缓存输入与输出费率，基础预算 `0.442368 × P_in + 0.027648 × P_out`，建议预留 20%，实现按格向上取整。全工作线已结算 + 未结算 + 整批预留需低于 USD 28，投影达到 USD 25 预警，累计达到 USD 30 硬停。余额覆盖未结算与整批预留，额外受 Owner 的整批美元上限限制。异常不按免费结算。历史 CNY 7.611826 与 CNY 7.528095914 的 CNY 0.083730086 差额保持待对账。

本地数值入口使用 `admission/BUDGET_PRIVATE.json` 和 `--preflight --budget-sha256 <SHA256>`。字段与单位可从 [门状态和数值模板](PROVIDER_MODEL_TOKEN_BUDGET_GATE.json) 恢复。字段审计结果仅为数字准入，证据来源及授权由下次审批绑定。

候选命令 `NOT_APPROVED`。以下参数由受控传输版本与新执行合同最终冻结。当前代码对该命令返回 `LIVE_NOT_AUTHORIZED`。

```powershell
python -I -S -B scripts/research/run_chinese5060_minimal_rag_pilot.py --live --owner-execution-approval <NEW_APPROVAL_MANIFEST> --output-dir <NEW_CONTROLLED_D_OR_E_RUN_DIR>
```

## PO-MHEP 决策记录

1. Issue ID `W1-5060-RUNNER-LIVE-GATE-01`。
2. 名称为真实传输、精确 Token 与累计预算准入。
3. 发现阶段为 Runner 工程验收，真实 Pilot 仍未启动。
4. `OBSERVED_FACT` 为 108/108 模拟成功、真实 0 调用、live 构造被拒。 `SOURCE_DERIVED_FACT` 为 Owner 09 的工程授权、账户确认和固定预算门。 `INFERENCE` 为现有模拟可验证流程和硬停。 `UNKNOWN` 为精确 token、当前机器预算承诺及所选端点的硬 cap 与计费语义。
5. 受影响约束为冻结输入与模型、D1 数据外传审批、USD 30/25/28、独立评价和历史封存。
6. 首次真实发送前必须闭合各门。发送后才发现用量或费用不匹配会产生不可回收的调用。
7. 风险包括实际 token 超上限、隐含账单、端点错误或模型别名、异常恢复重发、参考泄漏与工程数据误报为论文指标。
8. 选项 A 为本轮交付离线实现并暂停，新增 API 费用为 0，可直接复核。选项 B 为新审批绑定已核证据与审核后源码，批准一次有界真实批，成本为已核整批预留，未发送格可停，已发费用须对账。未授权的先调用探测不纳入候选。
9. LOCAL 推荐本轮按 A 收口。
10. 置信度来自源文件与 Git 绑定、三份模拟封存、测试和过程隔离。真实平台行为仍待核验。
11. 下次由 Owner 确认一次性真实运行的执行 SHA、数据外传范围、确切运行配置、计费硬上限及受控预算证据。既有账户核验沿用。
12. 决定前可复核脱敏证据与批准范围内的离线材料。真实请求、账户探测、下载、正式评分及后续研究阶段均未授权。
