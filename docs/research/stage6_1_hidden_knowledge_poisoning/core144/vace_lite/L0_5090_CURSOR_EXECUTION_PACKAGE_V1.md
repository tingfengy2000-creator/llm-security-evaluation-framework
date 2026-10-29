# 给RTX5090上Cursor的一次性交接：正常流程自动跑完L0-F5与Oracle

2026-10-29（JST）；PODR-151 / OR-105 / REL-2026-0120。
Handoff task `P1-VACE-L0-5090-CURSOR-HANDOFF-01`；实验任务仍为`P1-VACE-L0-F5-ORACLE-STRONG-BASELINE-01`。
**这是已批准的Worker执行包，不是已完成GPU实验。** LOCAL仍是5060；本机没有下载/安装模型或运行L0。
Owner明确要求由5090上的**Cursor**先完成，常规阶段自动推进，不要求逐步等Owner；真实硬门仍停止。

## Owner睡前只需做两件事

1. 把私有文件`L0_D1_PRIVATE_INPUT_V2.zip`复制到5090机器的项目`incoming/`或其它明确目录。
2. 在该机Cursor Agent中打开研究仓库，粘贴下方执行指令，并附上该ZIP的实际绝对路径。

代码、固定模型清单、解析器、预检/下载/推理/评价/归档入口都在Git。
**私有数据不在Git！** 仅pull代码无法凭空恢复120条、Oracle包和评价标签；ZIP必须另传，不能`git add -f`上传。
ZIP含runtime与evaluation分离目录；Cursor不要打开evaluation标签来调试提示词或预测。

| 输入身份 | 冻结值 |
| --- | --- |
| ZIP | L0_D1_PRIVATE_INPUT_V2.zip，2,204,548字节 |
| ZIP SHA256 | 03fae845b50d669373d3b08776caf5a1b2cf068ea7aa5b60dea89a65177e3eb2 |
| Bundle Manifest SHA256 | a7e05d2ebedbc68abc21fff46a0ad1597747712020957ac30cf1445353714a60 |
| 评价范围 | 已签署D1_DEV40完整组/120条/13事实家族；8组24条HOLD，不新增排除 |
| F5 | 已冻结独立Hybrid Top5完整快照，原排序，不重新检索/调权 |
| Oracle | 已冻结人工E1/E2原分配文本，原顺序；原本合法空E2不补造，不改用完整快照冒充原包 |

V1仅本机准备阶段保留，未发放；V2增加完整签署/标签/S路径/家族来源hash。不要用旧ZIP替代。

## 已冻结的模型与资源合同

模型仅`Qwen/Qwen2.5-7B-Instruct`，官方revision
`a09a35458c702b33eeacc393d103063234e8bc28`。
13个文件清单在`configs/research/paper1_l0/qwen_official_manifest_v1.json`：4份weights各自LFS SHA256，
tokenizer/config/原LICENSE的官方Git blob SHA1先验证，实际所有文件SHA256在Worker CONFIG_LOCK记录。
官方[模型卡](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct/blob/a09a35458c702b33eeacc393d103063234e8bc28/README.md)
声明Apache-2.0，默认config为32768上下文；本轮不启用YaRN或改模型配置。
官方[PyTorch说明](https://pytorch.org/blog/pytorch-2-7/)说明Blackwell/CUDA12.8支持背景，但是否真可用必须由本机kernel预检证明。

- RTX5090约32GB、BF16、SDPA、batch1，禁止CPU offload、量化或别的模型。
- do_sample=False、num_beams=1、seed20261029，保存实际GenerationConfig，严格deterministic开关与重复合成输出核验。
- 总上下文32768，输入≤31744、输出≤1024；不截断、不扩池。超长按预声明输入失败→INSUFFICIENT，保留完整分母及原输入身份。
- 模型约14.196GiB；**新增模型＋依赖总预算24GiB**，临时wheel/cache也计监控，不是只算最终权重。
- 优先复用已隔离且通过实际CUDA kernel的研究解释器/精确官方模型；版本在运行前冻结。
- 如需安装，自动建任务venv，不改全局；新env默认Torch2.8.0+cu128、Transformers4.57.1、Accelerate1.10.1、Safetensors0.6.2、NumPy2.2.6。
- wheel下载来自PyPI/官方PyTorch，安装前审计解压峰值＋模型余量；安装成功后只删除本任务已锁hash的新wheel缓存以省预算，可按记录恢复。
- Windows的模型、env、cache、TEMP/TMP必须在D/E；Linux使用已授权研究卷。不要把大型内容放C盘。
- 不装驱动/系统CUDA/管理员软件，不下载第二模型；推理只读本地文件，不联网核验候选。

## Cursor执行指令（可整段复制）

```text
Owner授权你在本RTX5090上执行P1-VACE-L0-F5-ORACLE-STRONG-BASELINE-01。
当前任务是把既定实验运行完，不是另做方法设计或人工仲裁。读取AGENTS.md、最新PODR-151、
current_work_state与本交接文件。LOCAL的5060阻断是另一台机器的历史事实，不禁止本次已授权5090工作。

代码仓库：https://github.com/tingfengy2000-creator/llm-security-evaluation-framework.git
分支：research/stage6-1-hidden-poisoning。
用Owner本条消息提供的固定提交SHA检出源代码，不自行用未来最新代码替换。
保留现有工作树；有无关改动时使用新独立checkout/安全detached worktree，不reset --hard、不覆盖文件。

私有输入文件：L0_D1_PRIVATE_INPUT_V2.zip，Owner会提供本机实际路径。
校验SHA256=03fae845b50d669373d3b08776caf5a1b2cf068ea7aa5b60dea89a65177e3eb2。
不要把该ZIP、候选、标签、证据正文、逐样本raw或模型推到Git。
不要打开evaluation/标签或Expected来调试预测；推理脚本会拒绝读evaluation目录。

选本机已有独立GPU研究Python（有则用--python明确传入；没有时用可创建venv的Python3.10-3.13启动器）。
给本Run选择一个唯一研究工作目录；Windows用D/E，Linux用已有研究卷。
先执行--check-only。若只显示NEEDS_ISOLATED_SETUP，这是普通准备状态，已批准脚本自动建venv、
在24GiB限额内装必要依赖；不用等Owner确认。若CUDA kernel真实失败、设备不符、hash错或超预算则停。
接着执行无--check-only的同一命令，自动完成模型核验/必要下载、冻结、合成门、240新预测、封存、独立评价和归档。

普通阶段连续推进，不逐步问我：不改prompt、parser、样本、证据或超参；不追分、不换模型、不改Guide。
原始JSON/引用解析失败按固定策略记INSUFFICIENT并继续整批；输入超长明确失败，不删关键条款。
语义合成门不合格、OOM/预算/CUDA/身份/完整性失败是硬门：保存INCIDENT和日志后停止，不修算法绕过。
暂时网络问题只允许同一官方文件/同配置有界重试；不能换镜像或模型。

Run ID固定VACE-L0-D1-20261029-R01。用持久终端或安全后台方式启动一份进程；Windows后台窗口隐藏。
检查ORCHESTRATOR_LOCK，不重复拉起；进程仍活就继续监测同一进程。
若终端连接中断但进程仍在，不终止/重跑；已死且未触发硬门时可同命令续跑，绝不重算已完成条目。
这份科研授权不覆盖Cursor/操作系统自身的工具权限，不绕过平台审批。

在COMPLETE.json出现并核验Return ZIP后停止。返回L0_RETURN_NO_WEIGHTS.zip及COMPLETE.json，
最终第一段直接报L0-F5与L0-Oracle各S1/S2/S3 Recall、总体Recall、HN-FPR和弃权率。
同时报TP/N、Clean FPR、Precision、历史HN、三元组、解析/输入失败、token/VRAM/耗时和区间。
这是D1_DEV，Oracle不是部署方法；不标正式GT/test，不实施VACE-LM、不跑D2D3或新训练。
Worker完成不等于Owner科学验收。若硬阻断就返回真实原因和已有原始工件，不填0或伪报完成。
```

## 两条实际入口命令

以下路径变量由Cursor用该机核实的绝对路径赋值，不需Owner手动拼接；不要直接执行占位字符串。

PowerShell（在固定提交的仓库根目录；`$ResearchPython/$InputZip/$WorkDir`由Cursor先赋值）：

```powershell
& $ResearchPython scripts/research/paper1_l0_worker.py --input-zip $InputZip --work-dir $WorkDir --check-only
if ($LASTEXITCODE -ne 0) { throw '只读预检失败，保存阻断，不启动推理' }
& $ResearchPython scripts/research/paper1_l0_worker.py --input-zip $InputZip --work-dir $WorkDir
```

Linux shell：

```bash
"$RESEARCH_PYTHON" scripts/research/paper1_l0_worker.py --input-zip "$INPUT_ZIP" --work-dir "$WORK_DIR" --check-only &&
"$RESEARCH_PYTHON" scripts/research/paper1_l0_worker.py --input-zip "$INPUT_ZIP" --work-dir "$WORK_DIR"
```

`--python <现有GPU研究解释器>`和`--model-dir <现有精确模型目录>`为可选；省略时脚本用启动解释器探测、必要时建独立env，
并查常见官方cache的本revision。指定existing model必须文件hash完整通过，不按文件夹名称猜模型。
若Cursor会话自身退出，GPU进程能否继续取决于它的终端启动方式；交接代码不能保证平台不终止子进程。

## 输出、隔离和恢复

工作目录保存CONFIG_LOCK、实际GenerationConfig、GPU/kernel/依赖/文件SHA、合成结果、raw240单条文件、
PREDICTION_LOCK、两条件逐样本/CSV/区间报告、Oracle差异、下一研究决策、全部命令日志及不含权重的Return ZIP。
先锁预测和raw，再由独立进程读评价标签/S；推理进程审计拒绝evaluation文件访问（非OS沙箱保证）。
引用UID和span只机械核验可回溯，不假称语义gold。XML转义不保证消除语义注入，但数据不被执行成工具指令。
解析只允许完整JSON/完整单fence、原文精确/空白等价/XML实体还原，不修写数字或用标签补答案。
所有弃权/输入失败保留在分母；不伪造AUROC/AUPRC。模型超长/JSON问题与事实核验能力要分开解释。
Oracle若更好，正文组织/长度也可能贡献差距，不能把差值全当检索损失。

断点续跑要求同源码/模型/依赖/prompt/输入hash；活进程不重复启动，死亡锁保留恢复记录。
不覆盖已完成raw，不重跑失败合成门追通过，不在看D1结果后改提示词。
脚本只自动做当前两条件到开发评分/归档，最终`L0_STRONG_BASELINE_D1_DEV_COMPLETE / OWNER_REVIEW_REQUIRED`。
**本机交接验收只可称CPU测试/输入封装完成，不能称5090、合成模型或实际L0效果已通过。**

## FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW

已审批范围内的主要风险：冷安装的CUDA依赖＋权重可能仍不适合24GiB，因此先复用研究环境，
对新wheel解压峰值/模型余量做保守审计并监控；这不是OS级磁盘配额或“任何环境都保证跑完”。
完整Top5可能超过32768上下文，输入失败需与LLM事实能力分开，不能为提高覆盖偷删证据。
Oracle原摘录与F5全快照的长度/组织差异是confounder；对比只在同120条、同骨干/提示/政策下解释为条件差异。
仅机械引用校验不构成语义gold。D1作者开发暴露、13家族小样本、历史基线不同操作点均明确保留。
本轮不新设GT或正式方法优越性，不以合成fixture的高指标当D1结果，不改D2D3以迎合模型。
正常工程兼容准备获准，但真实kernel/合成门失败不允许补prompt追通过、修改算法或切换模型。
