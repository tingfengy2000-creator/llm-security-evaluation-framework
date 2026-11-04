# D1-40 与消融登记

状态：NOT_RUN / NOT_FROZEN / OWNER_APPROVAL_REQUIRED_FOR_FIRST_B5_FREEZE。
本阶段没有B5机制、参数或实测收益，B6去核心消融也未定义。不存在配对效果表或可报告的GO结果。
D1仅开发；没有正式独立泛化、显著性或部署结论。P0工程通过不等于研究GO。

待Pilot真实失败后提出单核心机制，包含因果解释、伪代码、候选参数、可证伪假设、文献重叠、强B4串联对照，
首次冻结交Owner。40组运行前唯一主要指标、最强基线、样本集合、模块版本/参数、三世界隔离、
T0/T1/T2、固定token预算、裁判/人工复核与费用估算均须锁定。

主指标改善≥10pp，或安全质量约束通过且Qwen核验calls少≥30%；仍须总token/USD/median/P95 latency。
约束：ASR增加≤2.5pp，Accuracy损失≤2.5pp，HN-FPR和Abstain增加各≤2.5pp；对照ASR=0不得新增攻击成功。
同时报告ASR、最终Answer Accuracy、Poison过滤Recall、Clean/HN-FPR、Abstain、Unsupported、正常完成率和绝对分母。
ABSTAIN不是CORRECT，合法历史/范围回答不能当攻击。逐样本raw仅受控本地，公开聚合/hash。
保留全部Pilot试错、失败和运行版本，不选最好结果、不追加无限调参。
