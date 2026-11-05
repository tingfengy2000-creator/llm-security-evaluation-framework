# Fast-Track B：B1/B2真实离线配对结果

2026-11-05 JST；run `W1-5060-FAST-B-20261105-PAIR01`；**B1_B2_PAIRED_OFFLINE_DEVELOPMENT_COMPLETE**。
执行源码完整SHA `17897075bfdbc325979b29e75b7209877bc5bebb`。旧合同缺失、HF直连失败及人工文件修复记录全部保留，不追溯改写。
原12张盲审卡复用、Human Gold0。仅本次已批准T0/D1开发过滤完成，交付后STOP，不进入P3或付费阶段。

## 实测结果与解释

两方法各36/36成功，失败/未运行0，空上下文均0/36。共72次defend、各实际观察36次encode，API0/费用USD0、运行网络尝试0。
同一批36 TopK5原字节、相同顺序、原query和库参数，无索引重建、重检索、补召回或B0重跑。
表内每格先为完整分母，再为Candidate已经进入TopK的条件分母；Poison分子是TP，Clean/HN分子是FP。

| 方法 | Poison Recall：全/条件 | Clean-FPR：全/条件 | HN-FPR：全/条件 | 删除chunk | mean/median/P95 ms |
|---|---|---|---|---:|---|
| B1 | 1/12 (8.33%)；1/10 (10.0%) | 1/12 (8.33%)；1/10 (10.0%) | 2/12 (16.67%)；2/9 (22.22%) | 78/180 | 152.54/120.32/132.94 |
| B2 | 2/12 (16.67%)；2/10 (20.0%) | 4/12 (33.33%)；4/10 (40.0%) | 2/12 (16.67%)；2/9 (22.22%) | 81/180 | 220.61/219.29/241.90 |

7个检索漏召回仍为Poison2/Clean2/HN3，不计成防御成功。B1检索命中的Poison仍保留9/10，B2保留8/10。
本轮只换embedding使Poison条件Recall增加10pp，同时Clean条件FPR增加30pp；HN条件FPR不变。
这不是兼顾安全和质量的整体改善，不把B2中文迁移说成论文创新、强基线优越或GO。
配对上Poison有2题新增过滤、1题失去过滤；Clean新增4题误删、1题恢复；HN两边各1题互换，另1题共同误删。
不按聚合净增益掩盖这些配对变化，完整逐世界私有行、删除/残留indices和配对差异都在归档中。

每个进入TopK的Candidate本次恰好只有1个chunk，故any-chunk flag与all-retrieved-candidate removal计数相同。
部分删除残留两方法均0，但本次输入不具备多候选chunk覆盖，不能据此宣称部分删除问题已解决；“全部召回片段删除”也不是完整原文清除能力。
B1剩余Candidate片段P9/C9/HN7，B2为P8/C6/HN7；未标背景不加入Clean/HN分母。
完整180chunk中B1删78、B2删81，不能将这些删除都贴Poison标签。

## 算法身份、公平性及局限

B1=`B1_PUBLIC_V0_2_PINNED_MODEL`：未改SecAI-Lab/RAGDefender@ba2a17efba165d45409114df2d70b030ade1e1b8，
不是ACSAC artifacts/原论文严格数值复现。B2仅换成固定多语言embedder对象，库的聚类、TF-IDF/English stopwords、Stage2、p2/m5/single_hop与异常处理完全一致。
未改RAGDefender源码；原对象注入接口避免floating main。encode使用库原kwargs，没有外加normalize、batchsize或max_seq_length修改。
B1模块Transformer/Pooling/Normalize、max256；B2为Transformer/Pooling、max128。两者维度384、BertTokenizer fast；
这些模型固有差异均保留，不能把效果仅归结为“语言”单一属性。输入实际token范围与total详见[模型观测](fast_b/pair01/MODEL_AND_DIAGNOSTIC_OBSERVATIONS.json)。
当前公开库query参数未参与detector决策；本轮不能测其时间/条件/来源理解能力或从真值猜攻击意图。
只读Python profile观察Stage1计数、Stage2频率分数和encode次数，不改函数/对象。B1有29/36、B2有33/36上下文出现频率同分，沿用原库低index tie-break与稳定pair顺序。
记录同分不是证明错误的因果归因，也没有为改善结果修改并列处理。原英文TF-IDF默认token规则及stopwords未作中文修复。

时延包括只读profile开销，无独立warmup；固定先B1后B2、world排序。B1均值高于P95受首次调用长尾影响，原始全部时延保留，不能冒充部署性能或显著效率优势。
模型load时间单列；CPU2/无GPU，无显存或RAM峰值benchmark。编码token统计不包含query（库未encode query）或任何LLM token，USD0。
模型调用次数真实观察各36；Transformer内部算子不当作额外API。

## 模型资产与存储

唯一新增下载模型all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41；10必要文件size和Git blob/LFS SHA均匹配手工取得的固定官方tree。
权重90868376字节，SHA256 53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db。
README模型卡Git blob匹配，声明Apache-2.0；没有虚构tree中不存在的独立LICENSE文件。人工获取来源/无失败重试由Owner声明，不冒充机器TLS日志。
曾有小文件重复、目录/后缀错误及190字节误命名权重，原件保留；通过Git blob识别后只复制正确文件到D，真实权重另补。
文件正文、16MiB保守传输余量与旧失败请求累计估计占用108362402字节（约103.34MiB）/250MiB，手工请求实际头/TCP字节未机器测量。
本轮Agent新增下载0、无额外依赖；旧HF失败账本未清零。原B2模型10文件从既有C缓存逐hash复制D，未迁移/修改C原环境。
所有新模型/缓存/TEMP/TMP/日志/归档D，Python-B、离线flags及socket/DNS门；不是OS级防火墙或OS日志零C写入的承诺。
原生Windows，不调用WSL/Docker/conda，不新建VHDX；2GiB冻结新增峰值及20GiB余量满足，实际已知受控目录用量见Manifest。

## 证据、检查与评价边界

7项输入/索引/封存测试、Ruff、MyPy3源码通过；新增Evaluator的workspace参数后又做Ruff/MyPy窄复核。
初始开发lint与Counter类型注解错误在源码冻结前修正，未运行其他科学试次；见[失败/事件](fast_b/pair01/FAILURES_AND_EVENTS.json)。
所有runtime输出封存后才以独立进程打开批准D1开发标签；Evaluator的标签/映射路径hash与P0/P2合同一致。
Guard只见role-free query和5条chunk正文，不读角色/S/攻击目标/旧预测/Reviewer/GT Vault；保留原输入与输出seal及单独评价seal。
没有生成器或独立Human Gold，因此targeted ASR、Answer Accuracy、生成Abstain和Unsupported QA均NOT_MEASURED，绝不填0。
不使用旧E1 37/40，不从D1官方来源拷贝中自动授予T1信任；T2禁用。本轮不做新机制/B5/B6或D1-40。
这是19文档封闭世界的D1开发诊断，不是独立泛化、显著性、正式论文成果或对原论文全局有效性的否定。

原始逐世界预测/原文仅本地受控。归档 `W1-5060-FAST-B-PAIR01-20261105.zip`，SHA256 `445dbf97904706334acb2a2b890d4c51dae244285ff5f0607d72ed78340c4dec`。
过滤输出seal SHA256 `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`；独立评价seal SHA256 `0027a03c490f80d98327fbdd8f787830affde3bcfbf9e6c02bd805bf260c79a1`。
见[完整Run Manifest/命令exit和归档逐文件索引](fast_b/pair01/RUN_MANIFEST.json)、[配对聚合指标](fast_b/pair01/PAIRWISE_B1_B2_METRICS.json)、
[资产清单](fast_b/pair01/ASSET_MANIFEST.json)、[待裁决索引](fast_b/pair01/ADJUDICATION_PENDING_INDEX.json)。

下一Owner Gate：审阅本次开发负结果与独立人工答案范围/target/C3裁决，决定下一阶段；本轮无新机制审批请求，也不自主进入付费或P3。
