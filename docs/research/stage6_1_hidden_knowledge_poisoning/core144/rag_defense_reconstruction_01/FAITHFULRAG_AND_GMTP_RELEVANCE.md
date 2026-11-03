# FaithfulRAG 与 GMTP 的可借鉴部分

2026-11-04 JST；SOURCE_REVIEW_ONLY。固定身份及原文链接见[三方法审查](PUBLISHED_METHOD_REVIEW.md)。未调用它们的模型、未训练、未复制其代码。

FaithfulRAG 把参数知识外化为 Self-Facts，再用 embedding 对齐检索片段，以 Self-Think 处理局部冲突。固定代码 `faithfulrag/modules.py` 中对应 FactMiningModule、ContextualAlignmentModule、SelfThinkModule；pipeline.py 串起三阶段。对齐使用相似度检索相关片段，不是已验证的逻辑矛盾分类器。适合借鉴的是“细粒度事实与证据分离、局部对齐、冲突后再生成”的组织方式，不能直接复用成投毒标签。

可信上下文与参数知识冲突时偏向上下文可能合理；若上下文本身被投毒，这种偏向也可能强化错误采信。这里是威胁模型推断，未跑 FaithfulRAG 攻击实验。参数知识不得作为官方证据或 GT。中文迁移需要中文分句、数字/单位/适用范围/时间的规范化值、独立逐字 span 锚、明确缺失/未知状态；现有英文 NLTK 分句、空格词长分块与编号事实正则不能未经验证照搬。旧 E3/E4 失败保留，不能放宽旧 parser 后重算。

GMTP 固定 `src/defenses/method.py` 的 GMTP 支持 DPR/Contriever，以 query-document 相似度反向传播取得 token 梯度范数，筛高于均值的 token 后取至多 N 个，用 MLM 逐个 mask，取最低 M 个重建概率均值，再与 remove_threshold×remove_lambda 比较。默认 N=10/M=5 不等于中文已校准参数；阈值需可靠准备，不能用默认负值冒充有效检测。get_avg_mask_probs.py 与索引/语料准备属于原流程。源码核心可接受已给定 documents，不意味着本轮必须重建完整索引；但编码器、MLM、梯度、tokenizer 对齐与阈值的必要成本仍存在。

| 自然事实攻击 | 可能可利用的 GMTP 信号 | 本轮判断 |
| --- | --- | --- |
| 局部数值替换 | 若数值同时成为异常高影响/低概率 token，可能响应 | 自然、常见数字未必异常；UNKNOWN |
| 适用条件篡改 | 梯度或 MLM 可能关注条件词 | 句法通顺不保证事实正确；UNKNOWN |
| 历史版本错配 | 查询可能影响相关 token 梯度 | 概率不自带生效时间真值；UNKNOWN |
| 权威机关角色混淆 | 特定机构词可能引起异常信号 | 合法机构名称互换仍可能很自然；UNKNOWN |

建议保留 GMTP 为外部威胁对照候选，暂不强搭 DPR/Contriever/CUDA；保留 FaithfulRAG 的事实对齐思想，不把忠实性当安全防御。两仓库固定树未发现根 LICENSE，本轮不复制代码。后续内部运行、适配及再分发须分别核对许可和资源授权。
