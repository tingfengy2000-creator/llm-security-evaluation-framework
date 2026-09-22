# Paper 1 Final72 V1.1 Document Detector 原型报告

Status: `DEVELOPMENT_FINDING_ONLY / MULTIVIEW_SIGNAL_MIXED / PROTOTYPE_VALID_WITH_LIMITATIONS` (2026-09-22).
Task: `P1-FIRST-DOCUMENT-DETECTOR-V1_1-LOGO-PROTOTYPE-EXECUTION-01`.
冻结协议：[V1.1](PAPER1_FINAL72_DOCUMENT_DETECTOR_DEVELOPMENT_PROTOCOL_V1_1.md)。原始运行与逐文件 SHA 清单位于 Git 外 `paper1_final72_document_detector_v1_1_logo_20260922`；`result_hash_manifest.json` SHA256 `e788af67ee1a67d8635ddb11a9a27fee3d7c89009a87bb3d1788ddfd90737af`。预拟合代码 commit `d9956c44f7e9eec03201a227416cc44d6c78d14c`。本报告中的每个性能数都是 **Final72 development-set OOF diagnostic**，不是正式论文结果。

## 这次实际训练了什么，为什么用 LOGO

首次实际拟合的是固定 L2 Logistic Regression（`C=1`, `liblinear`, `max_iter=2000`, `class_weight=balanced`, seed `20260922`），没有调参或校准。训练输入只有非 Oracle 的 Semantic 3、Entity-Claim 9、Provenance 6、Temporal-Version 3 共 21 项；R 属于另一个 Stage B，六项 Oracle-only T 信号及两项不可观测的 Provenance 关系未进入。后两项并非因为分数低才删除：它们在原 V1 中 72/72 全缺失，缺少有证据的候选级语义；旧 23 列与 blocker 原样保留。

72 条只形成 24 个独立版本链匹配组，每组 Clean、Poison、合法历史 Hard Negative 各一。普通候选级随机切分会把同一事实链泄入训练与验证；24 折 Leave-One-Group-Out 每折只留出完整一组（69 训练 / 3 验证），72 条各得一个独立折外分数。每折 imputer 的中位数/众数和连续特征 scaler 只在 69 条训练样本上拟合；没有全局填补、缺失指示器或把 `NOT_APPLICABLE` 强行视为安全。输出的 probability 未校准，0.5 仅为预定操作诊断阈值。

## 九个预先指定模型的开发集对比

| 模型 | 特征数 | AUROC | AUPRC | HN-FPR@0.5 | P>HN | P>Clean | P 三元组最高 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S-only | 3 | .623 | .466 | .500 | 17/24 | 19/24 | 14/24 |
| E-only | 9 | .547 | .373 | .292 | 12/24 | 9/24 | 9/24 |
| P-only | 6 | .462 | .319 | .083 | 2/24 | 0/24 | 0/24 |
| T-only | 3 | .465 | .344 | .917 | 2/24 | 2/24 | 1/24 |
| Full SEPT | 21 | .647 | .496 | .333 | 18/24 | 18/24 | 17/24 |
| Full-S | 18 | .559 | .382 | .417 | 13/24 | 11/24 | 10/24 |
| Full-E | 12 | .592 | .419 | .625 | 16/24 | 18/24 | 13/24 |
| Full-P | 15 | .673 | .571 | .333 | 19/24 | 18/24 | 17/24 |
| Full-T | 18 | .674 | .536 | .333 | 18/24 | 19/24 | 17/24 |

Full SEPT 的 Precision@0.5=.469、Recall=.625、F1=.536、Balanced Accuracy=.635、Specificity=.646、MCC=.257；混淆矩阵 TN=31、FP=17、FN=9、TP=15。24 个 HN 有 8 个被误判为 Poison。负例只有 48 个，1 个 FP 就是 2.0833% FPR，因此 Recall@1%FPR **不可可靠估计**。不插值的 Recall@5%FPR 仅 .083（最多 2 FP），是分辨率粗糙的描述值，不能作为可靠 operating point。

Full SEPT 的 Poison>HN 为 18 胜/0 平/6 负，Poison>Clean 为 18 胜/1 平/5 负；平局不计胜。P−HN decision-score margin 均值 .732、中位 .613、IQR [.079,1.119]；P−Clean 均值 .435、中位 .318、IQR [.019,1.070]。难组为 `EDU-06`, `FIN-03`, `FIN-04`, `HR-03`, `INF-01`, `INF-04`, `INF-05`；具体失误标签保存在 failure-analysis JSON，不因此修改输入。

## 控制、稳定性和科学解释

2000 次匹配组 bootstrap 的描述性 95% 区间：AUROC [.517,.798]、AUPRC [.395,.738]、P>HN [.583,.917]、P>Clean [.583,.917]、P 三元组最高 [.542,.875]。它们是此开发集的不确定性展示，不是总体泛化置信区间。200 次组内“一组一个伪 Poison”置换，仍逐次重新跑完整 24 折：AUROC 均值 .485、AUPRC 均值 .358；观察值的经验 exceedance 分别约 .0249/.0448，仅作 pipeline sanity，不宣称正式显著性。预定的高表现审计阈值未触发；置换异常启发式亦未触发。

24 折均无收敛警告；最大绝对系数 1.279，最大跨折系数标准差 .192；72 个 OOF 概率中 1 个低于 .01、1 个高于 .99。21/69=.304 的特征/训练样本比仍偏高。Full SEPT 的每特征均值/中位数/标准差/正负折数与 view 汇总均已锁存；系数不可解释为因果重要性。特征矩阵无标签、ID 或 group 输入，组未交叉；按类别 missingness 与领域计数已留档。**七项特征在观测值上为常量**，且可信检索库仅 57 文档，可能过易；这两点均是未来正式 Benchmark 的 shortcut/信息量风险，不是本轮可删除特征的理由。

Full SEPT 略高于 S-only，但 Full-P 和 Full-T 的 AUROC/AUPRC 更高，因此本轮不能称“多视角优于单视角”或“Temporal 已降低 HN 误报”。T-only 很弱、Full-T 与 Full 接近：仅三项可部署 T、六项 Oracle-only T、PTS/Registry V2 覆盖有限，不能据此否定 Temporal 思路。P 也只有六项，另两项关系仍待原生采集。结论只能是 `MULTIVIEW_SIGNAL_MIXED / PROTOTYPE_VALID_WITH_LIMITATIONS`：pipeline 有开发集信号，但尚未建立稳健优势或正式泛化。

## 下一步与不可宣称事项

优先推荐单独批准 `P1-DOCUMENT-DETECTOR-FAILURE-ANALYSIS-AND-SCALE-HYPOTHESIS-REFINEMENT-01`，把 HN 混淆、T/P 覆盖、常量信号与易检索库风险变成 240-group 构建假设；不要反复修 Final72 直到变高。未来正式效果须来自 240 独立组、版本链分组且未经开发触碰的 test population。未做 Risk Calibration、Stage B Exposure Risk、XGBoost、MLM/PPL/GMTP、正式 detector 训练或论文结果。Owner 下一门尚未批准。
