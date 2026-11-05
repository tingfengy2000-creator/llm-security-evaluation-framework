# Fast-Track B恢复执行01：官方HF直连超时

2026-11-05 JST；run `W1-5060-FAST-B-20261105-RECOVERY01`，**BLOCKED_HF_DIRECT_CONNECTION_TIMEOUT**。
Fast B整体未完成，B1/B2均NOT_RUN，不是过滤失败结果。原14d718f checkpoint、失败/QA记录及盲审包不变。

## 已解决与本轮实际失败

合同缺失已由 `98228e202062b1216094acac90f83be29cc63074` 的[正式恢复版](W1_5060_FAST_TRACK_B_EXECUTION_PROMPT_RECOVERY_V1.md)解决。
不再寻找旧聊天附件；恢复文本不冒充原附件510342…的逐字节副本。已核AGENTS、Authority Map、PO-MHEP和
FAST-B-04/RESOURCE-REPRO-05原件，启动原分支clean，仅ff-only同步两条已知合同修复提交，未跨分支操作。

首次且唯一官方请求：HF模型树API，固定all-MiniLM-L6-v2 revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`，
原生HTTPS直连，未使用代理、镜像、Hub自动下载或备用来源。连接阶段抛出TimeoutError / WinError10060，
请求约42.15秒，进程exit1，没有HTTP状态、响应头或正文。未重试，未开始任何权重/配置下载。
故官方tree、逐文件远端size、模型卡/许可证及最小白名单均未核验，资产准入未通过，B1/B2不能启动。
该结果仅证明此次本机直连失败，不证明HF服务总体不可用或模型不存在。

HTTP响应正文/头实际收到0字节；网络账本保留该失败尝试，不清零，每请求1MiB保守传输预留仍占用总限额。
TCP/DNS低层实际字节未另测，不把HTTP正文0说成全网络0。累计预算保守占用1,048,576字节/262,144,000字节。
商业API调用0、费用USD0；没有模型载入、外传D1文本或使用付费探测。

## 原输入与材料复核

原seal `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`、完整封存成员及36份TopK原始字节均复核。
原P2 source SHA9aa21be13ae206dbbadb03b99528e362eba29378及报告提交3ca27c9416ea630e7f82c5b98ceed93099bd57ac存在，
Run Manifest列出的原源码/配置hash一致；selection逐字节为 `2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`。
无重新建库/检索/补召回/重排/改问法，B0未重跑；未读D2D3/Reviewer/GT Vault或评价标签。
原盲审包12题/38原子/16来源逐卡hash不变，直接复用，未再制作；Human Gold0、target UNKNOWN、C3待裁决。

| 条件 | 完整世界 | Candidate条件性世界 | 过滤Recall / Clean-FPR / HN-FPR | 部分删除/残留/全删/空集合/过滤延迟 |
|---|---:|---:|---|---|
| 原封存输入（历史计数） | 36，各角色12 | 29：P10/C10/HN9 | 不适用 | 漏召回7：P2/C2/HN3，语义原因未决 |
| B1_PUBLIC_V0_2_PINNED_MODEL | 应运行36，实际0 | 应报告29，实际0 | NOT_RUN | NOT_RUN |
| B2仅换中文embedding | 应运行36，实际0 | 应报告29，实际0 | NOT_RUN | NOT_RUN |

全部36世界的两方法NOT_RUN记录和输入文件hash见[配对结果状态](fast_b/recovery01/PAIRWISE_B1_B2_METRICS.json)。
未运行不能填0%，不能把7miss作检测成功；没有新TP/FP，背景无GT不贴负类。ASR/Answer Accuracy/生成拒答/Unsupported QA全NOT_MEASURED。

## 资源、质量与证据

[事前冻结](fast_b/RECOVERY_RUN_PLAN.md)：D新增峰值2GiB，20GiB安全余量、CPU2、RAM预计6GiB、wall1800秒；
实际未载入模型，本机D约311GiB空闲。所有项目新增代码、TEMP/TMP、日志和归档在D；Python-B，既有C解释器只读。
无需调用WSL/Docker/conda，不创建VHDX、不搬迁既有缓存；不承诺OS日志自身绝对零C写入。
4项既有盲审工具回归、Ruff、MyPy1源码通过（不构成下载器/模型/基线执行成功）；下载helper只作语法compile检查。
本轮无新公开业务代码，不对旧RAGDefender或数据作任何语义patch。
私有原始证据含唯一失败请求账本、STOP、完整argv/cwd/exit、请求起止、stdout/stderr、helper源码、核验命令记录；
进程起始时间未单独采集，明确使用请求起止而不冒充进程时间。受限原文/密钥/模型/预测均不进Git。

归档 `W1-5060-FAST-B-RECOVERY01-20261105.zip`，SHA256 `f5a608a948b54aa6e7c63108733f2357395cea30be4e0cd34fbdb82f4a4cb7ff`。
见[Run Manifest与逐文件私有索引](fast_b/recovery01/RUN_MANIFEST.json)、[资产门](fast_b/recovery01/ASSET_MANIFEST.json)、
[失败记录](fast_b/recovery01/FAILURES.json)、[待裁决包复用身份](fast_b/recovery01/ADJUDICATION_PENDING_INDEX.json)。

## PO-MHEP十二字段

1. Issue ID：W1-5060-FAST-B-HF-CONNECT-01。
2. 名称：固定HF官方模型元数据直连超时，资产准入未闭合。
3. 阶段：Fast B恢复后、模型下载及B1/B2运行前。
4. OBSERVED_FACT：唯一请求WinError10060、HTTP无响应、exit1；SOURCE_DERIVED_FACT：批准来源/revision和资产核验前置条件；
   INFERENCE：本次无法验证资产，因此过滤不可开跑；UNKNOWN：可用官方连接路径、远端文件/许可、两方法指标。
5. 约束：唯一官方来源/不代理替代/不自动重试/250MiB累计/模型与语义固定/AGENTS与PO-MHEP。
6. 原因：无模型身份和合法性证据不能用缓存替代或绕过公平性门。
7. 风险：擅自换源、重试或下载会产生许可/来源/计量/复现风险；等待延迟结果，但不污染数据与论文结论。
8. 选项：A保持阻断，Owner确认可用直连条件后明确恢复一次同源预检，保留旧账本，低污染/可逆；
   B改代理/镜像或改模型超出授权，须新的明确决策，本轮不执行，可能改变复现与安全边界。
9. LOCAL建议：A，保持原模型与结果边界。
10. 理由/置信度：本次失败日志高置信；无法由单次超时推断全局服务或网络成因。
11. 待Owner：确认官方直连可用条件并指示何时恢复同源预检；不是重新申请已批准的B1/B2算法范围。
12. 决定前：仅证据/治理/Git交付后STOP；禁止重试/替代源/模型、付费、B3–B6、D1-40、D2D3、T1/T2、GT或5090 Claim。
