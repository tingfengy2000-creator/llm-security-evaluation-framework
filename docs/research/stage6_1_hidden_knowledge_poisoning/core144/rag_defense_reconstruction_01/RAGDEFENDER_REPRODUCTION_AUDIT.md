# RAGDefender：两阶段核心运行成功，完整复现与迁移门未通过

2026-11-04 JST。复用暂停前证据，不重跑示例、作者测试或核心 API。

| 层次 | 状态 | 证据与限制 |
| --- | --- | --- |
| 作者默认示例 | BLOCKED_MISSING_ALL_MINILM_CACHE_OFFLINE | examples/basic_usage.py，exit 1；指定默认模型未缓存，未下载或改上游 |
| 作者测试 | NOT_PASS | 55 项：20 pass、13 fail、21 setup error、1 skip；原 stdout/stderr 保留，多数为模型缓存缺失，CLI help 另有 stdout None 问题 |
| 核心两阶段 API | CORE_ALGORITHM_VERIFIED_WITH_CACHED_NONPAPER_EMBEDDING | 固定 v0.2 源码未改，显式注入缓存多语种 MiniLM；核心脚本 exit 0 |
| 原论文端到端复现 | NOT_EXECUTED | 未跑 ACSAC claims、原 benchmark、攻击、检索器/生成器或论文数值 |
| 中文任务迁移 | MIGRATION_NOT_READY | 独立查询答案缺失；embedding/长度/分词/检索规模及多跳语义门未闭合 |

固定 SHA `ba2a17efba165d45409114df2d70b030ade1e1b8`，MIT。依赖声明包括 torch、transformers、numpy、pandas、scikit-learn、sentence-transformers、tqdm。实际 CPU 环境 torch 2.12.1、transformers 5.12.1、sentence-transformers 5.6.0、numpy 2.5.0、scikit-learn 1.9.0、pandas 2.2.3。隔离 env 只读复用旧依赖；新 env 内约 12 MB pandas/pytz/tzdata 安装不改变旧环境。未使用 GPU、未下载模型。

Embedding 为 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`，revision `16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`，最大编码 128 token；文件哈希见[机器结果](EXPERIMENT_RESULTS.json)。正文未在包装器截断，不代表 encoder 没有内部截断。后续必须量化受影响段落比例，不能把长证据后部被忽略当防御结论。

必须区分三个版本层：

1. 论文使用 Stella；v0.2 公共 API 默认 `all-MiniLM-L6-v2`；本轮显式使用缓存多语种 MiniLM。不同 embedding 不能混称原配置或直接比较数值。
2. v0.1.1 公共 defend 在估计数量后按列表尾部截断；v0.2 改为实际 Stage 2 相似对频次排名。不能混用旧输出与 v0.2 输出。作者迁移文档中的 fixture F1 不是本轮实测。
3. 多跳代码沿用 OR、混合 median/mean 阈值及结果翻转，作者文档明确与论文 Eq.3 的 AND/阈值不同。源码还对完整相似度矩阵求统计量；本轮未修补为论文语义。后续若改动须另标改写实现。

真实离线工程结果：single-hop fixture 6 输入删下标 [2]、保留 5；multi-hop fixture 5 输入删 [0,1,3,4]、保留 1。它们只验证执行、下标映射和输出保留关系；未证明原 fixture ground truth 等价，更非 D1 效果。

虚构中文时间探针把查询从 2022 改为 2024，均删 [0,1,2]。固定 defender.py 明确 query 未参与现有检测；这支持“当前代码不是 query-conditioned”的源码事实，不证明真实版本误删、E1 失效或 B4 缺口。single-hop singleton 实际触发 AgglomerativeClustering 至少两个样本的 ValueError。空输入和单输入不能偷换算法补丁为“原版可用”。

中文适配还涉及：默认英文停用词与基于词边界的 TF-IDF，中文无空格文本的词频含义；单跳强制两簇是否会误删纯净集合；重复来源集中程度是否等于攻击；少量/缺证场景是否满足原假设。以上均为风险，尚非实测论文结论。

原命令、flags、stdout/stderr、exit code 位于 Git 外 `experiments/rag_defense_reconstruction_01/logs/author_example.json`、`author_tests.json`、`core_api_audit_after_isolated_pandas.json`；结果为 `CORE_API_AUDIT.json`。[索引](PRIVATE_EVIDENCE_INDEX.json)绑定字节身份。[最小审计脚本](../../../../../scripts/research/run_ragdefender_offline_core_audit.py)仅供复核，当前不执行。
