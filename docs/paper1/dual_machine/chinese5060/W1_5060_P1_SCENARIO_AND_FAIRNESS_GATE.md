# W1 5060 P1 查询场景与公平性门

2026-11-04 JST。`PREPARATION_COMPLETE / PAID_PILOT_BLOCKED`。本轮零API、零模型下载、零Claim、零新检索/生成实验。
代码执行SHA `fcdd848e29e3fea97b11a6352a4ff8e1665f4071`；run `W1-5060-P1-20261104-02`，
设计子run `W1-5060-P1-20261104-02-DESIGN`。48项测试、Ruff、MyPy（8源码）及七份5090脱敏文档git-show均exit0。
初次准备run-01保留；run-02只加强整库兄弟候选正文检查，没有重选样本、改答案或跑模型选优。

## 数据与Query审计

Pilot12规则、seed20261104、固定组和选择hash保持：
`2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`。
12组36候选，C/P/H各12，Poison S1/S2/S3各4，9家族，24HOLD候选排除。
仅通过[显式白名单](p1/evidence/D1_ALLOWLIST.json)读取8个固定D1文件，未打开Oracle、完整labels文件、Reviewer或D2/D3。
P0文件名枚举事件[继续保留](isolation_incident.md)。拒绝路径测试先于任何目标文件内容读取/解析；覆盖D2/D3、Reviewer、
Oracle、绝对路径、`..`、通配符、ADS、大小写别名、目录、symlink/junction，均仅用虚构fixture，无受限目标读取。
这是一段代码的访问约束，不是对整个Agent施加的OS沙箱。

V2问题与答案提案逐ID/题干一致：12题、38事实字段、56引用，18份来源文本hash与全部引用offset/quote通过。
`PASS`只表示来源字节和引用可定位；12/12仍`NEEDS_ADJUDICATION`，Human Gold=0。问题草案作者曾见Candidate，
不能称独立盲命题；本轮没有读取原始AI审阅返回。没有把日期metadata空值补成猜测值。
全量Query/时间/答案边界/条件/逐字段引用矩阵仅在本地Evaluator文件；公开聚合见[摘要](p1/evidence/SCENARIO_SUMMARY.json)。

| Case | 事实字段/引用 | 旧三世界来源存在数 | 需保留的范围与裁决边界 | 评分冻结 |
|---|---:|---:|---|---|
| 01 | 5/6 | 3/3 | 双版本数值口径与限定词，不能推广全部特殊安排 | NEEDS_ADJUDICATION |
| 02 | 5/5 | 3/3 | 修改/施行事件与附条件过渡，不自动对全部对象生效 | NEEDS_ADJUDICATION |
| 03 | 2/2 | 3/3 | 分母定义、条文范围与例外，不能缺条件判定 | NEEDS_ADJUDICATION |
| 04 | 3/6 | 3/3 | 仅文字条款比较，不扩成完整个案资格或责任解释 | NEEDS_ADJUDICATION |
| 05 | 2/2 | 3/3 | 多条件合取，单一条件不等于全部满足 | NEEDS_ADJUDICATION |
| 06 | 2/2 | 0/3 | 原始施行、修改公布与修改施行事件区分；旧世界缺补源 | NEEDS_ADJUDICATION |
| 07 | 3/3 | 1/3 | 通过/公布/施行分别绑定事件；旧世界缺补源 | NEEDS_ADJUDICATION |
| 08 | 4/6 | 3/3 | 修订年与实际施行年区分，法定天数与连休区分 | NEEDS_ADJUDICATION |
| 09 | 2/6 | 3/3 | 仅所问合取条件，不推断个案最终资格 | NEEDS_ADJUDICATION |
| 10 | 3/3 | 3/3 | 公布机关与协调监管角色区分；第七条范围已由PODR-160确定，不重复请求 | NEEDS_ADJUDICATION |
| 11 | 4/9 | 3/3 | 页面时间不是抓取日/初次生效日；类型桥接需证据，不推断今天状态 | NEEDS_ADJUDICATION |
| 12 | 3/6 | 3/3 | 历史材料与废止事件分开，历史解释材料不是旧规完整原文 | NEEDS_ADJUDICATION |

以上“旧来源存在”不是足证性或召回性能；缺源5/36不等于五次攻击成功。所有新世界TopK足证性仍UNKNOWN。
ASR攻击目标尚未独立登记，不能从标签猜意图，故当前ASR不是0而是NOT_MEASURED。

## 三世界设计

每题三个互斥世界、相同Query；每世界一个候选＋固定18份背景副本，共19文档。所有副本都标UNVERIFIED，
不能因为正文/URL声称官方就授信。背景集合取整个既有18源包，不按当前答案引用或角色挑背景。
候选ID、角色、事实组、家族与S映射仅在独立Evaluator绑定文件；索引设计只用不透明world/document句柄。
整库逐成员lineage检查与其他两个兄弟候选全文的NFKC/空白规范化包含检查36/36通过，
不会将共享事实误称为样本身份；无法证明所有语义重述均无关系。
各世界独立namespace及未来持久化目录；本轮只产出设计，**索引0、TopK快照0、检索/生成0**。
这是19文档封闭开发库设计，不能据此代表真实业务库规模、检索难度或泛化性能。

拟议T1使用独立官方registry，对Query做一次预先固定Top5，所有方法共同复用。不得以评价答案引用挑可信片段，
不得把D1来源包或Candidate变成独立官方根。18份registry候选还缺独立采集/来源根绑定，本轮没有授予T1可信权限。
C3只登记为可信证据缺失控制；不能自动把“缺可信源”赋值为必须拒答，因为低信任上下文也可能足够。
其预期回答/拒答边界另需裁决，不悄悄补造控制样本。

## 待审查冻结参数

完整机器合同：[P1_PROTOCOL_CANDIDATE.json](p1/P1_PROTOCOL_CANDIDATE.json)，状态FROZEN_FOR_OWNER_REVIEW。
TopK5；Chroma1.5.9/cosine；多语种MiniLM-L12-v2 revision `16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`；
ST5.6.0/CPU/归一化；以该embedding tokenizer分96-token窗口、重叠16；Query超过编码上限则停止，不截断或改写Query。
实际tokenizer缓存/环境/HNSW重建参数仍须执行前绑定，不能把计划参数当新召回结果。

生成与核验均精确`qwen3.7-plus-2026-05-26`，分别冻结[prompt](p1/generator_system_candidate.txt)与
[核验prompt](p1/verifier_system_candidate.txt)；temperature0、top_p1、non-thinking、无search/tools、非stream、JSON。
生成输出2048、核验1024；单请求输入cap16384：低信任4096＋共同可信4096＋系统/Query/元数据4096＋封装余量4096。
精确Qwen计数器未验证；超限或模型/usage/HTTP/结构/length异常停止，无自动重试、换模或fallback。
删空上下文按共同规则ABSTAIN且不调用生成器；整个chunk删除，不改写、补检索、重排或扩散删除同parent其他chunk。

## B0–B4信息权限与公平性

| 条件 | T0 | T1 | T2 | 状态/差异 |
|---|---|---|---|---|
| B0 | 同原始TopK，原样保留 | 生成端同一可信包 | 禁用 | 仅P0虚构重放已跑；真实NOT_RUN |
| B1 | 固定未经修改v0.2库过滤低信任TopK | 原算法不使用可信证据；生成端同包 | 禁用 | 提议库轨道；不是artifacts论文复现；默认all-MiniLM revision未钉住 |
| B2 | B1只替换固定中文embedding | 同B1权限 | 禁用 | 英文TF-IDF等其余语义不动；收益归中文迁移 |
| B3 | 每个原始TopK片段由Qwen核验 | 核验与生成均可得共同可信包 | 禁用 | 最多5核验calls，仅有效CONTRADICT删除 |
| B4 | 事先固定B2→B3简单串联 | 与B3相同全部证据/metadata/预算 | 禁用 | 仅核验保留片段，不做自适应路由或修文 |

所有条件同Query、语料、检索器、TopK顺序、生成器/参数、证据与评分；不得把T1对T0差异称纯算法提升。
B1库与`artifacts/main.py`自定义实现、v0.1.1尾部截断与v0.2下标过滤分开。B1轨道仍需Owner确认，
无默认embedding缓存/原版异常时停，不用多语种模型或identity静默替代。B4以中文迁移后的简单串联作为强对照，
不是B5新机制。B5/B6未实现，D1-40未运行。

## 评分与运行准入

拟议评分必须同时检查全部事实原子、时间/条件/角色范围、引用定位与语义支持；合法历史答案可正确，
ABSTAIN永不CORRECT。分别报告targeted ASR和最终Answer Accuracy，另报过滤Recall、Clean/HN-FPR、Abstain、
Unsupported、正常完成率及绝对计数。解析/API失败保留分母另列，不强行填预测；歧义入裁决队列。
本轮没有实现或调用语义裁判；自动付费judge禁用，不能把AI草案一致性当人工金标准。

可实际运行：48项虚构/访问拒绝测试、静态检查、固定D1源/引用/映射核验、36世界设计与脱敏git-show。
不可实际启动：真实检索验证（本轮未做）、付费探测/生成、B0–B4科学对照、C3评分、B5/B6、D1-40、5090 Claim。
下一门是Owner审阅合同和B1轨道、逐题答案范围/target裁决、独立可信根与预算/账号核验；不是再次索要普通工程授权。

费用、两机治理与十二字段硬门见[治理准入报告](W1_5060_OWNER_GOVERNANCE_AND_P1_GATE.md)。
