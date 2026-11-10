# Paper 1｜下一批：中文真实版本化知识污染来源预检与科研预注册草案 V1

- Date: 2026-11-10 JST
- Supervisor context: Owner26 `BLOCKED`, branch `research/paper1-chinese-defense-5060`, snapshot HEAD `ed438e05725ba84c983737a6a7a58fa3284fabfd`
- Status: `PROPOSAL / SOURCE_PREFLIGHT_ONLY / NEW_SCIENCE_RUN_NOT_AUTHORIZED`
- Authority interpretation: Owner 在新会话要求“请继续我们的实验吧”，表示希望继续推进研究，不等于批准新数据上的科学试次、向第三方 LLM 外传、增加预算或改变已有一次性评估。
- THIS FILE IS NOT AN OWNER APPROVAL. Do not place it into `owner_approvals/` or label as signed.

## A. PO-MHEP 十二字段（拟议；未批准）
1. Issue ID: `W1-5060-NEXT-PUBLIC-VERSION-PREFLIGHT-PROPOSAL-20261110`.
2. Question: 能否使用独立可核的真实中文来源-版本-生效期-适用范围信息，在同一 TopK 的知识污染过滤中减少 RD-zh 正常证据误删且不增 Poison 保留？同时给中文版本敏感污染基准保存有效证据。
3. Discovery: Owner26 只完成 36 world 中的 RD_B2/RD_ZH；全七臂 DEV 0/36，D1-28 Eval 0/84。RD_ZH 已召回 Poison 保留6/10、Clean误删5/10、HN误删4/9。Owner20 Rule-V2 新集 NO_GO；Owner25 Oracle 合成缺同world RD，严格真实来源锚覆盖0/180。
4. Evidence status: OBSERVED 是上述 Git 报告、真实官方页面带有历次修订及生效/废止关系；INFERENCE 是公开来源可供构造独立查询与作用范围冲突；UNKNOWN 是准确条款变更粒度、第三方上传许可、取得片段版权和可用独立身份凭据、自然中文抽取正确率、真实最终RAG指标。
5. Inherited constraints: 不改旧 D1、Pilot12、100+20规则、Owner25、Owner26 的封存；不碰 HOLD8、D2/D3、Reviewer 原始标签；5090 Claim1–3不启动；不重跑84；绝不以Agent provisional Gold自称Human Gold。
6. Why now: 旧D1缺28组独立查询、外传许可和请求Token硬预算；继续反复工程排障不产生方法证据。真实公开来源优先解决可证伪性及论文可转向性。
7. Risks: 版本错误标注；旧版合法文档被当Poison；同值异范围；自称官方/最新版误赋权；多数或同源传播假证；按结果择样；数据过拟合；额外外部可信元数据的信息优势不公平；版权与第三方外传未经许可。
8. Options: A 公共来源只读预检并形成可审批预注册方案；B 先直接在原D1重跑七臂（当前三硬门未闭合）；C 立即主张新方法成立（无证据）。建议A。
9. Recommendation: 本次仅完成A；方法可行性下一批独立 Owner 批准，保持防御为主、基准为后备。
10. Confidence: 高（Owner26执行状态、官方法规/医保版本链存在）；中（可构造高质量对照）；低（VESA相对RD/Qwen的净收益与创新性）。
11. Proposed later study (NOT authorized): 先选来源链与独立问题，按事实族/文档谱系划分DEV与未暴露评价，先封存query、TopK与角色盲上下文再预测；固定RD_B2、RD_ZH及同证据预算的来源/版本/scope方案与直接Qwen基线，必要时做oracle上界但必须与部署臂分列。评价Poison retained、Clean/HN false delete、候选漏召回、Poison reinclusion、same-value-different-scope、version spoof、3/5-5/5 source collusion、Tokens/latency/cost、真实RAG ASR和Answer Accuracy（只有另批许可才能测）。前后证据权限与输入预算区分两个信息条件，不能将额外trusted metadata收益冒称纯算法收益。
12. Stop: 未收到明确新批研究授权以前，不做新正式样本评分、模型/API调用、下载权重、未知许可原文批量抓取、主线merge、不签Gold；如公开页面的实际获取权利/发布时间/正文权属不明，只保留URL与状态UNKNOWN，停止对原文复制传播；预注册草案写完并推到5060独立分支即STOP。

## B. 候选官方来源（起点，不是已签数据与已审 Gold）

1. 司法部国家行政法规库，《公共场所卫生管理条例》页面列出1987-04-01、2016-02-06、2019-04-23、2024-12-06历史版本，且新版条款体现适用范围。 `https://xzfg.moj.gov.cn/mobile/law/detail?LawID=1755`。再核每版文本对应修订与实际生效日期，不得以“修订日”等同“施行日”。
2. 国家医保局 2024年药品目录通知：`https://www.nhsa.gov.cn/art/2024/11/28/art_104_14886.html`，记载2025-01-01施行、2023版废止。
3. 国家医保局 2025年药品目录通知：`https://www.nhsa.gov.cn/art/2025/12/7/art_104_18970.html`，记载2026-01-01施行、2024版废止，并涉及适用范围和过渡条款。
以上三个网页是来源候选而非三个独立发布机构的证明。新版/旧版配对不能只比目录名称；必须在同一事实对象上证明真实冲突、非仅时间顺序。政府网页可公开访问不自动等于允许第三方商业API上传。

## C. 创新性相邻工作（下一阶段正式比较前需阅读）
- RAGDefender ACSAC 2025: `https://github.com/SecAI-Lab/RAGDefender`。
- 关于 stale-document poisoning 的具体论文与统计尚待文献复核，不能将未经核实的样本数写入正式创新性对照。
- FRESCO (Findings EMNLP 2026): `https://aclanthology.org/2026.findings-emnlp.54/`；已有演化语义冲突/重排序基准。
- ConfRAG (ACL 2026): `https://aclanthology.org/2026.acl-long.11/`；已有真实多源冲突问答。
候选差异须瞄准中文伪造新版、同值异scope、独立来源证明、协同多数污染、防御误删与同world强基线，而不是单纯“中文+时间”字样。

## D. 可直接交给5060的受限执行Prompt（仅预检，不作新科学试次）

你是5060 Codex。先读 `AGENTS.md`、治理规范、最新 Owner26 结果和本文件；用 `git fetch --prune --tags origin`、`git status --short --branch`、`git log -15 --oneline` 检查工作树及remote HEAD，clean时只 `pull --ff-only`。本任务是公开材料只读 PRE-FLIGHT，不是 Owner27 科学实验的执行权。

I. 检查上一轮所有真实停止条件是否如本文件：D1-28独立查询缺失、逐段出站许可未签、USD3最坏情况预算未证；不得通过改写状态制造“已解封”。
II. 只研究公开官网页面的来源身份、修订/发布/生效/废止/适用范围，优先本文件三个URL并可增加其他官方单位来源候选。不要自动批量下载网站正文或任何不可确认许可附件；可以人工可读元数据和少量必要核查，遵守网站条款；单条网页若存在权利疑问记录 `RIGHTS_UNKNOWN`。
III. 输出 `PUBLIC_VERSION_SOURCE_REGISTER_DRAFT.json`（仅URL、官网名称、发布/生效/废止/适用范围字段、是否存在可验证改版事实、证据URI、权利与独立性状态，不填未经核实值），`PUBLIC_VERSION_QUERY_PROTOCOL_DRAFT.md`（定义事实单位、无答案独立查询、样本分层与role-free/独立Evaluator隔离、信息条件公平与预注册撤回门），`PUBLIC_VERSION_NOVELTY_RISK.md`（对照上面四篇已有关工作）。
IV. 纯离线可运行JSON/schema QA与源URL静态一致性检查，不得运行新RD、Qwen、本地生成模型、检索结果预测、带 Gold 的评分；不读取D2/D3/HOLD8；不需要再次提交原Owner26停止报告。
V. 报告候选来源/真实版本冲突可核的数量、查询独立性障碍、待Owner批准的最小科学试次方案和预计资源，不许编造正例。将新增草案和必要治理执行日志推送本独立分支，注明 `PREFLIGHT_ONLY / SCIENCE_NOT_RUN / HUMAN_GOLD=0` 后STOP。不得向主分支merge。

**Gate:** 如果任何步骤必须调用商业API、批量复制不确定权利的第三方文本、获取非公开来源、修改科学参数或接触封存标签，则不做该步骤；交证据与可选择替代路径，等待明确的下一批 Owner 审批。
