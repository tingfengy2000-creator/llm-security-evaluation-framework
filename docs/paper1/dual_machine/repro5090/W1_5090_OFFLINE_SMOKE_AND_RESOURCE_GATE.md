# W1 5090 离线 Smoke 与资源门

日期：2026-11-04。执行机：5090，角色 COMPUTE_WORKER，没有自批权。
监督授权：`W1-OD-20261104-FAST-A-03`。状态：`OWNER_APPROVED` / `BOUNDED_OFFLINE_SMOKE_ONLY`。
授权原文在 5060 分支 `research/paper1-chinese-defense-5060` 的提交 `af68d89a870647be138cf5592ccd4a058e44a8ab`，路径 `docs/paper1/dual_machine/owner_approvals/W1_FAST_TRACK_A_OWNER_AUTHORIZATION_20261104.md`。本次只 `git fetch` 和 `git show`，没有 merge、rebase、cherry-pick 或 reset。
本分支执行前 HEAD 与远端一致：`01554702b0bc14b7203712c83423d8245eacb3d3`。工作区当时干净。
本分支已有的 `PODR-154` 只表示兼容环境被有条件接受。5060 同一编号是另一项决定。本文件不用 `PODR-154` 充当 Fast-Track A 的跨机身份。

上游保持 `ba2a17efba165d45409114df2d70b030ade1e1b8`。`git diff --ignore-cr-at-eol --shortstat` 在检查前和检查后都没有内容行。Windows 挂载上的 `git status` 仍显示大量 `M`，这是换行符噪声，没有被清理，也没有被提交。

## 1. 等级

| 对象 | 等级 |
| --- | --- |
| 下面列出的纯函数、预设映射、空输入和命令行拒绝 | `ALGORITHM_CHECK` |
| 四条虚构文档上的分组与筛选 | `SMOKE` |
| 包导入与 `info` | `SMOKE` |
| Claim 1 / 2 / 3 | `NOT_RUN` |
| 无防御 ASR、有防御 ASR、问答准确率 | `NOT_MEASURED` |
| 作者 `expected/result.txt` | `AUTHOR_EXPECTED`，本次未当作实测 |
| 本文 | 不是 `ARTIFACT_CLAIM_REPRO`，也不是 `PAPER_NUMERIC_REPRO` |

没有模型，没有 BEIR，没有权重。虚构样本的计数不能当成论文数字。

## 2. 执行前的静态审计

审计对象是上游 `tests/`、`ragdefender/cli.py`、`ragdefender/grouping/`、`ragdefender/identification/topk.py`、`ragdefender/similarity.py`、`ragdefender/embedders.py`。结论按调用链分成可跑和停跑。

可跑，因为源码在这些入口不会构造嵌入器、不会读 BEIR、不会打开权重：

- `tests/test_import.py` 的公开导入
- `tests/test_cli.py` 的 `info`、`--help`、未知 claim 被 argparse 拒绝
- `n_pairs_for` 的 0、1 和组合数
- `ClusteringBasedGrouping(embedder=None)` 的默认 `m == 5`，以及空文档在调用 `encode` 之前返回 0
- `resolve_preset` 和显式 `cpu` 设备解析
- 已传入本地张量时的 `estimate_n_adv` 和 `IdentifyAdversarial.select`

停跑，因为不能保证零网络、零权重或零 BEIR：

- `conftest.py` 的 `tiny_embedder` 会加载 `sentence-transformers/all-MiniLM-L6-v2`
- 任何依赖该夹具的相似度、聚类、浓度、识别和端到端测试
- `test_embedders.py` 里真正调用 `load_embedder` 的用例，以及 Stella 重测试
- `ragdefender defend` 和 `ragdefender evaluate`，它们会构造 `RAGDefender` 并调用 `load_embedder`
- `ragdefender reproduce claim1`、`claim2`、`claim3`，以及 `claims/claim1_poisonedrag/run.sh`、`claims/claim2_tan/run.sh`、`claims/claim3_garag/run.sh`
- `RAGDEFENDER_TEST_HEAVY` 没有设置

兼容环境里没有 `pytest`。没有安装它。第一次直接调用因此退出 1，原文是 `No module named pytest`。这不是通过跳过断言制造的通过。

进程内隔离只设置了 `HF_HUB_OFFLINE=1`、`TRANSFORMERS_OFFLINE=1`、`HF_DATASETS_OFFLINE=1` 和空的 `CUDA_VISIBLE_DEVICES`。没有改防火墙或系统安全设置。

## 3. 实际命令和结果

解释器：`artifact_acsac_compat` 的 Python。官方环境 `artifact_acsac` 没有被安装或升级。

| 步骤 | 退出码 | 结果 |
| --- | --- | --- |
| 兼容环境直接跑 pytest | 1 | `No module named pytest`。日志在 Git 外，sha256 `7db3e50912d5d6ae042f7c636b366d3862f9cfce6db16be1740d5349c159c72f` |
| 直接检查脚本 | 1 | 10 项里 9 项通过，1 项失败。stdout sha256 `4aa3c4ebd3bb47a5858e494f550b49543ff33a72a0b953391f7bd4ffb96df7e6`。stderr sha256 `c90077e7367a78b0de35fa3bd4193b0fa65e89f44049a88572c94e024d0c655a` |
| 修正后的公开导入 | 0 | 版本 `0.2.0`，公开类名 `Evaluator` |
| 兼容环境一元素 CUDA 求和 | 0 | torch `2.8.0+cu128`，CUDA 12.8，capability `(12, 0)`，求和 `1.0` |
| 官方环境只读版本 | 0 | torch `2.4.0`，triton `3.0.0`，bitsandbytes `0.43.1`，sympy `1.12`。没有重跑会改环境的命令 |

直接检查里失败的那一项是脚本自己的导入行写成了截断类名 `Evaluato`。库没有被改。失败原文保留在脱敏副本 `logs/offline_smoke_harness_stdout.txt`。随后的独立导入确认类存在。stderr 是本机 TensorFlow 注册 cuFFT、cuDNN、cuBLAS 工厂时的告警，以及找不到 TensorRT。没有下载记录。

通过项，按原样记录：

- 已删除的占位子包不在树里
- 测试夹具文件存在，但没有使用会下载的夹具
- `n_pairs_for(0)=0`，`n_pairs_for(1)=1`，`n_pairs_for(5)=10`
- 默认 `m` 是 5；空文档估计值是 0；浓度分组对空文档也是 0
- 四条虚构字符串的 TF-IDF 计数是 2
- 固定的 4×3 CPU 张量上，聚类估计、浓度估计和筛选结果分别是 2、2、`[0, 1]`
- `minilm-all`、`minilm-paraphrase`、`stella` 映射到代码里的预设标识；未知字符串原样返回；显式设备是 `cpu`
- `info` 退出 0，打印 `RAGDefender v0.2.0`
- `--help` 退出 0
- `reproduce claim42` 退出 2，argparse 报告非法选项。没有进入 claim1、claim2 或 claim3

代码身份是上游提交 `ba2a17efba165d45409114df2d70b030ade1e1b8`。本次没有加载模型，也没有读取模型配置来运行。配置哈希仍是 R0 的 `21d6096ea60a92c0a9c4dfdebde5ae1755ad36565b7fb61de3f5948f82a305e0`，没有重新计算成另一个值。

## 4. 环境比较

官方环境保持 torch 2.4.0+cu121 的 sm_120 失败记录，见 [官方失败日志](logs/official_torch240_sm120_kernel_fail.txt)。本次只重读了它的包版本。

兼容环境本次重新确认 torch 2.8.0+cu128 可以完成一次 CUDA 求和。此前已经记录的 20 个包差异没有新增安装，仍然是：

`bitsandbytes` 0.43.1 对 0.45.5；`torch` 2.4.0 对 2.8.0+cu128；`triton` 3.0.0 对 3.4.0；`sympy` 1.12 对 1.14.0；`typing_extensions` 4.9.0 对 4.16.0；`ragdefender` 仅兼容环境有 0.2.0；以及 12 个 CUDA 12.1 对 12.8 的 nvidia 运行库，其中 `nvidia-cufile-cu12` 和 `nvidia-cusparselt-cu12` 只在兼容环境出现。

`transformers` 4.41.2、`sentence-transformers` 3.0.1、`faiss-cpu` 1.8.0.post1、`faiss-gpu` 1.7.2、`xformers` 0.0.27.post2 的版本相同。`import faiss` 仍落到 CPU。`xformers` 的 CUDA 扩展在 torch 2.8 上不能加载。这些差异会限制以后任何数字的可比性：torch、CUDA、cuBLAS 和 cuDNN 影响所有 GPU 路径；8-bit 库只影响 LLaMA 那条硬编码路径；triton 影响 GPU 内核；sympy 影响符号计算。本次 Smoke 没有产生可与论文比较的数字。

## 5. 许可和资源附件

数字来自已经提交的 [审批门](W1_5090_OWNER_DECISION_AND_CLAIM_GATE.md)。本次没有登录、没有下载、没有联网查询，也没有用缓存缺失去触发请求。

| 对象 | 固定标识 | 许可 | 体积 | 本机状态 |
| --- | --- | --- | --- | --- |
| Llama-2-7B-chat | `meta-llama/Llama-2-7b-chat-hf`，读取时提交 `f5db02db724555f92da89c216ac04704f23d4590`；配置写的是 `main`，尚未冻结 | Llama 2 Community License，Hugging Face 手动门禁 | 仓库 `usedStorage` 53908103645 字节，约 50.21 GiB。单份 F16 约 13476835328 字节，约 12.55 GiB | 未下载。本机是否已接受许可是 `UNKNOWN` |
| Vicuna-7B-v1.3 | `lmsys/vicuna-7b-v1.3`，提交 `236eeeab96f0dc2e463f2bebb7bb49809279c6d6` | 模型卡写 Non-commercial。微调自 Llama 1，不是 Llama 2。门禁为 false。不得换成卡片里的新版本 | `usedStorage` 26954326092 字节，约 25.11 GiB | 未下载 |
| Contriever | `facebook/contriever`，提交 `2bd46a25019aeea091fd42d1f0fd4801675cf699` | 模型卡没有 license 字段。缺字段不是许可 | `usedStorage` 875963049 字节，约 835.6 MiB | 未下载 |
| BEIR | `nq`、`hotpotqa`、`msmarco` | 代码会在本地缺失时访问达姆施塔特的 zip。本次未访问 | 压缩包长度 498307926、654025350、1082258632 字节，合计 2234591908 字节，约 2.08 GiB。解压后体积 `UNKNOWN` | 未下载 |

显存硬停：此前核到的 RTX 5090 是 32607 MiB。一旦出现 OOM，受影响的 Claim 必须停，不能改量化或改环境来继续。Vicuna 配置的 `max_gpu_memory` 是 5GiB，放不下完整 7B float16；实际卸载没有测。LLaMA 代码路径写死 `load_in_8bit=True`。论文原机约 48 GB 且非量化。兼容栈的 torch 2.8、CUDA 12.8 和 bitsandbytes 0.45.5 使以后的数字不能标成论文原数字。

## 6. 仍未批准事项的 12 个字段

1. Issue ID：`W1-5090-OFFLINE-SMOKE-20261104`
2. 名称：许可证、权重、BEIR 和三条 Claim 的下一步批准
3. 阶段：离线 Smoke 已记录。Claim 仍是 `NOT_RUN`
4. 事实：pytest 缺失、直接检查的 9 项通过和 1 项脚本截断失败、随后的导入成功、兼容环境 CUDA 求和 1.0、官方包版本未变，都是 `OBSERVED_FACT`。许可和体积沿用上一份已提交调查，是 `SOURCE_DERIVED_FACT`。本机账号是否已接受 Llama 2 或 Vicuna 许可是 `UNKNOWN`。兼容栈会改变以后的 ASR 是 `INFERENCE`
5. 约束：`W1-OD-20261104-FAST-A-03` 只覆盖静态确认过的本地单测和虚构样本。它不覆盖 Claim 脚本、权重、BEIR、付费 API、D1/D2/D3、算法改动、量化或环境改动。5090 不能自批
6. 现在处理的原因：离线边界已经用完。再往前一步就会碰到许可、下载或真实 Claim
7. 风险：把 Smoke 计数写成论文 ASR；在许可未知时下载 Contriever；用 `main` 而不是冻结提交取 Llama 或 Vicuna；BEIR 缺失时自动下载；OOM 后改量化
8. 选项：停在本文件；或由 Owner 另批冻结提交、Contriever 许可、三个 zip，再按 Claim 单独放行。不批准就没有新的磁盘和显存占用
9. 建议：保持停止。置信度高的是本次命令、退出码和哈希。许可接受状态仍然未知
10. 理由：本次授权写明完成后停止，不得自动进入下载或 Claim
11. 需要 Owner 决定的是：Llama 2 门禁与冻结提交、Vicuna 非商业许可与冻结提交、Contriever 缺许可字段、三个 BEIR zip、以及 claim1、claim2、claim3 各自的命令
12. 决定前允许写本记录并推送本分支。禁止下载、运行 Claim、改算法、调用商业 API、读 D1/D2/D3、改两个环境、合并主线或其他机器分支

## 7. 文档收口

- human_ledger_checked = true；human_ledger_updated_if_required = true
- agent_ledger_checked = true；agent_ledger_updated = true
- current_work_state_updated = true
- execution_log_appended = true
- experiment_master_condition_evaluated = true；没有新指标，审批门没有从“Claim 未批准”改变，不追加新的 OR 编号
- owner_decision_condition_evaluated = true；授权身份是 `W1-OD-20261104-FAST-A-03`，已在 5060 提交 `af68d89a870647be138cf5592ccd4a058e44a8ab`。本分支不追加新的 PODR 编号，避免和另一分支已有编号相撞
- stage_process_condition_evaluated = true；这不是 Stage 6.1 的新试点，不改
- lessons_condition_evaluated = true；没有新的跨论文方法学结论，不改
- research_authority_condition_evaluated = true；冻结合同未变，不改
- readme_condition_evaluated = true；导航入口未改

原始长日志留在研究 Git 之外。5060 只读获取本分支。不要合并。本文件完成后停止，不自动启动下一阶段。
