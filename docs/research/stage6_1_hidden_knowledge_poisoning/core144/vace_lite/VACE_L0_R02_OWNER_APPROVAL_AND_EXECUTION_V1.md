# L0 R02：合成语义准确率改为诊断，工程硬门保留

2026-10-29（JST）；PODR-153 / OR-108 / REL-2026-0123。
Task `P1-VACE-L0-R02-SEMANTIC-DIAGNOSTIC-EXECUTION-01`；原科学任务仍是同D1_DEV的L0-F5/Oracle强基线。
状态：`R02_APPROVED_EXECUTION_PACKAGE_READY / WORKER_EXECUTION_NOT_OBSERVED`，不是已完成检测。

## 1. Owner本轮决定与唯一科学变更

Owner明确批准：“保持模型、提示词、解析器和证据不变，合成语义准确率改为诊断项，保留工程硬门，运行D1；保留R01全部失败记录和HARD_STOP。”

| 项目 | R01（历史保留） | R02（新Run） |
| --- | --- | --- |
| Run ID | VACE-L0-D1-20261029-R01 | VACE-L0-D1-20261029-R02 |
| 合成语义 | 5题必须全对才继续 | 原题/期望不变，如实报告准确率，不能因判错而拦D1 |
| 工程门 | 设备/CUDA/hash/预算/格式/引用/确定性 | 保留；任何真实工程失败仍停止 |
| 模型/提示/解析/证据/参数 | a83437a冻结身份 | 原身份不变，不修prompt追通过，不按理由改verdict |
| 失败历史 | SYN-3错误、HARD_STOP、无D1预测 | 只读保留；独立目录，不删除旧门或覆盖旧raw |

这是一项**观察过合成失败之后、D1预测之前**的有界门控修订，必须在报告中披露。
不能将R02写成原R01协议已通过，不能删除SYN-3或把其期望SUPPORT改为CONTRADICT。
不能把合成准确率当D1检出率，也不要求R02合成结果比R01更好。

## 2. 控制端已完成的失败证据审查

[失败回包](L0_5090_SYNTHETIC_GATE_EVIDENCE_RETURN_V1.zip) 10,100字节，SHA256
`a56c8b79a0a61879629a305325a7cbf1d0188ad7c73a187e93c31e528be838e6`。
原ZIP/10个原件hash和CRC均通过；空stdout保持0字节；八项原源码/配置身份与a83437a一致。
五题均以冻结纯解析器独立复算，与原记录逐字段相同；4/5语义正确，SYN-3仍CONTRADICT。
SYN-3理由却明确说2010年版内容一致、不存在矛盾；194输出tokens、EOS，既不是截断，也不是解析器翻转结论。
这证明该次输出判决与理由不一致，不足以单凭一题判定完整历史版本能力或D1效果。
非弃权的不足原因填“无”而不是空串是另一个输出合同偏差；原解析器未拦，R02只记录，不新加修复/归一化。
R01保持`L0_STRONG_BASELINE_SYNTHETIC_GATE_BLOCKED`，D1 0/240、指标NOT_MEASURED。

## 3. 严格不变的身份

- 官方Qwen/Qwen2.5-7B-Instruct，revision `a09a35458c702b33eeacc393d103063234e8bc28`，同13文件hash。
- 同R01隔离解释器与pip freeze，Torch2.8.0+cu128 / Transformers4.57.1等实际版本逐项相等。
- 同BF16、SDPA、GPU-only、seed20261029、greedy、batch1、context32768/input31744/output1024、12小时限额。
- 实际GenerationConfig逐字节SHA须等于R01；不能换temperature/top-k策略、模型或量化/CPU兜底。
- `llm_verification.py`整个文件（提示词/消息渲染/解析器/五个合成题）原SHA保持。
- 同签署40组/120条/13家族，8组24条HOLD；原F5顺序与原Oracle E1/E2（含合法空E2）逐文件hash相等。
- 不重新检索、改排序、摘录或标签；不复用旧126预测，也不把构造role作为runtime输入。
- D1仍DEV_EXPOSED，无Core正式GT/split；D2/D3数据与其各自质量门保持独立。

## 4. 最小工程实现

新入口` scripts/research/paper1_l0_r02_worker.py`与固定`worker_policy_r02_v1.json`。
新编排器只读核验原R01回包、实际文件、依赖和模型，从原input按原manifest复制**完全相同字节**到新目录。
无需再传ZIP、下载模型或安装依赖；源码禁止走setup/download，优先使用已核验的R01现有资源。
R02目录不得等于、嵌在或包含R01；只有空新目录（可预建启动cache/temp）或已绑定同一R01的R02续跑目录可用。
原失败文件/输入/日志建立SHA快照，check-only、预测后、评价后、退出时均复验；原HARD_STOP不动。
模型/env仅只读复用，cache/TEMP/PYTHONPYCACHEPREFIX均指向R02；不复制十几GB权重。
预算仍24GiB，并以R01已有占用加R02新增占用保守监控，不以新目录另获24GiB、不换环境。

共用infer的模型加载、生成、输入与逐样本解析逻辑不变；仅从冻结policy选择合成门行为并核验R01生成配置身份。
合成记录同时保存`semantic_all_pass`、`engineering_all_pass`和`execution_gate_passed`：
例如4/5时前者/all_pass仍false，而工程过门且获PODR-153批准时执行门可true。不能把语义失败改写成全对。
固定五题/期望/input hash、解析与引用有效、重复贪婪一致仍是工程要求；非弃权不足原因偏差仅诊断保留。
不使用简单关键词“修正”模型结论，不根据synthetic或D1失误再改prompt。

## 5. 执行与封存顺序

1. 使用Owner提供的**新R02提交SHA**独立checkout；保留R01原源码checkout与工作目录。
2. 启动Python前先把TEMP/TMP/PYTHONPYCACHEPREFIX重定向到R02，避免解释器启动向R01环境写cache。
   `--check-only`核R01十原件、模型/env/CUDA、输入身份和总预算；不存在资源时停止，不安装/下载替代。
3. 新R02冻结源码/模型/依赖/同证据输入/生成配置，再执行一次五题合成及一次固定重复。
4. 工程通过后，无论五题语义准确率如何，自动完成F5 120条与Oracle120条的**新**预测，逐条保留raw及trace。
5. 同旧合同：JSON/引用失败或输入超长按INSUFFICIENT保留分母，不重试模型、不截断证据；OOM/身份/预算/确定性故障仍硬停。
6. 全部240条预测及raw封存后，独立Evaluator才读标签/S；沿用原指标、Wilson及2000次家族bootstrap。
7. 保留R01未改最终收据后归档`L0_RETURN_NO_WEIGHTS.zip`与`COMPLETE.json`，停止等Owner审阅。

PowerShell（变量由5090 Cursor按已核验实际路径赋值；完整本机路径在Owner私有启动件）：

```powershell
& $R01Python scripts/research/paper1_l0_r02_worker.py --r01-dir $R01Dir --work-dir $R02Dir --check-only
if ($LASTEXITCODE -ne 0) { throw 'R02工程预检失败，保留日志并停止' }
& $R01Python scripts/research/paper1_l0_r02_worker.py --r01-dir $R01Dir --work-dir $R02Dir
```

只启动一份进程，已有活锁不重复拉起。断线先查存活；未触发工程HARD_STOP可同源码/配置续跑，已完成raw不重算。
R01 HARD_STOP绝不能删；R02若新工程硬停也不能删门绕过。平台权限不被科研批准替代。

## 6. 结果与解释合同

L0-F5与L0-Oracle分别报告S1/S2/S3 TP/N和Recall、总体Recall、Clean/HN FPR、Precision、三态数量、弃权率、
历史HN/严格三元组、解析/输入/证据/绑定失败、token/VRAM/耗时及区间；不伪造连续分数或AUROC/AUPRC。
所有弃权仍留在分母；不按理由把CONTRADICT改SUPPORT；R02合成准确率及输出合同偏差单列，不混进D1结果。
Oracle是诊断而非部署；与F5差距还有正文长度/组织差异，不全归检索。L0对V03变化不证明自适应结构贡献。
新Run/门控修订历史必须公开说明，不能伪装“首次完整尝试即通过”。

## 7. FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW

风险：事后修门被误写成原协议成功、共享资源被意外改写、理由覆盖结论、弃权藏分母、Worker无访问条件却伪称运行。
控制：独立Run与目录、同题同gold诊断、工程门不降、原R01十文件/总快照及生成配置对照、原解析器/评分不变、
先预测封存后评价；不对D1看分重跑、不动D2D3、不启动VACE-LM/正式测试/训练。
LOCAL只可称R02工程包准备与CPU验证完成；真正GPU执行/检测率须等待5090实际回包核验。
最终实验状态仍是`L0_STRONG_BASELINE_D1_DEV_COMPLETE / OWNER_REVIEW_REQUIRED`，不是Owner科学验收。
