# D1 资格建议与SEPT物化记录 V1

2026-10-27；PODR-144 / OR-098 / REL-2026-0113。
任务`P1-D1-QUALITY-HOLD-CLOSURE-AND-D1-SEPT-MATERIALIZATION-01`；
source HEAD `2ce4b1cdc0dc9d3953a0c11afc1d5961468bab4e`。
[协议](PAPER1_D1_QUALITY_AND_SEPT_PROTOCOL_V1.md)，
[并行状态V19](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V19.md)，
[文档收口](PAPER1_D1_QUALITY_AND_SEPT_DOCUMENTATION_CLOSEOUT_V1.md)。

## 结论与Owner最小动作

**40组120条建议准入、8组24条整组HOLD；有效评价仍0组0条。**
Owner只需审阅新中文决策表的三项批量确认并署名，不要求54条全部重新人工仲裁。
55非空建议完成身份/原答/枚举/既有规则和同题冻结证据核查：33项符合但待签、
21项符合但仅作HOLD问题记录、0038的1项范围前提未证；0028另2空格不赋值。
另18项当前/历史范围规范化建议不改变事实真假，仍须Owner确认，不是新增Guide规则。

本机扫描全部144条可见命题并锁定语义，之后才private join构造role/家族/设计路径；
没有用role或Expected决定事实。338个证据span的原文offset/SHA复验通过。
QA是作者侧有界复核，不是正式GT或独立真人终审。
原8组的范围、已发条文缺失、数字转录和机关排他前提问题继续隔离，未静默补Evidence。
没有在其余40组观察到新质量阻断；局部缺陷暂不要求整个family删除，未来family必须整体留出。
拟准入C/P/H各40、HKP11/10/11/8，独立证据路径建议S1/S2/S3=12/15/13；
这些不是已批准的性能分母。全部Owner最终值初始空，evidence_selection不生成唯一GT。

## 非Oracle工程工件

54份既有官方快照记录、34个唯一raw SHA，去重后33文档；新来源0，模型下载0。
Registry：host33、publisher0、issuer26、effective_start11、effective_end0、
current3、historical1；未知保留。版本/文档工程键不冒充完整官方版本元数据。
原有两份提取文本CRLF/LF字节差异保留并显式记录，不重算旧SHA。
仅原始URL＋规范化相同文本去重，不按同名合并不同版本。

检索只读Candidate主体和原文；无书名号的3条按本条前20字作主体前缀，未从Oracle补词。
继承Q_NO_TITLE、BM25字符2/3(k1=1.2,b=.75)、固定MiniLM CPU/L2/local-only、
等权min-max Hybrid、K1/3/5/10、主Top5；14,256条完整trace与精确重放锁定后，
工程进程才读人工E1/E2身份。质量轨道此前已读分配证据，不虚称全项目首次Oracle接触。
MiniLM revision16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1，tree SHA
14be5b8d047148b787bcca877c4b91722c10bc3e1a184ea3aaffe8b6fd3d1fb7。

独立D盘环境sentence-transformers5.6.0/torch2.8.0+cpu；32个锁定wheel离线安装，
pip check与模型身份通过。dry-run曾实际缓存wheel，事实保留；3GiB上限检查先阻止安装，
Owner明确调整到4GiB后才安装。实占3,672,518,140字节，未改全局或下载模型。
缓存/TEMP在E盘。首个检索运行完整stdout仅工具转录留存；新增独立精确重放的物理日志/退出码，
不将后续日志冒充首次运行原件。所有失败尝试及执行源保留。

## 同列、覆盖与实际阻断

B/C各144×21，Feature Set V1.1 SHA
a3190b3b3fd6f3323229a83f9c919143fdba9efe06f209ef492242cdc1e37ee8，S3/E9/P6/T3。
R、两项deferred关系和六项Oracle-only T未混入；列序/数值定义/未填补语义相同。
C只用实际已发E1/E2投影，144份E1/81份E2；63题本无E2，不制造第二份。
全144可计算B1991/3024、C1642/3024；建议120条B1640/2520、C1363/2520。
PTS启发式适用76条：B computed18/insufficient42/missing16；C3/32/41；另68不适用。
HKP3的T：B9/36 computed、C0/36；HKP4 B2/36、C0/36。
不将普通年份启发式适用量冒充Human版本命题真值，也不把词汇比较称为已完成版本推理。
两侧分别6/4列观测值常数，未依据标签或效果选列。

**新增工程阻断：Oracle留出FEMALE_WORKER_PROTECTION时，三项T训练列全空。**
冻结mode/median无统计量，不能只改C的列或填0；完整A/B/C比较必须另行决定可比设计。
B的13个family折统计均有观测，但未拟合任何模型。
INPUT_MISSING角色极差≥20个百分点筛查未见新flag，不等于shortcut风险已排除；
详细status/role/HKP/列值比较保留在私有审计。
S/E/P/T仍有字面集合、年份分区、跨版本绑定等启发式限制，物化不等于推理正确。

Hybrid Top5 reference：E1 131/144、E2 75/81、Any142/144、Both64/81；
建议S3的13条中E1 12、E2 13、Both12。这里只是冻结packet参考召回，不是检测Recall。
33/33文档超出Dense128-token窗口；未证明必要条款被截断或LLM跨文档推理失败，
不据此确定长上下文路线，不改窗口/模型/query/权重。

## 工件身份与边界

私有根`experiments/core144_d1_quality_sept_20261027/`；最新可信语料manifest在`outputs_v2/`，
早期`outputs/`V1保留为历史；交接明确选用V2。

| 工件 | SHA256 |
| --- | --- |
| 待签Owner XLSX | a6cbeba4d6b8ff5491d5449e318f14f4f69b69cc209e555d9348aaeddd864ec8 |
| 逐组资格CSV | 80e5a80463cee4ce3f492e79b56ec2568509618383963e7cdf3f3632512165a7 |
| 最新可信语料manifest | c54cf4c67059d6540757d88893e24f6f99b1cd8a453c9ab7dfd7c31fae0bb4dd |
| 检索trace | faa52ba750511171b0b2852f3f5419f2ca1c1363899b4cbcb0630b353dc94a9b |
| 非Oracle21列CSV | b1fd7e3aafc4ad39fb78b4b9e00408dca278f8c8ab8e5bfec0818de440300af3 |
| Oracle21列CSV | 80d89ea1c1929bda4219af0ce3e29f2791097e41b4dfabf785bcbfee9e84f14d |

原三AI输入/四人工原件/官方快照/旧75份seal不变；旧126分数不复用、不再拟合。
A文本分类、B非Oracle融合、C Oracle融合本轮fit=0，所有性能和CI均NOT_ESTIMATED，未知不是0%。
Core正式GT/2/1/1未做；D1_DEV_EXPOSED；D2/D3构造数据及其审批门独立不变。

当前：`D1_DATA_QUALITY_GATE_PENDING / D1_SEPT_MATERIALIZED / D1_PERFORMANCE_NOT_ESTIMATED`。
AUTO_CONTINUE=NO；下一步Owner质量签署＋独立Oracle缺失/可比设计决定，不自动进入新实验。

交接新命名空间`paper1_core144_d1_quality_sept_20261027_run01`已逐字节复验79个选定文件，
根目录为新Owner表与九项要求输出，quality/含原答建议和完整证据span，engineering/含锁与status。
不复制3.42GiB环境或wheel；最新manifest选V2，旧V1只在本机历史命名空间保留。
私有153文件索引SHA见[文档收口](PAPER1_D1_QUALITY_AND_SEPT_DOCUMENTATION_CLOSEOUT_V1.md)；
交接/Git使用post-seal回执，不改原封存清单。
