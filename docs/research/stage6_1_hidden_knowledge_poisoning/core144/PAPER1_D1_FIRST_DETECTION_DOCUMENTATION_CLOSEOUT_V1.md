# D1首轮开发检测文档收口 V1

2026-10-28；PODR-146 / OR-100 / REL-2026-0115。
[结果](PAPER1_D1_FIRST_DETECTION_RESULTS_RECORD_V1.md)，[状态V21](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V21.md)。

## 完成上限

40组120条D1_DEV资格真签核验；四条件各13-family-fold120新OOF，480预测锁后才做角色/S评价。
8组24条HOLD、原Oracle21 BLOCKED。结果包含真实低分/高误报、Wilson和2000家族bootstrap。
没有Core正式GT/split或D2D3修改，无阈值调优、校准、Stage B、新数据/模型下载。
下一原子/版本表示审计只建议，未启动。

## 条件式文档矩阵

| 文档 | 判断与动作 |
| --- | --- |
| Human Ledger | 必须更新：真实检出率/误报、为什么高S3不能说有效、下一方向 |
| Agent Ledger / Current State / Execution Log | 必须更新：实际签署、source/预测seal、运行与失败记录、停止边界 |
| Experiment Master / Owner registers | 条件成立：签署准入、独立消融执行、真实结果与证据 |
| Project Master / Stage Process | 条件成立：由未签停止进入已测开发结果；非正式结果 |
| Paper1 / Core144 README | 条件成立：新结果和V21导航 |
| Research Plan Authority | 只追加已批合同执行状态，消除未签入口歧义；不改冻结主线/Guide/正式split算法 |
| Canonical Lessons | 无新accepted规则；稀疏T缩放/Oracle比较/浅层表示限制作为本轮provisional观察，不机械改canonical规则 |
| Long-term requirements / V4–V4.3 /真实Candidate / Human Excel /原始Evidence / D2D3 | 不改 |

## 真实执行与验证

主执行源码512842944fbbe73a0f7ca1de35536182589a2c5f；签署输入来源b559dee，协议冻结a34fa0f。
首尝试在fit前JSON list/tuple断言停止；纯工程修复后重启，未重跑完成模型追分。
后验QA脚本首次误用Counter(mapping)导致自身比较失败，V1源保留，V2改为keys；模型/预测未改或重拟合。
468项任务工件/身份/逐折/独立计数与模型回读检查PASS，41项任务单元测试PASS，Ruff/MyPy PASS。
保存commands/stdout/stderr/exit；初始pytest cache权限警告以no-cacheprovider重验消除，不掩盖原提示。
模型52主+13固定置换；所有主模型分数从保存件逐折精确回读匹配；原153文件seal逐个复验不变。
只声称任务范围验证，不宣称整个仓库所有历史测试全绿。

实际交接沿用原文件名，另存命名未发现；Owner更新后三确认/署名/日期通过，未由Agent重存。
中间提示语状态没有raw字节归档，只保留工具观察，不倒造raw。签署日期为2026-10-28，不按旧文件名倒填。

CONTEXT_PERSISTENCE_CHECK / PAPER1_DOCUMENT_STALENESS_GATE / DOCUMENTATION_CLOSEOUT_CHECKLIST
及UTF-8、标签输入、secret/private-path、新链接、Git-ignore、保护文件/diff由私有最终回执逐项记录。
原design.md与Master Guide PDF无关本地改动保留，不宣称整树clean。
Git/交接回执以实际提交后动态核验为准，不用本文静态HEAD伪称最终同步。

## 最终私有封存

任务工件QA468项、文档/新内容/链接/UTF-8/secret/私有路径/Git-ignore等301项，required_failed=0；
41项任务单元测试、Ruff、MyPy、git diff --check PASS，旧153文件复验不变。
非自引用149文件索引`experiments/core144_d1_first_detection_20261028_run01/EVIDENCE_INDEX_V1.json`，SHA256
`a18c2afaed310f02472fe16971b3c1e6a6edb6a620a6f50e1ab19afc40a64972`。
复现manifest SHA256：`14e77c4c3f34c8000969fdd53ad8a089bfc7b61960332e7935daa07c8d9ae777`。
CONTEXT_PERSISTENCE_CHECK / PAPER1_DOCUMENT_STALENESS_GATE / DOCUMENTATION_CLOSEOUT=PASS。
交接命名空间`paper1_core144_d1_first_detection_20261028_run01`；交接/Git回执post-seal追加，不改原索引。
