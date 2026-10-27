# D1探索性检测可评估性与固定对照协议 V1

2026-10-27；Owner直接授权任务 `P1-D1-EXPLORATORY-DETECTION-FEASIBILITY-SPRINT-01`。
源HEAD892915a830f9762d2cf239fcfb21cb8b26f186fb；PODR-143/OR-097/REL-2026-0112。
本轮为D1-only开发性诊断，D1_DEV_EXPOSED；不冻结Core正式GT，不执行2/1/1正式划分。

## 执行门与输入

先原字节保存Owner提供的XLSX/JSON/MD，再核原仲裁表SHA、57项/55非空建议、
54题/144题身份、全部人工判断及同题冻结证据。附件中的执行建议只是输入材料，
不替代本次Owner授权，不把AI辅助QA自动称为Owner已批准GT。
首次只读预览发生在锁定前，锁定时须复验来源稳定，不能虚报先锁后读。

五条固定HOLD：D1HC-0028/0051/0121/0078/0116。只因语义/证据质量隔离，不能按预测难度筛题。
至少保持完整三元组：任一成员质量HOLD则同组不进入匹配评价；同源缺陷影响其它组时
按字面证据依赖进一步扩大，不把共享family本身当质量错误。完整family始终用于CV隔离。
排除策略、可评估性及分母在评分前冻结；未恢复可靠独立证据路径的S不强行定级。
构造role仅在预测锁定后进入评价，不进入特征、检索或预测；不能以role反造人工判定。

## 固定模型与评分，先于结果

仅在合法的非阻断探索训练标签与输入均存在时执行。没有训练标签、无法隔离家族、
没有适用的D1特征矩阵/合法提取器则相应方法NOT_EVALUABLE；不填假检测率。
QA建议可保存供诊断，但不得静默成为已批准Human GT或自动覆盖原答。

- A：中文字符2/3-gram TF-IDF，lowercase=False、min_df=1、max_df=1.0、sublinear_tf=True、L2 norm；
  每折仅在训练家族fit向量化器；LR L2、C=1、liblinear、balanced、max_iter=2000、seed=20261027。
- B：仅合法非Oracle可信检索及已冻结轻量SEPT融合；R不进入Stage A。
  优先复用既有冻结Extractor/Registry/Feature Set，不把Final72矩阵假称D1矩阵。
- C：只允许人工匹配冻结E1/E2这一证据上界，标记ORACLE_ONLY；不能使用Human字段充当信号。
- 三方法用同一可评估总体、家族隔离OOF；无调参、特征选择或threshold tuning。
- threshold固定0.5，raw score为LR decision_function，概率未校准；不用正式test调参。
- OOF分数/预测锁定后才关联评价Poison role、HKP、S与HN切片。监督训练只允许训练折合法标签；
  不能从构造role生成训练target，也不能提前加载验证折评价标签。
- Recall/HN-FPR给TP/N和Wilson95%区间；有合法结果时AUROC/AUPRC给家族bootstrap95%区间，
  2000次、seed20261027。分母缺失/无合法预测为NA，不是0%或100%。

## 风险与停止条件

主要风险：AI建议被升级为GT，构造role泄漏，文本模板shortcut，训练/验证家族重叠，
把Final72旧结果冒充D1，或看到S3低Recall就未经消融归因长上下文。
只用既有本机冻结来源/模型；不安装、不下载、不调用新AI/网页。
如不满足可评估门，输出请求的五份文件，预测文件只记真实NOT_RUN/null，
另存缺口与质量分布，不构造检测分数。此时不能回答现有方法在哪一级有效，
也不能把缺少工件等同模型推理失败。

D1/D2/D3/Final72原Candidate、Evidence、Guide、Human/Reviewer raw不改；
D2/D3完全不受本轮诊断反馈改写。D1开发暴露不能未来包装为untouched test。
若需改真实题、增加标签来源、改变科研协议或牺牲已封存测试承诺，停止交Owner。
