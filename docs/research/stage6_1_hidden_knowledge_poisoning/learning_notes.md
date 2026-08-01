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
