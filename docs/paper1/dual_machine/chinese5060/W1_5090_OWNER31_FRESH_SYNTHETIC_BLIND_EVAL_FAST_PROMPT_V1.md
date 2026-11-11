# 5090 Cursor｜Paper1 Owner31独立盲评快试（中文自写版次知识，不开任何新模型）

从5060研究分支只读获取 docs/paper1/dual_machine/owner_approvals/W1_OWNER31_LAST_CHANCE_QCER_CHINESE_METHOD_FASTTRACK_20261111.md，按Owner31有界授权立即执行。自己的工作分支始终research/paper1-ragdefender-repro-5090，先fetch/AGENTS/git status/HEAD。不要合并/读取5060的DEV逐片评分、Q-CER源码和变体选优结果、禁忌私有内容；5090原RAGDefender Claims1–3保持NOT_RUN，D2/D3/HOLD8锁定。

1. **不必再找官方网站、真人双审、模型下载或商用API**。为了快，独立生成4个中文自写虚构版本变更事实（至少2个全新虚构领域/来源家族），每组8个既定情境S1–S8，总32主世界，每世界11篇原创新语料片段，TopK由5060固定索引真实召回。模拟中文版本、历史适用期、同值异scope、合法异scope HN、单段投毒、3/5改写与同源重复、伪造“新版本”、5/5极端压力。数值/时间/对象要足够接近真实政策自然表达，但清楚标SELF_AUTHORED_FICTIONAL_PROVISIONAL，虚构机构不是可核官方真实署名；不要混用此前Owner27或28的事实组、句子/官方法条原文。
2. 在评价前用确定性不可根据防御成绩更换的四事实家族ID/排序SHA冻结生成计划，并尽量通过不同进程/无答案视图制作自然查询：query作者只看对象、event_date、scope、asked predicate，不能看正确值、攻击目标、已注入事实或角色。source creator自写语料与Gold托管、query过程各留hash；同一Agent流程隔离不等于人审，HumanGold继续0。
3. 私有D盘独立封存所有世界/P/C/HN/B角色、正确答案值与时点/范围、假值与目标、来源家族和docID映射，私有GOLD不允许public Git。公开role-free文件（每世界query/date+11中文自写段落+不透明ID）可放5090自身分支，**不能**在字段/文件名出现poison/gold/clean/attack/正确值标签；选择与角色数据SHA分开。全量SHA、schema和语料自己跑严格QA，未见句子不可后验替换。先sealed后交5060。
4. 与5060唯一接口是 **role-free world+docs Schema**，可复用Owner28字节哈希/opaque ID标准，也可由5060在方法冻结前预注册一个新接口。5090只看固定schema不看算法参数；若新Schema有差异，仅做无损ID/字段映射和双向字节校验，绝不能重写文段来满足结果。优先4组×8=32，若少于4组则仍可给工程演示但科学方法GO自动不成立；本地独立构造/QA硬限45min，越线STOP与报告。
5. 5060源码/参数/GitSHA已冻结后，允许其只读拉取角色盲包并跑七臂同TopK。5090**只在5060完整预测SHA封存之后**从自己的私有金标读取角色表，独立评分，一次计算七臂 P retained/C wrongDelete/HN wrongDelete/B separately，按实际召回分母和世界+四事实组+版本失效分层、两臂匹配；不得用结果给5060发个例Gold让其调参。不要误把没有召回P算模型成功，5/5如果真实未召回就NOT_COVERED。只给公开聚合+SHA，私有Gold继续私有。
6. 评分判定由Owner31合同硬门：Q-CER比RD_B2 P、Clean、HN都不更差且至少 P少3 或 Clean少4；与简单query-only/date-only消融不同，不能靠角色/真值/伪造新版本自称提权。达标只是AGENT_PROVISIONAL_METHOD_SIGNAL，不是正式方法可靠或可发表；失败则LASTCHANCE_NO_GO。生成层仅由5060在全部新增权限/费用/Token准入满足时启动，5090用预封存虚构正确值/攻击值评估后验数值代理，HumanGold0，文件SHA与回包必须闭环。
7. 只推送5090自己的研究分支、正式运行报告与封存清单，向Owner/5060回传Git HEAD、角色盲包SHA、私有Gold SHA、是否方法前冻结、实际32世界分母和总结。今日无需人工签名或第三人裁决；严格保留既有Owner30 5/22负结果，不重评分旧数据、不共享API密钥、不下载额外权重。STOP时AUTO_CONTINUE=NO。
