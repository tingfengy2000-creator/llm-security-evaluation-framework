# 5060 Pilot12 V2 单次真实生成结果

`RAPID_LIVE108_COMPLETED` · `OWNER12_LIVE_108` · 2026-11-05 JST

固定 36 世界、108 格和北京百炼专属 Workspace，模型 `qwen3.7-plus-2026-05-26`。原序首 3 格均通过工程检查，程序在同一次运行内完成余下 105 格。真实 POST **108**，HTTP 200 **108**，工程成功 **108**，失败 **0**，未运行 **0**，重试 **0**。108 份原始回包均已封存并逐份核验。

| 臂 | 发送 | 工程成功 | 回答 | 拒答 | 输入 Token | 输出 Token | 延迟中位数 / P95（秒） | 公示价估算 CNY |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| G0 | 36 | 36 | 15 | 21 | 18447 | 1905 | 1.588 / 4.223 | 0.052134 |
| G1 | 36 | 36 | 13 | 23 | 13003 | 1779 | 1.563 / 8.459 | 0.040238 |
| G2 | 36 | 36 | 11 | 25 | 12976 | 1470 | 1.470 / 2.585 | 0.037712 |
| 合计 | 108 | 108 | 39 | 69 | 44426 | 5154 | 1.557 / 3.029 | 0.130084 |

延迟为客户端实际单次传输时间，P95 采用 nearest-rank，最长 43.065 秒（G0）。实际单格最大输入 574、输出 126，108 格均提供完整 usage，缓存命中 Token 合计 0。0.130084 元按实际 usage 和北京公开按量价估算，账户实际扣款及美元结算未核。运行器在途预留归零。Owner 本轮的费用豁免仅覆盖这 108 格。[百炼模型与公开价](https://help.aliyun.com/zh/model-studio/qwen3-7-plus)

拒答是回包中通过 schema 的 `ABSTAIN`。G0/G1/G2 分别拒答 21、23、25 格，每臂分母 36。拒答和回答计数只描述模型输出，回答正确性及防御效果待独立评价。现有独立 Evaluator 未提供本轮 live seal 的可执行评价入口，暂定参考一致性为 `NOT_RUN`。Human Gold 0，攻击目标未知，正式 ASR、Answer Accuracy 和 C3 均 `NOT_MEASURED`。正式实验未开始。

## 可复核证据

- 执行源码提交 `8b0af037a15b7a718d968879e848c0cd3c5eab77`。独立准入 SHA256 `908d38a26d7589c1964ced1feada4e70b3884103d191ee17bda107159b01e60f`，绑定原 Owner12、单批豁免、精确 108 格、46 来源的出站范围审阅、既有北京 Workspace、后置 usage 和唯一输出目录。
- 原输入 grid SHA256 `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c`，wire plan SHA256 `0920add3e5b5383a9b685207cabeb539bb3d414ee1db30c6f7a313d37469bbcc`。
- 运行清单 SHA256 `5b8dc3b58d4c374565c3ccec1baadd470ccb20d55b1ebaf22be5ec35d24b788f`，输出封存 SHA256 `ca8aa84c7485149c887abe7b60e8890f4c01e81b21e8ac46f19cf83866ff5da4`。
- D 盘 Git 外私有 `OWNER12_LIVE_108_PRIVATE_EVIDENCE.zip`，SHA256 `a1a5eb07c74d2513bd8f14ac626799cfdc10f422341bae2cbd7c5c5feb029647`。归档含 108 份原始响应、逐格用量、延迟、发送事务、封存清单及核验日志。
- 离线回归 67 项，Ruff 和 MyPy 通过。治理测试 8 项通过，既有 Experiment Master 路径可移植性检查 1 项失败，历史行保持原样。

## 治理收口

本结果接续首发前阻断快照。按本次确认完成原 V2 的唯一一次执行，Owner12 本批授权已用毕，状态为停止。原预算政策继续约束其他批次。Human/Agent Ledger、Current Work State、Project Master、Experiment Master、Research Execution Log 与本阶段流程已同步。Owner Decision Register 已登记单批决定。论文研究计划、导航和长期方法经验的更新条件未触发。后续独立评价或新实验需另行定界。

[脱敏证据索引](RAPID_LIVE_EXECUTION_INDEX.json) · [原阻断快照](RAPID_LIVE_OWNER12_RESULT.md) · [原 Owner12 授权](../../owner_approvals/W1_5060_PILOT12_RAPID_LIVE_OWNER_AUTHORIZATION_20261105.md) · [本批豁免回执](../../owner_approvals/W1_5060_PILOT12_RAPID_LIVE_BUDGET_WAIVER.md)
