# Paper 1｜外部评审#2 / S0完成后的单变量混杂控制与路线决策预注册

**状态：`REVIEWER_FEEDBACK_INTEGRATED / S0_CHECKPOINT_OWNER_RELEASE_PENDING`。** 2026-11-06 JST。仅整理Owner最新转达的评审反馈、5060已完成S0封存结果并补充未来实跑约束。**本文不是`S0_CHECKPOINT_RELEASE`、不批准本地180片段新Encoder运行、不批准S1–S4或S5模型API、不指定5090承接S3**。当前5060研究分支上报S0最终HEAD=`25936c71f96d775cca9a7603d27164e952f3a0af`，Run `W1-5060-REVIEWER-REPLAN-S0-20261106-01`。若Owner后续授权，应以本文件做路标，不替代权限和独立Evaluator隔离。

## 1. S0已核结果（不是本轮重跑）

- 原封存12事实组、36世界、TopK5共180片段；B1删78/180、B2删81/180，已召回角色候选B2 Poison 2/10被删、Clean 4/10被删、HN 2/9被删；29/36候选被召回，7漏召回。
- 原TF-IDF逐世界`n_tfidf`重算36/36与封存记录一致（历史不保存词项列表，不能声称与历史top5词逐字对齐）；top-term位置180中171含汉字、142含至少4个连续汉字；12/36世界取大簇；关联不是删错因果证明。
- B2使用`SecAI-Lab/RAGDefender@ba2a17efba165d45409114df2d70b030ade1e1b8`修复后Stage2 indices；实际余弦计算先L2归一化，**不需要`RD-zh+norm`修正**。B2仅换多语言SentenceTransformer，TF-IDF仍原英文分词/stopwords、`m=5,p=2,single_hop,K=5`。
- 生产可核可信来源锚0/180；原v0.2抽取器49/180片段有具体值、25/81被删片段有具体值、**0/81能与查询scope绑定**；保留集合同scope唯一值1/36世界。此为**现有抽取器可观察性**，不等于人工语义判断81段没有事实。
- RD-zh char2适配器合成测试已过，但**RD-zh在真实D1上未跑**；S1–S4未跑；HumanGold0，正式ASR/答案准确率未测。旧历史108真实Qwen封存。

## 2. 新增第三混杂：网页页面模板 `WEB_CHROME`

评审人观察约100/189份**上游证据**含“首页”“历史沿革”“下载Word/PDF”“扫码下载”等网页模板词。**189不等于D1 TopK180**，没有已验证的180个TopK的模板比例。新增`S0-TEMPLATE-COVERAGE_READONLY`（允许现有合法只读来源内统计，**不编码任何新向量、不改任何片段**）：
1. 在已冻结36×5 TopK原文中，逐rank标注页面导航、页脚/下载/二维码等`WEB_CHROME_CONFIDENT`、可能合法正文`AMBIGUOUS`、无模板`NONE`；记录含模板片段数/180、含模板世界数/36、各世界候选与背景占比、每世界top5 TF-IDF词中模板字符特征占位（0–5）与`n_tfidf>=3`交叉、B2删除/保留的模板覆盖；**算法角色盲先封存**，之后独立Evaluator方可按Poison/Clean/HN解盲汇总；不得把角色信息送给滤波器。
2. **网页模板与答案模板是两个不同概念**：去网页导航的清洗只解决TF-IDF词面混杂；`X-MADAM-RAG`提示的“答案是X”这类显式答案模板依赖是事实抽取器的泛化问题，应由S1/S2独立自然化压力测试，不能混为同一消融。
3. 如页面词出现在实体名称、历史沿革正文（尤其query问历史版次）、技术正文、否定/日期/数值/条款内，不可按子串粗暴剔除；标AMBIGUOUS、保留原文。只在独立于role/target/Gold的**高精度页面组件定位**上做原文span级掩码，文本与scope完整性由无标签测试加原文SHA证明，伪造信任的source自称不成立。
4. 公开Git只能放汇总计数、SHA、遮蔽规则版本和可重放代码；原top5词、原文、出处、目标和逐rank角色私有D/E存储。预注册词表和段落边界，不准看到Clean/Poison效果才挑删词。

## 3. 将混杂控制固定为2×2单变量/交互对照（未授权实跑）

**严格定义：页面模板的去除只针对 Stage1 TF-IDF词面输入。** 为避免另一混杂，retriever、原TopK5字节、原chunk内容、源rank、Stage1聚类所用Embedding和Stage2向量、生成器及后续Qwen输入均**仍使用原始未清洗文本**。不可把“先改文档再重新编码”冒充单变量实验。不同分支只改变Stage1计算top5词元的输入视图`lexical_view`和/或分词器，仍用同一旧B2向量revision和TopK。

| 臂ID | Stage1 TF-IDF tokenizer | Stage1 lexical input | 归类 |
|---|---|---|---|
| `B2_RAW` | sklearn原英文默认词规则+英文stopwords | 原始文本 | 原历史冻结比较锚 |
| `RD_ZH_ONLY` | `analyzer="char",ngram_range=(2,2),stop_words=None` | 原始文本 | **仅改分词**（合法中文公平基线） |
| `RD_TEMPLATE_ONLY` | sklearn原英文默认词规则+英文stopwords | `WEB_CHROME`高精度span蒙版 | **仅去网页模板**，归类数据预处理对照 |
| `RD_ZH_TEMPLATE` | 同`RD_ZH_ONLY` | 同`RD_TEMPLATE_ONLY`蒙版 | **联合修正/交互**，仍是迁移与清洗对照，非VESA算法贡献 |

`char` analyzer不会因`stop_words`普通词表进行中文停用词过滤，故char2统一`stop_words=None`。**其他所有参数**`single_hop=true,p=2,m=5,clustering,Stage2`、固定初始向量、确定性tie顺序不变。网页蒙版必须保留输入总长度/边界策略、每次遮罩span哈希、原文段落映射；对无法可靠分离的模板宁保留，不动正文。若模板蒙版产生仅空格/空词表或任何改写到数值/条款、则标`MASK_UNSAFE`不参与候选对比；不得静默用不同fallback得出优化。
RD-zh（仅分词）是首要论文公平参照，联合对照是移除两类混杂后可供论文安全性主对照的补充，**不能把RD_TEMPLATE_ONLY或RD_ZH_TEMPLATE相对原始B2带来的提升写成VESA方法创新**。对于之后VESA方法，对各合法臂应用相同role-blind输入以及相同模板蒙版协议（如启用），不能只给VESA清洁文本而让RD读脏文本。

**权限：** 目前只有静态RD-zh适配器与只读S0统计被执行；新增在36世界对180原文本调用**本地已缓存的固定encoder、Stage1+Stage2离线过滤**需Owner明确`R1-10(A)`/新`S0_CHECKPOINT_RELEASE`；0外部下载、0商业API，旧B2永不改写。即便原embedding缓存可复用，也需记录向量identity/编码选择，不能偷把缓存替代为同一次新试次。

## 4. S0之后的路线决策：提前冻结、先验分支（仅用于研究排期）

待上述公平臂的36世界结果和可作用池独立汇总得出后，**只做一次**以下预注册的路线选择，不看G0/G1/G2逐格正确性、不事后更改阈值。对现D1开发集，样本小，阈值仅为Owner资源分配启发式，不用于统计显著性或发表主张：

- **分支K1-A `D1_DIAGNOSTIC_ONLY`：** `RD_ZH_TEMPLATE`的已召回Clean候选误删`<=2/10`（较B2历史4/10至少减2例），并且主方法现有可作用池`<=1/36`个保留集合有同scope唯一候选，或被删除候选scope匹配`=0/81`；则D1定位为“中文迁移/网页模板混杂的开发诊断 + 可用性不退化”，方法正面收益应在S2/S3与**新且独立、有来源证据的中文版本集**上证明。仍必须单列在D1上报告所有失败，不因转向更改原数据或Gold。
- **分支K1-B `D1_EXPLORATORY_METHOD`：** `RD_ZH_TEMPLATE` Clean误删`>=3/10`，**并且**预先固定抽取器在角色盲D1至少有1个B2/修正版被删候选与query在主体/属性/时间scope同值或可比（有效可作用池`>0`），且后封存独立评估不发现明显Poison误放。才允许将D1列为M1-safe/M2的**额外探索对照**；S2/S3仍是主要多毒安全性验证，不将D1作为独立外推集。
- **分支K1-C `INSUFFICIENT_OR_MIXED`：** 上述均不成立，或清洗导致过度删正文/可信来源锚仍为0、故不能定义可信scope。保留D1开发诊断定位，提交一次Owner决策：补充可靠来源登记、增加外部自然中文数据或修抽取器，**不得为落入分支K1-B在D1上调参**。
- **优先原则**：以上阈值以`RD_ZH_TEMPLATE`为消混杂诊断；论文方法主性能必须相对`RD_ZH_ONLY`与`RD_ZH_TEMPLATE`都公平报告，而且真实数据角色/指标仅在冻结后独立Evaluator可读。若某臂Clean误删0，不能计算“降低>=50%”的分母，记`NO_HEADROOM`。
- **Gate限制**：严格P0且没有真实可信锚时D1目前Clean可恢复下界为4/10是**相对旧B2**的条件性证明；换成RD-zh或移除网页模板后，**必须重新计算每个公平基线的误删门槛**，不能把旧B2的4/10下界当新修正版“必然的4/10”。修复基线不会赋予VESA独立新贡献。

## 5. X-MADAM-RAG必须在论文related work实质对比（2026-06-11）

**原文:** Kang, Yongqi; Fu, Yu; Zhao, Yong. `X-MADAM-RAG: Diagnosing and Handling Chinese-English Evidence Conflict in Retrieval-Augmented Generation`, arXiv:2606.12903, https://arxiv.org/abs/2606.12903 。文中方法：逐文档抽取候选、可见证据修复、确定性候选分组、冲突感知聚合，确与原M2“按答案值分组”高度重叠，不能自称首创。其原模板丰富的300样本上纯规则抽取strict accuracy=1.000；100样本自然化测试后规则抽取下降至0.000，X-MADAM-RAG下降至0.300，说明**自然中文无固定答案模板时的抽取鲁棒性是独立瓶颈**。该论文是中文/英文受控证据冲突，不是针对单文档隐蔽知识投毒与证据版本/生效期的完整防御；我们不能把它概括为“只做规则不关心安全”，也不能宣称VESA已优于它。
研究的**候选差异化贡献**只能待证：`single-candidate stealth factual poisoning`与多毒/多数毒威胁下`P0`稳健选择、`M3`事实生效时间/条件/版本与未证修订风险、对`RD/RD-zh`的可审计嵌入与无额外LLM核验成本；其中M2-detect与M2-vote必须作为已有工作与消融对照而非创新本体。
因此S1/独立S3至少包含**明显答案模板/自然表达去模板配对**、法规正文与页面导航模板交错、主体属性相同但version/scope不同的实例，独立Evaluator报告自然化前后`wrong/decided`、`wrong/total`与coverage。不能把在S2自己生成的规则化模板上>90%抽取当自然检索外推。

## 6. 对S0完成报告的审查与下一动作

- 可接受S0_COMPLETE并保留所有封存摘要；S1/S2/S3/S4全部`NOT_RUN`，S5`NOT_AUTHORIZED`，不得重写原W1-5060 S0收据、旧108回包和RD-zh静态适配器；网页模板`S0-TEMPLATE-COVERAGE_READONLY`为**追加只读诊断**，不要用改写过去S0 PASS状态的方式追加新实验。
- 下一任务**首先仅处理网页模板TopK覆盖率的只读诊断与四臂预注册计划**，新RD-zh/模板臂本地编码实跑权限、S3造题隔离方和S1放行必须由Owner明确签署；可将新权限与S0 checkpoint合并为一次短决策，而不是重复写准备包。
- 按P0/PO-MHEP必要报表只记录owner决定、源码SHA、冻结世界数/原role-free packets、网页模板蒙版SHA、真正额外encoder调用数（0或实际）、每臂结果及全世界分母；D/E安全与5090隔离，主研究合并/D2D3未授权。新一轮不做真实Qwen，不调用额外在线服务/不花费API费。
- 评审人下一次收件：S0已验收摘要、TopK模板覆盖计数、四臂对照是否获Owner批准以及如已运行的已封存结果、K1路线选择、M2与X-MADAM-RAG差异说明。所有未跑项保持NOT_RUN。

**科研边界**：修正分词或清除网页模板本身属于对照与预处理，不构成VESA的新算法贡献。0/180来源锚和0/81旧抽取器绑定意味着真实D1对P0主方法的正向机会缺乏证据；任何新的声称须经独立新数据或可靠来源锚验证。
