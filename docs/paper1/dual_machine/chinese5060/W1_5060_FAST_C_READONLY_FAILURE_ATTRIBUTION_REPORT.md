# Fast-Track C：只读失败归因

2026-11-05 JST；`W1-5060-FAST-C-20261105-ATTRIB01`；**PARTIAL_DIAGNOSTIC_UNRESOLVED**。
授权FAST-C-06、控制面4ba1ad732987be4a5c84b5808da210705e72739e。只读统计/交接已完成，阶段根因仍未充分识别。
本轮安全实验试次0、defend/encode/retrieve/LLM调用0、下载0、商业API0；未加载模型，未读取D2D3/Reviewer/GT Vault。
原P2、PAIR01数据与全部seal/旧负结果保持不变。不能用缺trace作为补跑理由，因果子问题到此停止。

## Observed：确定性复核的事实

【E1】全36世界(P/C/HN各12)、条件29(P10/C10/HN9)、MISS7(P2/C2/HN3)身份与计数复核通过。
下表列联格是“B1 flag→B2 flag”，不是新实验或ASR；每格写全分母计数/已召回条件分母计数。

| 分层 | 00 | 01 新删 | 10 恢复/失去过滤 | 11 共删 | 全/条件分母 |
|---|---:|---:|---:|---:|---:|
| Poison | 9/7 | 2/2 | 1/1 | 0/0 | 12/10 |
| Clean | 7/5 | 4/4 | 1/1 | 0/0 | 12/10 |
| HN | 9/6 | 1/1 | 1/1 | 1/1 | 12/9 |

Poison TP仍1/12→2/12（条件1/10→2/10），Clean FP1/12→4/12（1/10→4/10），HN FP均2/12（2/9）。
复核any-chunk、all-retrieved removal、partial与残留均与原私有行一致。每个召回候选仅1chunk，partial0不是多chunk鲁棒性证明。
Poison命中后的漏报B1为9/10、B2为8/10，剩余Candidate片段P/C/HN分别9/9/7与8/6/7；检索MISS不算检测成功。
旧chunk删除78/180、81/180是全TopK删除量（含Candidate及无GT背景），**不是“背景删除数”或背景FPR**。

【E2】旧72个profile都有n_adv、n_tfidf、5个frequency_scores及removed_indices，全部按保存的分数和原低index规则精确复算。
但cluster assignments、embeddings、top-similar pair身份与逐词TF-IDF权重均0/72覆盖；不得用0值替代不存在字段。
n_tfidf在两方法36/36完全一致；n_adv在13/36不同，删除集合在21/36不同，其中8/36删除数相同但对象不同。
因此有“计数变化和选择变化共现13”“同计数但选择变化8”“两者均不变15”，不是Stage1/Stage2错误因果分解。

【E2/E3/E4】任意频率同分B1=29/36、B2=33/36；真正跨删除cutoff的边界同分仅6/36、8/36。
10个候选flag翻转中，4个n_adv变化、6个n_adv不变；6个在任一方法有边界同分、4个两方法都无边界同分。
角色盲feature从不读取candidate身份；这些关联只在后封存Evaluator合并批准旧评价材料后计算。

| 已召回候选的开发错误 | B1 | B2 | 候选落在cutoff同分组的错误 |
|---|---:|---:|---|
| Poison保留 | 9/10 | 8/10 | 两者均0；保存分数严格低于实际删除cutoff |
| Clean误删 | 1/10 | 4/10 | B1=0，B2=1；其余为保存分数选中 |
| HN误删 | 2/9 | 2/9 | B1=1，B2=0 |

合计12+14=26个条件性开发错误决策，只有2个候选本身处于跨cutoff同分组；不能把上下文存在任何同分都说成该候选因同分而错判。
这是在已观察分数和count下的机械规则归类，不证明分数为何错误或任何替代tie策略会更安全。

## Source-Derived：静态源码与既有Git记录

【S1–S4】仅git-show读取ba2a17ef原库，未import/执行：Stage1由层次聚类与英文TF-IDF投票产生n_adv；
Stage2用依赖n_adv的最相似pairs累加频率，按降序和低index选n_adv条；Query不参与现有detector决策。
所以可核对保存的最终分数→选择，但不能据缺失embeddings/pair-set复建阶段内部过程，也不捏造版本感知能力。
【E6，GIT_SOURCE】旧模型观测：B1有Normalize且max256，B2无Normalize且max128，两种模型包差异不仅是语言目标。
旧观测显示两者输入均未超长；本轮没有重新tokenize或推理，不能将本次差异归因于截断。

## Inference：有边界的推论

【E2/E3/S2/S3】仅以Stage1计数变化解释全部21个删除集合变化不充分，因为8个集合变化发生在同count下；
同样，任意频率同分也不足以解释全部候选误删/漏报。以上只是排除“唯一解释”的必要条件检查。
Stage1 count是否等于真实恶意数量不可判定：18背景没有完整GT，不能假定它们全部是合法负类。
当前D1结果仍不支持仅换embedding获得安全+质量整体改善；不进行显著性或独立泛化声明。

## Hypothesis：未检验的机制问题

【E2/S2/S4，HYPOTHESIS】模型包差异可能通过聚类计数、相似pair构成或二者共同影响最终频率排序；
旧TF-IDF计数虽然相同，词项/权重及pair-set缺失，不能确定每次翻转的充分因果路径。
这仅是可检验问题，不是B5/B6方法设计、改tie规则的提议或未来实验许可。

## Unresolved：局部停止及裁决边界

cluster membership、embeddings、pair-set/逐词TF-IDF记录缺失，Stage1错计数、Stage2根因与tie反事实均INSUFFICIENT_TRACE。
本轮白名单内实际读取的旧评价行未保存HN合法历史版本/失效时间/时间条件/文本一致性子类，9个条件性HN均NEEDS_INDEPENDENT_ADJUDICATION；
不以候选文本自行推断合法性、攻击意图或target。来源全部SOURCE_UNVERIFIED：仅核快照/引用字节，不新增T1可信授予。
12事实组的36角色世界存在组内依赖，不是36独立query；旧未warmup时延不用于效率结论。
HumanGold0，target UNKNOWN，C3待裁决，targeted ASR/Answer Accuracy均NOT_MEASURED。

## 独立盲审交接与证据

【E5】独立进程仅核原12题/38原子/16来源和56处引用offset；原卡hash不变，无签署，无新Gold。
新独立review ZIP仅12卡、16源和空白裁决/独立性说明，共29成员，不含检索结果、角色映射、统计、旧预测或AI比较意见；未发给Reviewer。
来源许可/真实性没有新增外部核验，内部受控保留；公开Git仅hash/index，不公开源正文或署名原文。
ZIP SHA256 `2e289f68c8adee54187a4520d116182e20171a3dca3cd05daf3312a98a37f8c7`；仅受控本地保存，来源许可与独立审阅资格由Owner确认后再分发，return另存，不能覆盖原卡。

三资料流使用不同进程/白名单；role-free完整SHA lock后Evaluator才读批准旧Evaluator行，绝不返写角色盲输出。
每条解释的evidence_ref、SHA256、field、confidence及GIT_SOURCE/LOCAL_PRIVATE_EVIDENCE_VERIFIED/HYPOTHESIS区分见[证据索引](fast_c/EVIDENCE_CLAIM_INDEX.json)。
新统计代码5tests、Ruff、MyPy4源码（check-untyped-defs）通过。增强类型检查发现的5个Counter注解缺失已修正、原脚本保留；
最终源码dff1405固定后，仅再次计算旧JSON，8个输出文件逐字节一致。这是确定性复核，不是新安全试次或模型重放。
私有归档SHA256 `73b3f66a5b410e61cc8b9772885c77e026de502b3b9d78b295fa2e52b4a9fdb4`；见[Analysis Manifest/命令/读取白名单/归档索引](fast_c/FAST_C_ANALYSIS_MANIFEST.json)、
[Stage覆盖度](fast_c/STAGE_TRACE_COVERAGE.json)、[配对四格表](fast_c/PAIR_FLIP_AGGREGATE.json)、[同分关联](fast_c/TIE_ASSOCIATION_SUMMARY.json)、
[独立交接索引](fast_c/ADJUDICATION_HANDOFF_INDEX.json)。所有新输出/临时/缓存D，未提取旧ZIP到新路径，无新模型/数据下载或C项目写入。

## PO-MHEP十二字段：阶段因果不可识别

1. Issue ID：W1-5060-FAST-C-TRACE-01。
2. 名称：原trace不足以识别阶段根因与HN时效合法性。
3. 阶段：只读Fast C，在旧输入hash验证和确定性统计后。
4. OBSERVED_FACT：计数/最终分数/删除indices完整，内部pair/聚类字段缺失；SOURCE_DERIVED_FACT：原库选择链；
   INFERENCE：现有输出仅支持规则和关联复核；UNKNOWN：阶段反事实、背景真值、独立时间/范围判定。
5. 约束：只读旧输出，不补跑/补trace/新增路径/推断target，PO-MHEP与FAST-C-06。
6. 原因：继续给根因标签会把相关性变成因果。
7. 风险：错误科研归因、以结果设计GT/方法、背景误标、标签泄漏；停止因果子问题保留复现与后续架构空间。
8. 选项A：按现有证据交付PARTIAL及缺口，可逆、API0、不改科学资产；选项B：未来Owner另行指定确已存在的额外trace路径并授权只读核验；
   选项C：新增trace或试次本轮未授权，不执行。B/C有资源/复现/论文影响，需单独决策，不能自动继承本授权。
9. LOCAL建议：A；先由Owner审阅本次边界及独立裁决交接。
10. 理由/置信度：字节/统计高置信；根因、HN合法性/来源信任与无同分反事实未知。
11. 待Owner：是否存在可另行明确授权的旧trace；何时组织独立人工范围/target/C3裁决；本轮不要求批准新方法或实验。
12. 决定前：因果补证支路STOP，仅本次脱敏证据/文档/Git收口；禁止模型/检索/Guard重跑、B5/B6、D2D3/GT、付费、T1/T2/Claim。
