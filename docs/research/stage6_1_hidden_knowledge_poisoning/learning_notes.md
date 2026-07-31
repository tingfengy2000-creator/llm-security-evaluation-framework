# S6.1-LR1 学习与面试笔记

## 这一步做了什么

把 Paper 1 从“有研究方向”推进到“有外部证据锚点的研究控制面”：明确 PoisonedRAG 是攻击基线、GMTP 是检测/
防御基线、SafeRAG 是中文安全 Benchmark 参考，并把论文、源码、commit、许可、数据、模型、预算、指标、硬件和
复现门统一登记。

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

### 为什么 5090 不一定比论文的 A6000/H800 更容易复现？

显存容量、架构和软件兼容性不同。5090 是 Blackwell 32 GB；旧 CUDA/PyTorch wheel 可能没有兼容 cubin/PTX，
而 A6000 有 48 GB、H800 有更大显存。算力新不等于原环境二进制可运行或大模型显存一定足够。

## 初学者常见误区

- “GitHub 有代码”不等于“有可再分发许可证”。
- “当前 main HEAD”不等于“论文出结果时的 commit”。
- “跑通一个样本”不等于“复现论文结果”。
- “同名指标”不等于“公式、分母和聚合方式相同”。
- “换成新模型效果更好”不等于“严格复现”。
- “版本感知”不等于比较一个 version number。
- “检测准确率高”不能替代 Hard Negative FPR、Utility 和 Efficiency。
