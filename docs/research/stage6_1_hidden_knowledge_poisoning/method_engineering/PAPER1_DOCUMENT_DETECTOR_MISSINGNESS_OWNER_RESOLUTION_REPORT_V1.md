# Paper 1 Document Detector 缺失输入合同修复报告 V1

Status: `OPTION_A_NOT_SCIENTIFICALLY_FEASIBLE / CONDITIONAL_C_APPLIED / FEATURE_SET_V1_1_21_FEATURES_FROZEN / PHASE_A_PREFLIGHT_PASS / READY_TO_EXECUTE_FIRST_DETECTOR_PROTOTYPE`
Task: `P1-DOCUMENT-DETECTOR-MISSINGNESS-CONTRACT-OWNER-RESOLUTION-01` (2026-09-22).
Evidence: `E:\LLMGuard-Handoff\paper1_document_detector_missingness_owner_resolution_20260922`；[semantic contract](PAPER1_PROVENANCE_RELATION_FEATURE_SEMANTIC_CONTRACT_V2.md)。

## 为什么不能直接填 0

旧 23 列矩阵中，`host_publisher_relation` 和 `publisher_issuer_match` 都是 72/72 `INPUT_MISSING`，真实观测数为零。这不是少数样本漏填：上游没有把“候选文档的 URL host、页面发布者、文件发布机关”可靠绑定成可计算的候选级关系。训练折无法计算 mode。`0` 会凭空宣称某种关系为假；`-1` 或“缺失指示器”会改动冻结语义，甚至把来源缺口变成类别捷径。Owner 明确拒绝了这一 Option B。

## A 路径实际审计

先从已接受的五视角注册表核对语义，再审查冻结可信库、Registry V2 和 `Q_NO_TITLE + HYBRID + Top5` 结果；不访问新网页、不补 E3，也没有用 GT、Expected、A/B、Owner 判定或人工 E1/E2 来生成值。57 份可信文档都有 `source_host`；25 份有 `publisher`，25 份有 `issuer`，并且这 25 份是同文档成对出现。72×Top5 共 360 条检索记录均有 host，其中 122 条含成对 publisher/issuer；72 条候选中，66 条的 Top5 至少包含一篇具成对角色的可信文档，但这仍不是候选自身的来源关系。

这些是**文档级元数据可用**，不是两个**候选级特征已恢复**。Registry V2 的 57 条中 `issuer=25`、`authority=55`，但 `authority` 角色描述也不能替代具体 issuer。`host_publisher_relation` 在 accepted registry 中是类别型、方向未定义；现有合同没有“host 名称对应哪个发布机构”的受证据支持映射，也没有冻结的类别→数字编码。旧预检将它暂列 binary，不能以此覆盖原信号语义。`publisher_issuer_match` 的部分检索文档可以做同文档角色比较，但冻结合同没有规定：Top5 中哪篇文档是候选来源，或怎样把五篇文档的关系汇成一个候选值。直接选 rank1、任意一篇或“最像投毒的那篇”都会新造信号。72 条候选的两个特征均维持 `INPUT_MISSING`；合法 `COMPUTED=0 / NOT_APPLICABLE=0 / INPUT_MISSING=72`（各列）。所以 A 不能在不改变科学语义的前提下成功。这个判断在加载 class labels 前作出。

## 预授权 C：21 列版本化投影

按 Owner 的条件授权，创建独立 `PAPER1_DOCUMENT_DETECTOR_FEATURE_SET_V1_1`（SHA256 `a3190b3b3fd6f3323229a83f9c919143fdba9efe06f209ef492242cdc1e37ee8`）和 72×21 原始矩阵（SHA256 `2d418ae2fd6d22f848fcf812a6126fd68ff9b7b880c389a2ca510a5c94dd5b2d`）。21 列从 V1 确定性投影，行 ID、顺序和所有保留值完全相同；S=3、E=9、P=6、T=3，R 与 Oracle 仍排除。两列进入 deferred registry，等待正式规模数据原生采集 host、publisher、issuer、authority role、文档绑定及来源链。旧 Feature Set V1、Matrix V1、报告与 GT 均未改。

此排除基于**不可观测性**，并非看 AUROC、系数或其他标签结果删特征。新的矩阵先锁定，之后才加载 class/group 做审计。两个排除列在 Clean、Poison、Hard Negative 各 24/24 都缺失，故其缺失模式本身不区分类别；按 domain/group 的完整计数保存在 post-lock preflight。此结论不保证其余 21 项完全没有任何潜在 proxy，正式规模仍须继续审计。

## Phase A 结果与下一门

重新检查 24 个完整 matched groups、24 个 LOGO folds，每折 69 条训练、3 条验证，同组不跨折。21 项在每个训练折都有真实观测值，可按原协议由训练折独立计算 mode/median；最稀疏保留特征的最少训练观测数为 6，不存在空统计量。StandardScaler 仍只可在未来每个训练折内拟合连续特征；本轮仅验证合同与可行性，**没有实际拟合 imputer、scaler 或 Logistic Regression**。无常量补值、缺失指示器、调参、阈值、校准、OOF、bootstrap 或 permutation。

因此 `PHASE_A_PREFLIGHT_PASS / READY_TO_EXECUTE_FIRST_DETECTOR_PROTOTYPE`，意思是下一次独立执行任务可以按 V1.1 与既定 LOGO 开始第一版开发集原型；并不意味着已经有模型、指标或正式论文结果。Final72 仍是 development-exposed，不是 untouched test。未来 240-group 生成前，所有拟进入模型的特征都应先通过上游可观测性审查；尤其要原生采集 host、页面发布者、文件 issuer、authority 和文档/版本来源链，不能事后靠标签或人工 E1/E2 补齐。
