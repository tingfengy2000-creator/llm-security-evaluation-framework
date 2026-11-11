# Owner29｜当日端到端生成可行性首格停发记录

状态 `LIVE_STOPPED / 1_SENT / 0_VERIFIED / 95_NOT_RUN / AUTO_CONTINUE_NO`。Owner 本轮批准角色盲材料外传和新增 USD 5，确认余额充足并指示本批按 USD 5 执行。正式盲审、既有结果和历史额度记录保持原状态。

| 实际运行分层 | NONE | RD_B2 | RD_ZH | 合计 |
| --- | ---: | ---: | ---: | ---: |
| 固定格数 | 32 | 32 | 32 | 96 |
| 已发出 | 1 | 0 | 0 | 1 |
| 可核验成功 | 0 | 0 | 0 | 0 |
| 失败 | 1 | 0 | 0 | 1 |
| 未运行 | 31 | 32 | 32 | 95 |

原 32 世界的 TopK5 和掩码按封存哈希复用。DATE_ONLY 32/32 与 NONE 相同，未另发请求。每格仅发送问句、事件日期和该臂保留证据。模型为北京 Workspace 的 `qwen3.7-plus-2026-05-26`，temperature=0，非思考模式，max_completion_tokens=256。HTTP/模型成功状态、回答、用量、延迟和首格实际扣费均未知，已知费率小计 0 仅反映无可核验用量。首格继续占用 CNY 7.15867840 预留，含单次最高费率和缓冲，批次冻结上限 CNY 32.50。无正式 ASR、Accuracy 或新增 Human Gold，四事实组暂无可比较的回答配对。

| 证据 | SHA256 |
| --- | --- |
| 原 TopK Seal | `31ce5b1acfbfb0d6ceebe4acedda0f482ca506462baf48dd9f4ff36a37e4bd45` |
| 96 格请求清单 | `a3ce06197921e086a28fee2429f6cbe2c71acfbde4cddeee3d444ebf480050c2` |
| 实际 Runner | `1ed09aecadfb1e1e3199516678865fcd6870192598c046a94da4359fe06a7f57` |
| 真实尝试 Seal | `412a3f46cc384568d2880cf0a226416b18164866d0a921fc97a6163fb095d1ef` |
| 私有证据 ZIP | `9445062745d3ae1ade468fc4a390c5802fbba594c5c2b5c1d7137079a275d44f` |
| 离线修正版 | `fc5202753b7de0c70af9dbf21010cd393dd07d86927b7067ca2fafe4dfb0a352` |
| 离线修正测试 Seal | `cc991948b5269270addedd5f13094ad61688537cd2c30aff451b25cf5261f923` |

实际基线提交 `103389084b8502084f6aaa9ba93fca32f81d81b2`。真实命令为 `python RUNNER_PRIVATE.py --live`，进程退出码为 0 表示捕获故障并写出 Seal，实验状态由 Seal 判定。私有目录和证据 ZIP 位于 D 盘实验归档。标价及换算来源见 [北京百炼固定模型费率](https://help.aliyun.com/zh/model-studio/qwen3-7-plus)、[输出上限字段](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions) 和 [中国银行外汇牌价](https://www.boc.cn/sourcedb/whpj/)。

## PO-MHEP 停发与裁决

1. 事件 ID 为 `OWNER29-RAPID-POST-01`。
2. 事件为首格发送后回包归档失败。
3. 发生于 Owner29 真实生成首 3 格工程检查的第 1 格。
4. OBSERVED_FACT 为本地留有 POST_STARTED 与 POST_SENT、真实 Seal 记录 AttributeError、无回包文件。SOURCE_DERIVED_FACT 为 Runner 读取 `Reply.request_id`，实际接口字段是 `provider_request_id`，该读取位于写原始回包之前。INFERENCE 为字段错误解释了本地症状，并可用 FakeTransport 确定复现。UNKNOWN 为远端结果、实际账单和原始回包内容。
5. 受影响约束为单次执行、首错停发、零重试、完整分母及证据封存。
6. 当前 95 格保持未运行，避免继续发送后掩盖无法闭合的首格。
7. 工程风险是响应未封存，账本风险是已发首格费用未结算，科研风险是无完整配对。模型、数据、检索、算法和许可边界未扩展。
8. 选项一为停止并仅保留当前证据，新增费用为 0，无法取得回答层结果。选项二为 Owner 另行批准后只执行 95 个未发送格，保留首格缺失；最多 31 个完整配对，费用仍须包含首格未决预留，且任何新发送不可撤回。重新发送首格另属显式重试授权。
9. 本地建议保留首格失败；如果仍需要当日结果，仅申请继续 95 个未发送格。
10. 字段缺陷在本地可复现，修正版的全路径 FakeTransport 有 3 格成功、第 4 格模拟 HTTP 429 停发、92 格未运行，且 4 份模拟原始回包全部先落盘。该测试实际 API 调用为 0。
11. 若继续，需 Owner 决定是否接受首格永久缺失与最多 31 个完整配对，并批准放行剩余 95 格。
12. 决策前仅可核验归档、只读对账和离线修复。保留真实失败，不继续发送或重发首格，不评分或填补缺失输出。
