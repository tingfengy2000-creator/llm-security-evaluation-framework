# D1 首轮开发检测协议 V1（拟合前冻结）

2026-10-28；P1-D1-DEVELOPMENT-DETECTION-FIRST-RESULTS-01；PODR-146 / OR-100 / REL-2026-0115。
Run ID：`D1-FIRST-DETECTION-20261028-R01`。输入来源提交b559dee013e933ec1384a84d9df388693d3a5f72；
实际执行代码提交由拟合前独立source lock记录，不能将输入来源冒充执行提交。

## 资格与原件

Owner真实将签署页C13/C14/C15填写为“确认”，C17署名、G17日期2026-10-28。
实际更新的是原交接文件名D1_OWNER_FINAL_DECISION_REQUIRED.xlsx，不是最初报出的另存文件名；
记录此识别差异，不伪称找到了不存在的文件。对比D盘未签模板，只有上述五格逻辑值变化，
其余三页单元格值/公式、顺序和合并区域不变；原件未由Agent重存。
签署原件SHA256：`35609f9ea3fa5fad2fca440dab6b16e57c2bc7954b53d0381ac9cae114049b5d`。
原模板SHA256：`a6cbeba4d6b8ff5491d5449e318f14f4f69b69cc209e555d9348aaeddd864ec8`。
曾观察到三格仍是提示语的中间状态，未接受；Owner再次确认保存后重新读取并通过。
中间状态没有原始文件归档，不把工具观察冒充字节锁定。

本签署仅接受D1_DEV评价资格及适用规则QA，不是Core144正式GT：40完整组/120条/13事实家族，
8完整组/24条继续HOLD。有效Poison分母S1=12、S2=15、S3=13；负例80。
119条二元标签来自Owner接受的Human A/B一致判断，1条来自签署的规则核验QA。
S由获准的独立证据路径恢复；不以target S反推。构造角色在预测锁后才关联评价。
HOLD-only建议和0028两项空值不强行生效，不要求54条全部重做。

## 固定条件与训练

| 条件 | 输入 | 角色 |
| --- | --- | --- |
| A | Candidate-only中文字符2/3-gram TF-IDF | 文本基线 |
| B1 | 非Oracle SEPT21：S3/E9/P6/T3 | 保留原V1.1 |
| B2 | 非Oracle SEP18：S3/E9/P6 | 新增V1.2-DEV消融 |
| C | Oracle SEP18，同B2列序/定义/处理 | ORACLE_ONLY诊断 |

原Oracle SEPT21仅做预检，不拟合：留出女性劳动保护家族时三项T训练列全空。
不改原Feature Set/Extractor/历史；SEP18是诊断T不可观测性的独立开发配置，不是正式替换。
非Oracle输入来自此前已锁定的Q_NO_TITLE + equal-weight HYBRID + Top5 + Registry V2路径。
不新增来源、模型、下载、安装；R不进入Stage A。

- 留一事实家族交叉验证13折；同group/family不跨训练与验证，每条恰好一个新OOF。
- TF-IDF：char(2,3)、lowercase=False、min_df=1、max_df=1.0、sublinear_tf=True、norm=l2。
- LR：L2、C=1、liblinear、balanced、max_iter=2000、random_state=20261027。
- 二元14列：训练折众数，不缩放。连续列：训练折中位数后StandardScaler；无missing indicator。
- 缺失/不适用不代表安全，不任意填0；训练统计众数合法等于0不等于语义指定SAFE=0。
- 每折先核训练列全缺失；不合法仅阻断该条件，不临时删列、调阈值或改变填补合同。
- 固定阈值0.5，概率未校准；AUROC/AUPRC用raw decision score。
- 主报告方法事前指定B1合法则B1，否则B2，否则A；不按最高分挑选。
- Oracle收益只作同列B2与C配对对比；不能B1减C。

## 锁定顺序与复现

签署/标签资格 → 输入与配置SHA锁 → 逐折预检 → 代码提交/source lock → 训练 →
不带角色/S的预测SHA锁 → 评价进程才读构造角色、derived S、Oracle参考作分析。
训练只读取sanitized文本/数值列、split-only索引和获准training-target vault；
ID/family只索引，不进入模型。旧126条隔离OOF永不打开或复用。
保存每折joblib、统计量、系数/迭代数、输入/代码/运行SHA，不称FINAL MODEL。
本机sklearn1.7.2 / numpy2.3.5 / scipy1.16.3 / joblib1.5.2，Python3.13.9。
私有命名空间：`experiments/core144_d1_first_detection_20261028_run01/`，不进公开Git。

## 评价与不确定性

每条件报告S1/S2/S3 TP/N、总体Recall、Clean-FPR、HN-FPR、AUROC/AUPRC；
小样本率附Wilson 95%区间，另以13事实家族为单位2000次bootstrap，seed20261027、各条件相同抽样。
bootstrap仅重采样pooled OOF，不重拟合，属于开发性不确定性，不是正式泛化区间。
仅存在的分母计数；无合法条件/分母记BLOCKED/NA，不写0。
预先固定A条件一次组内三元组随机正例置换控制，seed20261028，不参与选模。
AUROC或AUPRC≥0.95时另做高性能shortcut审计；高分本身不构成有效性证据。
AUROC用正负配对独立核算、AUPRC按distinct score阈值重新核算，避免只复述同一计算函数。

## FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW

本轮仅13家族/40组，特征相关、小样本、证据语料简单、自然词面与missingness可能形成捷径；
家族隔离/无标签特征/冻结配置/控制实验降低风险但不能证明无全部confounder。
S是bigram相似度、E为浅层数值/否定等启发式；Oracle是当前冻结packet参考，不是唯一合法证据真值。
已知Dense文档编码截断128 tokens，不等于已证实关键事实截断或长上下文LLM能修复。
失败先区分参考召回、事实表示、版本关系、模型判别；不能确定因果时写UNRESOLVED。
即使C差也不能直接宣布推理模型失败；C仍受同一浅层Extractor限制。
不因为结果差重训调参；不因为结果好宣称SOTA、显著优越、可部署或正式泛化。

## 停止边界

`D1_EXPLORATORY_DEV_DIAGNOSTIC / D1_DEV_EXPOSED`。
D1真实Candidate、Evidence、Human raw、D2/D3数据不变；不执行Core正式GT/2/1/1 split、
校准、Stage B训练或新科研任务。完成结果和文档/Git收口后STOP。
