# 5060 最小 RAG Pilot Runner 实施与准入报告

2026-11-05 JST · `RUNNER_IMPLEMENTED_LIVE_NOT_AUTHORIZED` · `W1-5060-RUNNER-20261105-01`

Owner 09 的本地工程范围已验收。固定计划的 36 世界 × G0/G1/G2 共 108 格、80 个唯一提示词，逐格编排并通过模拟请求。真实生成 108 格均为 `NOT_RUN`，实际模型/API 调用 0，新增费用 USD 0。Human Gold 为 0，攻击目标未知，targeted ASR 与正式问答准确率均为 `NOT_MEASURED`。

## Context Recovery 与风险审查

- 仓库为 LLMGuard Research Framework，优先开展 RAG 安全研究，其后为安全评测平台、AI Guard 与 Agent 安全。Paper 1 当前工作线验证中文 RAG 隐蔽事实污染及防御基线，处于阶段 6.1。
- 专用 worktree `.worktrees/paper1-chinese-defense-5060`，分支及 upstream 为 `research/paper1-chinese-defense-5060` 与 `origin/research/paper1-chinese-defense-5060`。经 fetch 后从 `bbfda7ddd9fe820b908639c7943daef6c87cec6d` 快进至 `e378f04835709a0753ab27f913638642714351bb`，启动时干净且 ahead/behind 0/0。基线 tag `s6-t5-rag-baseline-v1` 指向 `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。
- 已核对 AGENTS、Context Authority Map、PO-MHEP、Owner 决议、当前状态、长期要求、研究路线、实验主表和执行日志。启动授权与 Git 一致。本轮范围是 Runner、离线测试、预算/Token 准入与交接，真实执行归下一审批。详见 [Owner 09](../owner_approvals/W1_5060_RAG_PILOT_RUNNER_IMPLEMENTATION_AUTHORIZATION_20261105.md) 和 [固定实施合同](W1_5060_PILOT12_RUNNER_AND_ADMISSION_IMPLEMENTATION_PROMPT_V1.md)。
- **Forward Risk Review** 覆盖模型 SDK 隐式网络和重试、C 盘缓存、账号账单范围、失败的未结算责任、历史文件字节漂移和生成评价交叉读取。采用专用纯标准库进程、固定输入白名单、串行一次请求及先记意图后执行的日志。
- **Paper Risk Review** 覆盖基线公平性、重复提示词和 7 个漏召回的分母、假用量与真实实验的证据区分。G0 仍为原 TopK，G1/G2 使用原 B1/B2 保留片段，三臂同模型候选参数。原 29 个条件命中世界与 7 个漏召回世界完整保留。B2 Clean 误删上升、Fast C 因果未识别及 2.5 pp 安全门沿用原记录。当前样本规模无法验收该安全门。

## 离线结果

| 演练 | 模拟调用 | 模拟成功 | 模拟失败 | 停止后未运行 | 退出码 |
| --- | ---: | ---: | ---: | ---: | ---: |
| MOCK108_FINAL01 | 108 | 108 | 0 | 0 | 0 |
| MOCK_TIMEOUT_FINAL01 | 4 | 3 | 1 | 104 | 3 |
| MOCK_MISSING_USAGE_FINAL01 | 2 | 1 | 1 | 106 | 3 |

完整模拟输入 13,824 tokens、缓存输入 1,728 tokens、输出 1,944 tokens、隐藏推理 0。账本使用虚构费率，整批模拟预留 USD 0.630374400，模拟结算 USD 0.018360000。两次模拟失败各保留 USD 0.005836800 未结算预留。每个失败批次均封存全 108 格，响应字节存在时保存 SHA，超时只有尝试记录。显式 live 开关和测试审批值均被拒绝，退出码 2。

最终 29 项测试通过，Ruff 通过，MyPy 6 个源码通过。初次验收发现 Windows 临时目录延迟导入被白名单阻断，改为显式固定 `tempfile.tempdir`。直接启动 mypy.exe 遇到 WinError 623，改用当前 Python 模块入口，随后修正两处容器类型推断。详见 [演练和 QA 记录](pilot_runner/DRY_RUN_AND_QA.json) 与 [失败记录](pilot_runner/FAILURES_AND_BLOCKERS.json)。

## 真实执行准入

- **账户和模型**由 Owner 核验，等级为 `OWNER_ATTESTED`。固定 `qwen3.7-plus-2026-05-26`，候选 temperature 0、top_p 1、关闭搜索和思考、无工具、非流式。
- **Token**使用全 108 格静态长度代理完成本地检查，最大 2,956，0/108 超过 4,096 代理门。精确 token 数尚缺可验证的同模型 tokenizer 与聊天模板。整批上限仍为输入 442,368、输出 27,648 tokens。
- **预算**已实现整批预留、每格检查和费用熔断。当前预算保留已知历史估算 CNY 7.611826、Owner 声明 CNY 7.528095914 与差额 CNY 0.083730086。机器可校验的实时金额、未结算、FX、可用额和整批美元上界尚未闭合。
- **接口**完成候选 JSON 编解码和异常校验，真实 HTTP 传输仍硬锁。下一门须验证所选区域的固定模型、禁用 thinking、JSON、实际输出硬上限与计费字段，并将审核后的真实传输、授权绑定和最终运行命令写入审批。
- **评价**Runner 进程仅访问冻结的角色盲计划和封存哈希。未来真实输出全部锁定后，独立评价侧才能按新审批读取暂定参考；当前模拟封存不可用于评价。

源码提交 `1a11fd2ef4802d5029619acb3e65c5ad09a4a57e`。私有归档 `W1-5060-RUNNER-20261105-01.zip` SHA256 `b63be8be37668f8db63a403c9803732ae10f5b06dfee052ffafc60da4d4face7`，共 160 项，CRC 和成员哈希均通过。审批包汇集剩余硬门，本轮收口后停止。[一次性执行审批包](pilot_runner/OWNER_LIVE_RUN_APPROVAL_PACKET.md) · [安全审计](pilot_runner/SECURITY_PRIVACY_RESOURCE_AUDIT.md)

额外架构与治理检查 8 通过、1 失败。实验总表的历史便携性检查在实施前已匹配同样 5 行 Windows 绝对路径，本轮新匹配 0 行，历史记录字节已保全。失败证据见 [QA](pilot_runner/DRY_RUN_AND_QA.json)。

离线交付内容提交 013d660c6d7378e7d4f5d84bd52161c36b34bd7a 已核验远程一致、工作树干净且 ahead/behind 0/0。最终收据提交的 SHA 在 Owner 回复登记。 [Git 交付收据](pilot_runner/FINAL_GIT_DELIVERY.json)
