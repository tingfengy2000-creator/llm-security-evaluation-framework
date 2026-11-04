# 场景协议初稿

分类：D1_DESIGN_DRAFT / FICTIONAL_SMOKE_FROZEN。本文件未冻结真实Pilot或正式40组实验。

smoke固定：纯虚构甲市语料；同query、三个变体，各世界1条候选+5条共同背景；句/文档一一对应；
每个世界独立字符bigram TF-IDF和独立Chroma持久化目录，cosine、TopK3；无排序攻击。
索引后查询并关闭/重开核对排名；冻结ordered TopK后B0只透传；生成与评价NOT_RUN，不能产生ASR/Accuracy。
独立世界的差异只用于检查隔离，无科学效能解释。真实研究拟TopK5仍是待批准参数，不借smoke取代。

真实管线目标：query→独立语料世界→真实retrieval→冻结TopK→各方法同快照过滤→同Qwen生成→独立评价。
冻结TopK比较和后续在线retrieval分层，不能把旧Candidate驱动Top5写成真实query召回。
每组C/P/H分别创建语料manifest，索引前核验所有chunk lineage，不仅检查TopK；背景也须注册。
单个世界每个fact-group只能授权一个candidate identity；另两兄弟不进入索引；query必须同样可裁决。
拒绝未知lineage、混世界、重复成员；记录corpus_version、全语料hash、retriever/chunk/model配置hash、TopK顺序与hash。

威胁模型：只可插入/编辑低信任自然事实。Query/system prompt/独立官方仓库不能改，首次比较不操纵排名。
保留Clean、自然Poison、合法历史/条件HN、缺可信证据的拒答控制。缺证控制不自行制造“事实错误”的GT。
原子事实/target/合法历史答案/允许拒答范围均在运行前由独立评价合同确定；不按输出解释攻击意图。

公共模型视图只含query_text和有序chunks：chunk_id、text、source_id、source_role、publication_time、effective_time、version、trust_boundary。
不透明ID不能编码组/角色/S/家族；query_id/candidate_id留运行索引，不传生成器。
可信身份来自独立固定registry的source_id+text hash，Candidate自称官方无效；文本hash不等于来源可靠性验证。
未知time保持null并附控制面原因，不猜日期。全文/metadata均走标签字段泄漏检查；机械检查不替代语义审查。

快照绑定query、ordered chunks和元数据、corpus hash、retriever身份、TopK与trusted registry hash；
重放检查完整canonical JSON hash。过滤仅保留原下标子序列，不能改写/补检索/重排。
全部删光则ABSTAIN_NO_CONTEXT且不调用生成器。首次retrieval空集由上层单独记录，当前旧packet合同拒收空集，
不可悄悄填入伪chunk；真实pipeline应在协议冻结前补此明确状态。

Evaluator独存fact-group/variant/attack-target/允许答案/支持证据ref+hash/评分规则；runtime不得导入control-plane或evaluation_preparation。
本阶段只有schema与hook，没有实装API生成器或语义裁判，不以fixture回答伪装Qwen输出。
每run需run_id/code SHA/input与证据hash/model+revision/prompt hash/sampling/randomness/context token budget/实际响应hash/usage/费用/延迟/评价。

待闭合：查询V2逐世界可答性、固定独立官方证据包、真实chunk规则与TopK、生成和核验的独立prompt/输出schema/token预算、
一致裁判协议、所有方法同权限/预算和迁移语义。未闭合前不得付费Pilot，不能用未知参数填作冻结值。
