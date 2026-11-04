# 第七条范围已收口，12题AI来源草案准备完成

2026-11-04 JST；PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；PODR-160。

Owner已选择“限定第七条核心职责”。LOCAL采用新题干，仅按第七条列人社部门总括职责，保留公布机关、令号与协调监管角色区分；原题、原范围差异及所有AI审阅均保留。

两位原审阅者分别完成修订题的3字段复核，6处引用定位通过；来源仲裁确认3字段语义等价、未决0，另3处引用定位通过。此轮是已选范围后的定向版本复核，不是新建独立审阅者或重跑全部12题。

第二版保存了12题问题草稿及隔离的评价侧答案提案，全部为SUPPORTED_PROVISIONAL，原先的职责范围待决项为0。另将条文对照和版面日期两处措辞在新题干中写明确，原问题及事实字段值不覆盖。题目内容变化对应新的不透明query ID，并保存前后文本哈希与版本原因；没有使用被测模型的效果结果来修题。

这些材料仍是AI_REVIEWED_DEVELOPMENT_DRAFT_NOT_HUMAN_GOLD。Owner确认的是职责问题范围，不是逐条事实标签、人工金标准、正式协议或付费实验。原草稿作者看过候选、审阅模型可能有相关错误等限制保持。暂不需要Owner从零整理或手填12题；数据查证、引用定位、格式隔离已由执行端和agent完成。

当前数据路径均在Git外：

- `experiments/rag_defense_reconstruction_01/ai_adjudication_01/prepared_drafts_v2/QUERY_DRAFTS_WITHOUT_ANSWERS.json`：只有query ID和问题正文。
- 同目录`EVALUATOR_ANSWER_PROPOSALS_PRIVATE.json`：答案草案、事实字段、来源支持及AI审阅限制，仅评价侧使用。
- 同目录`QUESTION_VERSION_CHANGELOG_EVALUATOR_ONLY.json`：原题与第二版身份及修订原因。
- `ai_adjudication_01/OWNER_REVIEW_SHORTLIST_V2.md`：已收口事项与后续准备门。

未构建可执行C0–C3实例，也未为任一模型增加证据权限。第一版的36世界引用来源出现性检查不能充当第二版逐世界足证性、真实检索召回或安全性能。下一步是准备可审阅的受控检索后场景合同，明确共同证据预算、反事实互斥、评分与失败处理，并闭合RAGDefender迁移可比性。付费执行继续受“不得自动调用API”和费用核对门约束。

本轮阿里云新增调用0、费用0；未重跑此前19项验证，无GPU/5090或模型下载。B4未实现，E1新弱点与方法效果未测试，正式实验NOT_STARTED。数据准备子任务有实际完成产物，完整Paper1任务仍未完成。

来源与收口证据：[第二版汇总](AI_DATA_PREPARATION_SUMMARY_V2.json)、[第二版检查](AI_DATA_PREPARATION_CLOSEOUT_V2.json)、[追加证据索引](AI_DATA_PREPARATION_EVIDENCE_INDEX_V2.json)。[第一版报告](AI_DATA_PREPARATION_OWNER_REPORT.md)中的范围待决状态为原始历史，已由本记录和PODR-160覆盖。
