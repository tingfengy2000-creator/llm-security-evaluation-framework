# Fast-Track A 启动与风险冻结

授权ID `W1-OD-20261104-FAST-A-03`；授权登记提交 `af68d89a870647be138cf5592ccd4a058e44a8ab`。
仅在5060研究分支从已核验授权文件快进，未合并其他分支、未改既有起点。
原始P1待批文本保留；此明确授权仅使T0真实检索/B0及有条件B1/B2、12张待审卡范围生效。

检索使用固定36份P1 role-free世界文件；其全部文件hash来自已封存P1索引，且重新核对原签署F5、manifest和选择hash。
选择只做字节身份核对，不解析其中角色/标签；Retriever不读取V2答案、World Bindings、开发标签或GT Vault。
Evaluator在全部36世界成功/失败输出封存并通过hash后才可打开批准的D1开发标签；未封存或篡改输出必须拒绝。
裁决卡独立进程只读V2问题/答案提案和来源，不读检索结果、角色、标签或预测，不自批Gold/target。

模型原位hash与既有10文件清单一致，namespace/model_id/revision匹配；112个依赖发行版已记录。
当前模型Tokenizer类BertTokenizer，is_fast=true、支持offset、每段两个special tokens；96/16窗口需重新编码检查，禁止为通过而改窗长。
所有chunk是原文字符切片，记录token/字符offset与原文hash；不改正文。Query超128编码token则该世界失败，不截断/改问法。
固定CPU2线程、normalize、TopK5、Chroma1.5.9、ST5.6.0；参数清单见[P2配置](P2_OFFLINE_EXECUTION_CONFIG_V1.json)。
Chroma实际HNSW默认cosine/ef_construction100/ef_search100/max_neighbors16/resize1.2/sync1000已空库探针验证。
公共配置不暴露seed，因此保存实际持久化索引二进制hash，证明关闭重开重放，不作跨机逐字节重建保证。
36个独立物理目录与collection指纹；共享embedding缓存只是同一固定模型的text-hash→vector纯函数，不学习语料统计或混合索引。

B1官方v0.2源码只读固定ba2a17efba165d45409114df2d70b030ade1e1b8、clean；默认为minilm-all→all-MiniLM-L6-v2。
已核白名单默认refs/main不存在，精确revision/缓存身份未闭合：B1 BLOCKED，B2连带BLOCKED。没有改用中文模型顶替B1。
这个门不影响已合格的B0/T0。B1/B2不运行时其指标为NOT_RUN，不填0。

FORWARD_RISK_REVIEW/PAPER_RISK_REVIEW：封闭19文档开发库、D1暴露和候选作者看过草案，不能推广业务规模或独立泛化；
检索缺失单列，不能当防御成功；未审定target/QA Gold，ASR与Answer Accuracy均NOT_MEASURED。
P0路径事件继续保留；本轮不做数据目录发现，仅读固定原件/世界白名单，模型目录枚举仅限已指定快照。
模型/依赖/参数/网络漂移停止受影响支路；一般单世界输入/检索失败保留36分母，不补样本、不调参数。
运行时禁Python网络连接/DNS、HF offline、telemetry关闭、local_files_only、trust_remote_code=false；不声称这是OS级网络沙箱。
资源冻结：新run磁盘上限2GiB、墙钟1800秒、CPU2线程；无GPU/无API/无下载/无安装。
允许后续封存、独立Evaluator开发计数、脱敏归档及本分支提交推送；完成后停止，不进入P3。
