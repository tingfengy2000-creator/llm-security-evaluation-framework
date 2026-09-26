# Paper 1 人类可读实验总规划与实验总账

## 2026-09-26：两条修订文本复核通过，现在可以发第二阶段材料

R3-gpt 和 R4-codex 已分别复核上轮改过的两条候选。两人都认为文字自然；原本设计为“同一人既享受、又不享受年休假”的那条仍被识别为文本内部冲突，另一条没有内部冲突。我们原样保存两份返回，没有为求所有评审一致而再改文本。机器再核对 24 条候选、旧版与新版证据、官方网页哈希、三元组样式和盲包字段；有界检查通过，但它不能代替下一阶段的事实与证据审查。[详细记录](../formal240/PAPER1_FORMAL_D1_CANARY_PHASE1_FINAL_CLOSEOUT_V1.md)。

因此，Owner **现在可以**把冻结的 Phase2 V4 题包及同一套 V4/V4.1 规则分别发给原 R3、R4 会话。这里的“可以发”不等于已经发出或审完，更不等于 Canary 被验收。R5-claude 只是有额度时可用的第三位辅助者；Owner 随后同步了两份真正的 R5 文件，我们已原样保存并核对其 24 条与 2 条返回。R5 在“文字自然度”上和主评审有少量差异，其中一条把刻意的内部矛盾当作不自然；这不等于候选又坏了，不会为了三人一致而改掉设计的矛盾。真人 A/B、其余40组、正式切分与训练继续等待后续门控。

## 2026-09-23：两位新盲审员复现同一措辞小问题，已准备两条定向复核

R3-gpt 和 R4-codex 的第一阶段答卷已按原样保存。Owner 澄清了误贴材料造成的误会：R3 并没有提前做第二阶段，因此没有给 R3 记流程事故。Owner 还确认两人各用全新隔离会话；这属于 **Owner 人工确认**，不是我们拿到了会话系统日志。两份答卷各有 24 条，题号、顺序和选项均有效；五项结构化判断全部一致。两人都指出同两条候选里的“第四条下”略显生硬。

为避免正式真人 A/B 后返工，我们只把这两条的固定短语改为“根据《职工带薪年休假条例》第四条，”，另外 22 条、事实内容和证据不变。两条修订文本使用新盲号，旧文本和旧答卷完整保留；一条原有的“既享受、也不享受”内部矛盾也仍在。现在给两位原评审会话准备的是 **仅两条的第一阶段复核包**，请他们重新判断自然度和内部冲突。第二阶段 V4 材料虽已预建，**还不能发**；只有两人定向复核都通过，才能另行放行。Canary 还没有 Owner 验收，真人 A/B、其余 40 组、切分和训练都不能开始。[锁定与修复记录](../formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE1_LOCK_AND_TARGETED_REPAIR_RECORD_V1.md)。

## 2026-09-23：把下一轮两位盲审员明确区分为 GPT 与 Codex

Owner 将下一轮的两个新评审席位命名为 `R3-gpt` 和 `R4-codex`，便于日后追溯是谁、在哪种平台完成评审。它们不是此前 R1/R2 的改名，也尚未开始评审。GPT 需要全新独立会话；Codex 更不能沿用当前知道项目构造、答案和旧分歧的工作会话，必须在空白、隔离的环境里只拿到本阶段应看的文件。两人拿到的信息和判定规则等价，平台不同不代表我们在做模型性能比较。

为避免再次出现“第二阶段身份对不上第一阶段”，每一位都要从只看候选文本的 Phase1 重新做起，分别保存原件、哈希和会话/访问证明。**两份** Phase1 都通过，才给两人第二阶段的冻结证据与 V4.1 说明。旧 R1/R2 回复、候选、证据与原协议不改；本轮只把分发前的隔离和登记要求写清楚。[给协调人的 V2 计划](../formal240/PAPER1_FORMAL_D1_CANARY_R3_GPT_R4_CODEX_REVIEW_PLAN_V2.md)可直接照门控执行。Canary 尚未验收，不得发给真人 A/B。

## 2026-09-23：D1 Canary 第二阶段发现“评审会话串位”，改用全新 R3/R4

Owner 收到的第二阶段回复这次确实已保存：原材料是一个同时粘贴 R1、R2 回答的文件，我们先保留整个文件，再不改动字节地截出两段 JSON。两段各 24 条，格式、题号和顺序都对。但所谓 R1 的原文自己说明：这个会话在第一阶段其实扮演 R2，本轮却被指定为 R1。因此，两份看似齐整的回答**不能证明来自两个始终独立的评审链**。R1 仍可帮助发现说明书问题，却不能与 R2 合算正式双审一致性；该问题属于评审流程，不是某条候选文本的事实缺陷。原 R1 把它写入一条 `phase2_issue=OTHER`，我们保留原填写，不假装从未发生。

只作为诊断，两份原文在事实总状态、最少外部证据、次生错误、证据充分性上各 24/24 相同；“版本主张”相差 6 条，“机关主张”相差 4 条，“实际看过的证据”相差 5 条，“候选问题”相差 1 条。差异显示旧说明可能让人把单纯“通过/公布/令号”当成版本，把经办或开证明的机构当成法规权威。我们没有修改任何旧回答，而是新增[通用 V4.1 字段解释](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md)，只解释这些边界，枚举和候选、证据均不变。[流程事件](../formal240/PAPER1_FORMAL_D1_BLIND_REVIEW_PROCESS_INCIDENT_V1.md)保留全部来源及哈希。

Owner 已要求使用两个全新、互不相见的 R3/R4 会话，从只看文本的 Phase1 重新开始；各自原件锁定后，才给同一会话 Phase2 证据和 V4.1。四份新原件与分歧处理、Owner Canary 验收之前，不能发给真人 A/B，也不扩到 D1 48 组。本轮是 Canary 提前发现说明歧义和流程缺陷，**不是正式数据失败或论文实验结果**。下方“Phase2 允许释放”是本轮事件之前的历史状态。

## 2026-09-23：D1 Canary 两份独立 Phase1 盲审返回已锁定

Owner 已收回两名独立外部 GPT Reviewer 的第一阶段结果。本轮只把两份原件按原始字节存入新的 E 盘证据目录，再核对它们是否回答了同一份 24 条题目、是否漏行或改动 ID、字段与选项是否合法。两份各为 24/24 条，ID 和顺序完全吻合，没有重复、缺失或额外字段。五个分类判断逐项都是 24/24 一致，没有分歧 ID；两条文字备注虽然用词不同，均指出同一条候选文本内部前后自相矛盾。原件及哈希、核验结果见[本轮锁定记录](../formal240/PAPER1_FORMAL_D1_CANARY_BLIND_PHASE1_RAW_LOCK_RECORD_V1.md)。Reviewer 的独立性来自 Owner 的实际流程确认，不能单凭答案一致反推。

因此，**可以进入向同两名 Reviewer 分别提供第二阶段冻结证据包的下一门**；这只是释放资格，不表示已经发送、收到或分析 Phase2。本轮没有打开内部正确答案/构造角色去评判 Reviewer，更没有批准 Canary、发给真人 A/B、生成剩余 40 组或启动正式实验。下方“Phase1 尚未返回”保留为上轮构造结束时的历史快照，已被本节更新。

## 2026-09-23：D1 为什么先做 8 组 Canary，而不是直接发给人工？

Owner 已批准正式 240 组中 D1 企业人力资源 Wave 的构建，但要求先用 8 个真实槽位、24 条候选检查“官方证据先行—事实锚点—文本—质量审计—外部盲审”能否走通。现在已采集并锁定 14 份政府页面快照（其中 5 份仅证明行政法规当前状态），写出 8 组事实锚点和 24 条构造候选。初版草稿先于完整逐信号预检，因此明确只算草稿；预检后另建正式待审版本。质量检查还发现两条污染文本独有分号，以及一个证据片段未包含难负例所需的第十条，均以保留旧版、追加新版的方式修复，没有抹掉过程痕迹。

目前机器可核验的项目包括：8 组确属冻结矩阵、24 个盲 ID、14/14 原始网页哈希、三元组长度/标点初筛、候选与 Phase1/Phase2 包一致、盲包不含内部 C/P/H、HKP、设计 S 或答案。但是自动抽取只覆盖标题、数字、机构和部分关系词，不能证明所有事实都没有第二处意外错误；S/E/P/T/R 的完整信号数值、按类别缺失率与方差也尚未测量。更重要的是，两名独立外部 GPT 的先文本后证据盲审**尚未返回**，所以 Canary 未验收、不能给真人 A/B，剩余 40 组也未生成。[D1 后续计划](../formal240/PAPER1_FORMAL_D1_FULL_WAVE_CONSTRUCTION_PLAN_V1.md)说明通过盲审与 Owner 验收后才如何分批扩展；所有内部构造证据保存在独立的私有 handoff 包，不能发给盲审者。

下一步由 Owner 分别将当前 Phase1 V2 包与同一 Phase1 prompt 发给 R1/R2，锁定两份独立返回后，才发 Phase2 V3 包与 Phase2 prompt；任何实质分歧先修复并全量重审，不进入 Human A/B。本轮没有正式标注、切分、训练或论文结果。

## 2026-09-22：正式 240 组为什么先冻结规则，而不是马上写 720 条？

项目负责人已决定关闭 Final72 的开发集构建阶段，开始正式规模 Benchmark 的**设计冻结**。Final72 的小样本模型表现有启发，但它被反复用于工程调试，绝不能再叫“未见过的正式测试集”。本轮建立了五个领域、四类污染、三档设计隐蔽度、每格四条独立事实链的 240 个**空槽位**；每组未来才会有当前正确、污染和合法难负例三条，720 只是目标，目前一条正式候选也没有生成。

最重要的修复是把“版本有没有修订、何时生效、是否现行”等**文件版本元信息**，与“修订后具体规定是否正确”和“谁修订发布”拆开判断。正式 V4 新增“文本内部已自相矛盾、无需外部证据”的选项；此前 Pilot 的已锁定答案不回写。隐蔽度最后由人工确认的错误及所需证据派生，不能为了填满 S1/S2/S3 设计格子而硬改真值。完整[标注 V4](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md)和[协议包](../formal240/PAPER1_FORMAL_240_GROUP_PROTOCOL_OWNER_ACCEPTANCE_PACKET.md)可供复核。

构建顺序将是先选可信官方证据、厘清版本和发布机关、画出证据路径，再写同一信息需求下的三条候选；每组只用一条中性查询。我们还事先规定了“难”证据库、元数据可观测性、常量/缺失检查以及按完整事实链切分的算法。Seed 已锁，但没有运行切分，更没有训练。下一步只需 Owner 单独审查并批准 D1 企业人力资源 48 组/144 条的实际构建；其他领域、人工分发和正式实验均不能自动开始。

## 2026-09-22：补齐遗漏的逐条分数后，第一版 Detector 告诉了我们什么？

Owner 先批准找原始文件；有界搜索确认原运行只留下完整模型的逐条分数，另八个模型只留下汇总。随后 Owner 授权按**完全相同输入、代码和设置**做一次证据重建：重建的完整模型逐条分数与原件逐项匹配，另外八个模型的汇总也与当时记录一致。原运行、原结果和历史痕迹都未替换。这是恢复分析所需的证据粒度，不是为了提高分数重新训练或一次独立复现实验。

在 Final72 开发集里，来源视角 P 和时间版本视角 T 单独使用时，对 24 组 Poison 与合法历史文本，有 20 组给出相同排序分数；这更像“分不出来”，不能草率说它们把 20 个历史文本判得更危险。合并 T 后有 17 组的 Poison–历史文本分数间隔缩小；合并 P 后有 19 组扩大，但少数组负向幅度较大。21 项输入里七项在观测值上不变，时间版本所需的关键关系仍有缺口。当前多视角结果因此仍是“混合”，不是方法成功或失败的正式结论。[详细分析](../method_engineering/PAPER1_FINAL72_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_REPORT_V1.md)解释难组、来源与版本缺口、哪些假设须去更难且独立的 240-group benchmark 验证。

下一步建议准备正式规模 benchmark 的证据库、版本/权威关系和困难合法历史样本，并在未来每个模型运行时保存逐条分数与折身份。**尚未批准**生成 720 条正式样本、正式训练、风险校准或论文效果宣称。下方“失败分析暂停”是 Owner 决策前的历史记录，不代表当前仍被该证据缺口阻断。

## 2026-09-22：为什么失败分析暂时停下？

第一次 Detector 原型本身有效、结果没有被推翻；它训练过九种固定视角组合。但原始运行最终只保存了完整模型每条候选的折外分数，其它八种组合只保存了汇总分数。新任务要求回答“加上时间版本或来源视角后，具体哪一组变好、哪一组变差”。仅凭 AUROC 等总体数字无法倒推出每组分数；若编造会误导正式 240-group 设计。当前 Owner 明确禁止重训，因此我们暂停这一部分并保留原始证据不动。[决策记录](../method_engineering/PAPER1_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_EVIDENCE_BLOCKER_01.md)给出三条路：提供当时确实存在的原始逐样本文件、单独批准一次严格等配置的追加证据重建，或明确同意只做部分分析。正式实验尚未启动。

## 2026-09-22：第一版 Document Poison Detector 到底怎么训练，得到了什么？

这一次终于真的拟合了第一个文档污染检测原型：固定的 Logistic Regression 把 21 项可独立获得的语义、事实主张、来源、版本信号合在一起。前一轮发现两项“发布机构关系”没有可信候选级输入，所以 Owner 允许在独立 V1.1 中暂缓它们；这不是为了刷分。检索行为 R 属于第二阶段“检索暴露风险”，没有混进文档本身判毒。

Final72 只有 24 条独立事实/版本链，每条链有 Clean、Poison、合法历史 Hard Negative 三种候选。如果普通随机切分，几乎相同的事实链会同时出现在训练和验证中。我们因此做 24 次 Leave-One-Group-Out：每次留出完整的一组三条，只在其余 69 条上计算缺失值填补、标准化并训练，最后每条得到一次折外分数。没有调参、找最佳阈值或做风险校准。

Full SEPT 在这个**已暴露开发集**上的 AUROC 为 `.647`、AUPRC `.496`；Poison 对合法历史 HN 在 24 组中胜出 18 组，但固定 0.5 阈值仍错判 8 个 HN。Semantic-only 的 AUROC `.623`；去掉 P 或 T 的版本若干指标反而高于 Full。所以本轮只能说“有混合信号、原型可运行但限制明显”，不能说多视角已胜出，更不能说论文最终检测效果。Temporal 仅有三项可部署信号，Provenance 还缺两项关系；7 项特征在当前小样本里为常量，57 文档可信库也可能过易。200 次组内标签置换与 2000 次匹配组 bootstrap 已做 sanity/不确定性检查，不提供正式显著性或泛化保证。

下一步更合适的是经 Owner 批准做失败组与规模化假设分析，把 HN 易误报、版本元数据、来源角色和检索库难度的要求带进未来 240-group，而不是在 Final72 上反复改模型到分数升高。[完整报告](../method_engineering/PAPER1_FINAL72_DOCUMENT_DETECTOR_PROTOTYPE_REPORT_V1_1.md)可查看九模型、难组和边界；正式 benchmark、校准与检索暴露模型仍未启动。

## 2026-09-16：为什么 Retrieval View 不能简单等于 Poison Detection？

本轮已经建成无标签泄漏的检索实验台：24 个中性“当前规定是什么”query 面对同一套 72 文档，字符 BM25 与固定
revision 的离线 Dense retriever 都保存了完整 rank/score trace。现在能稳定得到 rank、score、重复运行 stability；但没有
Trusted Version Registry，所以 7 个需要 current/history 身份的 R signals 仍不计算。

项目现正式采用两阶段风险：第一阶段用 S/E/P/T 判断文档本身的 `document_poison_risk`；第二阶段结合 query 和 R 判断
`retrieval_exposure_risk`。比如一份真实合法的 2021 年历史文件在“当前规定是什么？”下排名第一，可能造成回答采用旧版本，
所以 retrieval risk 较高；它仍然不是 Poison。

还必须区分“研究时已人工配好的 E1/E2”和真实 inference。Pilot 中直接拿 matched E1/E2 可以诊断 signal 是否有潜力，
但真实系统若没有独立 trusted evidence retrieval 或 version registry，就不可能合法得到同样输入。42 个 signals 中目前
29 个属于这种 oracle-only diagnostic，4 个是 query-runtime 可获得，7 个等待 registry，2 个 MLM/PPL 尚未冻结。

结论不是“Detector 可以训练了”：Document Detector 仍 `NOT_READY`；Retrieval Risk 为
`READY_WITH_LIMITATIONS`。下一步先补独立 Evidence retrieval 与 Trusted Version Registry，不自动训练 Detector。

## 2026-09-15：Final72 五视角信号可行性已完成，尚未训练分类器

我们现在不是在“训练分类器”，而是在检查五种安全证据是否真的存在、能否稳定提取，以及是否包含区分 Poison 和合法历史
Hard Negative 的信息。控制面先从候选、冻结 Evidence 与来源/版本信息生成无标签输入；另一个进程只读取这份输入，生成
72×42=`3024` 条 raw signal 并按 SHA 锁定；第三个进程核验锁定后，才加载 Clean/Poison/Hard Negative、HKP、S 和
matched-group 身份。Raw 中没有这些标签，也没有 Expected、A/B 或 Owner 仲裁值。

实际结果是：Semantic、Entity-Claim、Provenance、Temporal-Version 都有可计算信号，但很多只是确定性规则代理，部分为
常量、近常量或高度相关；Retrieval-Behavior 因 Final72 没有冻结合法 query 与独立 retrieval run，全部 720 项都标为
`INPUT_MISSING`，没有用标签倒推 query。MLM/PPL 没有冻结模型，因此保持 `MODEL_UNAVAILABLE`；GMTP 也因缺少完整可复现
依赖而推迟。类别各 24 条，24 个 Clean/Poison/Hard Negative 匹配组完整；Applicability 没有发现达到门槛的类别泄漏，
七个已知 Evidence 限制样本也没有形成强类别集中。

单信号的 Cliff's delta、AUROC/AUPRC 和 matched-group 方向仅用于 development-set 诊断，不能叫 Detector 准确率，更不能
声称方法优于 baseline、可泛化或达到论文结果。当前结论是 `READY_WITH_VIEW_LIMITATIONS`：S/E/P/T 足以继续方法工程，
但五视角版本在训练前应先补齐 Retrieval 输入。建议的下一任务是
`P1-RETRIEVAL-BEHAVIOR-SIGNAL-HARNESS-01`，仍需 Owner 单独批准。

## 2026-09-15：Final72 Ground Truth 正式接受，进入 Signals / Detection 方法工程

项目负责人已经以“接受，但保留已知冻结证据限制”的方式正式验收 Final72 Ground Truth。72 条候选、576 个最终字段和
每个字段的 A/B、Owner 仲裁与 correction lineage 都完整；11 项 Evidence 限制继续明确写成证据不足或证据缺失，没有被
隐藏或事后补证。Expected V3 仍只是人工仲裁完成后的研究质量对照，不能覆盖人工真值。

Final72 从现在起是开发与方法工程数据，不是论文最终独立测试集。因为我们已经用它校准标注规则、处理仲裁并检查方法，
任何在它上面反复调试的方案都必须叫 development-exposed。未来论文最终效果必须来自扩大后的 Benchmark、按 version chain
分组切分，以及从未参与开发的 test population。

### 我们接下来到底怎样检测知识污染？

`Signals（信号）` 是可观察证据，例如候选更像历史版本还是当前版本、主张中的数字/条件是否与证据冲突、声称机关是否与
真实发布/制定/修订关系一致、检索结果是否被历史版本占据。`Detection（检测）` 是把这些信号组合起来，输出污染风险。
Signals 本身不是答案，也不能读取 Ground Truth。

第一版方法使用五个视角：Semantic 看语言和语义接近度；Entity-Claim 看主体、数值、日期、条件、例外和关系；Provenance
区分网站、页面发布者、制定/通过/修订机关与官方转载；Temporal-Version 判断现行、历史、废止、替代和时间绑定；Retrieval-
Behavior 看 rank、score、top-k 版本构成与稳定性。MLM/PPL 只是语言自然度 baseline/语义信号，GMTP 是可复现时使用的外部
检测 baseline，不是我们的全部方法；核心 proposed method 仍是 Version-aware Multi-view Detection。

本轮只把信号定义、适用性、baseline、Logistic Regression fusion、风险校准候选、证据化解释、指标、消融和 240-group
Scale Readiness 写清并建立代码接口。没有跑实际信号矩阵，没有训练 Detector，没有得到准确率或优越性结论。下一步需由
项目负责人单独批准第一轮 `SIGNAL_FEASIBILITY_AND_SEPARABILITY_STUDY` 的输入、模型、query/retriever、参数和统计合同。

## 2026-09-15：Final72 Ground Truth Candidate 已生成，等待项目负责人最终接受

人工仲裁已经正式结束。系统先从四份不可变 A/B 返回重建全部 72 条、576 个字段：A/B 相同的 498 项直接沿用，两人不同的
78 项使用项目负责人在不知道 Expected V3 时作出的决定，随后再应用 8 条已批准规则 overlay 和 10 条一致性 correction
overlay。每个最终值都能回查 A、B、Owner 决定与 overlay；原始答卷和 Owner 工作簿均未修改。

只有上述 Human-adjudicated candidate 完整锁定后，才第一次把 Expected V3 用于研究者侧质量核验。Expected V3 不是
Ground Truth，也没有覆盖任何人工值。Expected 明确定义的 504 个字段中，469 个与 Human candidate 一致，35 个差异覆盖
28 个样本；其中 4 项是 Expected V3 需要以后另行版本化修正的 QC 缺陷，11 项来自已经由 Owner 以
`INSUFFICIENT_EVIDENCE / EVIDENCE_MISSING` 固定下来的已知 Evidence 限制，20 项是非阻断的人类仲裁差异。Expected 没有
定义 `phase2_issue`，因此其 72 个比较槽位明确记为不可比较，没有虚构预期值。新的 Ground Truth blocker 为 0。

当前产物是 `PILOT4_FINAL72_GROUND_TRUTH_CANDIDATE_V1`，不是已接受的 Ground Truth，也不是正式冻结数据集。Final72 已参与
校准、人工仲裁和研究者 QC，未来只能用于 development / method engineering，不能再称为 untouched final test set。项目
负责人下一步只需决定是否接受该 GT Candidate；在明确接受前，不开始 240-group、正式 Dataset freeze 或 Detector evaluation。

## 2026-09-15：Owner 仲裁一致性已闭合，未解决项为 0

项目负责人已逐项确认上一轮 9 个核验项。控制面没有修改 A/B 原始返回，也没有修改 Owner 原始工作簿，而是新增了 10 个
字段级 correction overlay：4 条把非事实冲突的 minimum 统一为 `NOT_APPLICABLE`；1 条把个人信息保护法样本的
`phase2_issue` 改为 `NONE`；1 条只把证券法样本理由中的 E3 笔误改为 E1；学位条例/学位法样本用 4 条字段记录冻结
packet-only 结论并移除 E3/E4 依赖。合计 6 个值发生变化，4 个值保持不变但理由和证据链得到规范化。

重新检查全部 72 条、576 个字段后，枚举、minimum/overall、内部矛盾、Evidence missing 和有效 Evidence 引用关系全部
通过，未解决一致性 blocker 为 0。原 Owner 工作簿 SHA256 仍为
`a4c65a22dd3a410c7744be5f256206d7217b8fda33d63c58ac99bb386fe95b01`。本轮到此停止：Expected V3 没有加载，Final72
Ground Truth 没有生成，下一步必须由 Owner 单独批准。

## 2026-09-15：Owner 仲裁已回收并锁定，剩余是定向一致性确认

项目负责人已经完成工作簿。控制面把这份返回文件按原始字节保存，没有改写任何填写痕迹；5 个候选缺陷决定和 78 个字段
仲裁全部完整。五个候选都被 Owner 判为“标注理解差异”，没有候选被自动隔离。78 个字段中，Owner 选 A 46 项、选 B 26 项、
选择 A/B 之外的第三值 6 项；其余 498 个字段沿用 A/B 一致结果，因此已形成一个 72 条、576 字段的仲裁后候选视图。

这个候选视图还不是 Ground Truth。原因不是要 A/B 重新标注，而是有少数关系约束需要 Owner 最小追加确认：4 条在 overall
不是 `FACTUAL_CONFLICT` 时仍填写了实质 minimum 值；1 条把决定性 overall 与 `EVIDENCE_MISSING` 并置；4 个理由引用了
工作簿未绑定的 E3/证据3。此前 Owner 已批准的两条规则——“文本内部矛盾时 minimum 为 NOT_APPLICABLE”和“显式修订命题
属于 version claim”——已经作为单独覆盖记录绑定，原工作簿和原填写均保持不变。下一步只需逐项确认建议值或补充 E3 来源，
不需要重新保存工作簿，也不需要重新标注 72 条。

## 2026-09-13：Owner 仲裁工具已准备，Expected 仍未打开

我们没有让系统根据“预期答案”自动判谁对，而是先把 A/B 四份原始答卷的复现性再次固定下来。现在有一份专门给项目
负责人使用的中文工作簿：第一页先处理 5 个“候选本身可能有缺陷”的问题；只有被判为标注理解差异的样本，才进入后面的
普通字段仲裁。其余 78 个分歧按同一候选连续排列，并保留 A/B 原值、理由、规则和冻结官方证据。

所有需要负责人填写的格子目前都是空的，系统没有代做决定。负责人可以从完整下拉选项中选择第三种值，不被迫在 A/B
之间二选一。Expected V3 仍保持封存；只有工作簿填写完成并在下一任务中先按原始字节锁定、校验和提取 Owner 决定后，
才可能单独批准加载 Expected 做研究者 QC。当前没有 Ground Truth，也没有开始数据集冻结、检测器、训练或正式实验。

## 2026-09-13：两位标注人的 Phase2 已锁定，当前需要 Owner 处理分歧

HUMAN-A01 与 HUMAN-B01 都完成了第二阶段。控制面没有改答案，而是先把两本工作簿按原始字节保存，再核验 72 条编号、
顺序、枚举、理由、条件逻辑和 Evidence 链接，最后导出严格八列 CSV。四份人工返回现在全部不可变锁定；只有在这个门
关闭后，A/B 的不同匿名编号才被还原到同一 Candidate。本轮没有加载 Expected V3，也没有把预期答案当裁判。

一致性预检显示：overall fact status 相同 54/72，version 59/72，authority 67/72，minimum evidence 62/72，derived stealth
64/72。`evidence_selection` 反映“实际看了什么”，不是 benchmark 标签，因此它的 18/72 只作过程观察。总体有 78 个需要
实质裁决的字段分歧，覆盖 40 个 Candidate；B 另标出五个 late candidate defect。它们可能是候选缺陷，也可能是标注理解
差异，控制面不能替 Owner 自动决定。

下一步不是重新让 A/B 全量标注，而是 Owner 只看 disagreement-only packet：先判断五个 defect flags，再逐项决定其余分歧。
在裁决完成、pending=0 且所有门重新核验前，不生成 Ground Truth，也不启动 Dataset、Detector、Training、5090 或正式实验。

## 2026-09-09：Phase2 七字段返工风险已审计，V3.2 可以分别发放

HUMAN-A01 与 HUMAN-B01 已各自独立完成 72 条第一阶段标注。控制面没有改动答案，而是按原始字节保存并核对：A 文件
3313 bytes、SHA256 `bb74908f7433bca1c834e8e7ea8e8721316edb1a503202805f90dd0e974d8bac`；B 文件 3658 bytes、
SHA256 `b27d291dcf86088dccc9a7fc7e5dda1e5c1e7af54ac7db7c3bad5d78b215daf2`。两份文件的编码、五列格式、72 个编号、
编号顺序、选项和值与理由规则都通过，因此“双 Phase1 都完成并锁定后才放 Phase2”的门已经关闭。

分发前又做了一次七字段返工风险审计。结果不是协议有错，而是 V3 的 Evidence 入口和真人说明仍可能造成重复理解成本。
因此新建 V3.2：Candidate 同行直接显示 E1/E2 标题和完整官方 URL，live URL 是首选核验入口；`02_证据` 的 144/144
冻结正文继续作为稳定备份。工作表不再加保护，真人可以调行高、列宽、缩放、换行和筛选。Guide V4 用十步流程、
九个完整例和十类常见错误解释七字段；规则、枚举、Candidate、ID、顺序、Evidence 和 Expected 均没有改变。

这一步只让 Phase2 具备受控分发条件，不代表 A/B 已一致。当前还没有计算 agreement、没有仲裁、没有 Ground Truth，
也没有启动 240-group、Dataset freeze、Detector、Training、5090、Formal Experiment 或 Paper Result。下一步仅是 Owner
分别把 A/B 各自的四份 Phase2 V3.2 文件交给本人，并继续保持两人隔离。

## Human-readable Research Plan & Experiment Ledger

Document Role = `PAPER1_PRIMARY_HUMAN_ENTRY`<br>
Audience = `项目负责人 / 导师与领导 / 新团队成员`<br>
Reading Path = `5 minutes / 15 minutes / 30 minutes`<br>
Current Evidence Cut = `Retrieval harness complete / two-stage boundary frozen / deployability audited`<br>
Last Updated = `2026-09-16`

> 这是一张“项目地图”，不是 raw evidence，也不产生新授权。读完第 0 节可掌握当前状态；读到第 8 节可理解论文方法；
> 读完第 19 节可进入项目工作。精确状态、协议、决定和证据分别通过链接下钻。

## 0. 先看这里：5 分钟了解 Paper 1

| 问题 | 当前回答 |
| --- | --- |
| 中文论文题目 | 《面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法》 |
| 英文论文题目 | *Stealthy Factual Poisoning in Versioned RAG Knowledge Bases: A Benchmark and Multi-View Detection Framework* |
| 一句话研究问题 | 在版本、时间和来源关系复杂的中文知识库里，如何识别“语言自然、检索相关、事实却被悄悄改变”的内容，同时不误伤合法旧版本和正常更新？ |
| 一句话核心方法 | 构建 Clean–Poison–Hard Negative 匹配数据，用 Semantic、Entity-Claim、Provenance、Temporal-Version、Retrieval-Behavior 五类互补证据估计风险，再做可校准的过滤或降权。 |
| 当前阶段 | ✅ Retrieval harness 已完成；Document Risk 与 Retrieval Exposure 已分层。 |
| 当前任务 | `P1-RETRIEVAL-BEHAVIOR-HARNESS-AND-DEPLOYABLE-SIGNAL-BOUNDARY-01`：检索运行与输入威胁模型收口。 |
| 当前完成度 | ✅ 24 queries、72 corpus、Sparse+Dense 双运行、8448-row R matrix、42-signal audit 完成。 |
| 当前唯一人工动作 | Owner 决定是否批准 Trusted Evidence Retriever + Version Registry prototype；不自动训练 Detector。 |
| 当前主要 blocker | 29 signals 仍是 matched-Evidence oracle；7 个 R signals 缺 Trusted Version Registry。 |
| 已经可以说什么 | R 的 rank/score/stability 工具链可复现；Retrieval Risk 已具备受限工程入口。 |
| 绝对不能说什么 | 不得称为 Detector 结果、正式 test 结果、superiority、generalization 或有效防御。 |

当前实验状态固定为：

当前状态枚举如下；它只说明已经批准和仍在等待的边界：
`PILOT4_FINAL72_GT_ACCEPTED / RETRIEVAL_HARNESS_COMPLETE / DOCUMENT_DETECTOR_NOT_READY /
RETRIEVAL_RISK_READY_WITH_LIMITATIONS / NO_DETECTOR_TRAINING / NO_FORMAL_RESULT / AUTO_CONTINUE_NO`

保留的历史状态链含 `PREANNOTATION_ONLY`：`PILOT4_BALANCED_SET_REPAIRED / READY_FOR_SECOND_OWNER_PREFLIGHT` →
`PILOT4_FINAL_PREANNOTATION_READY_FOR_OWNER_REVIEW` → `PILOT4_QUALITY_CONVERGED` → Schema V3.1 hardening → 当前外部盲审包状态。历史 package 不被覆盖。

状态的动态权威入口是 [Current Work State](../../../governance/current_work_state.md)。

历史协议框架事实：`S6.1-P1-R1 = HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`；该接受不等于数值协议、Dataset 或正式实验冻结。

## 1. 项目背景：我们到底在研究什么

RAG（Retrieval-Augmented Generation，检索增强生成）先从知识库找文档，再让生成模型依据这些文档回答。它比只依赖模型
参数更容易更新和审计，但也把安全边界扩展到“谁能写入、替换或伪装知识库内容”。

知识污染（knowledge poisoning）是把错误或恶意内容放进知识库，使它被检索并影响回答。隐蔽知识污染（stealthy
knowledge poisoning）更难：文本语法自然、主题相关、与 query 很相似，错误藏在数值、适用条件、版本时间或来源权威中。

版本化知识库尤其困难，因为“与当前事实不同”不等于“恶意”。旧政策、合法修订、尚未生效条款、地区差异和例外条件
都可能是真实文档。若 Detector 只看语义，它可能把这些内容误判为污染。因此 Paper 1 不只需要 Poison，还必须设计
Hard Negative（困难负例）：表面像污染、实际合法，用来测量误伤。

简化例子：

| 类型 | 候选文本 | 解释 |
| --- | --- | --- |
| Clean | “修订后的职业教育法自 2022 年 5 月 1 日起施行。” | 与当前权威版本一致。 |
| Poison | “修订后的职业教育法自 2022 年 6 月 1 日起施行。” | 语言自然但改变了关键生效日期。 |
| Hard Negative | “原职业教育法自 1996 年 9 月 1 日起施行，后被修订文本替代。” | 描述历史版本，日期不同但不是污染。 |

核心难题不是“找出所有不同”，而是“用版本、时间、来源和检索行为证据区分恶意事实改变与合法差异”。

### 为什么这次不再重跑 Full72

Pilot4 的外部复核已经证明 72 条候选在 Phase1 没有候选缺陷；Phase2 也不是全面失控，而是绝大多数字段稳定，分歧主要
聚集在“一个正确命题只是提到历史日期，还是必须依赖历史/版本限定才成立”这个字段边界。此前还发现少量 Expected 字段
和 Evidence Pool 设计问题。把这种局部测量工具问题写成“实验失败”不准确，再让 reviewer 重做全部 72 条也会浪费人工。

本轮因此采用更窄但更严格的方法：先把边界、Expected 和 Evidence 逐项修复并保留全部旧版本，再把 21 条真正受影响样本
与 16 条在领域、候选类型、HKP、隐蔽等级和命题结构上匹配的控制样本混合，交给全新的隔离 reviewer。Reviewer 不知道
哪些被修、哪些是控制，也看不到旧 ID、sample ID、mapping、expected 或 mismatch 分类。这样能直接回答“新规则是否更清楚，
同时有没有把原本稳定的判断弄坏”。现在这 37 条已经返回并完成锁定：M4/BR18 与 M8 通过，但 controls overall 只有
13/16。逐项审计显示，主要原因是 Expected V2 仍把若干当前有效更新过度标成“合法历史”，而不是 reviewer 或 Evidence
Pool 全面失效。因此下一步是一次追加式 Expected V3 处置和同 raw 重算，不是继续要求 reviewer 反复标注；协议和 A/B
仍须后续独立批准。

Expected V3 已把上述审计发现变成 7 个追加式字段更正，但没有覆盖 Expected V2，也没有改 reviewer raw。为避免“看答案改
答案”，本机先只读取候选、Guide 和冻结 E1/E2，生成并哈希锁定 Expected V3，之后才加载 reviewer value 做重算。结果把
M2 从 3/16 降到 2/16、控制组 overall 从 13/16 提到 16/16、exact relevant fields 从 29/37 提到 35/37；剩余两条均为
非系统性 reviewer variance。所有冻结门通过后，Owner 正式选择 `ACCEPTED_WITH_NONBLOCKING_NOTES`，关闭校准并确认不需要
R4。现在不再反复做校准标注；下一道门是独立审批正式 A/B 执行，而不是自动发放标注材料。

### Pilot4 最终留下了什么

Pilot4 先暴露了候选自包含性、sample-ID 泄漏、Phase1/Phase2 同上下文、Evidence 重复与 Expected 边界等问题；其根因分别
落在候选设计、盲法隔离、证据传输和控制面标签合同，而不是简单的“reviewer 填错”。最终规则是：候选先过盲法质量门；
Phase1 与 Phase2 结构分离；raw return 先锁定再加载 mapping/Expected；每个证据槽保留冻结官方快照与 URL provenance；
Expected 不是自动真值；自然度只作 QC、evidence selection 只作过程描述；A/B 必须独立，分歧由 Owner 定向仲裁。共 13 条
有证据支持的 lesson 已提升为 accepted，正式 A/B 重复性、Final72 Ground Truth、正式 Dataset/split 和规模化统计仍保持
provisional，必须由后续真实执行证据决定。

## 2. 专业术语中英文速查

| 术语 | 中文速解 |
| --- | --- |
| RAG | Retrieval-Augmented Generation；先检索知识，再基于检索内容生成回答。 |
| Benchmark | 基准数据与评估协议；不只是一个文件，还包括切分、标签、指标和可复现合同。 |
| Ground Truth | 经冻结流程确认的参考真值；Pilot-only 真值不等于正式 Benchmark 真值。 |
| Clean | 与权威事实、适用范围和版本状态一致的候选。 |
| Poison | 保持自然和相关性、但实质改变事实状态的候选。 |
| Hard Negative | 看起来可疑但实际合法的困难负例，用于测量误报。 |
| Matched Triplet | 同一事实主体下匹配的 Clean、Poison、Hard Negative 三元组。 |
| Version Chain | 同一主张的前版、现版、修订、废止或替代关系链。 |
| Provenance | 内容来自哪里、如何获取、如何派生的来源链。 |
| Authority | 发布主体的权威身份、层级、管辖范围及其是否支持该命题。 |
| HKP | Hidden Knowledge Poisoning；本项目的四类隐蔽知识污染变异。 |
| Stealth | 隐蔽性；错误需要多大证据成本才能被发现。 |
| S1 / S2 / S3 | S1 本文即可发现；S2 一个直接官方证据可确认；S3 需要跨版本/来源的联合证据链。 |
| Semantic View | 语义视角；观察 query 与候选是否相关、表达是否异常。 |
| Entity-Claim View | 实体—主张视角；观察主体、属性、数值、条件等关系。 |
| Provenance View | 来源视角；观察发布者、引用链和权威匹配。 |
| Temporal-Version View | 时间—版本视角；观察生效、失效、修订、替代与版本顺序。 |
| Retrieval-Behavior View | 检索行为视角；观察排名、邻域和扰动下的检索稳定性。 |
| Signal | 某一视角输出的结构化诊断证据或分数，不等于最终预测。 |
| Detector | 将允许的多视角输入融合成污染判断或风险分数的检测器。 |
| Risk Score | 候选为污染的风险估计，需经过校准才能用于阈值决策。 |
| Calibration | 让预测分数与实际风险概率/阈值行为相符。 |
| FPR | False Positive Rate；把真实非污染误报为污染的比例。 |
| Recall | 在真实污染中成功检出的比例。 |
| Precision | 被判为污染的样本中真正是污染的比例。 |
| AUROC | 不同阈值下真阳性率与假阳性率权衡的面积；类别极不平衡时需结合 AUPRC。 |
| AUPRC | Precision–Recall 曲线面积；更直接反映低污染率下的检出质量。 |
| Poisoned@K | Top-K 中污染文档的暴露数量或比例，越低越好。 |
| Recall@K | Top-K 是否保留相关正常文档，越高越好。 |
| MRR | Mean Reciprocal Rank；首个相关结果排名的倒数均值。 |
| nDCG | Normalized Discounted Cumulative Gain；考虑相关性等级和位置的排序质量。 |
| Ablation | 消融实验；删除一个视角或训练设计，测量其独立贡献。 |
| Generalization | 泛化；在未见攻击、领域、版本模式或来源上的表现。 |
| Adaptive Attack | 知道防御规则后主动规避检测的攻击。 |
| Hard Filtering | 风险超过阈值时直接从候选集合移除。 |
| Soft Downweighting | 不直接删除，而按风险降低检索分数。 |
| Dataset Freeze | 数据身份、标签、切分、许可与 hash 被正式锁定，之后不能任意调整。 |
| Formal Experiment | 在冻结协议、数据、代码、参数和统计计划下执行的正式实验。 |

## 3. Paper 1 最终要证明什么

以下是科研证据链，不是已完成结论。`PILOT_SUPPORTED` 只表示 Pilot 提供了可行性或失败模式证据。

| # | 最终主张 | 当前证据状态 | 当前解释 |
| --- | --- | --- | --- |
| 1 | 中文版本化 RAG 存在难被简单语义相似度识别的隐蔽事实污染。 | `PILOT_SUPPORTED` | Pilot3 显示语义/时间诊断信号很弱，支持“问题值得研究”，不构成总体性能结论。 |
| 2 | 可构建含 Clean、Poison、Hard Negative、版本链、权威关系和 S1–S3 的中文 Benchmark。 | `PILOT_SUPPORTED` | Pilot1–4 支持来源、标注和构造可行性；Formal Benchmark 尚未冻结。 |
| 3 | Semantic-only 不足，且容易把合法历史版本误判为污染。 | `PILOT_SUPPORTED` | Pilot3 暴露 HN 误报与弱语义信号；尚无正式对照统计。 |
| 4 | Entity-Claim、Provenance、Temporal-Version、Retrieval-Behavior 提供互补证据。 | `PILOT_SUPPORTED` | 五视角信号可运行，结构化 Temporal/Provenance prototype 已实现；互补收益尚未正式建立。 |
| 5 | Multi-view 方法更可靠地区分真实污染与合法版本差异。 | `NOT YET ESTABLISHED` | Formal Detector 未实现，组合矩阵和正式 test 尚未冻结。 |
| 6 | calibrated risk 的过滤/降权降低污染暴露并保持正常检索效用。 | `NOT YET ESTABLISHED` | Option B 合同与工程 primitive 存在，但 effectiveness 未建立。 |

目前没有任何一项处于 `FORMALLY ESTABLISHED`。正式建立必须满足第 18 节的全部条件。

## 4. Benchmark 总体设计

### 4.1 正式五领域

`PAPER1_FORMAL_DOMAIN_SET = OWNER_CONFIRMED`

| ID | 中文领域 | English |
| --- | --- | --- |
| D1 | 企业人力资源 | Enterprise Human Resources / Enterprise HR |
| D2 | 财务 | Finance |
| D3 | 信息安全 | Information Security |
| D4 | 采购与研发 | Procurement and R&D |
| D5 | 教育与科研 | Education and Research |

这五个领域只用于未来 Scale Pilot / Formal Benchmark 规划。Pilot4 实际覆盖四领域，这是不可回写的历史事实。

### 4.2 HKP 与隐蔽等级

| 类型 | 含义 |
| --- | --- |
| HKP1 | 数值或实体被改变。 |
| HKP2 | 适用条件、例外或否定关系被改变。 |
| HKP3 | 生效、失效、废止、替代或版本顺序被改变。 |
| HKP4 | 来源、权威层级、机构归属或引用关系被伪装。 |

- S1：候选自身、内部矛盾、明显时间逻辑或普通常识即可发现事实错误。
- S2：候选本身自然，但一个直接官方来源或同一文件的直接上下文即可确认错误；“打开一个官方页面”不等于跨文档。
- S3：必须依赖多个版本、文档、来源、时间演化、authority chain 或 provenance chain 联合确认。
- 正确候选不评价 S1/S2/S3，而是 `NOT_APPLICABLE`；证据不足时为 `UNCERTAIN`。

### 4.3 Scale Pilot 结构

`5 Domains × 4 HKP × 3 Stealth × 4 Independent Chains = 240 independent groups`

- ✅ `STRUCTURE CONFIRMED`
- 📌 `EXECUTION NOT STARTED`
- 📌 `FORMAL DATASET NOT FROZEN`

若每组生成 Clean + Poison + matched Hard Negative，则约为 `240 × 3 = 720 candidate records`。这个 720 是
`PLANNED DERIVED SIZE / NOT FROZEN / NOT GENERATED`，不是当前数据事实。

## 5. Clean / Poison / Hard Negative

Clean 是正确对照，Poison 是实质事实被改变的攻击候选，Hard Negative 是“像污染但合法”的压力测试。三者应在同一主体、
主张、长度和检索相关度上尽量匹配，避免模型靠格式或主题捷径分类。

Hard Negative 是 Paper 1 的核心，因为真实版本库里最危险的错误不是漏掉明显 Poison，而是把历史、修订、例外或转载
全部删除。关键子类包括：

- `legitimate historical version`：合法历史版本；
- `legitimate update`：合法更新；
- `legitimate exception`：合法例外；
- `scope difference`：地区、部门、对象或条件范围不同；
- `authority repost`：权威来源的合法转载或转发；
- `near-miss-but-true`：表达极像错误，但细节仍为真。

因此 Hard Negative FPR 既是数据质量指标，也是方法是否可部署的关键指标。

## 6. 五视角方法

| View | 中文名称 | 输入 | 主要看什么 | 主要覆盖 | 可能失败 | 当前实现状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Semantic | 语义视角 | query、候选文本、允许的语义特征 | 相关性、局部异常、语义偏移 | 全部 HKP 的表层信号 | 自然改写、合法旧版与污染都可能很相似 | `METHOD CONTRACT ACCEPTED`; `DIAGNOSTIC PROTOTYPE`; 非 Formal Detector |
| Entity-Claim | 实体—主张视角 | 主体、谓词、对象、数值、条件 | 哪个事实槽位发生变化 | HKP1、HKP2 | claim extraction 错误、隐含主体 | `METHOD CONTRACT ACCEPTED`; Pilot3 diagnostic |
| Provenance | 来源视角 | source、issuer、authority、引用关系 | 谁发布、是否匹配命题、来源链是否可信 | HKP4 | 来源信息缺失；Pilot3 中 35/36 为 N/A | `STRUCTURED PROTOTYPE IMPLEMENTED`; engineering only |
| Temporal-Version | 时间—版本视角 | 生效/失效时间、版本关系链 | 旧版、现版、修订与合法历史 | HKP3、部分 HKP2 | 版本链缺失或事实映射不完整 | `STRUCTURED PROTOTYPE IMPLEMENTED`; Pilot3 Temporal AUROC 0.465，仅诊断 |
| Retrieval-Behavior | 检索行为视角 | rank、score、邻域、冻结扰动 | 候选在 Top-K 和邻域中是否异常 | 全部 HKP 的运行时表现 | query 敏感、计算成本、分布漂移 | `METHOD CONTRACT ACCEPTED`; diagnostic primitive |

必须区分三层：

1. `METHOD CONTRACT`：五视角的允许输入、输出和边界已经作为 P1-R1 框架接受；
2. `DIAGNOSTIC PROTOTYPE`：Pilot3/Pilot4 已验证信号接口和部分结构化实现能运行，并暴露失败模式；
3. `FORMAL DETECTOR`：尚未实现，也没有建立 detection effectiveness。

详细方法合同见 [P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 7. 多视角组合、消融和泛化

Single View 包括 S / E / P / T / R；Multi-view 可包含 S+E、S+T、E+P+T 和 All-5。组合必须在 formal protocol freeze
前确定，不能查看 test 结果后挑最好组合。

计划消融：minus Semantic、minus Entity、minus Provenance、minus Temporal、minus Retrieval，以及 without Hard Negative
training/calibration。消融回答“哪个组件真正贡献了性能”，也必须如实报告负贡献。

Track C 泛化计划：unseen HKP、unseen domain、unseen version family/pattern、cross-source transfer 和 adaptive attack。
这些都属于 `EXPERIMENTAL PLAN / NOT EXECUTED`。统计比较族、split 和阈值规则见
[P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 8. Option B：轻量解毒

```text
Retriever
  -> Top-K
  -> Five-view Detector
  -> calibrated Risk Score
  -> Hard Filtering / Soft Downweighting
  -> New Top-K
```

- Hard Filtering：若 `risk >= tau`，则移除候选。
- Soft Downweighting：`adjusted retrieval score = retrieval score - lambda × risk`。

安全端要看 `Poisoned@K ↓`；效用端要看 `Recall@K / MRR / nDCG` 尽量保持。二者是分开的共同主结果，不能用一个综合
分数掩盖“安全提高但检索失效”。当前仅能说合同和工程 primitive 存在；Option B effectiveness 为
`NOT ESTABLISHED`，也不包含 trusted context package、完整可信上下文构造或端到端 Agent 防御。

## 9. 从开始到投稿：完整实验路线图

| 阶段 | 为什么做 | 主要工作 | 输入 | 输出 | 当前状态 | 结束条件 | 下一 Gate | 详细链接 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S6.1-LR1 | 选清研究路线 | 外部工作与 Paper1 对齐 | 论文/仓库 | 路线与角色 | ✅ 已验收 | Owner 接受 | R0 | [LR1](../stage_process/S6.1-LR1_work_process.md) |
| S6.1-R0 | 先查能否复现 | 代码/环境/工件预检 | 外部 baseline | 工程证据与 blocker | ✅ 带边界验收 | 证据可恢复 | FU1 | [R0](../stage_process/S6.1-R0_work_process.md) |
| S6.1-R0-FU1 | 关闭关键工程门 | 来源、bundle、5090 smoke | 冻结合同 | 单样本工程可行性 | ✅ 已关闭 | Owner 验收 | P1-R1 | [FU1](../stage_process/S6.1-R0-FU1_work_process.md) |
| S6.1-P1-R1 | 把想法变协议 | RQ、数据、方法、统计、Option B | LR1/R0/FU1 | 接受的框架 | ✅ 框架已接受 | 数值参数待 Pilot 冻结 | Pilot | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Pilot0 | 工程合同能否运行 | schema、split、泄漏 guard | synthetic fixture | 工程基础设施 | ✅ 已关闭 | 测试与 Owner 验收 | Pilot1 | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot1 | 真实中文来源能否构建 | 版本链、公开来源、候选包 | 官方公开文档 | 36 条候选与包 | ✅ 已关闭 | 来源/包可行 | Pilot2 | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot2 | 人能否可靠标注 | A/B、V2、agreement、owner 仲裁 | 36 条候选 | 36 条 Pilot-only GT | ✅ 可行性关闭 | GT/协议可唯一生成 | Pilot3 | [Pilot2 closure](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| Pilot3 | 信号能否运行 | 五视角 180 条 SignalRecord | Pilot2 GT | 弱信号/失败模式 | 🧪 已完成并停止 | 诊断报告 | Pilot4 | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| Pilot4 first preflight | 人工发放前低成本检查 | 24 triplets/72 candidates/12-row sample | lessons + public sources | 首版 package | 📌 历史：退回修复 | Owner 指出缺陷 | targeted repair | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot4 targeted repair | 修复实质缺陷 | 语义、stealth、echo、applicability、独立 QA | 首版与 owner feedback | repaired 72 + second sample | 🔧 已完成 | 修复验证通过 | second preflight | [Current State](../../../governance/current_work_state.md) |
| Pilot4 second Owner preflight | 决定能否发人 | Owner 审查 repaired 12 rows | repaired workbook | targeted repair | 📌 历史：已触发 Repair-02 | Owner 明确决定 | Repair-02 | [Current State](../../../governance/current_work_state.md) |
| Pilot4 Repair-02 final preflight | 关闭第二轮系统性缺陷 | Owner 审查 final 16 rows | genuine-S3/S1/length/template/HN evidence | quality convergence | 📌 历史：已进入后续收敛 | Owner 明确决定 | Schema V3/V3.1 | [Current State](../../../governance/current_work_state.md) |
| Pilot4 Protocol hardening | 排除标签感知循环验证与候选核验路径泄漏 | locked Full72、candidate before/after、V3.1 三表 | b705cc + additive candidate version | 外部两阶段盲审路径 | 📌 历史：已进入外部盲审 | 阶段隔离完成 | Phase1 外部复核 | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot4 external Phase1 return | 锁定陌生复核者的第一阶段原始判断并拦截候选缺陷 | 原始 CSV、公开 Phase1 ID 集 | immutable return + 5-row blind triage | 项目负责人盲态处置 | ✅ 历史门已关闭 | fresh Attempt2 72/72 无候选缺陷 | Phase2 已完成 | [Current State](../../../governance/current_work_state.md) |
| Pilot4 targeted R3 | 检查局部协议修复及匹配控制 | 37 行外部 return、Guide V3.2、Expected/Evidence V2 | immutable raw + gate assessment | Expected V2 定向修正决定 | ⚠️ 当前 Owner 门 | 7-field/6-candidate additive decision | 同 raw 重算 gate | [Current State](../../../governance/current_work_state.md) |
| Pilot4 A/B 72 annotation | 获得独立人工判断 | Phase1/2、双锁定 | Owner-accepted package | 四份 returns | 📌 未批准/未开始 | returns hash-lock | agreement | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot4 agreement | 量化一致性 | 合法子集 agreement | A/B returns | agreement/disagreement | 📌 未开始 | 逻辑/一致性验证 | adjudication | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot4 adjudication | 解决必要分歧 | Owner 只裁决分歧 | minimal packet | 唯一决定 | 📌 未开始 | residual inconsistency=0 | GT | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot4 72 Ground Truth | 形成小规模参考真值 | 确定性合并与 QA | validated returns/owner decisions | 72 Pilot GT | 📌 未开始 | identity/logic/leakage PASS | re-evaluation | [Experiment Master](../../../governance/experiment_master_record.md) |
| Pilot4 signal re-evaluation | 验证修复方向 | 重新运行 diagnostic signals | 72 Pilot GT | failure-mode comparison | 📌 未开始 | 诊断可解释 | readiness | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Scale Readiness Gate | 防止盲目扩规模 | 六类 readiness 审计 | Pilot4 closure | PASS/blocked | 📌 未开始 | 六类门均 PASS | Owner scale approval | [第17节](#17-什么情况下才能进入-240-group) |
| 240-group Scale Pilot | 验证规模/方差 | 5×4×3×4 groups | approved design | scale pilot data | 📌 未批准/未生成 | coverage/quality PASS | power analysis | [Research Plan](research_plan_authority.md) |
| Power / Precision Analysis | 决定正式样本量 | CI/方差/稀有组精度 | scale pilot | frozen sample plan | 📌 未开始 | 统计精度达标 | formal freeze | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Formal Dataset / Protocol Freeze | 锁定身份与分析计划 | data/split/license/metrics/seeds | accepted scale evidence | frozen contract | 📌 未开始 | Owner 明确批准 | implementation | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Formal Detector Implementation | 实现最终模型 | 五视角融合与校准 | frozen train/dev | executable detector | 📌 未批准/未实现 | tests + frozen identity | evaluation | [Research Plan](research_plan_authority.md) |
| Formal Detector Evaluation | 测主性能 | locked test evaluation | frozen detector/data | primary metrics | 📌 未开始 | evidence complete | multi-view | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Multi-view Evaluation | 验证组合收益 | single/multi-view compare | same split/budget | paired results | 📌 未开始 | preregistered comparisons | ablation | [第7节](#7-多视角组合消融和泛化) |
| Ablation | 解释组件贡献 | leave-one-view-out 等 | full method | contribution evidence | 📌 未开始 | planned family complete | generalization | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Generalization | 测外推能力 | unseen domain/HKP/version/source | held-out families | generalization results | 📌 未开始 | frozen Track C complete | Option B | [第7节](#7-多视角组合消融和泛化) |
| Option B Detoxification | 测安全—效用权衡 | hard filter/soft downweight | calibrated risk | Poisoned@K + utility | 📌 未开始 | co-primary endpoints | paper evaluation | [第8节](#8-option-b轻量解毒) |
| Paper Evaluation | 汇总证据 | 统计、失败、威胁、复现包 | formal runs | tables/figures | 📌 未开始 | claims audit PASS | writing | [第18节](#18-什么情况下才能称为正式论文结果) |
| Paper Writing | 形成论文 | 方法、结果、局限、工件 | accepted formal evidence | manuscript | 📌 未开始 | Owner/导师审查 | submission | [README](../README.md) |

## 10. Pilot0–Pilot4：为什么每一步都需要

### Pilot0：工程合同可不可运行？

Pilot0 用 synthetic fixture 验证 schema、分组切分、泄漏 guard、攻击/Hard Negative 接口和 manifest 是否可执行。它避免在
真实数据上才发现基础设施错误。结论仅是工程基础设施可行。

### Pilot1：真实公开中文版本来源能不能构建？

Pilot1 审计公开中文版本链、来源许可边界和候选构造，形成 36 条非正式候选。它证明公开来源到盲化包的工程可行性，
不证明 Benchmark 已完成。

### Pilot2：人能不能可靠标注并形成 Ground Truth？

Pilot2 经历 schema 适用性、编码、旧值映射、独立复核和 owner 一致性门，最终形成 36 条 Pilot-only Ground Truth。它证明
标注协议与 GT 生成流程可行，也留下了不可回写的失败证据。

### Pilot3：五视角信号是否能运行、失败模式是什么？

Pilot3 在 36 条 Pilot-only GT 上生成 180 条 SignalRecord。它发现类别失衡、S1/S3 collapse、Provenance 35/36 N/A、
Temporal AUROC 0.465 和 Hard Negative 误报等问题。它是 diagnostic smoke，不是 Detector 性能实验。

### Pilot4：扩 240-group 前最后一次小规模校准

Pilot4 把 Pilot1–3 的教训前移到人工发放前：先设计 coverage 和 field schema，再构造并独立验证 24 matched triplets、
72 条平衡候选。首轮 preflight 被退回后只做 targeted repair。当前 repaired 72 仍是 preannotation candidates。

四个规模不能混淆：`36 records = development/diagnostic evidence`；`72 repaired candidates = balanced Pilot/preannotation
candidates`；`240 groups = future Scale Pilot`；`Formal Dataset = 未来经正式 freeze 的数据`。

## 11. 数据标注流程

```text
Candidate Generation
  -> Machine QA
  -> Owner Preflight
  -> A/B Phase1
  -> hash lock both
  -> A/B Phase2
  -> hash lock both
  -> agreement
  -> disagreement-only packet
  -> Owner adjudication
  -> Ground Truth
```

Phase1 评估候选自身可见的自然度、相关性、局部可检测性和隐蔽等级，不提前看到 Phase2 的官方事实材料。Phase2 用官方
来源和版本背景判断事实、版本、历史/更新和权威命题。盲法防止后一阶段答案反向污染第一阶段难度判断；A/B 独立可测量
协议是否清晰。

Owner 只在双方结果锁定后裁决必要分歧。Owner 的目的不是“提高 kappa”，而是形成可审计的唯一最终决定；agreement 必须
保留标注人真实差异。完整规则见
[标注教训与未来数据规则](annotation_lessons_learned_and_future_dataset_rules.md)。

## 12. 数据构造永久规则

- `subject uniqueness = 100%`：法律、政策、制度和标准主体必须可唯一识别。
- 候选与 query 必须 self-contained；不能依赖“该条例”“2017 年版”等隐含上下文。
- coverage before generation：先冻结覆盖矩阵，再生成文本。
- mutation semantic alignment：attack metadata 必须与实际事实变异一致。
- stealth evidence path：S1/S2/S3 必须来自发现错误所需证据路径。
- no evidence echo：候选不能回显标准答案或证据措辞。
- no experimental meta-language：候选不能出现“本样本”“对照组”等实验语言。
- applicability 必须 claim-derived，不能由生成器意图直接声明。
- `Generator != Validator`：构造者声明 PASS 不等于独立验证。
- G1–G14 全部门禁必须对序列化产物重新计算。
- independent Round D 必须从 source fact 反向核验。
- semantic near-duplicate 必须区分 triplet 内匹配与跨独立组泄漏。
- label isolation：Ground Truth/attack ID 不得进入 retriever 或 inference feature。
- raw return immutable：人工原始 return 不回写；纠正必须追加绑定。

唯一完整规则见 [canonical lessons](annotation_lessons_learned_and_future_dataset_rules.md)。

## 13. 已发生 Blocker 时间线

| 日期 | 阶段 | Blocker | 问题是什么 / 为什么重要 | 解决方案 | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-31 | R0 | evidence mismatch | 首次 Worker evidence 与声明不匹配，无法复核 | corrected evidence + 本机 control-plane review | ✅ RESOLVED | [R0 process](../stage_process/S6.1-R0_work_process.md) |
| 2026-08-01 | W2 | model download/evidence blockers | 模型下载失败、磁盘命令来源不完整 | additive correction、offline bundle、H2 resume02 | ✅ `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED`（仅工程门） | [FU1 process](../stage_process/S6.1-R0-FU1_work_process.md) |
| 2026-08-27 | Pilot2 | distribution metadata issue | 登记时间错误曾导出盲法污染推断 | 保留原记录，追加 owner-confirmed actual order | ✅ RESOLVED / 元数据历史保留 | [Owner correction](../s6_1_p1_pilot2_return_owner_correction.md) |
| 2026-08-27 | Pilot2 | Schema V1 ambiguity | YES/NO/UNCERTAIN、适用性和 authority 命题歧义 | Schema V2 + 独立复核 | ✅ RESOLVED | [Schema V2](../s6_1_p1_pilot2_annotation_v2.md) |
| 2026-08-27 | Pilot2 | NOT_APPLICABLE 缺失 | 正确或不适用命题被迫填错误枚举 | present/correctness dependency | ✅ RESOLVED | [Schema V2](../s6_1_p1_pilot2_annotation_v2.md) |
| 2026-08-27 | Pilot2 | encoding/header/process metadata | GB18030、列名和过程字段影响导入 | UTF-8 BOM 合同与缺陷显式保留 | ✅ RESOLVED | [Targeted review](../s6_1_p1_pilot2_targeted_rereview.md) |
| 2026-08-28 | Pilot2 | V1 mapping defect | 带中文后缀列未识别，旧值被伪装成 absent | allowlisted alias + fail closed | ✅ RESOLVED | [Targeted review](../s6_1_p1_pilot2_targeted_rereview.md) |
| 2026-08-28 | Future data | candidate subject ambiguity | 裸指代使样本缺上下文 | `BROKEN_CANDIDATE / MISSING_CONTEXT` 门 | ✅ RESOLVED AS PERMANENT RULE | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-08-31 | Pilot2 | agreement disagreements | 47 条 A/B 分歧 + 37 条内部逻辑冲突 | disagreement-only owner packet | ✅ RESOLVED | [Post annotation](../s6_1_p1_pilot2_post_annotation.md) |
| 2026-08-31 | Pilot2 | owner consistency blocker | 4 个候选有非法枚举/同字段冲突 | 独立 owner correction record | ✅ RESOLVED | [Closure](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | class imbalance | Clean 仅 1 条，无法支持正式估计 | Pilot4 平衡为 24/24/24 intent | ✅ RESOLVED FOR PILOT4 DESIGN | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | S1/S3 collapse | 隐蔽等级证据路径不充分 | Pilot4 evidence-path stealth contract | ✅ RESOLVED FOR GENERATION | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-08-31 | Pilot3 | Provenance 35/36 N/A | 来源命题覆盖不足，视角不可估 | Pilot4 claim-derived applicability/coverage | 🔧 ENGINEERING REPAIR; formal effect open | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | Temporal AUROC weak | 诊断 AUROC 0.465 | structured temporal/version repair | 🔧 PROTOTYPE REPAIRED; effectiveness open | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | HN FP | 合法版本差异产生误报 | 六类 HN 与结构化调整 | 🔧 DESIGN REPAIRED; formal effect open | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-09-01 | Pilot4 | attack metadata misalignment | metadata 与实际变异可能不一致 | mutation-semantic contract + rejection | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | stealth index assignment | S 值由目标格赋值而非证据路径推导 | evidence-path derivation | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | evidence echo | LONG 候选回显答案/证据 | natural rendering + echo blocker | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | experimental meta-language | 文本含实验描述，形成捷径 | meta-language rejection | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | applicability metadata | 适用性由 metadata 意图而非 claim 推导 | claim-derived applicability | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | builder-declared PASS | 构造器自报通过，未验证序列化产物 | independent G1–G14 + Round D | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | HN evidence weakness | 困难负例证据链过弱 | source-fact reverse check | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | Repair-01 acceptance | 第二次预审发现 S3 necessity、S1 cue、实际长度、模板与 HN 语义问题 | Repair-02 | ✅ SUPERSEDED BY FINAL REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | final preannotation acceptance | Repair-02 工程门完成但尚无人工作出接受决定 | quality convergence | ✅ SUPERSEDED BY FULL QUALITY GATES | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | source/schema/visibility convergence | Phase1 hint、人工跨文档、伪来源核验、HN 支持与字段可操作性存在系统性风险 | actual-source verification + Schema V3 + full72 + dry-run | ⏳ READY FOR OWNER ACCEPTANCE REVIEW | [Current State](../../../governance/current_work_state.md) |
| 2026-09-01 | Pilot4 | duplicate visible evidence slots | 55/72 candidates、23 triplets 的 E1/E2 指向同一 visible official URL | 23 verified companion sources + distinct URL/hash/document identity + A/B independent order + Schema V3.1 | ✅ RESOLVED / OWNER ACCEPTANCE PENDING | [Current State](../../../governance/current_work_state.md) |
| 2026-09-02 | Pilot4 | sample-ID leakage | 早期 Full72 reviewer 可用 `sample_id` 查询隐藏标签集合，脱敏输入不等于真实标签盲法 | 旧结果追加重分类为 contaminated evidence；使用一次性 opaque ID、隔离 mapping 与外部复核路径 | ✅ ENGINEERING REPAIR / FINAL OWNER ACCEPTANCE PENDING | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-02 | Pilot4 | combined Phase1/Phase2 packet flaw | 第一阶段候选与第二阶段证据同时进入一个 LLM 上下文，“先别看 Evidence”不能保证严格盲法 | 保留 combined packet 历史；重建 candidate-only Phase1、withheld Phase2 与 return hash-lock 释放门 | ✅ PHASE-SEPARATION REPAIR / EXTERNAL PHASE1 RETURN PENDING | [Current State](../../../governance/current_work_state.md) |
| 2026-09-02 | Paper 1 governance | documentation closeout gap | 代码、测试或 push 完成后，人类总账和控制面文档仍可能停留在旧任务 | 每项 Paper 1 任务强制执行文档收口清单和跨文档陈旧状态门 | ✅ POLICY ACTIVE | [Closeout contract](../documentation_separation_contract.md) |
| 2026-09-02 | Pilot4 | external Phase1 candidate defects | 外部 blind reviewer 在 Attempt1 的 72 行返回中标记 5 条候选缺上下文、指代模糊或其他局部问题；在处置前释放证据可能把候选缺陷带入 Phase2 | 原始 return 不回写；blind-ID triage、Owner 五项处置、局部修复与 fresh Full72 Attempt2 | ✅ `RESOLVED BY FRESH ATTEMPT2 ZERO-DEFECT RETURN` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-02 | Pilot4 | final-corpus blind review consistency | Owner 接受五项 reviewer issue；若只重标五条并与旧 67 条拼接，会混合不同 corpus/reviewer 的证据 | 五条 source-backed 局部修复；67 条不变；统一 final72 生成 72 个新 ID 与 fresh Full72 Attempt2；Attempt1 永久保留为 defect-discovery evidence | ✅ `ATTEMPT2 PHASE1 LOCKED / PHASE2 RELEASED` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-02 | Pilot4 | final Phase2 expected comparison | 首次返回有 23 条临时访问限制；retry 后全 0，但对比暴露 16 条 primary status 边界、expected/minimum-evidence 问题与一条缺失版本证据 | 两份 raw 分别锁定；raw lock 后才解锁 mapping/expected；生成完整 mismatch taxonomy 和定向修复建议 | ⚠️ `OWNER PROTOCOL ACCEPTANCE PENDING / RECOMMEND TARGETED REPAIR` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | targeted R3 gate failure | R3 raw 37/37 完整，M4/M8 通过；M2 3/16、controls overall 13/16，且 7 个分歧字段由 Expected V2 缺陷解释 | 保留 R3 raw 与 Expected V2；只申请 additive Expected V3，批准后复用同一 raw 重算，不默认 R4 | ⚠️ `EXPECTED_V2_SYSTEMIC_REPAIR_BLOCKER / OWNER DECISION PENDING` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | Expected V3 gate closure | Owner 批准 7 字段/6 候选定向修正；V3 在 reviewer load 前由 Guide/Evidence 独立锁定；M2 2/16、controls 16/16、all exact 35/37、A–F PASS | 停止校准，不做 R4；提交 Owner Protocol Final Decision Packet，协议和 A/B 分开审批 | ✅ `CALIBRATION STOP MET / OWNER PROTOCOL DECISION PENDING` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | Owner protocol acceptance and A/B preflight | Owner 以 nonblocking notes 接受协议并关闭校准；Accepted Stack V1 固定 Final72、Guide V3.2、Expected V3、Evidence Pool V2 与冻结快照+URL provenance；2 条 variance 原样保留 | 提升 13 条证据支持的 lesson；重建 A/B 角色、盲法、双阶段锁定、agreement/Owner 仲裁边界并生成审批包；不发包 | ✅ `PROTOCOL ACCEPTED / A_B EXECUTION APPROVAL PENDING` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | A/B execution approval and Phase1 packets | Owner 指定 HUMAN-A01/HUMAN-B01 两个不同真人，确认完整隔离、互不看结果和禁用 LLM；批准完整 Final72 A/B execution 与 Phase1 分发 | 各自 72 新 ID/独立顺序，两个五文件 Phase1 包；Phase2 各 144/144 快照预构建但封存 | ✅ `A_B EXECUTION APPROVED / BOTH PHASE1 READY / WAITING OWNER DISTRIBUTION / PHASE2 WITHHELD` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | A/B human usability V2 | Owner 在实际发放前发现 V1“协议正确但不像给真人看的说明书”；本轮只补字段含义、枚举边界、decision flow、教学与完整填写例、reason 写法、CSV 操作和自检 | V1 不改且未分发；A/B Candidate/ID/顺序不变；三列 Packet 只读、五列 CSV 专门答题；Phase2 人类说明预构建但继续封存 | ✅ `RULE CHANGE 0 / BOTH PHASE1 V2 DISTRIBUTION READY / PHASE2 V2 WITHHELD` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-09 | Pilot4 | Phase2 human annotation rework risk control | 双 Phase1 已锁定、Phase2 获准释放后，Owner 在分发前要求确认七字段是否容易导致大规模返工；V3 的内部跳转、保护状态和说明密度不够适合真人连续填写 | 先做只读风险审计；不改协议，只把官方 URL 放到 Candidate 同行、保留冻结快照作备份、移除工作表保护并扩展 Guide V4 | ✅ `SEMANTIC BLOCKER FALSE / A_B V3.2 READY / WAITING OWNER DISTRIBUTION` | [Execution log](../../../governance/research_execution_log.md) |

## 14. 当前项目状态

- `PILOT4_AB_ALL_FOUR_RAWS_LOCKED / OWNER_ADJUDICATION_RETURN_RAW_LOCKED / OWNER_ADJUDICATION_CONSISTENCY_CLOSED / UNRESOLVED_CONSISTENCY_BLOCKER_0 / EXPECTED_V3_NOT_LOADED / NO_GROUND_TRUTH_YET / WAITING_FOR_OWNER_NEXT_APPROVAL`
- `PILOT_LEVEL_ANNOTATION_READINESS_ONLY`
- `PILOT4_A_B_EXECUTION_APPROVED / PILOT4_AB_DUAL_PHASE1_RAW_LOCKED / PHASE2_RELEASE_ALLOWED`
- 历史预检状态 `NO_HUMAN_DISTRIBUTION` 已被本轮 Owner 分发批准取代；它仅作为时间线事实保留，不能描述当前授权。
- `PILOT4_CANDIDATE_CORPUS_POST_EXTERNAL_PHASE1_REPAIR_V1` 已形成 72 条；仍非 Ground Truth、非 Formal Benchmark、非 frozen Dataset。
- class intent 为 Clean / Poison / Hard Negative = `24/24/24`。
- 生成覆盖为 `4 HKP × 3 intended-S × 2 replication = 24 poison cells`，对应 24 matched triplets。
- Attempt1 72-row 原始返回继续按 `5001 bytes` 与 SHA256 `59446c4b...889261` 完整保留；它是有效的缺陷发现证据，不是 final corpus acceptance review。
- Owner 接受五条 issue；五条局部修复的 semantic/source parity 均为 `5/5 PASS`，其余 67 条 candidate text 与源行 byte-identical。
- Attempt2 使用 72 个新 opaque ID，Attempt1 ID 复用为 0；canonical raw SHA256 为 `1e5e81fe...63c9c5`，schema/72 IDs/
  enums/7 reasons PASS；59 条 NATURAL、13 条 MINOR_ISSUE、7 条局部冲突，且 72/72 `phase1_issue=NONE`。六项 release
  fact 全部为 true。第一份 Phase2 raw 的 23 条 `SOURCE_UNREACHABLE` 作为过程证据保留；同一 reviewer retry 的 final raw
  将其降为 0，并以 `16321 bytes` / SHA `6f6cc042...92f1` 锁定。raw-lock-before-expected PASS；Phase1/Phase2 exact 分别
  `58/72` 与 `48/72`。43 个 mismatch 的 taxonomy 为 M1=13、M2=16、M4=3、M5=6、M8=4、M9=1。
- Targeted R3 raw 保持 `12062 bytes` / SHA `80a10a1e...0b4441`。Expected V3 先经 reviewer-blind 独立审计锁定，再加载 raw；
  只改 7 字段/6 候选。V3 overall `35/37`、version/authority/minimum/issue 各 `37/37`、exact `35/37`；M2 `2/16`、
  controls overall/exact `16/16`，M4/BR18 和 M8 4/4 通过，A–F 全部 PASS；只剩 2 条非系统性 reviewer variance。
- A/B Phase1 与 Phase2 已由两位真人独立完成并完成四 raw lock；dual Phase2 gate 后 mapping 已解锁并完成 agreement preflight；Expected V3 未加载。当前有 78 个 material field disagreements（40 samples）与五个 late-candidate-defect flags 待 Owner 裁决；72 Ground Truth 未建立；
  240-group 未开始；Dataset = `NOT FROZEN`（未冻结）。
- Formal Detector = `NOT IMPLEMENTED`（未实现）；Formal Experiment = `NOT STARTED`（未开始）；Our Method Result = `NONE`。

当前 Git 身份与远端同步状态必须动态核验；`a843697`、`cad3b2b2` 与 `871aecf` 均作为不可变历史身份保留。

## 15. 当前下一步

唯一当前动作：**Owner 决定是否批准 `P1-RETRIEVAL-BEHAVIOR-SIGNAL-HARNESS-01`。** 该任务应冻结合法 query、retriever、
corpus、top-k、score 和 repeated-run trace，再补齐 Retrieval View。当前也可以另行讨论四视角 prototype，但任何 Detector
training、threshold tuning、240-group 或正式结果都必须是独立审批，不能由本轮自动继续。

```text
Attempt1 (immutable defect-discovery evidence)
  └─ five Owner-accepted defects -> five repaired + 67 unchanged -> unified final72
       └─ fresh opaque IDs + fresh order -> Attempt2 Phase1 in new isolated reviewer context
            └─ immutable return + zero defects -> Candidate Quality Gate PASS -> same-reviewer Phase2
                 └─ Guide/Expected/Evidence targeted repair -> R3 locked and compared
                      └─ additive Expected V3 -> same-raw gates A-F PASS
                           └─ Owner accepted with nonblocking notes -> calibration closed
                                 └─ A/B approved + roster frozen + V1 preserved but human-usability superseded
                                      └─ V2 manuals/packets ready, Phase2 V2 withheld
                                           └─ dual Phase1 raw locked -> Phase2 V3.2 UX repaired without semantic changes
                                                └─ A/B complete -> Owner adjudication -> Final72 GT accepted
                                                     └─ label-blind 42-signal extraction -> raw lock -> analysis
                                                          └─ current: READY_WITH_VIEW_LIMITATIONS / Retrieval input gap

未来在独立审批下：
Retrieval harness -> optional first multiview detector prototype -> Scale Readiness -> Owner 单独批准 -> 240-group
```

## 16. 论文实验指标

### Detection

- AUPRC：在污染稀少、类别不平衡时，比总体 accuracy 或单独 AUROC 更直接反映“检出的污染有多少是真的”。
- AUROC：看全阈值排序能力，但必须与 prevalence、AUPRC 和低 FPR 指标一起解释。
- Recall@1% FPR：只允许 1% 正常样本被误报时能找回多少污染；真实系统中低误报非常重要。
- Hard Negative FPR：合法历史/更新/例外被误杀的比例，是 Paper 1 的关键指标。
- F1：Precision 与 Recall 的调和平均；依赖阈值和 prevalence。
- Calibration：风险分数是否能支持可解释的阈值决策。

### Retrieval

- Poisoned@K：Top-K 中污染暴露，越低越好。
- Recall@K：相关正常内容是否仍被保留。
- MRR：首个相关结果是否靠前。
- nDCG：多等级相关结果的整体排序质量。

详细统计、配对比较、CI、Holm correction 和主要终点见
[P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 17. 什么情况下才能进入 240-group

Scale Readiness Gate 必须至少同时通过六类检查：

| 类别 | 必须回答 |
| --- | --- |
| DATA | Pilot4 72 候选/GT 的平衡、自包含、匹配和失败模式是否支持扩规模？ |
| ANNOTATION | A/B 流程、适用性、agreement 和 owner 仲裁是否可重复且成本可控？ |
| SIGNALS | 五视角 signal 是否有足够覆盖、方向正确、缺失机制可解释？ |
| LEAKAGE | exact/normalized/semantic/template/entity/version/label leakage 是否 fail closed？ |
| SOURCE | 五领域来源、版本链、许可与发布策略是否可追溯？ |
| METHOD | Formal Detector 的输入、融合、校准、baseline fairness 和资源计划是否可冻结？ |

Pilot4 PASS 只关闭小规模校准门，**不自动启动 240-group**。Scale Readiness PASS 后仍需 Owner 单独批准。

## 18. 什么情况下才能称为正式论文结果

| 层级 | 能说明什么 | 不能说明什么 |
| --- | --- | --- |
| Engineering Validation | 代码、schema、环境、接口或证据链能运行 | 方法有效、可泛化 |
| Pilot Diagnostic | 小样本暴露方向、失败模式和协议问题 | 总体性能、最终论文数字 |
| Scale Pilot | 估计方差、样本量、覆盖和资源 | 正式 test 结论，除非协议明确规定 |
| Formal Experiment | 冻结数据/代码/参数/统计计划下的结果 | 未经 claims audit 的论文主张 |
| Paper Result | 通过证据、统计、复现和结论边界审计的正式结果 | 超出协议和数据支持的 SOTA/生产安全承诺 |

例如 Pilot3 Temporal AUROC `0.465` 只能写成“小样本诊断暴露弱时间信号”，不能写成 Paper 1 最终性能。正式论文结果
至少要求 Dataset/Protocol Freeze、正式 Detector 身份、预注册比较、locked test、统计不确定性、失败处理、完整 evidence
index 和 Owner 对 claims 的接受。

## 19. 文件导航：想了解更多应该看哪里

| 我想看什么 | 应该打开哪个文件 |
| --- | --- |
| 5/15/30 分钟掌握 Paper 1 | 本文件 |
| 目录总入口与文件分类 | [Paper 1 README](../README.md) |
| 当前研究方向与边界 | [Research Plan Authority](research_plan_authority.md) |
| 详细实验协议、RQ、指标和统计 | [P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md) |
| 数据标注经验与未来规则 | [Annotation Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot 实际过程 | [S6.1-P1 Work Process](../stage_process/S6.1-P1_work_process.md) |
| 当前正在做什么/禁止什么 | [Current Work State](../../../governance/current_work_state.md) |
| Owner 已确认决定 | [Project Owner Decision Register](../../../governance/project_owner_decision_register.md) |
| 实验控制面与证据索引 | [Experiment Master Record](../../../governance/experiment_master_record.md) |
| 按时间查看执行历史 | [Research Execution Log](../../../governance/research_execution_log.md) |
| AI/Codex 结构化恢复上下文 | [Agent Experiment Ledger](../agent/experiment_ledger_agentUse.md) |
| 人类/机器/证据如何分层 | [Documentation Separation Contract](../documentation_separation_contract.md) |
| 为什么本轮不移动文件 | [Document Inventory](../document_inventory.md) |

> STOP：A/B execution 和 Phase1 分发已由 Owner 批准，但真实分发尚未登记；Owner 现在只分发各自六个 Phase1 V2 文件，V1 不得发送。
> 两份 Phase1 锁定前不释放 Phase2；四份 raw 锁定前不做 agreement；当前不生成 Ground Truth，也不启动 240-group、
> Dataset freeze、Detector、训练、5090 或 Formal Experiment。
# 2026-09-16：系统开始自己找可信证据

过去的信号实验已经知道“这条 Candidate 应该看哪两篇 E1/E2”，只能算诊断上限。本轮先把所有官方快照合并成统一的 57 文档库，隐藏每条 Candidate 的 E1/E2 对应关系，再让 Sparse、Dense 和 Hybrid 检索器自己找证据。检索结果锁定以后，才拿人工对应表检查找得准不准。

结果说明这条路可行但还没完全成熟：Sparse/Hybrid 在这个小型冻结库里表现较好；Version Registry 只有部分版本时间和 current/history 关系，因此 21 个原 Oracle-dependent signals 有了合法替代路径，8 个 Temporal signals 仍不能部署。项目已经从 Benchmark diagnostic 跨到 deployable method prototype，但还没有训练 Detector，也没有论文结果。

# 2026-09-17：先排查“检索器是不是靠题面提示”，再冻结检测器输入

本轮没有训练检测器。我们先补齐冻结官方材料中可以直接证明的版本、机构和有效期信息，再把每条查询做成四种形式：完整信息、去掉来源标题、只用候选正文、只用结构化命题。结果显示，去掉来源标题没有造成实质下降，说明当前原型不是主要靠标题找答案；但自由文本比结构化查询明显更强，说明它仍可能依赖词面重合。这个风险已明确登记，不能把当前高召回当作正式方法效果。

在不看标签、不把缺失当安全、不使用人工 E1/E2 选证据的前提下，项目冻结了第一版 23 项 S/E/P/T 原始特征。它们只是将来模型的输入材料；R 检索行为属于第二阶段，尚未合入。当前可以进入受限的 Detector 开发设计，但下一步应先改善检索难度和结构化查询鲁棒性，再申请训练批准。

# 2026-09-21：第一版 Detector 为什么还没有开始训练？

训练本来计划使用 Leave-One-Group-Out：每次把一个完整的 Clean/Poison/HN 三元组留作验证，其余 23 组训练。这样同一事实/version chain 的三个样本不会跨训练和验证，比随机拆 72 条更能防止泄漏。

但正式 fit 前发现，23 个冻结特征中的 `host_publisher_relation` 和 `publisher_issuer_match` 在所有 72 条里都没有值。训练折既算不出 mode，合同也没有规定“缺失等于 0”。如果 Codex 自己填 0、删掉两列或增加“缺失”特征，就等于改了 Owner 刚冻结的输入规则，而且可能让缺失状态变成类别捷径。因此本轮停在 Phase A：24 组 LOGO 结构已经验证，模型一次也没有 fit，没有 AUROC/AUPRC。Owner 需要决定是补上游 provenance 数据、明确批准恒定工程表示，还是版本化为 21-feature 合同。

# 2026-09-22：输入合同已经修好，但还没有训练模型

负责人这次给了明确顺序：优先从已有官方材料补真实来源信息；不允许把两项全缺失特征填成 0 或加“是否缺失”列；如果现有证据仍无法按原含义计算，就单独冻结 21 列版本。审计发现，官方文档虽然部分记有网站、发布者和机关，但这不等于我们已经知道“候选文档”与这些机构的对应关系。尤其网站域名不能直接当作发布机关；也不能从 Top5 检索文档里挑一篇最支持某个类别的来给候选赋值。所以优先修复未能成立，按负责人事先批准的后备方案保留其他 21 项，旧 23 项原样留档。

新版输入经过了 24 折逐折检查：每次只在训练组里都有足够真实值来计算缺失填补统计量；被排除的两列在三类样本中都是同样缺失，不构成这两列自身的类别捷径。这只是证明“可以安全地开始下一次开发集模型运行”，不是已经训练，更没有准确率或论文结论。Final72 仍只用于方法开发。正式 240 组数据必须在构造时就把网站、页面发布者、文件制定机关和来源链采集齐，不能以后靠人工答案补。[详细审计报告](../method_engineering/PAPER1_DOCUMENT_DETECTOR_MISSINGNESS_OWNER_RESOLUTION_REPORT_V1.md)。
