# S6.1-LR1 学习与面试笔记

> 本文件是 `NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL`。结构化 Stage Guide 见
> [Stage 6.1 Hidden Poisoning Learning Guide](../../learning/stage6_1_hidden_poisoning.md)；事实冲突时以
> Git、Owner Decision、Current Work State、Experiment Master Record 和 canonical Paper 1 route 为准。

## 这一步做了什么

把 Paper 1 从“有研究方向”推进到“有外部证据锚点的研究控制面”：明确 PoisonedRAG 是攻击基线、GMTP 是检测/
防御基线、SafeRAG 是中文安全 Benchmark 参考，并把论文、源码、commit、许可、数据、模型、预算、指标、硬件和
复现门统一登记。

项目负责人随后将 LR1、Context Recovery Governance、Paper-First Principle 和 current Paper 1 route 正式接受。
RTX5090 Bootstrap 随后通过人工验收，证明 WSL GPU、PyTorch cu130、FP16/BF16 basic tensor 和 Git sync 可用；
`S6.1-R0` 的历史执行批准已完成到 R0-I 审查；当前为 `RETURNED_FOR_WORKER_CORRECTION`。Archive/index hash 完整，
但 GMTP sample-absence/Docker 结论与 exact upstream 冲突，SafeRAG 只有 `DATASET_ARTIFACT_ONLY` smoke 且脚本 provenance/
all-row coverage 待修正。LOCAL 仍不运行 baseline，S6.1-P1 仍未开始。

项目负责人还接受 Control-Plane-First Token Economy Principle：研究设计、分析、解释和文档优先 LOCAL，硬件执行与
raw evidence 优先 Worker；节省 token 不能覆盖 Paper-First、研究质量、安全、标签隔离、历史不可变或可复现性。

## 为什么先做对齐

若先做自建数据或 Detector，最容易出现三种偏差：用不同设置与论文数字比较、只在为方法量身设计的数据上有效、
把工程 smoke 当作研究结论。Paper-first 原则把“比较资格”前置，使后续失败也能成为可审计 blocker。

## 企业相关性

企业知识库的核心风险不是只有明显恶意文本，而是“看起来合理的局部事实变更”：政策金额、适用条件、例外、
生效时间、责任主体和来源链。Paper 1 的版本/时间/来源/事实联合建模，目标是减少对合法更新的误杀，同时发现
高相关、自然语言化的隐蔽篡改。

## 与前一阶段的关系

S6-T5 回答“如何透明、可追溯地检索并构建 Retrieved Context”；S6.1 才开始回答“检索到的事实是否可能被恶意
污染”。前者是受控工程 baseline，后者是论文威胁、检测和统计实验，不能把前者的通过率当成后者的安全效果。

## 面试问题

### 为什么不能直接比较论文表格和我们的数字？

因为数据版本、attack budget、Retriever、Top-K、模型、prompt、指标分母和随机种子任一不同都会改变结果。
只有通过 strict-comparison eligibility gate 才能做严格横向比较。

### GMTP 为什么重要，又为什么不够？

GMTP 用 Retriever similarity gradient 找高影响 token，再用 MLM masked-token probability 判断异常，对优化型
cheating tokens 很有针对性。但自然的事实篡改可能没有明显低概率 token，也不直接覆盖合法版本演化、来源伪装
和版本链异常，因此适合作为强基线而非 Paper 1 的完整答案。

### 为什么 SafeRAG 只优先 Silver Noise 和 Inter-context Conflict？

两者最接近 Paper 1 的“相关但有噪声/事实冲突”核心。Soft Ad 和 White DoS 更偏内容传播与拒答攻击，当前先延后，
避免第一篇论文范围膨胀。

### 为什么 hash 全通过仍可能退回证据？

Hash 只能证明“收到的字节没有变化”，不能证明字节中的研究断言正确。R0-I 用 official exact-commit tree 发现 GMTP
实际包含 200-sample artifacts，而 Worker audit 写成缺失，因此必须纠正再接受。这是 evidence integrity 与 scientific
validity 的区别。

### 为什么 5090 不一定比论文的 A6000/H800 更容易复现？

显存容量、架构和软件兼容性不同。5090 是 Blackwell 32 GB；旧 CUDA/PyTorch wheel 可能没有兼容 cubin/PTX，
而 A6000 有 48 GB、H800 有更大显存。算力新不等于原环境二进制可运行或大模型显存一定足够。

## 初学者常见误区

- “GitHub 有代码”不等于“有可再分发许可证”。
- “未确认再分发许可证”不自动等于“不能进行未来获批的内部研究复现”；必须分别判断 SOURCE_ACCESS、
  INTERNAL_REPRODUCTION、STRICT_COMPARISON_ELIGIBILITY 与 REDISTRIBUTION_ELIGIBILITY。
- “当前 main HEAD”不等于“论文出结果时的 commit”。
- “跑通一个样本”不等于“复现论文结果”。
- “同名指标”不等于“公式、分母和聚合方式相同”。
- “换成新模型效果更好”不等于“严格复现”。
- “版本感知”不等于比较一个 version number。
- “检测准确率高”不能替代 Hard Negative FPR、Utility 和 Efficiency。

## W2 执行批准的教学边界（2026-08-01）

W2 获得 `APPROVED_TO_START` 只表示 RTX5090 可以按冻结合同验证 GMTP detection-core 的最小可执行性；它不表示
任务已运行、通过或被验收。企业工程中，这种“批准、执行、证据复核、结论接受”四层分离可以防止把环境兼容性
smoke 误报为防御效果。

W2 的固定 GMTP-packaged HotFlip/Contriever/NQ 样本与 L1 的 PoisonedRAG LM-targeted artifact 不是同一工件，因此
即使 smoke 通过，也只能回答“该 detector core 在当前兼容环境能否对两个固定文档产出工程中间量”，不能回答
F1、AUPRC、ASR、论文复现或跨 baseline 正式比较。

面试可追问：为什么 source patch 必须停止？因为兼容性补丁可能改变 tokenizer、gradient 或 threshold 行为；未经
Control Plane 审查就继续运行，会让“原算法 smoke”与“改写算法实验”失去可区分性。常见误区是把
`APPROVED_TO_START`、`PASS` 和 `HUMAN_ACCEPTED` 当成同一个状态；本项目要求三者严格分离。

## Attempt 1 Evidence Blocker：脚本不是执行证据（2026-08-01）

W2 Attempt 1 的 archive 能证明 GMTP/source/input/environment identity 和模型下载阻断，也能证明 smoke 未执行；但
打包脚本中“稍后会打印 main repo HEAD/status”的命令不能证明这些输出实际进入 archive。企业审计里，代码表示
intended procedure，captured output 才表示 observed fact。两者混用会让 clean-tree、revision 或资源事实无法追责。

因此即便外层 SHA、内部 index 全通过，缺少 mandatory fact 仍要 `W2_ATTEMPT1_EVIDENCE_BLOCKER`。初学者常见误区是
“hash 全绿就表示 summary 全真”；实际上 hash 只保护已提交字节，不能补出未提交的证据。H1 已获批准也不意味着可
越过前置 evidence gate：先补齐主仓库 HEAD/clean 与环境字节计量，再开始离线模型工件准备。

## Correction 01：工具名称不等于命令派生证据（2026-08-01）

Correction 01 证明了一个更细的审计边界：`MEASUREMENT_TOOL=du` 只能说明声称使用了哪个工具，不能说明运行了
`du --apparent-size --bytes`、allocated-size 对应命令或其他具有相同语义的明确参数组合。没有命令行与原始输出，
审查者无法排除两个数值被交换、单位被换算或 flags 语义不同。

企业场景中，资源合规不仅要保存最终数字，还要保存“命令、参数、原始输出、规范化字段、manifest”这条派生链。
面试可追问：为什么两个数字都小于 ceiling 仍不能 PASS？因为算术正确只验证阈值比较，不验证数字的测量语义和
来源。初学者常见误区是把内部一致性当成外部可验证性；前者说明文件彼此不矛盾，后者才支持治理门禁关闭。

## PO-MHEP：主权不是改写事实，而是决定能否继续（2026-08-01）

PO-MHEP 把两个容易混淆的权力拆开：L0 Git/raw evidence 回答“实际上发生了什么”，L0.5 项目负责人主权回答
“知道这些事实后，是否允许继续”。项目负责人不能用治理声明把不存在的 run 变成存在，但可以在证据不足、论文
风险、架构取舍或资源风险出现时要求整个执行链停止。

企业价值在于把 Agent 和 GPU Worker 从“自主解决问题”改成“在冻结合同内执行并返回证据”。5090 的算力越强，
越不能让它自行选模型、改参数或批准结果；否则性能优势会放大不可复现和越界风险。面试可追问：为什么“不确定”
也要升级？因为当选择影响多个 Stage 或论文结论时，低置信默认决定的未来返工成本远高于当下人工决策成本。

`FORWARD_RISK_REVIEW` 是事前检查后续推翻、label leakage、技术债和论文 reviewer attack surface；
`CONTEXT_PERSISTENCE_CHECK` 是事后保证聊天丢失仍能从 Git + private evidence + hash/index 恢复。初学者常见误区是
把治理等同于“多写文档”；真正目标是让授权、执行、证据、结论和下一门禁形成可物理恢复的闭环。

## Correction 02：实质性关闭规则避免证据包装无限循环（2026-08-01）

Correction 02 已获批准，但仍然只修复 GNU `du` 的测量来源链。`du -sb` 统计 apparent bytes，即文件逻辑长度；
`du -sB1` 按文件系统已分配块折算 bytes。两者都可以低于资源上限，却回答不同问题，因此合同必须同时保存准确
命令、flags、raw stdout/stderr、exit code、工具版本、时间和环境身份，而不能只保存两个摘要数字。

`MATERIALITY_AND_FINAL_CLOSURE_RULE` 的企业价值是把“科学上实质的缺口”和“包装格式偏好”分开。SHA/index、命令
执行、原始输出、GNU 工具身份、环境身份、资源、mutation 和可追溯性属于实质问题；字段顺序、Markdown、空白或
可从原始证据推导的重复字段不是。通过后必须关闭当前包装 blocker，避免治理流程因审美差异无限循环。

面试可追问：为什么 Worker 的成功状态仍叫 `READY_FOR_CONTROL_PLANE_REVIEW`？因为 Worker 只能声明证据已准备，
不能自我接受。LOCAL 仍需核验 archive/sidecar、index、raw/manifest 一致性和无 mutation，之后才能重分类 Attempt 1。
初学者常见误区是把 Owner 批准、Worker 执行成功、Control Plane 验收和 W2 完成混为一谈；Correction 02 只跨过第一
个门，后续三个状态仍各自独立。

## H1：模型工件准备不等于模型验证（2026-08-01）

Correction 02 的 17/17 索引、GNU `du` 原始命令和 11/11 materiality 检查通过后，证据包装门必须关闭；否则治理会
把审计质量变成无限追求格式一致。关闭这个门只说明 Attempt 1 可以被准确分类为“有效但被模型下载阻断的工程 run”，
不说明 detector 成功，也不说明 GMTP 与现代环境兼容。

H1 随后只做离线工件供应：固定 repo + commit、`token=False`、单线程下载、文件级 SHA、2 GiB 资源门和安全 tar。
企业场景里，这相当于把网络获取与生产/算力执行拆成两个可审计控制点：Control Plane 准备确定字节，Worker 再验证
相同字节，之后才可能获准加载。面试可追问：为什么有 `pytorch_model.bin` 仍不能写“models loaded”？因为文件存在
证明的是供应链身份与完整性，运行时反序列化、设备放置、依赖兼容和推理行为均尚未发生。

本轮 H1 的 17 个模型文件合计 `1320352375` bytes，bundle SHA 为
`aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`。初学者另一个常见误区是把 bundle 的本机
自校验当成 Worker 验收；正确状态仍是 `OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`。

## H2：条件式批准不是自动继续权（2026-08-01）

H2 把一个工程门拆成先后两个不可颠倒的部分：H2-A 先证明 5090 收到的是本机冻结的同一 bundle、同一模型 revision
和同一文件集合；只有 18 项安全与完整性条件全部通过，H2-B 才能加载本地模型并调用一次固定双文档 detection core。
这不是把 Worker 变成审批者，而是项目需求提出人预先批准了一个明确的条件分支；条件失败时，授权自动失效并停止。

企业价值在于同时减少无价值审批往返和防止执行漂移。审批合同已经精确限制源码、输入、模型、参数、环境、离线变量、
调用次数、资源与证据，因此 H2-A 通过后的 H2-B 不产生新的自由裁量权。面试可追问：为什么仍不能写“GMTP reproduced”？
因为一次双文档工程调用只回答兼容性与可执行性，不能估计 Accuracy、Recall、ASR、泛化或统计不确定性。

初学者常见误区是把 `Auto Continue = CONDITIONAL_WITHIN_H2_ONLY` 理解为自动进入下一阶段。它只允许 H2-A PASS 后
进入同一 H2 的一次 H2-B；完成或任一 blocker 都必须返回本机，父 W2 仍需独立复核，P1 与正式实验没有获批。

## H2 resume_02：不可变证据需要追加命名空间（2026-08-01）

Resume_01 在 bundle 缺失时正确停止，并生成了可验证的 blocker evidence。Bundle 后续到位后，覆盖 resume_01 虽然
看似省事，却会让审计者无法区分“第一次确实缺包”和“第二次包已到位”两个时间点。正确做法是保留原目录与 archive，
由项目需求提出人明确批准全新 resume_02；这叫 additive evidence namespace rollover，不是删除失败记录后重跑。

企业价值是让失败证据、补救决定和后续执行同时可追溯。面试可追问：为什么 H2-B 仍可执行一次？因为 resume_01 在
H2-A 就停止，`call_count=0`，原单次调用授权尚未消费。初学者常见误区是把新目录理解为新实验；本次只改变证据路径，
源码、输入、模型、参数、资源和 claims boundary 全部不变。

## H2 resume_02 复核：单样本对可证明可执行，不能证明有效（2026-08-01）

Resume_02 把供应链、环境和执行三类证据闭合到同一条链：bundle sidecar/实际 SHA、archive safety、19 项模型 index、
两个固定 revision、环境 pre/post SHA、四个 offline 变量、未修改 source/input、RTX5090 CUDA placement、唯一一次函数调用，
再到脱敏结果和资源测量。Control Plane 还要独立复算 returned archive 的 `25/25` index；Worker 自报 PASS 不能替代复核。

企业价值在于把“能否在冻结环境中运行”与“检测是否有效”分开。一个 benign retained、一个 poisoned filtered，只证明
这两个固定输入在这次调用中的工程行为；它没有样本量、负载分布、阈值校准、误报/漏报统计、置信区间或跨攻击验证。
面试可追问：为什么数值看起来区分明显仍不能写 Accuracy 或 effectiveness？因为两个挑定文档不是抽样评估，不能支持
总体性能推断。

初学者常见误区是把 `CONTROL_PLANE_REVIEW_PASS` 等同于父 W2 或论文结论验收。正确状态机是：Worker 完成待复核 ->
Control Plane 接受工程证据 -> 项目负责人单独决定父 W2；即使 W2 后续获验收，P1 与正式实验仍需要新的明确批准。

## W2 人工验收：关闭工程门不等于获得论文结果（2026-08-02）

项目需求提出人已完成最后一个独立动作：把父 W2 验收为
`HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`。这证明治理状态机中的“证据接受”和“父任务验收”确实是
两个门。W2 的退出条件已满足，FU1 可以关闭；但其证据仍只有一个冻结 benign/poisoned 样本对，因此不能估计误报、
漏报、置信区间、泛化或 GMTP 论文复现程度。

企业场景中，这种边界允许团队确认遗留组件可在目标硬件和离线供应链下运行，同时避免采购、合规或论文团队误把
smoke 当作安全承诺。面试可追问：为什么 benign retained、poisoned filtered 仍不能写“检测有效”？因为这是单次冻结
样本的工程观察，不是从目标分布抽样得到的性能估计。

下一步只是 P1 正式协议候选审查。候选把 Dataset、五视角方法、指标、统计和证据合同写清，并把“解毒”拆成互斥的
A/B/C 范围供人工决定；在批准前仍不得构建数据、实现 Detector、训练或运行正式实验。

## P1-R1：Option B 把“解毒”变成可检验的轻量干预（2026-08-02）

项目需求提出人选择 Option B 后，Paper 1 的“解毒”不再是模糊口号，而是两个可复现操作：hard filtering 在风险达到
冻结阈值时移除候选；soft downweighting 从标准化检索分数中减去风险惩罚。两者都依赖同一个可校准 Detector，但必须
分别报告安全结果和检索效用，不能用单一综合分数掩盖“安全提高、正常检索受损”的代价。

企业价值在于建立最小可部署决策边界：安全团队可以审计某文档为何被移除或降权，搜索团队也能量化 Recall、MRR、
nDCG 和 hard-negative 误伤。它仍不是完整可信检索链，因为没有 trusted context package、上下文构造、Agent 策略或
生产运行平台；这些能力一旦混入 Paper 1，会同时扩大变量、资源、reviewer attack surface 和因果归因难度。

面试可追问：为什么安全与效用必须是共同主结果？因为只优化 AUPRC 或攻击成功率可能把所有疑似文档都删除，从而得到
看似安全但不可用的系统。初学者常见误区是把“协议候选给出了阈值、样本量和种子”理解为这些值已经冻结；实际上
P1-R1 仍是 `REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`，Pilot 才能验证样本量、方差和资源估计，且 Pilot 也需要
单独批准。

## Pilot2 Schema V2：低一致率可能先是适用性问题（2026-08-27）

条件型标注字段如果没有“命题是否存在”的入口，标注人会把“没有提到”分别解释成 YES、UNCERTAIN 或空值；此时很低的
kappa 可能主要测量字段问题，而不是事实判断能力。V2 先问 version/history/authority `*_present`，再只在 present=YES
时判断 correctness；present=NO 自动得到 NOT_APPLICABLE。这样可把 applicability disagreement 与 correctness
disagreement 分开，未来只在双方都认为适用的子集计算 correctness agreement。

同样重要的是证据不可变：修复 schema 不能回写 GB18030 raw return、补造 B 的历史 time/lookup 值或伪装原声明已签。
正确做法是提供本人 V1 只读参考、新 V2 表、逐字段 KEEP/REVISE 记录和 retrospective declaration。测量工具被修复只
能宣称“复核准备就绪”，不能宣称 agreement 已恢复或论文结果成立。

## Pilot2 Targeted Re-review：应修测量缺陷，不应让人重复稳定答案（2026-08-27）

完整 schema 是覆盖边界，不等于每次人工修复都要重做全部字段。先用 V1 disagreement、缺失值、applicability 变化和
下游依赖做 field audit，可把真正受 schema 修复影响的字段变成定向任务，同时把定义稳定、非上游的答案作为本人 V1
只读参考。本轮由此把每位标注人的实质任务从 576 降至 360，减少 37.5%，但仍保留三组 present/correctness 与
overall fact 的依赖链。

这种收敛只有在证据和隔离边界不被削弱时才成立：raw 与完整 V2 不回写，A/B 不见 peer result，原值只读，新值使用
冻结枚举和联动提示，缺失历史数据明确标为不可恢复。企业标注流程中，这比“把整张表再填一次”更容易解释、审计和
估算，也减少疲劳导致的新噪声；但它只证明复核工具准备就绪，不证明 agreement、Ground Truth 或模型效果。
