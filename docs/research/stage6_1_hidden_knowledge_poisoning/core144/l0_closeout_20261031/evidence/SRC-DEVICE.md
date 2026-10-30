# L0-F5 / L0-Oracle尚未运行：当前执行机不是指定RTX5090

**L0-F5：NOT_EXECUTED；L0-Oracle：NOT_EXECUTED。S1/S2/S3、Recall、FPR和弃权率均未测量，不能填0或沿用V03结果。**
2026-10-28；Task `P1-VACE-L0-F5-ORACLE-STRONG-BASELINE-01`；PODR-150 / OR-104 / REL-2026-0119。
本记录是预检阻断，不是强模型实验结果、CUDA软件故障诊断或方法可行性结论。

## 1. Issue ID

`L0-DEVICE-IDENTITY-BLOCKER-01`。

## 2. 问题名称

本执行机仅枚举到RTX5060 8GB，未发现本轮指定的本地RTX5090 32GB。

## 3. 发现阶段 / 任务

模型与环境只读初检，尚未模型下载、隔离环境安装、revision/权重/许可冻结、合成推理或D1执行。
源HEAD `46f509ac5f2e43da39ef1690926197bd97417e19`，唯一研究worktree；upstream核验0/0，无HEAD tag。
既有无关design.md修改及PDF保持，不自动pull或覆盖。当前Paper1主线是版本化困难负样本基准、分层失败归因和轻量核验。

## 4. 事实分类

| 类型 | 事实 |
| --- | --- |
| OBSERVED_FACT | 两次只读`nvidia-smi -L`/query仅列出GPU0 NVIDIA GeForce RTX5060，8151 MiB，驱动616.92 |
| OBSERVED_FACT | 当前进程未设置CUDA_VISIBLE_DEVICES；无RTX5090设备列举。CIM补充读取无访问权限，不提升权限重试 |
| SOURCE_DERIVED_FACT | Owner指定官方Qwen/Qwen2.5-7B-Instruct、本地RTX5090 32GB、新增模型依赖合计≤24GiB，硬件/CUDA预检失败即停止 |
| SOURCE_DERIVED_FACT | 既有项目治理区分LOCAL控制面和RTX5090 Worker；历史Worker完成不等于本机当前有5090或已获本任务远端执行入口 |
| INFERENCE | 当前执行机不满足本任务设备身份前提，不能静默用5060、CPU、量化或别的主机替代 |
| UNKNOWN | 5090的现时主机/项目路径/执行入口；该机模型权重、CUDA kernel和隔离研究环境状态 |
| UNKNOWN | 模型revision/tokenizer/weights SHA/许可证完整核验、dtype/框架依赖/上下文/实际token与VRAM；均未冻结 |

已有目录初检仅覆盖有限位置，不能声称全机器没有Qwen权重；模型/CUDA软件是否可用尚未判定。
`nvidia-smi`显示驱动API能力不等于指定设备上的Torch CUDA推理已通过。

## 5. 受影响约束

Owner的设备/资源身份和“预检失败即停止”硬门；PO-MHEP的环境偏差/主机身份与复现边界。
原D1_DEV40组120条13事实家族、8组24条HOLD、同模型F5/Oracle、先封存后评分、数据不改等边界仍有效。

## 6. 为什么必须现在处理

设备错误若不先关闭，下载/安装会占预算但不能验证获准条件；偷偷换卡或量化将改变dtype、上下文及速度/VRAM比较。
不能在未指定正确执行机前把“本地5090实验”写入Manifest，也不能把预检失败归咎于模型不会事实推理。

## 7. 下游风险

工程：8GB显存与32GB资源合同不符，可能OOM/截断/CPU offload；架构：控制面/Worker身份混淆；
实验：硬件、精度、上下文或模型替换破坏可比性；论文：伪造执行环境或把无结果当失败性能；
复现：模型/运行身份无法绑定；时间/资源：无效大下载或重复缓存；安全/许可：系统安装或新远端/源未经确认。
FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW结论：**暂停执行，不改变协议、不下载、不换模型或硬件**。

## 8. Owner选项

### A. 明确RTX5090的执行入口（推荐）

行动：在5090机器打开本研究任务，或提供已授权Worker主机与项目绝对路径及运行方式；随后先只读预检，再按原合同冻结。
优点：保留原Qwen/32GB比较；缺点：需要一次主机交接；成本：预检和来源/环境核验，尚不能给下载时间保证。
风险：另一机环境仍可能不符，未核实前不推理；后续/论文影响：保持同条件基线可比；可逆性：无数据改动，可随时停。

### B. 明确提出另一个设备/精度合同（本轮未批准）

行动：Owner另行决定是否研究5060/量化等独立条件；不能自动当本任务等价执行。
优点：可能利用当前设备；缺点：模型精度/上下文/成本条件变化；成本：需新协议与容量预检，未保证8GB能运行。
风险：精度和证据截断confounder；后续/论文影响：须独立标记，不能冒充32GB基线；可逆性：设计可撤回，安装不得先做。

### C. 保持暂停

行动：仅保存本次只读证据和治理记录，待设备可用；优点：零下载/安装风险；缺点：本轮没有检测数字。
成本：当前无新增模型依赖磁盘占用；风险：推进延迟；后续/论文影响：不改变数据或方法证据；可逆性：后续可新attempt恢复。

## 9. LOCAL建议

采用A；当前先按C封存阻断。本轮不自行联系/控制另一台GPU机器，不准备可执行Worker下发包绕过停门。

## 10. 理由与确定性

设备枚举直接支持“当前可见不是5090”；不推断5090不存在于用户其他机器。
对硬件身份不符结论明确，对替代环境和模型可行性保持UNKNOWN，不给虚构资源估计或检测率。

## 11. 需要Owner提供的信息

**RTX5090所在的执行主机及项目入口是什么？** 可在该机打开任务继续，或说明已授权Worker和项目路径。
不需要重新批准原模型科学目标；但跨机入口/身份和实际环境必须先确认。

## 12. 决定前允许 / 禁止的工作

允许：只读核验、证据/上下文保存、文档与Git收口。
禁止：模型下载、依赖安装、驱动或全局环境改动、5060/CPU/量化/其他主机替代、合成/真实推理、D1评分、D2D3、正式split/GT或VACE-LM实现。
本轮新增模型/依赖下载=0字节；安装=0字节；推理=0；不形成L0预测或指标文件。
状态：`L0_STRONG_BASELINE_PREFLIGHT_BLOCKED / HUMAN_DECISION_REQUIRED`，不是`L0_STRONG_BASELINE_D1_DEV_COMPLETE`。

## Evidence / documentation closeout

私有命名空间`experiments/vace_l0_strong_20261028_run01/`，保留设备查询原始stdout/stderr/exit code、UTC时间和SHA。
文档仅保存必要设备摘要，不发布设备UUID/主机标识或本机私人绝对路径。
Human/Agent/Current/Owner/Execution/Experiment Master/Project Master/Stage Process与导航同步；
Research Plan Authority、长期合同、Guide、数据和历史不改，原V03结果保留。
本轮无需Ruff/MyPy业务算法验收；仅对新增预检记录的静态治理测试/UTF8/链接/秘密/历史保护及diff检查。
阻断状态和下一步已物理保全，停止等待执行主机信息。

静态预检/历史合同54项测试、任务范围Ruff/MyPy、28项保存/链接/UTF8/隐私/历史检查通过；
这些都不代表GPU或合成推理通过。旧149+61+27+73共310文件hash不变，无关design/PDF原SHA保持。
27文件私有索引SHA `37a008c91b9bbf9cbaa500d3c6221ac264f9f811b72e43f749fb432764987891`；
blocked Manifest SHA `7064f74c55b02321706233800f3c0ccd6f4f210de7fefc3c466c0f188318141a`。
17项文档收口字段true，仅表示BLOCKED状态记录完成，execution_done=false，不能报任务已完成。
