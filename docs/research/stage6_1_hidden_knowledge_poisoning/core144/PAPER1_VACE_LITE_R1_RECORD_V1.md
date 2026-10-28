# VACE-Lite R1：S1表层捷径已测，方法规格仍待Owner审阅

2026-10-28；PODR-147 / OR-101 / REL-2026-0116；Run `VACE-LITE-R1-20261028-R01`。
[预注册规则协议](PAPER1_VACE_LITE_R1_A0_PROTOCOL_V1.md)，
[V0.2候选规格](vace_lite/VACE_LITE_V02_METHOD_SPEC.md)，
[基线与评价计划](vace_lite/VACE_LITE_BASELINE_AND_EVALUATION_PLAN.md)。

## 实际完成与结果

完全相同的签署D1_DEV：40完整组/120条/13家族，S1/S2/S3正例12/15/13，C/P/H各40。
8组24条继续HOLD。两套规则分别冻结后，单次确定性预测240条，封存后才关联标签/S/历史同120 OOF。
未使用旧126池，不训练，不称A0为OOF。

| 规则 | S1 TP/N及Recall | S2 TP/N及Recall | S3 TP/N及Recall | 全Recall | Clean-FPR | HN-FPR | Precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0-original | 12/12，100% | 0/15，0% | 4/13，30.77% | 16/40，40% | 0/40，0% | 3/40，7.5% | 16/19，84.21% |
| A0-general | 10/12，83.33% | 7/15，46.67% | 1/13，7.69% | 18/40，45% | 6/40，15% | 5/40，12.5% | 18/29，62.07% |

仅二元cue flag，AUROC/AUPRC为NOT_REPORTED_BINARY_ONLY，不制造连续风险或填0。
原三句式严格是“既…又/也”“同时又/又是/又享有/同时允许”“同一”；无新增词语。
评委未给执行源码，故声称句式忠实转写，不声称代码字节级复现或匹配旧126统计。
general六类只写一次，无漏报补词、无合并取最佳。

原规则S1的12/12中，8/12有O1/O2组合线索，4/12只因“同一”；
这说明模板风险，不等于正则证明了同主体/同条件矛盾。合法HN同cue3/40、Clean0/40；
S1组内HN误报2/12=16.67%，不能将全HN7.5%冒充S1约束。
原规则P>C win/tie/loss16/24/0，P>HN13/27/0，三元组严格最高13/40；
general为12/28/0、13/27/0，严格最高11/40。tie不算win。
每规则O1/O2/O3的P/C/H命中为4/0/0、6/0/0、13/0/3；有重叠，不能相加算总命中。
general G1–G6命中分别9/0/0、5/0/0、2/0/0、3/1/1、2/2/3、6/3/2。

原规则S1 Wilson95为75.75–100%，总Recall26.35–55.40%，HN-FPR2.58–19.86%；
general S1为55.20–95.30%、总Recall30.71–60.17%、HN-FPR5.46–26.11%。
2000次家族bootstrap/seed20261028仅开发描述；原规则S1为100–100%的经验退化区间，
不能推断未来不确定性为零，必须同时保留Wilson。

## 与历史方法的公平范围

历史A/B1/B2/C仅引用同120条、同文本SHA的既有OOF，不重训。A的总Recall30%/HN-FPR17.5%，
B1=50%/37.5%，B2=52.5%/45%，C=57.5%/40%；操作点不同，不能仅凭A0高Precision称其全面优于所有模型。
A0对S1很好，但S2原规则0/15；不能把S1词面提升当新方法贡献。

## 候选方法与论文定位

Owner暂定贡献：版本化困难负样本基准＋分层失败归因＋轻量命题—证据核验。
六槽位为主体、关系、数值/单位、范围、时间/版本、来源/机关角色。
Candidate→提取→独立可信Top5→同范围/版本对齐→SUPPORT/CONTRADICT/INSUFFICIENT→分流。
INSUFFICIENT不转成Poison/Clean。相对正则和同证据L0的能力只是假设，未运行VACE或新模型。
L0/L0-Oracle、slot抽取参考、资源/模型/提示/上下文锁、HN≤10%/20%操作点及复核预算均为后续门。
没有新slot标签，不能用AI自评当gold；不单独声称中文、NLI或命题分解创新。
当前120条40–68字符、中位数55，是短候选命题；长文档嵌入仅后续独立条件。
V0.1全文未找到，V0.2依据Owner本轮要求及原外部意见新增，不伪称旧稿全文redline或外部文献已独立核实。

## 私有证据与停止

私有根`experiments/vace_lite_r1_20261028_run01/`，交接命名空间`paper1_vace_lite_r1_20261028_run01`。
五主文件为A0_D1_SURFACE_BASELINE_RESULTS.csv、A0_D1_S1_TEMPLATE_SHORTCUT_AUDIT.md、
VACE_LITE_V02_METHOD_SPEC.md、VACE_LITE_BASELINE_AND_EVALUATION_PLAN.md、VACE_LITE_OWNER_DECISION_REPORT.md。
逐ID/逐规则命中、S1签名、合法HN语义、置信区间、外部raw/代码/配置/锁/日志/manifest均保留私有。
规则与预测源提交b5064ef4d0e9fccabd904fad14ec2bd7bd2fb941；预测240条SHA
`50b5426c196d4d13f26dcaed5d140777656a38978c91ce23497dd49a6897a8a2`。
数据/原答/Evidence/Guide/Stage1–5/Final72/D2D3不变；无训练、VACE、L0、Core GT/正式split或校准。
`VACE_LITE_V02_OWNER_REVIEW_REQUIRED`，完成文档/Git后STOP。

[文档收口](PAPER1_VACE_LITE_R1_DOCUMENTATION_CLOSEOUT_V1.md)：757项任务QA、52项测试、Ruff/MyPy/diff PASS。
私有61文件索引SHA67014299e842d7768c8d82fe80df1625d86b13bc87627e10abde2370744acdf4；
manifest SHA8698edc5e37823e072fb4c0bcc6afc330150f8797722ffee592690ad2b8ccdfa。
Git/交接回执追加，原无关design/PDF保留，不声明全工作树clean或全仓历史测试全绿。
