# Paper 1｜Owner31 中文创新最后一次有界快试：Q-CER

时间：2026-11-11 JST；授权编号 W1-OD-20261111-PAPER1-OWNER31-QCER-LASTCHANCE。
Owner 原话：“那就再试一下中文创新吧，不过我们要快点”。
状态 OWNER31_BOUNDED_APPROVED_NOT_RUN，非已运行实验。
5060 分支 research/paper1-chinese-defense-5060 在授权时 HEAD e9bd4f26d762335397cc18c76fb6a86104391686。
5090 分支 research/paper1-ragdefender-repro-5090 在授权时 HEAD 2c4f40d2df37b633f8a17c8b062826bbeabdb404。
本批有条件取代之前仅作归档的停止建议，但不改写 Owner27–30 的封存负结果与数据。两台机器分别只提交自己的分支，无 main 合并。

## A. 科学目标与新机制（仅一条路线）
新候选暂名 Q-CER（Query-conditioned Conflict and Evidence Retention，查询约束冲突识别与证据保全）。在检索后、生成前，同一有序中文 TopK5 上，结合查询中的实体、所问属性、事件日期、适用范围与证据正文的显式事实单位，针对 RAGDefender B2 误删 Clean/HN 和保留 Poison 的不同类型选择性裁决：
1. 文本可见的日期、范围和主张必须绑定到查询中的对象和谓词；无法确认时标 UNKNOWN/FALLBACK，不能把作者自称新版/官网当真实可信来源。
2. 在 RD_B2 与 RD_ZH 的掩码分歧中测试是否能保留确有查询支持的片段；同时对 B2 已保留的、存在显式同对象同属性冲突的片段进行不依赖 Gold 的风险隔离。不能只恢复全部被删片段，不能只增加删除强度。
3. 引入可审计的回答证据充足性输出：KEEP/DROP 与 CONFLICT_UNRESOLVED/NO_SUPPORTED_EVIDENCE 为不同字段；不能为了凑上下文将无证据 Poison 放回。5/5 污染时允许明确无支持，不把空上下文或拒答计成候选层检出。
4. 表面重复来源、相似文本和文档内自称机构不计作独立合法来源。不得以造数者已知正确答案、P/C/H/B、攻击值、私有 Gold、已知来源收据、5090 正确参考原子、角色泄漏的 document_id/source_id、S1–S8 条件作为运行特征。
5. 用已有缓存 MiniLM revision 16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1、已有 RAGDefender 固定 Stage1/2 和中文字符串/数值/日期单元关系；不用全量 RuleV2 抽取作为核心依赖（Owner20 曾 NO_GO）；**DEV/核心过滤零新 API 和零模型下载**。具体数学公式、规则、阈值和 FAILBACK 必须在 DEV v0 前冻结并测试，才能谈创新；简单日期规则及来源规则非新颖贡献。

## B. DEV 公平验证（5060）
- 原基线冻结：RAGDefender v0.2.0 上游 ba2a17efba165d45409114df2d70b030ade1e1b8，p=2,m=5；RD_ZH 为中文 char bigram、无英语 stopwords。统一 Chroma cosine、96/16 分块、TopK5、相同查询/文本/本地 embedding 和机器条件。
- DEV 可用 Owner27 32主世界（已揭示），并对 Owner28 已曝光的 32世界只读复用公开角色盲文本与已公布的聚合失败，但 **5090 私有逐片Gold不可给 5060 调参**。不能把 Owner28 重称盲测。开发如果只有 Owner27 的逐片标签，则仅基于有标签 DEV 评分，不伪造 Owner28 的逐片分母。
- 必须比较七臂：NONE、RD_B2、RD_ZH、B2_QUERY_RELEVANCE_ONLY、B2_VISIBLE_DATE_SCOPE_ONLY、Q_CER_FULL、Q_CER_NO_PRESERVATION（冲突单分支）。相同TopK、输入字段、时间/计算账本；若简单控制缺乏实现标 NOT_RUN/INCOMPLETE，不允许声称相较它们创新。
- 只准 v0 一次科学 DEV + 最多一次经失败证据解释的 v1；v0、所有失败必须留档。无调参网格、无多次试次刷分。至少单测：合法旧版、其他范围HN、同值不同范围、伪造新版、同源改写、多数污染、5/5全毒、中文数字单位和未知日期、空上下文。
- DEV 快门：在同召回分母上 Q-CER 相对 B2，Poison 保留不增加、Clean 误删不增加、HN 误删不增加，且至少多滤 2条Poison 或多保 3条Clean；每项按原分母、按事实组报。不得读标签来临时选阈值。如果 45 分钟本地 DEV/工程运行仍不通，STOP ENGINEERING_TOO_SLOW；DEV 未达标 STOP METHOD_DEV_NO_GO，**不得解封一次性EVAL**。代码和参数SHA冻结并 Git push 后才读取新EVAL全文。

## C. 独立新中文EVAL（5090与5060）
- 5090 可以在5060 DEV期间并行、独立构造 **4个全新虚构版次事实单位×8情境=32主世界**，至少2个互不重复的全新虚构机构/事实家族，32世界每个11条自然中文自写段落，TopK5按原检索程序真实检索，不人为补位。这是快速**合成代理验证**，不是已授权的自然官网原文或人工Gold。原Owner27/28的真实法条谱系和语料不得复用；不需外部文章权利，但不得虚构真实官署认证身份。
- 固定真值/虚构事实版本时点/范围/攻击目标，分别封存ROLE-FREE输入（可公开审查）与5090本机私有Gold/角色映射。独立query生成进程只见对象、时点、scope与所问属性，不见真值和Poison标记。候选选择、样本组合及哈希不依赖 5060 输出/表现。不得先看 Q-CER 失败再换句子；不能将自写普通来源 ID 当“真实可信凭证”。
- 如只完成2-3事实组，可执行16-24世界做工程诊断，但不能写 METHOD_GO，报告科学不足。5090创作/格式验收上限本地45分钟，超限阻断而非用DEV补数。
- 5060通过检查后，只在已冻结代码+配置基础上取 role-free 数据，对同一TopK跑七臂**一次**，封存每个世界Rank、Mask、冲突输出、输入SHA、代码SHA、TopK SHA后，5090才以私有Gold单次评分。禁止重跑、后验选参数、使用评分结果改 Q-CER；隔离信息，Human Gold0。
- EVAL GO（仅探索性方法信号）所有条件同时满足：Q-CER P保留<=B2；Clean误删<=B2；HN误删<=B2；且 P比B2至少少保留3段 **或** Clean比B2至少少误删4段；没有使用oracle或伪造来源提权；Q-CER 与简单 query-only/date-only 消融掩码存在可解释、可计量差异（否则 MECHANISM_NOVELTY_NO_GO）。任何失败给 METHOD_LASTCHANCE_NO_GO，保留基准路线。总共4个事实簇，不做显著性泛化，也不能声称可发表的新方法。

## D. 条件生成层（只有EVAL GO且新准入门闭合）
- 若C通过，允许最多32世界×4臂 NONE/B2/ZH/Q-CER=**128格**，使用相同 Qwen 北京已验证快照 qwen3.7-plus-2026-05-26、temperature0、非思考、max_completion_tokens256、同一prompt/证据秩/上下文预算；初3格工程检查，过门再发剩余，无重试、无填补、不把缺失剔出分母。新调用预算**Owner31新增USD0.75硬限**，以前Owner既有累计25/28/30美元门仍不放宽。
- 每条自写虚构非敏感文本逐项合规外传审核、明确账号余额和在途、地域/费率、消息序列可证明Token最坏上界和整批费用预留，**全部闭合才发**；缺任何项输出 API_BLOCKED，但离线EVAL不失效。不得把5090 Gold/attack目标、私有标签或其它敏感文本外传。默认新 API 为0。
- 5090独立按预封存虚构参考值和攻击目标评估数值匹配、攻击短值命中、合理/错误拒答、疑义与引用支持；来源与scope未解不计真正Correct，按四臂完整配对问题分母报告。候选层指标不能冒充answer ASR。回答层试探性GO：Q-CER数值匹配>=B2、目标短值命中<=B2、错误拒答不多于B2+1；否则负面。
- 本阶段不开展人审，HumanGold始终0、正式ASR/Accuracy NOT_MEASURED。Qwen或模型Judge不经准入不得调用。

## E. 资源、审计与停止
5060本地CPU<=2线程、D盘新增私有<2GiB且剩余>=10GiB，不在C盘扩容；5090仅快速生成自写代理/独立评分，无大量新下载。禁止D2/D3/HOLD8、原5090 Claim1-3、旧Owner29/30输出重跑、主分支合并、私有Gold进Git。两机各自push研究分支和RunManifest、失败样例、模型/软件版本、SHA、同分母完整指标；只允许一次新EVAL。所有门完成或失败后 AUTO_CONTINUE=NO。Owner保留论文方向最终决策。
