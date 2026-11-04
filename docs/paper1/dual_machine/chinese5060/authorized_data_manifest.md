# 授权数据与代码清单初稿

状态：P0_AUDIT；原始来源起点 `8dec9453de2ebd5ea03e4cbdf753b2f0d7347177`。
本次授权见[Owner收据](owner_instruction_receipt.md)，治理审计见[上下文报告](governance_audit.md)。

| 资产 | 已有身份与允许用途 | 本次核验边界 |
|---|---|---|
| 签署D1开发包 | private_input_v2；D1_DEV_EXPOSED；40组120条、13家族；C/P/H各40，S1/S2/S3为12/15/13 | 专用Evaluator只读核hash/计数；不建立正式GT |
| HOLD | 包声明8组24条，排除 | 不打开HOLD内容，不自动补入分母 |
| 旧F5 | runtime/f5.jsonl；120×Top5；7,384,615字节 | 仅核验与审计。不是查询级RAG输入合同或独立官方真值 |
| 旧评价标签 | evaluation/labels.jsonl | 仅独立审计进程计数和复核既有抽样，不进检索/防御/生成 |
| Pilot12 | 已冻结12组36候选9家族；各S四组；seed20261104 | 复核旧选择，禁止按结果重抽 |
| 查询V2草案 | 既有12题SUPPORTED_PROVISIONAL；PODR-160闭合职责题范围 | AI开发草案、人工Gold0；本次不读取评价答案提案或Reviewer原审阅 |
| 独立官方证据 | 需逐世界确认足证性、来源角色、有效时间和共同权限 | 不能把Candidate/标签/旧Oracle替代；未授予新来源权限 |
| D2/D3/Reviewer/独立测试答案 | 禁止访问 | 无内容读取、索引、API或方法反馈；最初文件名发现不代表内容访问 |

固定SHA256：

- bundle manifest：`a7e05d2ebedbc68abc21fff46a0ad1597747712020957ac30cf1445353714a60`
- F5：`c849260e2a41fa9186e6d69ed6442cbebdaa7ff272beece9dfadc22e61cf535c`
- evaluator labels：`d904e349211ec7af648b68afadb31e46a30196ba20a53b5a40a382ec0df7afaf`
- 旧选择：`2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`

签署资格来源为既有D1首轮协议/PODR-146和后续开发合同；本次不重开人类签署表、不改标签。
`audit_chinese5060_inputs.py`先验证上述固定字节hash，再打开白名单文件；输出只有聚合/hash，不公开组ID/正文/标签行。
不打开Oracle、历史预测或旧E1错误做选择。签署原件、源签署摘要与HOLD本体未重新验签，需明确保留此限制。

代码真实存在：ChromaVectorStore（显式向量、持久化cosine、collection指纹）、SentenceTransformerEmbeddingProvider
（lazy加载、revision与local_files_only）、DenseRetriever（TopK与排序/来源trace）。依赖声明Chroma1.5.9、ST5.6.0。
旧全量Top5与候选驱动query不能直接用作独立查询的真实召回成绩。现有实现可复用，不代表当前真实查询索引已就绪。

当前上游缓存固定 `ba2a17efba165d45409114df2d70b030ade1e1b8`，本地clean；MIT。
`ragdefender/`库与`artifacts/`原实验代码分离。已有非论文多语种MiniLM工程结果不升级论文复现。
真实中文Retriever/Chunk/TopK/生成评分合同仍待闭合；smoke单独使用公开虚构语料与字符bigram，绝不标B2。
