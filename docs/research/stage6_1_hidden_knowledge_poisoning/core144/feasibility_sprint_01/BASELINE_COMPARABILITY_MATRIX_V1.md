# 历史基线与新对照比较边界 V1

## 最新同骨干完整开发对照（2026-11-03）

| 条件 | Run | Recall | Clean FPR | HN FPR | 弃权 | Strict |
| --- | --- | --- | --- | --- | --- | --- |
| E1/E2（各自） | D1-DEV-BEIJING-CONT-A01 | 37/40 | 0/40 | 1/40 | 13/120 | 30/40 |
| E3/E4（各自） | 同上 | 0/40 | 0/40 | 0/40 | 120/120 | 0/40 |

结论CONDITIONAL：直接API有效开发观察，新增机制未证。新E1与旧7B/规则/OOF-LR的模型、提示和计算不同，差值不能当算法贡献；E3/E1输出预算也不同，未做计算匹配消融。
[完整报告](FEASIBILITY_OWNER_REPORT.md)。下表NOT_RUN保留为最初冻结时的历史状态，不是当前结果。

以下是原已报告开发结果，未在本轮重新运行、校准或改变阈值。全部不能当独立测试。

| 方法 | 原Run ID | Recall | Clean FPR | HN FPR | 比较边界 |
| --- | --- | --- | --- | --- | --- |
| TF-IDF+LR | D1-FIRST-DETECTION-20261028-R01 | 12/40 | 3/40 | 7/40 | 家族OOF，二元，固定0.5，无三态/同API成本等价 |
| SEPT21+LR B1 | D1-FIRST-DETECTION-20261028-R01 | 20/40 | 18/40 | 15/40 | 浅层特征OOF；不是新API关系核验 |
| A0-original | VACE-LITE-R1-20261028-R01 | 16/40 | 0/40 | 3/40 | S1为12/12，但有关键词捷径与合法HN误报 |
| VACE V0.3-F5 | vace_v03_f5_20261028_run01 | 6/40 | 0/40 | 0/40 | 114/120弃权，Strict0/40，零FPR不等于有效检测 |
| L0-F5 | VACE-L0-D1-20261030-FULL01 | 5/40 | 1/40 | 1/40 | 旧Qwen2.5-7B，完整Top5；与新API差异含骨干 |
| L0-Oracle | VACE-L0-D1-20261030-FULL01 | 14/40 | 4/40 | 2/40 | 人工E1/E2参考输入，只能诊断，不是部署比较 |
| Oracle ClaimAligned | VACE-L0-D1-20261030-ORACLE-ALIGN01 | 15/40 | 6/40 | 5/40 | 单次提示负结果，不追加旧L0提示 |
| E1/E2/E3/E4 | NOT_RUN | null | null | null | 新同精确API骨干；优先用于组件/贡献比较 |

V03 Run标识已核对本机原`PROTOCOL_FREEZE_V1.json`的run_id；该冻结文件SHA256为`4f347f7b47a8cdbe6fbb7941e1dc379fb7bec84b27ed01d4cf32a1e895814c9f`。
对应[原执行记录](../vace_lite/VACE_V03_F5_EXECUTION_PROTOCOL_V1.md)及[结果](../vace_lite/VACE_V03_VS_BASELINES_COMPARISON.md)保留不改。
其他来源：[首轮结果](../PAPER1_D1_FIRST_DETECTION_RESULTS_RECORD_V1.md)、[A0记录](../PAPER1_VACE_LITE_R1_RECORD_V1.md)、[L0收口](../l0_closeout_20261031/README.md)。
历史行属于Our Development Result，不是Published Result或外部Reproduced Result；本轮没有外部论文复现数。
共同样本与正文身份不等于相同FPR/模型/训练成本。主要方法判断必须用E3-E1，机制归因分别看E2-E1、E3-E2及预算允许的E3-E4。
