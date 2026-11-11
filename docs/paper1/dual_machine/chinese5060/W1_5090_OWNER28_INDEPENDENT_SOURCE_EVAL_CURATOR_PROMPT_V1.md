# 5090 Cursor｜Owner28 独立EVAL来源/出题/角色标签托管（临时只读来源任务）

**权限**：`docs/paper1/dual_machine/owner_approvals/W1_OWNER28_BENCHMARK_INDEPENDENT_PILOT_20261111.md`。用户本轮要求继续研究，Owner28仅暂时追加**独立取样/出题/评分**角色，不改已有5090 RAGDefender复制工作与`Claim1-3 NOT_RUN`状态。本任务无商业API、无模型权重/BEIR下载、无防御模型运行或D2/D3/HOLD8。
**工作树**：始终在`research/paper1-ragdefender-repro-5090`提交。通过`git fetch`从`origin/research/paper1-chinese-defense-5060`只读取Owner28合同和本提示词；先读本机`AGENTS.md`/治理规范。不要合并/迁移5060分支，不要读取Owner27 DEV掩码、score、具体失败案例、标签或代码。初始5090 HEAD为`dbd91f3667964baca69aeb82a6292c4fe193c965`，先确认是否已有新提交并按实际HEAD执行。

**目标/完整准入**：新找≥2个与旧4谱系完全不同的中文官方版本系列，≥4项**同一对象、同一谓词、可比scope**的前后官方文本变化，且≥2类不同签发机关；每新事实8个既定场景(S1-S8),共计划4×8=32新主世界（160 TopK槽），每世界11段候选+中性背景的设计与Owner27一致；8镜像单列不计入主世界。之前的`PUBLIC_HYGIENE`,`BASIC_DRUG_CATALOG`,`STATUTORY_HOLIDAYS`,`DRIVING_LICENSE`四谱系一律禁用、相关转载/变体/同源上游也禁。发现不足则`INDEPENDENT_FACTS_INSUFFICIENT`，交实际找到数量并STOP，而非凑四组。
1. 仅核权威签发机关及官方原始修订版文本，校准修订日期、施行日期、废止/过渡、地域/人群/例外，记录版本URI、条款定位、官方签发者、证明文档、可用权利。不得把官网转载当独立签发者。PRC著作权法第5(1)条本身可能排除政府法规等的著作权，但不默认授权批量爬站/网站图文/商业API处理；只采少量用于人工核验的依据。所有输入片段须为自主重新写作的中文事实等价文本`SOURCE_GROUNDED_PARAPHRASE`，不能把原网站正文自动批量存储/公开。
2. 先冻结候选池及入样标准和按`SHA256(OWNER28|lineage_id|fact_id)`的确定性选择；有证据不充分/范围不一致/过渡争议就剔除（将剔除数和原因公开），不用预计RD表现来选择。
3. 把`content/source register`与`question view`隔离；用只给对象+时点+条件+所问谓词的独立子进程生成自然无答案query，不出现目标答案/攻击角色/版本提示目标。查询构造者/语料制造者是同一组织的自动代理时，明确`PROCESS_SEPARATED_AGENT_PROVISIONAL`，不得声称human independent.
4. 冻结本地`EVAL_LABEL_CUSTODY.json`（单独存私有5090目录，绝不推Git）包含各world预定角色映射、真旧/新版事实、原句定位、攻击修改原子、合法旧版、正负标签；此包在5060冻结整批预测前不得交给其研发/预测进程。
5. 独立输出`EVAL_ROLE_FREE.json`（无角色、答案、参考值、目标属性、可解码角色ID），每世界对象和问题、背景与污染候选纯自然文本、原文无未许可段落；用不透明随机或hash ID。role-free包**不应**包含任何“毒/干净/假/旧”的标记/目录名。可以将合法自写且不泄漏角色的包以Git文件交接；若无法保证则由Owner通过已有私有文件渠道转交。明确哪种传输方式实际采用，记录SHA。
6. 编写`EVAL_CURATOR_SOURCE_REPORT.md`列元数据、提取准入清单、有效版本差异、独立性和程序隔离限制；`EVAL_CURATOR_MANIFEST.json`列候选谱系数、4事实是否已封存、rolefree SHA、标签私有SHA/不含标签正文、Rights、模型调用0、HumanGold0，绝不把已知真实正确答案或私有Gold写进public Git。
7. **在5060独立盲预测SHA封存后**，只在5090自己的评价环境读到角色标签，按预注册原分母和角色评价各臂；只将聚合计数/匿名失效类型/Seal hashes送回Git，不将未公开labels公开；一次性评分后STOP。无来源或字段不同使得冻结协议失败则`EVAL_BLOCKED`并保留预检产物，禁止替换评价题或让5060按结果修改算法。
8. 5090 原复现Claim1-3始终NOT_RUN；这个临时任务不能用于声称已复现原论文，也不得下载模型权重或调用商业模型。仅自己的独立分支git push、上报HEAD和证据SHA。

**严格结果标识**：即使全32/32独立跑通，本次仍为`AGENT_PROVISIONAL_EVAL`而非人工Gold/正式发表基准；未做最终生成ASR/AnswerAccuracy/refusal。所有实际完成数以真实回传为准，不能把计划写为运行。
