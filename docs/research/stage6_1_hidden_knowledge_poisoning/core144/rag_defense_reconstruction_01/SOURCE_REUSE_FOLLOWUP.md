# 已有来源可复用性补充核查：找到官方问答线索，尚未形成 Pilot 真值

2026-11-04 JST；PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；SOURCE_EXTENSION_RECORD。

本轮附件与原任务书 SHA256 相同：`0486430f972336160947296e7bf3185c1875a07806906ebf02ed4c5b4e1aca5c`，不是新的付费、B4或正式实验授权。Git起点4a6e76c，工作树干净、远端一致。继续范围仅为既有来源只读核查和证据/治理保存；未重跑此前示例、测试、检索或模型。

新增事实：

- 冻结12组的36候选涉及28份不同证据文档；28份均在上游33文档语料和注册表找到，正文及文本哈希与交接包相同。没有追加外部来源或下载。
- 上游注册表在这28份中的已知字段为：issuer 24、authority_role 3、publication_date 4、effective_start 9、current_history_role 4；publisher/effective_end 均0。25份有 metadata_source 记录。authority_role 在交接包schema中被省略，不能据包内缺字段推断上游完全没有。此处按不同文档计数，不能与上一轮按证据出现次数的缺失数直接相减。
- 找到旧 `QUERIES_TEXT_ONLY_V1.jsonl` 共120条，120条均含完整候选命题；冻结子集36条也全部如此。固定构造代码以候选标题/前20字加完整候选生成检索串。这些是 candidate-conditioned retrieval queries，不是独立QA问题，不能直接复用成新任务查询。
- 28份来源中有2份明确包含原作者问答，本轮用显式问答边界定位出17条片段线索，已保存源文档身份、字符起止和哈希；它们不含新生成的标准答案。片段定位可能不穷尽全文，答案结束边界仍是待复核候选。

两份问答来源分别是本地已冻结的上海人社答复页面与1988年女职工旧规解答页面。前者的问题含“公司的做法”这类依赖上文的指代；后者必须明确历史版本语境。这里只证明归档正文存在问答，不作现行法律效力或法律适用判断，也没有重新验证在线页面。

这扩展了上一轮“被审计交接包没有独立QA字段”的结论，未推翻它：包内缺裁决记录，与上游正文存在可利用的问答可以同时为真。不能再把下一步简单描述为“从零编题”，也不能把17条来源线索称为17条已裁决Pilot实例。

在本次来源清点完成时，`ready_independently_adjudicated_groups=0 / needs_adjudication_groups=12`；尚未建立源问答与事实组的语义对应，未产生新query/答案/场景。随后Owner明确“请继续”，LOCAL在同一冻结12组上整理了下述待裁决问题草稿；仍无正式query/答案/场景，也未使用E1成败挑题或打开旧预测、Human/GT/Expected载荷。全部实验问题仍停在[负责人报告](OWNER_FEASIBILITY_DECISION_REPORT.md)的RD01-DATA-MIGRATION-GATE。

建议先审阅这17条来源问答线索，核定：问题是否独立、完整题干、目标时间/版本、适用范围、机关角色、答案支持span边界，以及是否能在不按结果选题的前提下服务原冻结事实组。无法对应或仍不唯一的组保持NEEDS_ADJUDICATION，不用修改候选或标签补齐。正式裁决包、真值和模型输入仍未生成。

FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW：本次是只读来源核查，不是新实验；官方问答不自动等于当前版本真值，旧检索串可能把待判断事实直接带入query，元数据不能用候选角色补造。来源范围和判断边界公开保留。付费、B4、下载、5090及历史/数据工作线修改仍禁止自动开展。

证据见[SOURCE_REUSE_AUDIT.json](SOURCE_REUSE_AUDIT.json)和[补充证据索引](SOURCE_REUSE_EVIDENCE_INDEX.json)。原私有归档与PUBLIC结果保持；新增定位载荷仅在Git外。本文不是Owner对方法、独立裁决或付费Pilot的接受决定。

## Owner继续指令后的具体审阅材料

新建Git外 `experiments/rag_defense_reconstruction_01/adjudication_review_01/REVIEWER_SOURCE_ONLY_DRAFT.json`：12条问题草稿、23次官方来源引用、可定位摘录、版本/时间/条件/角色待核事项；expected_answer全部null，所有批准字段为false。裁决人可直接填写，无需从空白模板重新寻找来源。

草稿作者已看过三元组候选正文，故这些问题不是独立命题或独立真值。后续须由审阅者基于官方来源独立裁决。审阅文件不附候选记录、候选/组ID、S/角色/GT或旧输出；源摘录自身可能与合法候选表达重合，不能据此宣称内容层面完全盲化。源引用池是各世界来源的合并审阅材料，不是运行时统一证据包；真实实验仍需逐世界核验足证性和所有方法公平访问。映射只在独立的CONTROL_MAPPING_EVALUATOR_ONLY.json。

具体风险包括：日期事件不同不能合成一个模糊标签；年休假单项排除不等于全部资格判定；2026答复的报道时点不能冒充本日现行标准；1988解答本身不能证明2012废止事件。这些只作为待裁决问题保留，没有写出标准答案。

新包检查通过：12条唯一review ID，全部答案空且未批准，来源摘录偏移/哈希与原文一致，审阅文件无候选/组ID，私有文件保持Git-ignore。详见[准备状态](ADJUDICATION_REVIEW_PREPARATION.json)。未发付费请求，未实现B4，未创建模型可执行实例。
