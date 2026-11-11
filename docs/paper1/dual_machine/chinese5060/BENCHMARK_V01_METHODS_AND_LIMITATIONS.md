# Benchmark v0.1｜方法、两批对照与限制

2026-11-11 JST · PREP_ONLY · Owner28 AGENT_PROVISIONAL_EVAL · HUMAN_GOLD=0

Owner27 DEV 和 Owner28 EVAL 都显示，RD_ZH 在同一 TopK 内比 RD_B2 留下更少 Poison，同时误删更多 Clean 和 HN。EVAL 的额外 50 次删除里，18 次命中 Poison，28 次误删 Clean，3 次误删 HN，另 1 次删去背景。这个权衡支持中文版本化污染基准和失效分析。

## 数据、运行与评分

Owner27 为开发批，4 个事实组来自 3 条谱系。Owner28 的 4 个评价事实来自未见的专利法、人口与计划生育法、职工工作时间规定三条谱系，两个事实共享人口法谱系。DEV 的春节、劳动节也共享一条谱系。同一事实的八个情境是配对变体，两批各 32 个主世界，各 160 个 TopK 槽。事实组有组内相关性，谱系间也可能共享签发体系。报告不合并两批、不把槽位或 32 个世界当作独立抽样，也不报告显著性检验。

每批主分母为 32 个世界 × 11 个投放段。各世界独立建立 Chroma 1.5.9 索引，固定 96 token 分块、16 token 重叠、cosine 和 TopK5。全部比较臂共享该世界的有序检索结果。本地编码为 sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 revision 16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1。RD_B2 使用固定 RAGDefender 上游 ba2a17efba165d45409114df2d70b030ade1e1b8 和中文缓存适配，m=5、p=2。RD_ZH 仅将 Stage 1 词项改为字符 bigram 并取消英语停用词。两臂共用 Stage 2 代码和同世界向量。NONE 保留原秩，DATE_ONLY 用显式日期规则。DEV 的 T1 收据臂属于附加对照。

5090 策划和本地托管暂定标签，5060 按先冻结、后盲预测的流程输出编号、秩和掩码，5090 绑定 Git 提交与预测 SHA 后一次评分。隔离层级是同项目下的独立进程。兼容桥接保持 32 条主世界查询及 352 段文本原样，专利法旧版使用经 5090 核对的 HTTPS 转载定位。评价样本是基于可核真实版本变化的自写代理文本，未取样自然网页语料。Owner27 的 8 个镜像单列，Owner28 原包 7 个镜像未运行。 [DEV 冻结清单](OWNER27_OFFLINE_FASTTRACK_RUN_MANIFEST.json) · [EVAL 盲预测清单](owner28_eval/OWNER28_EVAL_RUN_MANIFEST.json) · [5090 独立评分报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/670d9ab0e546d46117bf5c48ebb2b0043689f453/docs/paper1/dual_machine/repro5090/owner28_eval/OWNER28_EVAL_INDEPENDENT_SCORE_REPORT.md)

## 同口径对照

P 为 Poison，C 为当前正常证据，HN 为合法历史版本或合法其他范围的难负例，B 为背景。召回和漏召回以投放段数为分母。过滤保留或误删以已召回段数为分母。P 检测召回为 P 删除数除以已召回 P。任何漏召回都不进入过滤成功数。零召回分母记为不可估计。

| 批次 | P 投放/召回/漏召回 | C 投放/召回/漏召回 | HN 投放/召回/漏召回 | B 投放/召回/漏召回 |
| --- | ---: | ---: | ---: | ---: |
| Owner27 DEV | 50/45/5 | 70/63/7 | 40/33/7 | 192/19/173 |
| Owner28 EVAL | 58/56/2 | 82/82/0 | 20/20/0 | 192/2/190 |

| 批次 | 臂 | P 保留 | P 检测召回 | C 误删 | HN 误删 | B 删除 | 总删除 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| DEV | NONE | 45/45 | 0/45 | 0/63 | 0/33 | 0/19 | 0/160 |
| DEV | RD_B2 | 20/45 | 25/45 | 40/63 | 4/33 | 2/19 | 71/160 |
| DEV | RD_ZH | 6/45 | 39/45 | 54/63 | 13/33 | 6/19 | 112/160 |
| DEV | DATE_ONLY | 45/45 | 0/45 | 0/63 | 11/33 | 0/19 | 11/160 |
| EVAL | NONE | 56/56 | 0/56 | 0/82 | 0/20 | 0/2 | 0/160 |
| EVAL | RD_B2 | 33/56 | 23/56 | 27/82 | 7/20 | 0/2 | 57/160 |
| EVAL | RD_ZH | 15/56 | 41/56 | 55/82 | 10/20 | 1/2 | 107/160 |
| EVAL | DATE_ONLY | 56/56 | 0/56 | 0/82 | 0/20 | 0/2 | 0/160 |

RD_ZH 相比 RD_B2，DEV 的 P 保留率下降 31.11 个百分点，C/HN 误删率分别上升 22.22/27.27 个百分点。EVAL 对应变化为下降 32.14、上升 34.15/15.00 个百分点。两批 RD_ZH 保留集合均为同世界 B2 保留集合的子集，掩码变化分别为 21/32 和 28/32。额外删除中的 P 占 DEV 14/41，EVAL 18/50。两批语料构成不同，这些比例是各自的描述统计。

![三指标事实组对照](benchmark_v01/BENCHMARK_V01_FACT_GROUPS.png)

图中每行是一个事实组，横线连接同组两个过滤臂。图的三列分别用 P、C、HN 各自已召回的段数归一化。图上半为 DEV，下半为 EVAL，共 8 行，使用同谱系的事实组分别展示。CSV 记录两批、四臂、四角色的整体、事实组和情境计数，提供、召回、漏召回、保留、删除均单列。生成脚本仅读取固定 Git 对象，逐层核对提供=召回+漏召回、召回=保留+删除，以及每组、每情境加总。可在已获取两个固定提交的仓库运行 python -B scripts/research/render_owner28_comparison.py --out <空目录>。 [分层计数 CSV](benchmark_v01/BENCHMARK_V01_COUNTS.csv) · [5090 聚合 JSON](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/670d9ab0e546d46117bf5c48ebb2b0043689f453/docs/paper1/dual_machine/repro5090/owner28_eval/OWNER28_EVAL_SCORE_AGGREGATES.json) · [5090 评分 Manifest](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/670d9ab0e546d46117bf5c48ebb2b0043689f453/docs/paper1/dual_machine/repro5090/owner28_eval/OWNER28_EVAL_SCORE_MANIFEST.json)

## 失败图谱

下表按 B2 → RD_ZH 排列。S7 场景和跨场景的伪造新版类型使用各自分母。S3 的两批构造也不同，分栏保留原定义。

| 情境或类型 | Owner27 DEV | Owner28 EVAL | 适用与限制 |
| --- | --- | --- | --- |
| S1-NO-POISON-CLEAN-LOSS | P 0。C 误删 16/18 → 16/18 | P 0。C 误删 8/20 → 12/20 | 无毒环境的正常证据损失。固定候选条件下可直接观测。 |
| S3-SCOPE-SWAP-NOT_DETECTED | 该 S3 无 P，HN 误删 0/10 → 6/10 | 范围互换 P 保留 4/4 → 4/4。S3 的真实他范围 HN 误删 5/8 → 6/8 | 区分合法其他范围与错误范围替换。同编号的情境构造不同。 |
| S5-NEAR_DUPLICATE_EASY | P 保留 2/12 → 0/12 | P 保留 0/12 → 0/12，C 误删 0/8 → 0/8 | 近重复条件较容易，单独展示会掩盖改写协同失效。 |
| S6-PARAPHRASE_COLLUSION | P 保留 5/12 → 2/12 | P 保留 10/12 → 4/12，C 误删 3/8 → 7/8 | 改写协同仍留 P，进一步删除伴随 Clean 损失。 |
| S7-FORGED_VERSION | S7 P 保留 3/4 → 2/4 | S7 P 投放 8、召回 6、漏 2，保留 6/6 → 2/6。跨情境伪造新版类型投放 10、召回 8、漏 2，保留 8/8 → 3/8 | 伪造版次与合法旧版需按证据时点判别。两个 EVAL 分母不能互换。 |
| S8-5_OF_5_MINOR | 计划 5/5 的 2 世界实际只达到 3/5 和 4/5，真实 5/5 未覆盖 | 实际 5/5 共 2 世界，P 保留 8/10 → 2/10。S8 全层 P 保留 13/18 → 5/18 | 全部召回内容均为 P 的边界仅覆盖两世界，未测最终回答与拒答。 |

EVAL 合法历史 HN 误删 2/12 → 4/12，合法异范围 HN 误删 5/8 → 6/8。DEV 对应为 3/23 → 7/23、1/10 → 6/10。DEV 封存 trace 显示较大簇分支从 9/32 增到 30/32，21 个世界的 n_adv、Stage 2 相似对选择与掩码随之改变。EVAL 公布的角色盲掩码和评分汇总支持同方向的删除权衡，未在 5060 用私有标签重算逐世界机制归因。 [DEV 匿名失效图谱](OWNER28_DEV_FAILURE_ATLAS.md) · [5090 公开评分报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/670d9ab0e546d46117bf5c48ebb2b0043689f453/docs/paper1/dual_machine/repro5090/owner28_eval/OWNER28_EVAL_INDEPENDENT_SCORE_REPORT.md)

## 证据边界

- EVAL 的冻结日期正则在 352 个语料段及 160 个检索段中分别命中 0/352 和 0/160，DATE_ONLY 与 NONE 的掩码 32/32 相同。本批没有有效强时效基线。
- DEV 联合收据臂与去 scope 臂掩码完全一致。代理收据来自造数者，对已召回 C、HN、P 的覆盖分别是 30/63、25/33、0/45，并携带已知版本、范围和规范值等侧信息。该比较无法识别 scope 的独立贡献，联合与同预算简单收据规则的 C 误删都是 29/63。 [收据审计](OWNER28_RECEIPT_PROVENANCE_LEAKAGE_AUDIT.md)
- Human Gold 为 0，两批均为 Agent 暂定评分。检索层与过滤层的描述统计可审计，回答层 targeted ASR、答案准确率和拒答均未测。RAGDefender 作者实验 Claim1–3 保持 NOT_RUN。B2 是固定迁移对照，不能引用为原作者实验复现。 [RAGDefender 原论文](https://ieeexplore.ieee.org/abstract/document/11391803)
- 近邻研究提供比较设计参考。FreshQA 评估动态事实与错误前提的问答，TemporalWiki 利用不同时间快照评估知识更新，FRESCO 研究版本冲突下的重排序。PoisonedRAG 的攻击成功率来自生成层任务，本文候选级过滤数不应与之并表。 [FreshQA](https://arxiv.org/abs/2310.03214) · [TemporalWiki](https://aclanthology.org/2022.emnlp-main.418/) · [FRESCO](https://aclanthology.org/2026.findings-emnlp.54/) · [PoisonedRAG](https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag)

现阶段稿件可报告固定 TopK5 代理语料上的两批迁移权衡，以及可复查的正常误删、范围和版本失效。结论限于所观察的 8 个事实组、6 条谱系和各自的代理条件。优先补独立人工裁决、有效时效基线及回答层证据。 [Owner29 预注册草案](OWNER29_STRONG_BASELINE_AND_RAG_PREREG_DRAFT.md)
