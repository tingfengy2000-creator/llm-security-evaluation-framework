# 5060 Fast-Track B：离线准入审计与独立盲审材料

2026-11-05 JST；**PARTIAL_DELIVERY / HUMAN_DECISION_REQUIRED**。下载和B1/B2未执行，不能声称Fast-Track B目标完成。
控制面完整提交 `f491c0a507e5555e9611c022cfba66980ad8cbca` 已仅ff-only同步到原5060分支；启动clean，0/0。
已读AGENTS、Context Authority Map、PO-MHEP、Current Work State、Project Master、Owner Register、长期需求、
Experiment Master、研究方案权威、P1/P2协议、执行日志及文档分离合同。两项Owner决定：
[FAST-B-04](../owner_approvals/W1_FAST_TRACK_B_OWNER_AUTHORIZATION_20261105.md)、
[RESOURCE-REPRO-05](../owner_approvals/W1_STORAGE_AND_REPRO_RESEARCH_DIRECTION_20261105.md)。

## 执行合同缺口和停止范围

本轮消息要求严格遵循“随附最终Prompt文件”，但当前消息无可读附件/路径，聊天附件接口返回空清单；
固定控制面Owner授权目录仅三份Owner文件（Fast A、Fast B、存储补充），没有最终Prompt。
不能据两份授权推断缺失文件没有额外资源、安全或证据门。已向Owner请求确切文件身份，未获得回复。
按PO-MHEP A/F/G和Context Recovery，下载/载入模型/B1/B2进入HUMAN_DECISION_REQUIRED。
十二字段决定材料见[启动与风险核验](fast_b/STARTUP_PREFLIGHT_AND_RISK.md#human_decision_required最终prompt缺失十二字段)。
本记录只保存明确允许的独立材料与只读审计，随后停止；不能将本次停机理解成Owner撤销原条件式批准。

## 本轮实际核验

- 官方本地clone HEAD=`ba2a17efba165d45409114df2d70b030ade1e1b8`，工作树clean，18份库/项目/许可文件的Git blob与本地字节核对。
  checkout可能有CRLF差异，分别保留本地SHA和Git内容SHA，不修改源码或历史hash。源码MIT；HF模型许可尚未联网核验。
- 静态调用链：v0.2公开库默认minilm-all；可传入已实例化SentenceTransformer对象，load_embedder原样返回，
  因而后续固定本地资产无需修改库或让其访问floating main。本轮未载入模型验证数值等价。
- 既有参数single_hop、p=2、m=5；层次聚类n_clusters=2，其余sklearn默认；英文stopwords及默认TF-IDF token规则保留，
  不做中文分词或异常fallback；Stage2选精确indices。query在当前detectors中未使用。
  B1应标B1_PUBLIC_V0_2_PINNED_MODEL，非ACSAC artifacts/严格论文数值复现；B2只能替换固定多语言embedding。
- 原P2 OUTPUT_SEAL及所有封存成员逐文件hash通过，36份TOPK_PRIVATE原字节核验；没有重新建库、查询、重排、补召回或修改快照。
- 4项盲审投影泄漏/准入测试通过，Ruff通过、MyPy1源码通过。原P2的56测试是历史证据，不作为本轮重复执行。
- 新HF请求0、模型下载0字节、商业API调用0、费用0；B1/B2过滤均0次。ASR和Answer Accuracy均NOT_MEASURED。

## 分母与结果边界

| 条件 | 完整世界 | Candidate进入TopK的条件性世界 | 本轮过滤Recall / Clean-FPR / HN-FPR | 删除/残留/空集合/延迟/异常 |
|---|---|---|---|---|
| 原P2封存输入 | 36；P/C/HN各12 | 29；P10/C10/HN9 | 不适用：是输入检索身份 | 原miss7：P2/C2/HN3 |
| B1公共v0.2 | 计划36，实际0 | 计划29，实际0 | NOT_RUN，不写0% | NOT_RUN，不作原版失败归因 |
| B2仅换embedding | 计划36，实际0 | 计划29，实际0 | NOT_RUN，不写0% | NOT_RUN |

29/36和角色计数来自已交付P2聚合，不是本轮新过滤结果；7miss语义原因仍UNRESOLVED。
未来须同时保留any-chunk candidate flag、all-retrieved-candidate-chunks removal、partial removal和残留数；
不能把任一chunk删除称为整个Candidate消除，不能为未标注背景计算FPR。
当前没有这些实测数值，没有独立Human Gold，不能使用旧E1 37/40代替查询级RAG成绩。

## 12题独立待审包

固定原卡V2索引SHA `ec18c60e6841617e3edaae9bb5b8e5af05fc7fcab49029b7b8672f85758cc908`，
12题、38事实原子、16份对应官方来源原文。所有引文offset和来源hash核对；题目、事实值、引用、时间与条件不改。
本轮脚本不读候选、标签、TopK、旧预测或两机实验结论；只有批准SOURCES和固定未签卡作为输入。
输出仅保留question、proposed facts/范围/引用，不包含query_id、事实组/角色映射、原AI理由或历史一致性判断。
审阅身份/日期/独立性声明、答案等价类、target独立证据、C3必要证据与移除操作全部待填写。
这是**盲审材料准备**，未发给审阅者、未完成盲审、Human Gold=0；AI不能签署或接受。
审阅者若曾暴露候选/预测/结果必须申报，由Owner判断资格；签署return另存，原包不可覆盖。
本包没有独立攻击记录，target保持UNKNOWN；不得根据自然文本或检索表现猜意图，C3仍不评分。
全文仅受控本地；Git仅[脱敏索引](fast_b/evidence/BLIND_PACKET_INDEX_PUBLIC.json)，不授予T1可信权限。

## 存储、证据和命令

原1GiB D/E限额已按新决定取消；本次独立preflight/材料支路预冻结新增峰值64MiB，安全空闲20GiB、wall300秒。
开始D盘约311GiB/E盘约337GiB；原生Windows，不启动WSL/Docker/conda，不创建VHDX。
启动TEMP/TMP实际指C，所有后续Python项目进程先重定向TEMP/TMP及HF/Torch/XDG/pip/MPL/工具缓存到D，使用-B。
既有C盘解释器文件只读，不迁移旧模型缓存；项目新代码/缓存/临时/日志/归档全部D。未声称OS级零C写入或RAM峰值已测。
下载支路资源峰值/最小文件白名单/逐请求累计流量尚未冻结；本报告不能作为下载准入通过。
完整命令argv/cwd/source hash、stdout/stderr/exit、环境版本与路径在Git外归档；
首次source核验保存了全部Git-blob hash，后续只读补存18条逐文件git-show stdout/stderr/exit，不覆盖首个归档。
原始源码/模型/私有卡不进入公开Git。见[preflight证据](fast_b/evidence/PREFLIGHT_AND_BLIND_PACKET.json)及
[源码证据补记](fast_b/evidence/SOURCE_AUDIT_SUPPLEMENT.json)。

| 私有归档 | SHA256 |
|---|---|
| preflight及未签盲审材料 | `3c5f7400eac166e32f353d032e874a389b8a5846034e9411b0fc358a349957b9` |
| 逐文件源码核验/私有wrapper补记 | `1d5104c77f31ef382afafbd536982dbae020e1c2647efdb11c946aa690f5c08d` |

## 下一门及文档收口

Owner提供最终Prompt路径/内容或明确完整合同身份后，首先核hash及其附加条件，再冻结下载最小白名单/资源/来源/累计流量门；
不能将当前状态自动变成可下载或可跑B1/B2。另需独立人工返回答案范围/target/C3；不重复申请已明确授权的普通步骤。
禁止商业API、B3/B4、B5/B6、D1-40、D2/D3/Reviewer/GT Vault、T1/T2、正式ASR/QA或跨分支合并。
本次为受阻checkpoint收口，Fast-Track B总体未完成；Git交付后STOP，不推进后续任务。

文档QA初次因Windows默认GBK解码Git UTF-8 diff失败，显式按UTF-8读取后脱敏/链接扫描通过；
未改实验输入、源码或指标，详见[收口事件](fast_b/CLOSEOUT_EVENTS.json)与[发布检查](fast_b/STAGED_PUBLICATION_AUDIT.json)。

受阻checkpoint内容提交 `be79889fbbb0f47c2d14e61952dffc2af283f9fa` 已核对origin同SHA、工作树clean、ahead/behind=0/0；见[Git交付回执](fast_b/evidence/GIT_DELIVERY.json)。最终回执提交的HEAD另在交付时实查。
