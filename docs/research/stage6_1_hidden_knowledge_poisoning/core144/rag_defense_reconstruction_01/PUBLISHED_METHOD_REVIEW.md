# 三项已发表方法审查：信号与适用边界

2026-11-04 JST；PAPER1-RAG-DEFENSE-RECONSTRUCTION-01。静态审查及既有离线执行，非论文结果复现。来源为本任务保存的论文快照和固定代码，不表示再次检查在线最新版本。

| 方法 | 论文、固定代码与许可 | 输入、信号与输出 | 资源与本轮状态 |
| --- | --- | --- | --- |
| RAGDefender / ACSAC 2025 | [论文](https://kevinkoo001.github.io/assets/pdf/acsac25-ragdefender.pdf)；[固定源码](https://github.com/SecAI-Lab/RAGDefender/tree/ba2a17efba165d45409114df2d70b030ade1e1b8)；v0.2.0，根 LICENSE 为 MIT | 检索段落集合；聚类/词频或相似度集中程度估计污染数量，再按高相似段落对的加权频次定位；返回保留段落及删除下标 | 核心可 CPU 执行；已用缓存多语种 embedding 跑通，非原论文配置 |
| FaithfulRAG / ACL 2025 | [论文快照 v1](https://arxiv.org/html/2506.08938v1)；[固定源码](https://github.com/XMUDeepLIT/Faithful-RAG/tree/9181b1132f2f6548775e4f992a9a44fccdd018e9)；固定树未发现仓库根 LICENSE | 查询、检索上下文与模型自身事实；Self-Fact Mining → Contextual Knowledge Alignment → Self-Think；生成上下文忠实回答 | 多轮生成、分句与 embedding；仅静态审查，无训练/生成/复制代码 |
| GMTP / Findings ACL 2025 | [论文](https://aclanthology.org/2025.findings-acl.1263.pdf)；[固定源码](https://github.com/mountinyy/GMTP/tree/15b48d150f93711371eb8da22c211cd84a0cf4df)；固定树未发现仓库根 LICENSE | 查询、文档、可求梯度的检索器和 MLM；检索相似度梯度找高影响 token，masked token probability 识别异常；过滤文档 | 作者实现 DPR/Contriever、CUDA、MLM 与阈值准备；仅静态审查 |

RAGDefender 的原威胁是假定攻击者注入查询相关、诱导目标答案的段落，并在困难设置中优先召回攻击段落，同时至少保留一个正常段落。其几何/词频信号不是事实真值判断，也不直接解释合法版本或机关角色。单跳配置 m=5，Stage 2 p=2；不是通过 D1 调阈值获得的参数。论文单跳使用两簇与 TF-IDF 投票，多跳使用集中程度；Stage 2 从高相似段落对累计频次后删除估计数量。详细实现差异见[审计](RAGDEFENDER_REPRODUCTION_AUDIT.md)。

FaithfulRAG 主要比较模型参数知识与上下文事实的不一致；这种冲突不等价于上下文投毒。其事实抽取、局部对齐思想可作为候选组件，但上下文忠实性不能代替来源可信性。[迁移分析](FAITHFULRAG_AND_GMTP_RELEVANCE.md)给出具体限制。

GMTP 针对异常高相似度及不自然高影响 token 的动机，与自然数值/范围/版本变异存在威胁差异。自然错误也可能有低语言异常信号，这是适用性推断，未在本任务验证。不能据此预先宣判基线失败。

论文 Published Result、本地 Reproduced Result 与 Our Method Result 必须分开。本任务未填任何可横向比较的论文 ASR/准确率。代码许可未确认的方法只做静态分析；公开可读不自动等于允许复制/再分发。论文、模型、数据和依赖许可仍须分别核实。
