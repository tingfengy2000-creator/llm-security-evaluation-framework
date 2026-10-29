# Core144状态V29：Owner批准L0 R02，数据线不变

2026-10-29（JST）；PODR-153 / OR-108 / REL-2026-0123。
[R02批准与执行合同](vace_lite/VACE_L0_R02_OWNER_APPROVAL_AND_EXECUTION_V1.md)。

| 工作线 | 当前事实 | 下一门 |
| --- | --- | --- |
| 原实验R01 | 真实5090/Qwen已加载，合成4/5，SYN-3判决/理由冲突；D1未运行 | 原失败记录和HARD_STOP永久保留，不在原目录重跑 |
| 当前实验R02 | Owner批准仅将合成语义准确率改诊断，保留工程硬门、同模型/prompt/parser/输入/参数；新Run工程包就绪 | 5090固定新源码check-only→合成工程门→240新预测封存→独立评价/归档 |
| D2数据线 | 两个HN修复仍待原会话定向两阶段复审，全144未最终验收 | 不因R02启动而改题或发Human |
| D3数据线 | 两S3单源反例仍待Owner决定，Phase2暂扣 | 独立数据/Owner门不变 |

R02 Run `VACE-L0-D1-20261029-R02`；只读复用R01权重/env/input；新目录不得嵌套或覆盖旧目录，不重新下载或安装。
当前仅LOCAL工程验证，R02实际GPU执行未观察、D1指标未测量，不能写已完成或填0。
D1_DEV40/120/13家族、8/24HOLD，D2/D3/Guide/Human/Evidence/正式GT/split均不变。
旧R01严格语义门仍失败；本次只为新R02显式supersede该门，不抹除历史或给Worker自主调参权限。
