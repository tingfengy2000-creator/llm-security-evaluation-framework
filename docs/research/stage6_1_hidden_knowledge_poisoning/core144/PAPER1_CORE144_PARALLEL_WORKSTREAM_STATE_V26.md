# Core144状态V26 — 5090 Cursor交接包就绪，GPU实验尚未执行

2026-10-29 JST；PODR-151 / OR-105 / REL-2026-0120。
Task `P1-VACE-L0-5090-CURSOR-HANDOFF-01`，父任务L0强基线科学范围不变。
[Cursor执行合同与命令](vace_lite/L0_5090_CURSOR_EXECUTION_PACKAGE_V1.md)。

| 项目 | 当前事实 | 下一步 |
| --- | --- | --- |
| LOCAL | 5060阻断保留；可准备代码/私有包，不在本机推理 | 不下载权重、不假称CUDA通过 |
| 执行端 | Owner明确5090使用Cursor，正常阶段可自动继续 | Worker自行验证5090/kernel/预算/合成硬门 |
| 代码 | 同模型F5/Oracle、固定prompt/parser、日志、续跑、封存后评价、归档入口 | 固定Git提交后在Worker运行 |
| 私有输入 | 40组120条13家族，runtime/evaluation分离，8/24 HOLD | 另传V2 ZIP，不放Git |
| 模型 | 官方Qwen2.5-7B revision a09a35458c702b33eeacc393d103063234e8bc28；权重清单/预算24GiB | 只在Worker复用/必要下载并核验SHA |
| 预检验收 | CPU合同/虚构端到端测试，不是真实模型/5090运行 | 不能把静态/模拟结果报成L0检测率 |
| 实验状态 | L0-F5/Oracle NOT_EXECUTED，WORKER_NOT_STARTED | 完成两条件评分/私有Return ZIP后Owner审阅 |

不因无人值守豁免身份/资源/合成/数据质量硬门；不补标签、不改真实数据/Guide/GT，不运行D2D3或VACE-LM。
状态`L0_5090_CURSOR_HANDOFF_READY / WORKER_NOT_STARTED`。V25只描述LOCAL硬件，未被重写成5090通过。
