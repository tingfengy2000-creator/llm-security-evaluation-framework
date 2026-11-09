# 5060｜Owner19 S1-B 可行性数据准备与封存

2026-11-09 JST · `FEAS_DATA_READY / PROVISIONAL_GOLD / EVALUATION_NOT_RUN / S2_S5_LOCKED / AUTO_CONTINUE=NO`。Run `W1-5060-S1B-FEAS-DATA-PREP-20261109-01`。本批交付数据和预注册协议，尚无新数据上的方法性能。

## Context Recovery / 风险核查

Paper 1 当前目标是以有界研发判断中文 RAG 隐蔽事实投毒防御的可行性，长期优先 RAG Security，再到评估平台、Guard 和 Agent Security。读取 AGENTS、Context Authority Map、PO-MHEP、状态／决策／实验账本、R1/R2、Owner18 和 Owner19 合同。历史 S1 `S1_FAIL_STOP`、R2 `K1-C`、Owner18 暴露开发结果和 P0 信任门照旧。经 Git preflight，5060 发布检出从 `33d67cfbdbc93b90bdcfa27241be6539f28c3f14` 快进至远端 `0d09a2575f885307e22a357943e89acae1d57832`，开工干净，无未提交或未推送修改。原 5060 检出分叉，保持原状。授权与 Git 一致。 [Owner19 十二字段授权](../../owner_approvals/W1_5060_S1B_FEASIBILITY_DATA_PREP_AUTHORIZATION_20261109.md)

FORWARD_RISK_REVIEW 与 PAPER_RISK_REVIEW。构造表、源段、问题、暂定标签的物理分件降低输出泄漏，未来预测进程仍须执行白名单和封存门。本次同一 Agent 作者，近重复筛查是词面指标，合成域及显式适用条件会带来偏差。无标题／有标题预先分层，范围同值、重复冲突和跨段证据按独立支持集合处理。同一正文的改写比较只诊断问法，无法单独估计正文表达变化。此数据不能证明正式防御或模型公平泛化。

## 数据与质量

| 层 | 主语义案例 | 实际视图 | 使用方式 |
| --- | ---: | ---: | --- |
| AGENT_GENERATED_PROVISIONAL_FEASIBILITY | 100 | 120 | 70 可回答、30 应 UNKNOWN，另有 20 条问句改写 |
| D1_DEV_EXPOSED | 0 | 0 | 既有开发回归记录，不读原文、不重跑 |
| 历史旧73 | 0 | 0 | 只读验证封存推理输入 SHA 后进行去重，无旧标签读取 |
| PUBLIC_DATASET_PROXY | 0 | 0 | CMRC2018 官方元数据审查，未取数据文件 |

10 类场景每类 10 条主案例（7 可答、3 应拒识、2 条额外改写），覆盖标量、时效、适用范围、否定例外、等价证据、跨范围同值、多段绑定、未证修订、网页导航、重复与冲突。10 个虚构来源家族各 10 条，分布于 4 个主题域。主集 70 条显式文档标题、30 条无标题，避免单一标题模板。20 条从属视图保持原文和 oracle，仅换问法，预先取各类前两条可答例，故不提供拒识改写配对统计。拒识原因分布为证据不支持 19、同范围冲突 6、适用日期无法绑定 2、未证修订 3。

- 120 个唯一视图 ID，100 个唯一主实体及决策情境。按固定种子派生不带组别的 ID，运行时文件只有 `id/query/evidence`。配对关系另封存。
- Unicode 字符与 UTF-8 字节半开区间及原文哈希逐一复核。105 个可接受证据集合、523 个区间检查，含多段绑定和等价证据。裸数值、不同范围的同值、横跨竞争证据的过宽引文均不通过。
- 主集内 4,950 对、与旧73 交叉 7,300 对。去标题与数字后按字符三元组 Jaccard 筛查（正文 ≥0.84，或问句与正文均 ≥0.72），均 0 告警。最大正文相似度分别为 0.0600 和 0.1081。未进行 D1 原文查重，跨真实分布的语义去重未证。
- HFL 固定版本 `137f2c45a24275fb68f6961c4d357f46288886aa` 元数据标明 CC BY-SA 4.0。CMRC2018 的中文抽取题与 `answer_start` 适合辅助跨度或领域外诊断，缺统一版本、生效范围和可信来源标注。本批未做逐文件获取准入，数据文件传输 0 字节。未来若纳入，须另列来源层、保留署名并核对相同方式共享条款。 [HFL 固定元数据](https://huggingface.co/api/datasets/hfl/cmrc2018/revision/137f2c45a24275fb68f6961c4d357f46288886aa) · [作者论文](https://aclanthology.org/D19-1600/)

## 封存与测试

私有文件在 D 盘 `experiments/paper1_chinese5060/W1-5060-S1B-FEAS-DATA-PREP-20261109-01`。运行输入、暂定 Gold、真值与配对、来源与协议、原始构造材料分别存放并生成五份 ZIP。哈希及覆盖汇总在[脱敏 Manifest](W1_5060_S1B_FEASIBILITY_DATA_PREP_MANIFEST.json)。同一保管环境内的文件隔离不等于独立人审或 OS 账户隔离。标注等级 `AGENT_GENERATED_PROVISIONAL_FEASIBILITY / NOT_INDEPENDENT_AUTHOR / NOT_HUMAN_GOLD`，Human Gold 0。

- 总封存 SHA256 `531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`
- 输入 SHA256 `bd2bc5e6586789070c20dde123bfe72843181aa861aca229fdb0c23091328dee`
- 暂定标注 SHA256 `8f745f921424c6e61357ec19800bc4a1f198e92a26d36377a3a238d634598371`
- 评分协议 SHA256 `43d4d22770f5887058fabfc0162368e77cd36bd6c7d85d846417789515f5341e`
- QA ZIP SHA256 `5f9f7f7b5f3e1a0d3a1af2b27530a2fa161c4c325178e85e5c1a3a596cd831e7`（27 个日志或退出记录）

用本机既有 Python、D 盘 TEMP/TMP 和 `-B` 执行 `python -m llmguard.domains.retrieval.hidden_poisoning.chinese5060.s1b_feasibility_data seal --root <private-root>`，封存代码 Git `ba198c7e5c4185a3b852271aee9a86b48f8f9be1`。新版校验 `verify --root <private-root> --seal-sha256 <receipt>` 对原封存逐字节重放通过，错误回执拒绝，Git `7581256c601ca2f0ed4cfcc17eb3833eeb2dcbd7`。首轮预检捕获 1 个超额配对视图，按预设配额删除该视图；一次 shell 转义错误和初版 MyPy 类型名冲突均留档。最终 5 项单测、Ruff、MyPy 通过。原 seal 保持原字节。

## 后续一次性规则评价审批卡（草案，尚未获批）

- 候选 Run 类型 `ONE_SHOT_FEASIBILITY / NOT_INDEPENDENT_AUTHOR`。冻结 Rule-V1 `68d34a5d877206f4e6d7d9e2bdda16784145a76a` 与 Rule-V2 `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`，两臂读取同一 120 条角色盲输入。待冻结共同适配器、运行环境、只读白名单、输出格式和独立评分执行角色后，再申请一次授权。
- 两臂先封存全量输出，然后评分侧解锁暂定标签。100 个主情境为主分母，20 改写独立配对汇报。保留原参照门值命中／有答案 ≥90%、错抽／已决定 ≤2%、禁止全 UNKNOWN。另报 wrong/total、覆盖／拒识、严格范围／跨度正确性、应拒识误答、未证新版与跨范围误答、Wilson 95% 区间和技术失败。未证修订／跨范围零误答仅为拟议附加 guard。
- 等价证据按集合间 OR、集合内 AND 判定，候选引文全部位于同一个允许窗口，并覆盖所有绑定线索。跨段必须覆盖两处连接键。禁止用标签回填适配器缺字段，禁止结果后改标签、重选、重试或调参。以后 UIE/Qwen 公平对照须另封存新数据。
- 本批新规则预测、评分、揭盲、新模型下载／安装／加载／推理、模型 API 调用、费用均为 0。S2–S5 锁定，正式 ASR/Accuracy 未测。Owner 决定只覆盖数据准备。

收口同步 Human／Agent Ledger、Current Work State、Project Master、Experiment Master、Research Execution Log 与 Week 1 Tracker。既有 Owner 登记保留，本批无新增授权。没有阶段变更、验收知识提升、冻结研究路线或 README 导航变化，Stage Process、Lessons、Plan 和 README 不增改。完成发布后停止。

## DOCUMENTATION_CLOSEOUT_CHECKLIST

```text
human_ledger_checked=true
human_ledger_updated_if_required=true
agent_ledger_checked=true
agent_ledger_updated=true
current_work_state_updated=true
execution_log_appended=true
experiment_master_condition_evaluated=true
owner_decision_condition_evaluated=true
stage_process_condition_evaluated=true
lessons_condition_evaluated=true
research_authority_condition_evaluated=true
README_condition_evaluated=true
cross_document_current_task_consistent=true
cross_document_status_consistent=true
cross_document_next_action_consistent=true
cross_document_blocker_consistent=true
markdown_links_valid=true
```
