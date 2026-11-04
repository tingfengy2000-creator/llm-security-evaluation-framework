# 基线与公平性初稿

本轮编号按Owner新指令，旧重构协议的B1=Qwen直验在本轮应称B3；仅登记映射，不改写旧文件或结果。
旧E1/E2核验TP37/40不是最终Answer Accuracy，更不是query→retrieval→generation成功率。

| 本轮方法 | T0：无独立证据 | T1：相同固定官方证据 | T2：按需官方检索 | 当前状态 |
|---|---|---|---|---|
| B0无防御 | 原TopK | 共同生成证据政策须另冻结 | 后续分层 | 仅虚构上下文smoke |
| B1原版RAGDefender | 固定原版语义 | 同证据可得层需标包装权限，不能称原法使用了证据 | 后续分层 | 未获5090语义交接，NOT_RUN |
| B2中文适配 | 仅明确中文embedding/分词迁移 | 同B1，记录全部迁移差异 | 后续分层 | NOT_RUN，不是新贡献 |
| B3直接Qwen核验 | 仅原TopK | 同官方证据/metadata/token预算 | 后续分层 | NOT_RUN |
| B4简单RAGDefender+Qwen | 固定简单串联 | 与B5同等级证据/metadata/总预算 | 后续分层 | NOT_RUN |
| B5单核心候选 | 由真实失败后提出 | 必须强B3/B4同权限对照 | 后续审批 | NOT_PROPOSED |
| B6去核心消融 | 同B5其他参数 | 同B5全部权限 | 后续审批 | NOT_PROPOSED |

不能把T1/T2相对T0的改善称为纯算法优势。所有方法相同query/语料/TopK/顺序/生成器/参数/评分；
给B5的元数据和证据也给B3/B4；比较token预算须包含验证+生成+评判，成本去重与逻辑条件成本分开。
固定可信补充不替换投毒正文作首周默认。中文embedding单独收益归B2。

上游静态审计锚点：[官方仓库](https://github.com/SecAI-Lab/RAGDefender)，固定
`ba2a17efba165d45409114df2d70b030ade1e1b8`。
官网明确`ragdefender/`为库，`artifacts/`产出论文表图。v0.1.1尾部截断与v0.2实际Stage2下标不能混算。
本地read-only核对：query在defend里未参与检测；单跳强制两簇；英文stop_words+默认词边界TF-IDF不是中文分词；
多跳实现OR/混合阈值/翻转与其文档所列论文AND不同。均不在本工作线悄悄修正为“原版复现”。
既有缓存多语种MiniLM最大128 tokens，论文Stella/库默认all-MiniLM/本地多语种三者不同；
编码截断风险、singleton错误、少量/纯净集合删除风险需实测，不能仅据源码判定D1失效。
新smoke可量化虚构中文analyzer token数，只是迁移风险工程探针。

FORWARD_RISK_REVIEW/PAPER_RISK_REVIEW：D1暴露、小样本家族相关、AI答案非Gold、query作者见过候选、
旧Top5候选条件化、额外证据权限、中文分词/截断、上游版本语义均可能混杂。
当前措施是分层、独立场景/评分、保留未知与固定选择；不是宣称风险已消失。
在真实Pilot和迁移语义闭合前不提出新方法优越性或跑40组。
