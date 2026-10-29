# Core144状态V28：5090 L0停在合成语义门，D2/D3分工不变

2026-10-29（JST）；PODR-151 / OR-107 / REL-2026-0122。实验源码仍为 `a83437ab0a685d69114093fd4bd0e6ab22f354aa`。
[合成门阻断](vace_lite/VACE_L0_5090_SYNTHETIC_GATE_BLOCKER_V1.md)。V27的“尚未收到5090回包”已被本状态取代；D2/D3事实不改。

| 工作线 | 当前可核实状态 | 下一门 |
| --- | --- | --- |
| 原对话实验 / L0 | RTX5090已加载官方Qwen2.5-7B。SYN-3期望SUPPORT、实得CONTRADICT，合成门失败。D1 240条NOT_EXECUTED，指标未测量 | Owner审阅硬停。禁止删HARD_STOP后重跑或按这次失败改prompt |
| 新对话D2 | 48组144条，37建议已处置、两个HN最小修复待原R3/R4定向两阶段复审 | 先两题Phase1原件锁/验收，再正式targeted Phase2；全144验收前不发Human |
| 新对话D3 | 48组144条；两个拟S3路径可单源反驳，Phase2 withheld | Owner先决定有界修复/重分配/HOLD |
| 新对话本身 | 交接包仍就绪；本记录不创建会话 | 数据线不得读取本L0失败来改Candidate/Evidence/Guide |

D1_DEV40/120/13家族及8/24 HOLD、原数据/Guide/人工/Evidence/历史均不变。Core正式GT/split未执行。无VACE-LM、无训练。
