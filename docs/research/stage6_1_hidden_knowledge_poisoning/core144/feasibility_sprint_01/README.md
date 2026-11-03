# Paper 1 一周可行性冲刺

> 最新执行准备：Owner已提供北京Host/Key并确认许可；[北京V2](BEIJING_EXECUTION_ADDENDUM_V2.md)覆盖下方先前缺口历史。95项CPU测试及Ruff/MyPy通过；真实API尚未调用，下一门是单次虚构接口探测。

Task `PAPER1-FEASIBILITY-SPRINT-01`；2026-11-03；LOCAL 5060 负责，5090不使用。
方法状态 `PROPOSED / EXPERIMENTAL`；当前 `LOCAL_ENGINEERING_COMPLETE / PAID_EXPERIMENT_BLOCKED`。

先读[负责人报告](FEASIBILITY_OWNER_REPORT.md)，再读[实验合同](FEASIBILITY_PROTOCOL_V1.md)。
这是独立新方法研发，不是对旧L0追加提示，不接受或覆盖L0的历史负结果。

| 入口 | 用途 |
| --- | --- |
| [比较边界](BASELINE_COMPARABILITY_MATRIX_V1.md) | 历史Run与同骨干新对照 |
| [内部证书](S1_INTERNAL_CONTRADICTION_SPEC_V1.md) | 不按真实分层路由 |
| [关系核验](CLAIM_RELATION_VERIFICATION_SPEC_V1.md) | 六槽与一次按需补查 |
| [模型/条款核验](API_PROVIDER_REVIEW_V1.md) | 官方文档、地区、价格、保留与参数风险 |
| [费用清单](API_COST_MANIFEST.json) | 实际费用与保守预算分开 |
| [结果](EXPERIMENT_RESULTS.json) | 未执行项为null，不伪造性能 |
| [下一决策](NEXT_RESEARCH_DECISION.md) | 当前结论与最小剩余事项 |
| [工程核验](ENGINEERING_VALIDATION_V1.json) | 合成测试、数据身份和文档门 |

代码在 `src/llmguard/domains/retrieval/hidden_poisoning/feasibility_sprint/`。
入口为 `scripts/research/paper1_feasibility_sprint.py`；独立评价入口为 `scripts/research/evaluate_paper1_feasibility.py`。

## 本地可运行命令

从本工作树根目录执行。无需GPU、依赖安装或密钥：

```powershell
$env:PYTHONPATH='src'
New-Item -ItemType Directory -Path experiments/feasibility_check -Force | Out-Null
python -m pytest tests/unit/test_paper1_feasibility_sprint.py -q --basetemp=experiments/feasibility_check/pytest01
python scripts/research/paper1_feasibility_sprint.py preflight --config configs/research/paper1_feasibility_sprint/api_gate_v1.json --run-dir experiments/paper1_feasibility_sprint_01/dev01
```

预检当前应退出2并报告阻断，且不发送请求。测试里的输出与费用是明确的虚构桩，不是付费模型实测。
实际API配置保存在Git外；Key只从`DASHSCOPE_API_KEY`读取，不在聊天、配置或日志中填写。
本任务已获Global外传授权；账号地区/工作区、数据许可确认和Key仍须闭合，不能用其他项目密钥或静默改服务商。
原始输入位置由本机私有准备索引恢复，不在公开Git中写用户绝对路径。
