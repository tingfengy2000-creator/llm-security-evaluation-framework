# W1 5090 Owner 决策与 Claim 审批门

- 监督 ID：`W1-OD-20261104-5090-ENV-01`，`W1-OD-20261104-DUAL-GOV-02`
- 正式决定：`PODR-154`
- 执行记录：`REL-2026-0125`
- 实验索引：`OR-112`
- 任务：`P1-RAGDEFENDER-REPRO-5090-CLAIM-GATE-01`
- 运行：`W1-5090-CLAIM-GATE-20261104`
- 分支：`research/paper1-ragdefender-repro-5090`
- 决策写入前 HEAD：`aa85841ff83be31c86e0fa305d3a84d70f2158b5`
- 上游：`ba2a17efba165d45409114df2d70b030ade1e1b8`
- 状态：`COMPAT_ENV_CONDITIONALLY_ACCEPTED / CLAIM_EXECUTION_NOT_APPROVED`

本文件只记录环境批准和三个 Claim 的准入材料。它不运行 Claim，不下载权重，不调用商业 API，也不改算法。

## 1. 已记录的 Owner 决定

写入前，登记册最上方是 `PODR-153`。全库没有 `PODR-154`、`REL-2026-0125` 或 `OR-112`。因此本次决定使用下一个序号 `PODR-154`，不沿用旧编号。

`PODR-154` 只包含两件事：

- 有条件接受独立环境 `artifact_acsac_compat`，作为后续复现的兼容环境。
- 必须保留原始环境 `artifact_acsac` 在 RTX 5090 sm_120 上的 GPU 失败记录，不升级、不覆盖。

明确不包含：模型权重下载、Claim 1–3 运行、商业 API、算法语义变更。

## 2. 官方环境的 GPU 失败证据

2026-11-04 在未改动 `artifact_acsac` 的前提下重跑了一元素 CUDA 运算。

| 项 | 结果 |
| --- | --- |
| torch 运行时版本 | `2.4.0+cu121` |
| 构建 CUDA | 12.1 |
| 设备 | NVIDIA GeForce RTX 5090，capability `(12, 0)` |
| `cuda.is_available()` | True |
| `torch.ones(1, device="cuda")` | `KERNEL_FAIL` |
| 异常 | `RuntimeError: CUDA error: no kernel image is available for execution on the device` |
| 该构建列出的架构 | sm_50、sm_60、sm_70、sm_75、sm_80、sm_86、sm_90 |

证据：[official_torch240_sm120_kernel_fail.txt](logs/official_torch240_sm120_kernel_fail.txt)。官方环境的包版本没有因这次探测改变。

## 3. 两个环境的依赖差异

比较方法：对两个环境已安装的 Python 发行版做名称和版本对照。官方环境 191 个，兼容环境 194 个，版本不同或只存在于一侧的有 20 个。其余包版本相同，包括 `transformers==4.41.2`、`sentence-transformers==3.0.1`、`faiss-cpu==1.8.0.post1`、`faiss-gpu==1.7.2`、`xformers==0.0.27.post2`。

| 包 | 官方 `artifact_acsac` | 兼容 `artifact_acsac_compat` | 对复现数值的可能影响 |
| --- | --- | --- | --- |
| torch | 2.4.0（运行时 `2.4.0+cu121`，CUDA 12.1） | `2.8.0+cu128`（CUDA 12.8） | 高。矩阵乘、注意力和采样的内核不同，可能改变生成 token，从而改变 ASR 与准确率。兼容环境的数字不能写成官方环境或论文原机的数字 |
| nvidia-cublas-cu12 | 12.1.3.1 | 12.8.4.1 | 高，随 torch 的线性代数实现一起变化 |
| nvidia-cudnn-cu12 | 9.1.0.70 | 9.10.2.21 | 高，卷积和部分注意力实现不同 |
| nvidia-nccl-cu12 | 2.20.5 | 2.27.3 | 单卡 Claim 路径上直接数值影响低；仍是 CUDA 栈差异 |
| nvidia-cuda-nvrtc-cu12 | 12.1.105 | 12.8.93 | 随 CUDA 栈变化，影响运行期编译的内核 |
| nvidia-cuda-runtime-cu12 | 12.1.105 | 12.8.90 | 随 CUDA 栈变化 |
| nvidia-cuda-cupti-cu12 | 12.1.105 | 12.8.90 | 分析接口，预期不改 ASR |
| nvidia-cufft-cu12 | 11.0.2.54 | 11.3.3.83 | 本 Claim 路径不直接做 FFT；保留为栈差异 |
| nvidia-curand-cu12 | 10.3.2.106 | 10.3.9.90 | 若随机核走该库，可能影响随机性；脚本固定 seed 12 |
| nvidia-cusolver-cu12 | 11.4.5.107 | 11.7.3.90 | 求解器差异；Claim 主路径不直接调用 |
| nvidia-cusparse-cu12 | 12.1.0.106 | 12.5.8.93 | 稀疏核差异；Claim 主路径不直接调用 |
| nvidia-nvjitlink-cu12 | 12.3.101 | 12.8.93 | 链接器，随 CUDA 栈变化 |
| nvidia-nvtx-cu12 | 12.1.105 | 12.8.90 | 性能标记，不改数值 |
| nvidia-cufile-cu12 | 不存在 | 1.13.1.3 | torch 2.8 的新增依赖，不改算法 |
| nvidia-cusparselt-cu12 | 不存在 | 0.7.1 | torch 2.8 的新增依赖，不改算法 |
| triton | 3.0.0 | 3.4.0 | 中。8-bit 内核和 torch 内部代码生成可能不同 |
| bitsandbytes | 0.43.1 | 0.45.5 | 高，但只落在 LLaMA 路径。`Llama.py` 把 `load_in_8bit` 写死为 True。Vicuna 配置是 `load_8bit=False`，这条路径不走 8-bit |
| sympy | 1.12 | 1.14.0 | 低。它是 torch 2.8 要求的依赖，不是 ASR 公式 |
| typing_extensions | 4.9.0 | 4.16.0 | 可忽略。类型标记，不参与计算 |
| ragdefender | 不存在 | 0.2.0 可编辑安装 | 对这三条 Claim 脚本无数值影响。`artifacts/` 不导入该包 |
| faiss-cpu / faiss-gpu | 1.8.0.post1 / 1.7.2 | 同版本 | 两个环境之间没有版本差。两边 `import faiss` 都解析到 CPU 版，`StandardGpuResources` 不存在。若作者机器实际走了 GPU 索引，这是两边共同的偏差，不是兼容环境独有 |
| xformers | 0.0.27.post2 | 同版本 | 没有版本差。兼容环境里它的 CUDA 扩展对不上 torch 2.8。仓库源码不导入 xformers |

论文原机是 Quadro RTX 8000、约 48 GB、非量化。作者文档写明 artifact 的 8-bit 路径会和论文数字略有差别。兼容环境又在 8-bit 之外更换了 torch 和 CUDA 栈。三层数字必须分开：论文原结果、官方环境结果、兼容环境结果。官方环境目前没有 GPU 结果。

## 4. 权重与数据的只读调查

没有下载任何权重或语料，没有登录，没有调用模型服务。

| 对象 | 身份 | 许可与来源 | 本机接受状态 | 体积 |
| --- | --- | --- | --- | --- |
| LLaMA-7B | `meta-llama/Llama-2-7b-chat-hf`，配置写 `revision=main` | Llama 2 Community License。Hugging Face 页面为手动门禁，须向 Meta 提交许可同意后才能取权重。API 在本次读取时的提交是 `f5db02db724555f92da89c216ac04704f23d4590`。配置里的 `main` 还没冻结成这个提交 | UNKNOWN，未下载 | 仓库 `usedStorage` 53908103645 字节，约 50.21 GiB，含 safetensors 和 pytorch 两套副本。F16 参数 6738417664，单份权重大约 13476835328 字节，约 12.55 GiB |
| Vicuna-7B | `lmsys/vicuna-7b-v1.3`，配置写 `revision=main` | 模型卡写明 Non-commercial license，微调自 LLaMA（Llama 1，不是 Llama 2）。来源是 LMSYS 的 Hugging Face 仓库和 FastChat。门禁为 false。本次 API 提交 `236eeeab96f0dc2e463f2bebb7bb49809279c6d6`。卡片提示存在更新版本；不得擅自替换 | UNKNOWN，未下载 | 仓库 `usedStorage` 26954326092 字节，约 25.11 GiB，文件是两片 pytorch bin。单份 7B F16 权重大约仍是 13 GiB 量级，精确分片字节本次未逐文件读取 |
| Contriever | 代码映射 `facebook/contriever` | 模型卡没有给出 license 字段。来源是公开 Hugging Face 仓库，提交 `2bd46a25019aeea091fd42d1f0fd4801675cf699`。缺许可字段不能当成已经允许下载 | UNKNOWN | `usedStorage` 875963049 字节，约 835.6 MiB |
| BEIR 语料 | `nq`、`hotpotqa`、`msmarco` | 代码在本地没有数据时，会从 `https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{name}.zip` 下载。本次只做了 HEAD | 未下载 | zip 的 `Content-Length`：nq 498307926 字节，hotpotqa 654025350 字节，msmarco 1082258632 字节。合计 2234591908 字节，约 2.08 GiB。解压后的体积未测 |

显存方面，本机此前核到的是 RTX 5090、32607 MiB。LLaMA 路径按代码会以 float16 加载并打开 8-bit。Vicuna 配置是 `load_8bit=False`、`max_gpu_memory=5GiB`、`cpu_offloading=True`。5 GiB 上限放不下完整的 7B float16 权重，实际是否卸载到 CPU 要等批准后的运行才能证实。论文原机约 48 GB 且非量化，和这条 artifact 路径不同。

## 5. 三个 Claim 的准入材料

三条脚本默认 `CONDA_ENV=artifact_acsac`。那个环境不能执行 CUDA 内核。若将来获批，命令必须显式改成兼容环境，这只是环境选择，不是算法修改。下面的命令是待批文本，本次没有执行。

共同边界：

- 只覆盖作者文档中的 Figure 4 开源模型行。GPT-4o、Gemini、13B 和 Table 4 不在这三条命令里。
- 作者写明 8-bit artifact 数字与论文原机数字可以不同，只要求趋势相同。
- `expected/result.txt` 对应的是仓库里的旧实现，不是论文公式的逐字节复现。`ConcentrationBasedGrouping` 与论文 Eq. 3 的差异保持原样，不在运行前修改。
- 每个配置是 `M=10` 个目标问题、`repeat_times=10`、`seed=12`、检索器只有 Contriever。
- 停止条件：许可未确认、权重或语料下载未单独批准、官方环境被要求升级、兼容环境 CUDA 失败、显存不足、出现商业 API、需要改算法、读到 D1/D2/D3、或有人要把兼容环境数字写成论文原 ASR。任一发生即停。

| 项 | Claim 1 | Claim 2 | Claim 3 |
| --- | --- | --- | --- |
| 目录 | `claims/claim1_poisonedrag` | `claims/claim2_tan` | `claims/claim3_garag` |
| 攻击 | PoisonedRAG，Zou 等，USENIX Security 2025 | Tan 等，ACL 2024。旧名 Blind | GARAG，Cho 等，EMNLP 2024 Findings |
| 数据 | NQ test、HotpotQA test、MS MARCO train | 同左 | 同左 |
| 模型 | Contriever；`llama7b`→Llama-2-7b-chat；`vicuna7b`→Vicuna-7B-v1.3 | 同左 | 同左 |
| 网格 | 三个数据集、两个生成器、四种附加投毒强度，共 24 次调用。NQ 的 `additional_adv_per_query` 为 0/5/15/25；另外两个数据集为 0/2/6/10。对应相对 top-k 的 100/200/400/600% | 只跑附加强度 0，即 100%。三个数据集乘两个生成器，共 6 次 | 与 Claim 2 相同，6 次，方法名是 GARAG |
| 作者给出的耗时 | 单卡约 4–5 小时 | 约 1–2 小时 | 约 1–2 小时 |
| 待批命令 | `CONDA_ENV=artifact_acsac_compat bash claims/claim1_poisonedrag/run.sh` | `CONDA_ENV=artifact_acsac_compat bash claims/claim2_tan/run.sh` | `CONDA_ENV=artifact_acsac_compat bash claims/claim3_garag/run.sh` |
| 脚本内部 | `conda run -n artifact_acsac_compat python run_poisonedrag.py`，然后 `eval.py --method PoisonedRAG` | `run_tan.py`，然后 `eval.py --method Tan` | `run_garag.py`，然后 `eval.py --method GARAG` |
| 执行准入 | `NOT_APPROVED` | `NOT_APPROVED` | `NOT_APPROVED` |
| 权重准入 | `BLOCKED` | `BLOCKED` | `BLOCKED` |
| 语料下载准入 | `NOT_APPROVED` | `NOT_APPROVED` | `NOT_APPROVED` |

Claim 2 与 Claim 3 的 expected 文件数值行相同，只有方法标签不同。这是上游文件事实，不是本次测量。

## 6. 仍需 Owner 批准的事项

1. 在本机接受 Llama 2 Community License，并批准下载 `meta-llama/Llama-2-7b-chat-hf` 的一个冻结提交，而不是浮动的 `main`。
2. 接受 Vicuna 的非商业许可，并批准下载 `lmsys/vicuna-7b-v1.3` 的冻结提交 `236eeeab96f0dc2e463f2bebb7bb49809279c6d6`。不得改用卡片里提到的新版本。
3. 批准从 UKP 下载 nq、hotpotqa、msmarco 三个 zip。代码会在本地没有数据时自动下载。
4. 对 `facebook/contriever` 的许可作出决定。本次模型卡没有许可字段。
5. 分别或一次性批准上面三条 `CONDA_ENV=artifact_acsac_compat` 命令。
6. 确认将来的数字只能标成兼容环境复现，不能标成论文原结果，也不能标成官方 `artifact_acsac` 的结果。

在这些决定下来之前，不下载、不运行、不改算法。

## 7. 尚未批准事项的决策字段

1. Issue ID：`W1-5090-CLAIM-GATE-20261104`
2. 名称：三个 artifact Claim 的权重、语料和执行批准
3. 阶段：环境已有条件接受，Claim 未运行
4. 事实：官方环境 GPU 失败是 `OBSERVED_FACT`。依赖差异是 `OBSERVED_FACT`。许可文本和仓库体积来自本次读取的模型卡与 API，是 `SOURCE_DERIVED_FACT`。兼容环境会改变 ASR 是 `INFERENCE`。本机是否已经接受 Llama 2 或 Vicuna 许可是 `UNKNOWN`
5. 约束：`PODR-154` 不包含下载和 Claim。PO-MHEP 禁止把未批准的大型下载和论文结论混在一起。5090 没有自批权
6. 现在处理的原因：环境门已经关闭，下一步唯一会改变资源、许可和论文数字身份的动作就是下载和运行
7. 风险：错误许可下载、把兼容环境数字写成论文 ASR、8-bit 与 torch 2.8 同时偏离原论文、BEIR 自动下载、Vicuna 非商业限制
8. 选项：继续停在本门；或按第 6 节逐项批准。逐项批准可逆，前提是权重放在隔离目录且不写入 Git。不批准则没有新的磁盘和显存占用
9. 建议：先批许可和冻结提交，再批语料，最后按 Claim 1、2、3 的顺序单独放行。置信度高的部分是环境事实；许可是否已被本机账号接受仍然未知
10. 理由：官方环境不能跑，兼容环境已被接受为后续环境，但数字身份还没有被批准
11. 需要决定的问题就是第 6 节的六项
12. 决定前允许写治理记录。禁止下载、运行、改算法、调用商业 API、读 D1/D2/D3

## 文档收口

- human_ledger_checked = true；human_ledger_updated_if_required = true
- agent_ledger_checked = true；agent_ledger_updated = true
- current_work_state_updated = true
- execution_log_appended = true
- experiment_master_condition_evaluated = true；审批门变化，已追加 `OR-112`
- owner_decision_condition_evaluated = true；已追加 `PODR-154`
- stage_process_condition_evaluated = true；这不是 Stage 6.1 的新试点阶段，stage process 不改
- lessons_condition_evaluated = true；sm_120 偏差已留在环境证据里，不单独立成跨论文方法学结论
- research_authority_condition_evaluated = true；冻结合同未变，不改
- readme_condition_evaluated = true；导航入口未改

5060 只读获取本分支。不要合并。
