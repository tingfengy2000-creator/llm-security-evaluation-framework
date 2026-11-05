# 5060 Codex｜立刻推进 Paper1 Pilot12 V2 真实生成（Owner12一轮3+105）

**执行优先级：真实科研结果 > 形式性准备。所有必要数据/资金/外传风险仍要守住，不重新设计、不新建下一轮Fast-Unblock。**
- Owner决定 `W1-OD-20261105-5060-RAPID-LIVE-12`，完整12字段授权 `docs/paper1/dual_machine/owner_approvals/W1_5060_PILOT12_RAPID_LIVE_OWNER_AUTHORIZATION_20261105.md`，owner记录提交`d0737d3e6f43b322586df9ead88f9e8faecd5969`。**本次是明确一次性受限真实执行许可**，但仅在真正的数据权限、费用和模型路由最小门通过后可启动；与旧Owner11的零调用任务不同，不能把Owner11的live硬锁沿用成无论如何不执行。
- 分支`research/paper1-chinese-defense-5060`，旧证据回报HEAD`c03dd74507ad1a09fd5118933732562fa244cac2`；5090/D2D3无任何授权。
- 固定V2：`qwen3.7-plus-2026-05-26`、系统消息和query原文、36世界(G0,G1,G2)×3=108请求，80 unique prompt hashes均按槽发送不去重；仅`max_completion_tokens=256`、nonthinking、temperature0/top_p1/JSON；不再切回V1；不得改Prompt/样本/TopK/过滤结果/角色/检索/模型或另加模型judge。
- SHA256原件：V2 proposal `e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e`、V2 wire plan `0920add3e5b5383a9b685207cabeb539bb3d414ee1db30c6f7a313d37469bbcc`、V2 grid `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c`、P2 `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`、PAIR01 `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`；private source reconciliation `21db4e4feebf39df6410ae4b2954542b5c2e30d3bf176f9b8c8e105122e05a26`、endpoint recovered `3e84064dbfdcbb13e4d3d5213c3d85158898073bc01e8b41b8067370ddb31882`。旧V1、Runner、全部seal只读。

## 0. Context recovery与快速路径

按AGENTS.md/context_authority_map、Owner/PO-MHEP、Current Work State、Research Log、最近15个commit做一次必须的恢复；仅在干净分支/上游一致时ff-only更新，禁止stash/reset/rebase/force push/merge。必要记录最短化，只使用已有PO-MHEP模板，不新增研究讨论、Reviewer、HumanGold、数据集。

请按照下述顺序**一个工作批次完成**：
(1) 窄化修改现有`fast_unblock_admission.py`/`fast_unblock_runner.py`和独立Checker，替换错误的“无服务端Tokenizer永不放行”与`LIVE_AUTHORITY_SHA256=None`硬锁，但保留原始来源/账户/资金/签名/身份隔离；
(2) 用既有D/E真实材料快速核最小门；
(3) 所有最小门PASS则立即按原序**真实首3格**并完成工程审核，成功就**继续剩余最多105格**；别再STOP给Owner递交一次“准备完成报告”；
(4) 首错STOP并封存，全108可追溯；生成后才做独立D1暂定答案评价（若原Evaluator已支持），不混为正式Gold/ASR。

## 1. 四个最小执行门

**A｜来源/数据权利最小门（不可省略）**
- 已恢复46/46哈希：15法规规范文本、2官方网页/解读、29签署D1候选（F5→P1→P2→V2）。**不再要求46份单独申请或“29未匹配”重新溯源**。参考原`SOURCE_ORIGIN_RECONCILIATION_PRIVATE.json`和既有`D1-DEV-BEIJING-CONT-A01`历史授权，只做一次覆盖全部46源的严格**实际出站字节**范围审计。识别真实个人隐私、凭证、内部秘密、明确禁止第三方推理的许可；上述明确禁令出现立即STOP，不改冻结内容。对于研究者自己控制的候选数据，Owner12的新“进行真实V2研发验证”是当前限定用途授权，可作为其项目材料使用授权；但不能替不受Owner控制的第三方赋权。对29候选若能依据原签署清单、生成链和项目权限判断为Owner控制的D1开发素材，记录`OWNER12_SCOPED_RESEARCH_USE`而不是`COPYRIGHT_PROVEN`。仍缺必要合法基础时**只提出一项明确Owner事实缺口并STOP**，不能猜署名/版权或发送。
- 处理方固定`ALIBABA_CLOUD_MODEL_STUDIO`，范围为冻结system/query/retainedTopK，区域为已恢复`cn-beijing` Workspace、用途仅D1开发生成；从未批准D2/D3、Reviewer/GT、reference/role/target外传。过去6类Regex0命中只是补充，必要上下文审阅单次完成并封SHA。

**B｜北京Workspace与真实wire最小门**
- D/E原已核北京host+本机`DASHSCOPE_API_KEY`从环境取；必须先比对host属官方 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 和原封存Workspace绑定，API Key所在region正确；绝不把key、真实WorkspaceId或余额写入Git/模型输出。
- HTTPS TLS证书验证、官方host allowlist、无环境代理、无自动重定向或retry、**串行1、单发POST**。不发送测试probe、count-tokens、余额接口或多余模型请求；首3格本身就是唯一连通工程检验。
- Wire固定V2/JSON、nonthinking、`max_completion_tokens=256`（官方有≤10token差异说明）；预算将输出266作为候选容差，若真实`completion_tokens>266`、model id错、no usage、API错误，首错STOP。**官方公开兼容不等于实测通过**，真实首次工程检验不可重复或换模型补试。

**C｜Owner接受后置usage（替换先验严苛证明）**
- 原`INPUT_CAP=4096`保持数值但把验证点改为每次真实返回后`usage.prompt_tokens`验证；旧108条最长2444 UTF8 bytes只说明量级，**不得冒称已严格证明**。在首次实际请求发出前有`C_RISK_ACCEPTED_OWNER12`记录，明确接受首次越4096可能已外传与收费。每次收到usage若>4096或缺失立刻STOP，所有剩余`NOT_RUN`；全108仍固定且无重复。Cache命中tokens必须计入原始prompt_tokens，不用折扣后数充当输入长度。
- 对预算按“最多107个合规<=4096 + 最多一个首次越界可达官方模型输入上限991808、按更高价档计费”的**单个超限请求情景**建实现金额上界；这是并发1、每次成功回答即验usage、首越界停止才能成立。若可能有服务端额外/失控计费而无法给合理上界则标未知，不假PASS。不得自行把模型输出字段回改V1。

**D｜简单、数值有界的预算/余额**
- 复用历史361收据核算CNY7.611826、未配对预留0（不抹去Owner旧数和差额CNY0.083730086）；用实际本机北京价格、历史其他工作线/当期未结算和Owner已核的当前可用资金作一个D/E私有数值快照。若账单API不能离线读取，不强求逐张截图或空跑探测；可用有出处的官方**更高**计费档、包含失败在途的保守上界、明确日期与一个可信转换上界计算美元；Owner负责自己可控资金可签一项不含凭证的bounded声明，不可虚构金额。
- 估算上界要覆盖108个正常请求和**一个**首次越4096的最大输入请求、266输出候选/每格、至少20%风险reserve以及pending；若输入越界超过模型输入限额，捕获为错误并预留可能收费。严格`settled+pending+whole_reserve < USD28`，>=USD25警示，>=28不得开始新请求，USD30全工作线累计硬限且账户可用额覆盖，发生计费不明/失败即STOP；无需把过去361次全部再核算一轮。可设置额外当前批次累计额下限作熔断，但不得用Mock0.63或公开CNY1.34宣称实际价已核。
- 资金或数据权限是真实硬约束：缺到足以无法估量/无法安全发送时只允许一次明确阻断，不创建其他可疑途径。

## 2. 修正受审代码许可模式

现有`LIVE_AUTHORITY_SHA256=None`让任何历史批准都无法构造LiveTransport；请将执行许可固定到**Git内已经存在的Owner12十二字段原件SHA256**（对完整原文件原字节hash，而非未来由Agent自己写的假Owner签名）。独立本地checker另建`RAPID_LIVE_ADMISSION_MANIFEST`绑定：上述已批准Owner12 hash、最终Runner源文件SHA及commit、冻结V2 proposal/plan/grid、46个source索引和最小审计、北京Workspace host私有SHA、私有费用/汇率快照SHA、批准的C风险改门、输出目录D/E全路径和唯一runID、108固定格和首三格检查点。此Manifest是**执行前实际证据校验报告**，不是伪造新的Owner签字。只有授权文件正确+Checker实审A/B/C/D通过才能打开本次单次live传输，任何一项不通过必须在读取API key或建立socket**之前**失败；`--live`或环境变量本身绝无授权效力。若改动代码会使先前源commit失效，先完成测试、冻结最终源码及新commit的sha，再由checker独立验证源SHA，不要求Owner对尚未知的commit另外再批准，因为本Owner12已经授权在冻结范围内的最小修复。
- 必须使用原`send_intent`持久事务、首三格工程检查、同一轮4–108、全108`SUCCESS/FAIL/NOT_RUN`封存、费用账本预留/结算、零自动重试/重复；旧离线成功案例必须全部回归。若HTTP200但模型事实错，这只是**科研输出**，不能触发调参/重选，完整原输出保存；如果JSON无效/因截断不能判读，按原冻结工程异常规则停发并标记。
- 绝不能因为未知来源/预算/身份或缺实际支付能力而提前发送。相反，**不要**把没有闭源Tokenizer形式证明、缺重复审核历史账单、或者未给每份官方法规额外版权许可当作单独STOP理由。

## 3. 直接真实执行，报告事实而不是继续申报

- 全部最小门合法PASS后立即真实按冻结序列1、2、3（本身在108格内）、三次均HTTP/模型/usage/成本/JSON/finish_reason和seal工程PASS则**自动继续**4–108；独立owner12文件已经授权，不在首3之后新请示。任一错误立即STOP、保留已经发生的HTTP/可能在途费用；不能选择“成功案例”继续或跳过失格。
- 原始响应与usage/费用/请求SHA/运行环境/端点版本/首3门及失败、全108槽封存在D/E独立目录（C盘禁项目可控新增，D/E余量>=20GiB）；公开Git只脱敏摘要和sha。生成完成后**先封存**，再独立D1开发Evaluator只读暂定JSON算按事实组统计的`PROVISIONAL_REFERENCE_CONSISTENCY`、拒答/错误/成本/latency，HumanGold0、target/C3/正式ASR与Accuracy均NOT_MEASURED。
- 不准实测完整109次或另加judge，禁止D2/D3、GT/Reviewer、其他新方法、5090 Claims、crossbranch/main merge、额外pip/模型下载；任何新研究路线都需未来Owner另批。

### 单次交付与STOP

建议只新增`docs/paper1/dual_machine/chinese5060/pilot_rapid_live/RAPID_LIVE_OWNER12_RESULT.md`及`RAPID_LIVE_EVIDENCE_INDEX.json`两份**脱敏**材料（如AGENTS必要治理做简短索引、PO-MHEP）。报告实际owner12 SHA、源码commit、V2 SHA、局部A/B/C/D门PASS/仍缺、真实API POST/success/fail/notrun/首3及总计费、实际token/latency和Run seal；或如真实法定权限/资金仍不足，**只列最多一条需Owner提供的精确信息**，不再开启另一轮“准备任务”或把所有旧计划重写。
交付状态四选一：`RAPID_LIVE108_COMPLETED`，`RAPID_INITIAL3_STOPPED`，`RAPID_PARTIAL_STOPPED`，`RAPID_LIVE_BLOCKED_MINIMAL_ACTION_REQUIRED`。仅原5060分支合法commit/push，最终HEAD、working tree clean、ahead/behind 0/0、与remote一致后STOP。
