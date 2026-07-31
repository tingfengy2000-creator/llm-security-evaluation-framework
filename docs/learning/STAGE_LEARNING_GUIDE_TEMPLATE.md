# Stage <ID> Learning Guide Template

> Authority: **NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL**
> Canonical governance/route: `<relative links>`
> Last evidence review: `<date or UNKNOWN>`

## 1. Stage 是什么

说明正式名称、范围和不包含什么。

## 2. 为什么存在

说明要解决的工程/研究问题和企业价值。

## 3. 与上一 Stage 的关系

说明复用哪些 accepted contracts/evidence，以及新增的研究变量。

## 4. 前置知识

列出安全、RAG、检索、机器学习、统计和工程前置知识。

## 5. 中英文术语

用表格定义术语、英文、中文和本文口径。

## 6. Threat Model

定义攻击者能力、目标、入口、限制、可信边界和非目标。

## 7. Architecture

说明组件关系，不把计划中的组件写成已实现。

## 8. Data Flow

说明数据从输入、检索、特征、决策到评估的流向，以及 Ground Truth 隔离。

## 9. Core Components

区分 Implemented、Planned、External Reference 和 Deferred。

## 10. 核心代码目录

只链接真实存在的 canonical 目录；不存在则写 `NOT IMPLEMENTED`。

## 11. 核心数据结构

说明 stable DTO、字段、身份、audit 和敏感边界。

## 12. 关键算法

区分论文已发表算法、计划复现算法和 Our Method 候选。

## 13. Experiment Design

区分 `DESIGN_FREEZE`、`ENGINEERING_VALIDATION` 和 `FORMAL_EXPERIMENT`。

## 14. Metrics

给出名称、公式/分母、方向、适用任务和状态。

## 15. 为什么选择这些指标

说明 safety、utility、efficiency、class imbalance 和 hard negative 风险。

## 16. External Papers

只链接权威论文/官方 artifact，并记录 Published/Reproduced/Our Method 区别。

## 17. Difference from External Work

说明研究 gap；没有结果时不得写“优于”。

## 18. Current Innovation

区分 proposed contribution、direct evidence needed 和 established result。

## 19. Completed Work

只列可由 Git/原始证据核验的内容。

## 20. Current Status

引用 Current Work State；动态 Git 值现场核验。

## 21. Blockers

引用 canonical Blocker ID，不创建竞争性 blocker 文件。

## 22. Blocker Resolution

区分 WORKAROUND、MITIGATED、RESOLVED 和 ACCEPTED_TECHNICAL_DEBT。

## 23. Claims Allowed

列出当前证据允许的有限声明。

## 24. Claims Prohibited

列出未建立的安全、统计、泛化和生产声明。

## 25. Reproduction Guide

引用已接受 protocol；没有批准时明确 `REFERENCE_ONLY_DO_NOT_RUN`。

## 26. Interview Explanation

给出 30 秒、2 分钟和深挖版本。

## 27. Likely Interview Questions

给出问题、回答要点、追问风险和常见误区。

## 28. Paper Method Mapping

将组件/信号映射到 Method 小节和待证明实验。

## 29. Paper Evaluation Mapping

将 RQ、baseline、dataset、metric、ablation、robustness 和 statistics 映射到 Evaluation。

## 30. Common Misunderstandings

列出“工程跑通=安全有效”“版本号=version-aware”“不同设置可直接比较”等错误理解。

## Authority Reminder

本模板及其派生 guide 均为 **NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL**。事实冲突时回到 Git、Owner Decision、
Current Work State、Experiment Master Record 和 accepted protocol/route。
