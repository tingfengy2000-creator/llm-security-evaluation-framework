# D1探索诊断文档与核验收口 V1

2026-10-27；PODR-143/OR-097/REL-2026-0112。
[任务事实](PAPER1_D1_EXPLORATORY_DETECTION_CLOSEOUT_RECORD_V1.md)，
[状态V18](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V18.md)。

## 状态与完成边界

本次交付是NOT_EVALUABLE诊断及证据/上下文保全，不是有效检测实验完成。
预检漏项导致126条预备OOF隔离；有效评价0/0，不计算实样性能或重新拟合。
8组24条质量排除，40组120条是待审结构上限。状态文件的S切片来自组内Poison证据路径；
对C/HN只是同组三元组分层参考，不表示它们拥有污染等级。
HUMAN_DECISION_REQUIRED / Auto Continue=NO，下一步Owner语义/材料门，不擅自修题/规则。

## 文档矩阵

| 文档 | 判断与处理 |
| --- | --- |
| Human Ledger | 必须更新：用中文说明不可测、非零检出率及预检漏项 |
| Agent Ledger | 必须更新：输入SHA、真实预备运行、隔离及缺口 |
| Current Work State | 必须更新：最新D1门及D2/D3独立原门 |
| Research Execution Log | 追加REL-2026-0112，不改旧记录 |
| Experiment Master | 必须更新：OR-097区分隔离预备运行和有效评价 |
| Owner Decision Register / Owner Register | 仅登记明确批准的开发范围，不把QA/HOLD决定写成已接受GT |
| Project Master Context / Stage Process | 必须更新开发暴露、停止原因与下一审批门 |
| Research Plan Authority | 只追加Owner明确D1_DEV_EXPOSED和不得未来称untouched；正式划分算法/路线不改 |
| Canonical Lessons | 暂定质量门经验，不升级为新标注规则 |
| Paper1/Core144 README | 最新状态导航；旧日期历史保留 |
| Long-term requirements / Guide / schemas | 不改：长期目标、字段和枚举未变 |

## 核验结果

最终Run03：64项工件/工具核验通过，其中任务及相关合成测试42项通过；
任务三文件Ruff/MyPy、UTF-8、新增公开内容secret/private-path及Markdown链接检查通过。
原三输入、原144身份源、旧46/46/50份D1证据和55份D2封存内容复验不变；
Stage1–5/Final72、Guide/schema及D2/D3 Candidate/Evidence未修改，私有输出Git-ignore通过。
没有实样性能计算；合成测试中的虚构指标仅验证计算函数，不是D1结果。

扩展治理/架构检查57项为51通过、6项历史静态文档失败；相同6个failure ID已在
source HEAD892915a的只读Git正文投影上复现，0新增失败、0 errors。
原失败及基线日志保留，不改历史字节或重算旧hash，不声称全仓/全部治理测试绿色。

初次验证脚本遇D2索引字典/列表形状差异而中止；其局部checks字段为true不代表完整通过，
失败文件保留，Run03为最终结果。第二次确实检出Master Context缺显式NOT_EVALUABLE码，
补齐后重验。首次MyPy缺第三方stub及Optional缩窄失败，仅添加精确import-untyped声明和
等价局部类型缩窄；执行时源代码已先按原SHA存档，没有据此重跑模型或改变阈值/配置。

DOCUMENTATION_CLOSEOUT_CHECKLIST、CONTEXT_PERSISTENCE_CHECK及PAPER1_DOCUMENT_STALENESS_GATE：PASS。
Human/Agent/Current/Execution/Experiment/Owner/Stage/Authority/README按上表条件同步；
当前任务、NOT_EVALUABLE、Owner质量门、禁止项和D2/D3原门一致。
私有索引封存及交接/Git回执见本轮post-seal记录；Git动态值最终单独复验。

私有75份工件封存索引`EVIDENCE_INDEX_V1.json`，SHA256
`546089be0e1e2ac4d80dd48c38f1152b19ededbc828d26556cb70a5f753f6c38`。
该索引保留封存时公开文件摘要；本段索引引用属于post-seal文档追加，不回写原清单。

不宣称全仓测试通过；原拟合stdout/stderr未独立存完整文件的复现缺口明确保留。
任务私有证据索引、逐项验证、命令/退出码和交接/Git回执独立存放；不把后续回执写回原锁。
原有无关design修改及未跟踪PDF保持原SHA、不纳入本次提交，不能虚报全工作树clean。

## 上下文恢复清单

- 唯一当前任务/状态/源HEAD、批准与禁止项：协议、记录、Current State和V18。
- Owner决定与理由：PODR-143 / OR-097；12字段blocker随私有证据保全。
- 可宣称：输入核验、质量阻断、隔离运行、可测条件缺口；不能宣称任何检测率/优越性/长上下文收益。
- Formal experiment：Core正式GT/2/1/1未执行；D1已开发暴露，D2/D3不随诊断改写。
- 下一步：P1-D1-QUALITY-HOLD-CLOSURE-AND-D1-SEPT-MATERIALIZATION-01只是建议，未启动。
- Git同步与私有索引：以本轮实际回执为准，不能用静态源HEAD代替提交后动态Git事实。
