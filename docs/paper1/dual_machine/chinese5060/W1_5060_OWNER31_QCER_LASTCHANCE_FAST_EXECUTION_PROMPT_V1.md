# 5060 Codex｜Paper1 Owner31：最后一次中文方法创新快试（立即执行）

**唯一科学授权源**：docs/paper1/dual_machine/owner_approvals/W1_OWNER31_LAST_CHANCE_QCER_CHINESE_METHOD_FASTTRACK_20261111.md。先read AGENTS.md和合同全文。本prompt是可直接执行指令：不再等待重复的Owner确认，按合同各Gate自主推进，普通单测修复自行处理，绝不放宽科学/预算/角色边界。以origin/research/paper1-chinese-defense-5060为本机研究分支、git fetch+clean+ff-only后开始；绝不merge 5090/main，也不把旧测试重写为新试次。

**第一优先级：尽快拿真实数值；不再进行新项目预检作文。**
1. 复用已经存在的Owner27/Owner28 Chroma cosine+MiniLM缓存、B2和RD_ZH代码、相同TopK5；从git的当前Python实现直接添加一个小型、独立、可单测的Q-CER模块，禁止重新实现全工程。
2. Q-CER核心输入只允许query(event_date/scope/entity/property) + 有序TopK5正文 + B2/ZH原掩码 + 同模型可见相似度；禁止正确答案、私有Gold、官方收据、造数者标签、角色化文件名/索引ID、攻击目标。用query条件与片段文本的可审计相同实体/属性/日期/范围绑定建立冲突，避免“所有最新=正确”和“多数即正确”；旧合法版本、其他scope HN、UNKNOWN要显式区分。采用对B2被删证据的有限恢复和B2留下可疑冲突段的有限隔离。证据不足输出CONFLICT_UNRESOLVED，不盲恢复、也不盲删。用一个明确算法、冻结参数、可解释决策码，不做大模型全量事实抽取。
3. 保存 v0 代码、参数、方法说明及字节SHA，写8类虚构fixture单测（noPoison/合法过去/HN异scope/S3同值错范围/S5重复/S6改写/S7伪造新版/5-of-5与空证据），Ruff+MyPy+pytest。接入同TopK对照七臂NONE/RD_B2/RD_ZH/B2_QUERY_RELEVANCE_ONLY/B2_VISIBLE_DATE_SCOPE_ONLY/Q_CER_FULL/Q_CER_NO_PRESERVATION。简单对照也只能使用同样query/文本/日期字段。
4. **DEV可视并不等于EVAL**：按Owner27 32主世界既有角色和TopK做真正有分母的同世界对照；Owner28 32世界公开掩码与评分聚合可以做只读诊断，5090私有逐片Gold仍不可取得。最多DEV v0和一次有诊断依据的v1，保留两个结果不得覆盖。判断P retained<=B2、C wrongDelete<=B2、HN wrongDelete<=B2且至少多滤2P或多保3C；否则立即STOP METHOD_DEV_NO_GO，报告错误与为何失败。DEV/代码本地运行45min资源门，CPU2,D盘私有增量<2GiB,剩余>=10GiB。不能重刷不同seed或阈值。
5. DEV通过后**立即冻结并push**“方法源SHA/参数/映射/固定代码版本/接口schema/全DEV报告”，然后只读等待5090新的role-free新中文32世界输入。尤其不能先看未见EVAL文本再改代码、单测或阈值。5090只读引用本合同和接口即可，禁止索取Gold。
6. 5090已有全新EVAL rolefree时严格核SHA、样本由不同虚构事实组成、4事实组×8情境、每世界11自写文段、角色盲和人审标志。使用相同冻结MiniLM/TopK/七臂只跑一次、先封存预测和排名hash再由5090独立读私有标签评分。若只达16/24世界只作诊断，不能宣称GO。收到5090评分结果后判断EVAL硬门（比B2 P/C/HN三项都不劣且>=3少P或>=4少删C，full与query-only/date-only有非零机制差异）；没有达到立刻METHOD_LASTCHANCE_NO_GO且停新算法，不因看到Gold返回v1。
7. **仅 EVAL硬门GO 后**按合同试一次4臂×32世界最多128个Qwen生成格：先确认Owner31独立新增USD0.75及旧累计预算余额、权利出站、准确token请求上界和北京region/fixed model；没闭合写API_BLOCKED，不向外发。模型仍固定qwen3.7-plus-2026-05-26，统一提示/输出/温度，前3工程检查，失败保留缺格不重试；每条源码回包先归档，支出与时延精确记录。绝不把隐私Gold发给模型，User已同意合成自写非敏感文本的限额科研外传（仍须内容合规）。若EVAL不GO，科学试次止于离线候选级。
8. 结果必须有完整机器可复算清单：每臂P/C/HN/B的投放/召回/漏召回/删除/保留；候选P检出和Clean/HN代价；mask每world配对，按4事实组、S1..S8、实际3/5,4/5,5/5、旧合法/伪造新版分层；每个算法贡献的反事实(有消融)、平均/p95时延、CPU/token/USD、失败案与negative outputs。Agent EVAL/HumanGold0、ASR正式NOT_MEASURED。每个新文件只能在5060分支提交，更新Tracker及Execution Log真实阶段状态，回传HEAD、代码SHA、DEV/EVAL实数与唯一GO/NO_GO，不要写“即将运行”冒充完成。

**STOP**：改旧Owner27–30科学记录，D2/D3/HOLD8解封，5090 Claim1–3，main merge，新的权重下载或额度无上限，重复独立EVAL，Q-CER从测试标签偷取正确答案均禁止。遇阻塞交当前实际成果而不请求重复审批。
