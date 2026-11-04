# W1 5090 R0 初始状态审计

- run_id: `W1-5090-R0-20261104`
- worker: `5090_cursor`
- status: `R0_AUDIT_RECORDED / CLAIM_EXECUTION_NOT_RUN`
- reproduction_level: `R0_AUDIT_ONLY`
- research baseline: `4dc9161e79b79ece70a7c17144175a19b985770d`
- branch: `research/paper1-ragdefender-repro-5090`
- upstream HEAD: `ba2a17efba165d45409114df2d70b030ade1e1b8`
- config_hash: `21d6096ea60a92c0a9c4dfdebde5ae1755ad36565b7fb61de3f5948f82a305e0`
- logs_hash: `0f6b3de615c5d19d795b49df5ead98d1df85baa2d56229dbe1dbd2efe5b572ab`
- measured ASR / accuracy: `NOT_MEASURED`
- sample_n: `UNKNOWN`

标签含义：`VERIFIED` 是本机命令或文件字节直接核到的事实；`REPORTED` 是仓库或作者文档里的陈述，本机没有重跑；`UNKNOWN` 是没有测量；`BLOCKED` 是当前不能当作可运行。作者 `expected/result.txt` 里的数字只属于 `REPORTED / AUTHOR_EXPECTED`，不是本机实测。

## 1. Git 与治理

| 项 | 状态 | 事实 |
| --- | --- | --- |
| 研究仓库 | VERIFIED | 工作区下的 `llm-security-evaluation-framework`。根目录 `paper1` 本身不是 Git 仓库 |
| remote | VERIFIED | `origin` = `https://github.com/tingfengy2000-creator/llm-security-evaluation-framework.git` |
| 审计前分支 | VERIFIED | `research/stage6-1-hidden-poisoning`，与 origin 一致，工作树干净 |
| 本分支起点 | VERIFIED | 从上述 HEAD 新建 `research/paper1-ragdefender-repro-5090`。创建前远端没有这个分支 |
| HEAD | VERIFIED | `4dc9161e79b79ece70a7c17144175a19b985770d`，`research: record the Oracle claim-alignment tradeoff` |
| 冻结合同文件 | BLOCKED | `01_PAPER1_DUAL_MACHINE_EXECUTION_CONTRACT_V1.md` 不在研究仓库。本审计按已收到的执行提示和仓库治理记录，没有把缺失合同写成已批准的 Claim 运行 |

适用治理文件都在基线 `4dc9161` 上读取。SHA-256 是本机 `Get-FileHash`：

| 路径 | SHA-256 | 角色 |
| --- | --- | --- |
| `AGENTS.md` | `a926e0708d3244a91577b1a179634ab4b4250ff72a7122b2d8b26193b5ddac2e` | 5090 = `COMPUTE_WORKER / NO_SELF_APPROVAL_AUTHORITY` |
| `PROJECT_MASTER_CONTEXT.md` | `130b9237cff4a6a35a16d93d2921f085c67842a5a378121ad9848bb9b34bb648` | L0 Oracle 对照已完成，等待 Owner 审阅 |
| `docs/governance/current_work_state.md` | `5da2ad3f57120a89ff0bbcd03ae9aa1bde73a5d78fc9ad6752a38883dfeba4d4` | 同上，且写明不再开新模型 |
| `docs/governance/project_owner_decision_register.md` | `f150d2cc041b2ee44f9e339ea8c8f7d3b476168c3228e5a1eba990600514e017` | 最新条目 `PODR-153`，范围是 L0 R02 |
| `docs/governance/dual_machine_execution_policy.md` | `274a0efef70db25b44af5c2058a152d7a625f9705cdc2d1253d4f1f5fd9ec142` | 正式复现未在该快照中批准 |
| `docs/governance/project_owner_sovereignty_and_mandatory_escalation_principle.md` | `66069cc3154d6d7c4c24e7f9deb9a34610514fe7b3b10aec3eb2dd27190753c7` | 新依赖、大下载、系统安装需停回控制面 |
| `docs/governance/long_term_research_requirements.md` | `fd2ae79a48d17717f3e05eecd7102e470eaa3f6a37295badee2766e459997473` | 复现失败必须登记 blocker |
| `docs/governance/experiment_master_record.md` | `6b8fe241697bc982adef4647371b897322b1c25a231d2a3f06a4ac6bd841c94e` | 实验索引 |
| `docs/governance/research_execution_log.md` | `f9a41fddc2bfb26b8b62831d6163a1dbfe1436ed245d1a6ee640e6a0a2a1099b` | 执行时间线 |
| `docs/research/stage6_1_hidden_knowledge_poisoning/hardware_execution_policy.md` | `77b30048f4c45f990c1a7d78c76da7e9cfb5d12b1d3a3de64046e47dbea6447a` | 原环境与兼容环境必须分开 |
| `docs/research/stage6_1_hidden_knowledge_poisoning/documentation_separation_contract.md` | `10967a480778cbce25b30084d2601d38e5517d52e62f46de52625730e1937062` | 文档收口 |

`REPORTED`：上述治理在本审计开始时没有 RAGDefender Claim 运行批准，也没有 `RunManifest.git_commit`。本提交是 R0 审计回传，不把 L0 Oracle 结果改写成 RAGDefender 结果，也不启动三个 Claim。

## 2. 设备环境

| 项 | 状态 | 事实 |
| --- | --- | --- |
| 操作系统 | VERIFIED | Windows 11 专业版 10.0.26200，64 位 |
| CPU / 内存 | VERIFIED | Intel Core i9-14900，24 核 / 32 线程；内存 63.6 GB，空闲 41.4 GB |
| 磁盘空闲 | VERIFIED | C: 98.7/300 GB；D: 742.8/931.5 GB；E: 748.2/1607.3 GB。测量时间 2026-11-04 16:01 UTC+8 |
| GPU | VERIFIED | `nvidia-smi`：RTX 5090，驱动 610.88，CUDA UMD 13.3，32607 MiB，当时占用 0 MiB |
| 代理 | VERIFIED | 进程环境无 HTTP/HTTPS 代理；WinHTTP 直连 |
| PATH 上的 conda | VERIFIED | `conda` 命令不存在 |
| 已安装 conda | VERIFIED | 驱动器 E 的 Anaconda 前缀里 `conda 26.1.1`。环境只有 `base` 和 `pose_openmmlab`。没有 `artifact_acsac` |
| 工作区 `.venv` | VERIFIED | Python 3.13.9，`import torch` 为 `ModuleNotFoundError` |
| 系统 Python 3.14 | UNKNOWN | 未在该解释器上测试 torch |
| 既有 L0 虚拟环境 | VERIFIED | Python 3.13.9，torch `2.8.0+cu128`，CUDA 构建 12.8，`cuda.is_available()==True`，设备 RTX 5090，capability `(12, 0)`，设备内存字节 `34190458880`，单元素 CUDA 求和为 0.0 |
| 该 L0 环境的身份 | VERIFIED | 它是先前 Qwen L0 任务的隔离环境，不是作者 `artifact_acsac`。本轮没有改它 |
| WSL | REPORTED / NOT_RUN | `wsl -l -v` 显示 `Ubuntu-24.04`，状态 Stopped，WSL2。本轮没有启动 WSL，也没有在 WSL 里跑 `nvidia-smi` 或 conda |
| 官方 env 与 5090 | BLOCKED | `artifacts/env.yml` 锁定 linux-64、Python 3.10.14、`torch==2.4.0`、`transformers==4.41.2`、`bitsandbytes==0.43.1`。Windows 原生 `conda env create` 与该锁文件不匹配。torch 2.4.0 能否在 sm_120 上运行是 `UNKNOWN`，因为环境没有创建 |

## 3. 上游 RAGDefender

隔离克隆不在研究 Git 内。本机 `git rev-parse` 与 `git diff`：

| 项 | 状态 | 事实 |
| --- | --- | --- |
| remote | VERIFIED | `https://github.com/SecAI-Lab/RAGDefender.git` |
| 默认分支 HEAD | VERIFIED | `ba2a17efba165d45409114df2d70b030ade1e1b8`，2026-05-14，merge `refactor/v0.2.0` into `main` |
| 工作树 | VERIFIED | 相对 HEAD 的 diff 为空，porcelain 为空 |
| tag `v0.2.0` | VERIFIED | 注释标签对象 `1f32c868ac5d17151917377c178834a569728143`；指向提交 `2be0bb2f84b2bf4ef4a0f6d8387ad1c0d3df847a` |
| tag `Release` | VERIFIED | `bcc3f4f13cc39fdcb5ffd4402b950e4dcd707f1d` |
| `v0.2.0` 提交到 `main` | VERIFIED | 唯一差异是新增 `.github/workflows/codeql.yml`，101 行。没有算法文件差异 |
| 许可证 | VERIFIED | 仓库 `LICENSE` 为 MIT，版权 2025 SecAI Lab, Sungkyunkwan University。文件 SHA-256 `2242ce2d80454d449576d7ac791c22b3ec9d3907877d68a070e4f30a7aaeab41` |
| 研究仓库中的上游副本 | VERIFIED | `src/` 下没有 `ragdefender` 实现。没有用中文算法替换上游 |
| 包与 artifact | VERIFIED | `artifacts/*.py` 不导入 `ragdefender`。`artifacts/main.py` 自己定义 `find_num_adv`。`ragdefender/cli.py` 的 `reproduce` 只转调用 `claims/*/run.sh` |
| 作者文档中的公式差异 | REPORTED | `docs/reproducing-paper.md` 写明 `ConcentrationBasedGrouping` 与论文公式有三处已记录差异，`expected/result.txt` 对齐遗留实现。本机没有跑测试，所以这不是 `ALGORITHM_CHECK` |

模型配置只核到文件内容，没有下载权重：

| 文件 | SHA-256 | 模型 id | 本机可运行性 |
| --- | --- | --- | --- |
| `artifacts/model_configs/llama7b_config.json` | `dbeef84c33d1c0433ddf595fe726c76374c9d1414395763b743ac93f747a9291` | `meta-llama/Llama-2-7b-chat-hf` | BLOCKED。配置里的密钥字段是占位符，不是可用凭证。Llama 2 权重许可是否已在本机获准为 UNKNOWN |
| `artifacts/model_configs/vicuna7b_config.json` | `775774c0977e84408f97ada7a2d42b92c120c202c339deb14cbd55fa11dfb6f8` | `lmsys/vicuna-7b-v1.3` | UNKNOWN。权重未下载，许可证接受状态未核 |

`artifacts/src/models/Llama.py` 把 `load_in_8bit` 写成代码常量 `True`。Vicuna 配置读取 `load_8bit`，而该 JSON 的值是 `False`。三个 `run.sh` 的注释写的是 8-bit。这是上游文件之间的不一致，本轮没有修改。

## 4. 三个 Artifact Claims

三个 Claim 的状态都是 `NOT_RUN`。没有 `SMOKE`，没有 `ALGORITHM_CHECK`，没有 `ARTIFACT_CLAIM_REPRO`。

| Claim | 入口 | 脚本调用 | 数据集 / 检索器 / 生成器 | 依赖 | expected 文件 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| PoisonedRAG | `ragdefender reproduce claim1`；`claims/claim1_poisonedrag/run.sh` | `conda run -n artifact_acsac python run_poisonedrag.py`，然后 `eval.py --method PoisonedRAG` | NQ、HotpotQA、MS MARCO；expected 文件含 contriever、dpr、ance；LLaMA-7B、Vicuna-7B；扰动比例 100/200/400/600% | 官方 linux env、两个 7B 权重、BEIR 数据。env 不存在，权重未核 | SHA-256 `5124ea6f5c01e3a163f60ae57aabed42e113eb8eaaf7c18f7133a21220005864`，4924 字节 | NOT_RUN / BLOCKED |
| Tan et al. | `ragdefender reproduce claim2`；`claims/claim2_tan/run.sh` | `run_tan.py`，然后 `eval.py --method Tan` | 同上三个数据集；expected 只有 contriever、100% | 同上 | SHA-256 `56433fd30ad76f5e56fdcb46c2fd3e55fa568175757c29da26e76731c8645b94`，839 字节 | NOT_RUN / BLOCKED |
| GARAG | `ragdefender reproduce claim3`；`claims/claim3_garag/run.sh` | `run_garag.py`，然后 `eval.py --method GARAG` | 同上；expected 只有 contriever、100% | 同上 | SHA-256 `7cb98b139bab9ba0fa2c9aff8a48aad76a443b045521d6fe25c0770dbd409a8d`，843 字节 | NOT_RUN / BLOCKED |

`VERIFIED`：Claim 2 与 Claim 3 的 expected 数值行相同，只有方法名 `Tan` / `GARAG` 不同，且 Claim 3 文件没有末尾换行。这是作者提交的 expected 文件事实，不能解释成两次攻击实测相同，也不能填成本机 ASR。

`REPORTED`：作者 `docs/reproducing-paper.md` 把这三个 Claim 映射到论文 Figure 4 的开源模型行。GPT-4o、Gemini、13B、Table 4 的其他 RAG 架构是 `NOT_AUTOMATED` / `OUT_OF_SCOPE`。本任务没有商业 API 授权。

`claim.txt` 的措辞把 Tan 和 GARAG 写成 defense baseline。`run.sh` 和 reproducing 文档把它们写成攻击评估入口。本审计同时保留这两种作者文本，没有改任何一方。

## 5. 运行证据

| 项 | 值 |
| --- | --- |
| 已执行 | Git 预检、`nvidia-smi`、既有 L0 环境的 torch CUDA 探测、公开仓库克隆、上游 diff、conda 环境列表、claim 文件哈希 |
| 未执行 | `conda env create`、`pip install -e .`、pytest、examples、三个 `run.sh`、`ragdefender reproduce` |
| run_id | `W1-5090-R0-20261104` |
| config_hash | `21d6096ea60a92c0a9c4dfdebde5ae1755ad36565b7fb61de3f5948f82a305e0` |
| 命令摘要 | `docs/paper1/dual_machine/repro5090/logs/r0_initial_audit_commands.txt` |
| logs_hash | `0f6b3de615c5d19d795b49df5ead98d1df85baa2d56229dbe1dbd2efe5b572ab` |
| sample_n | UNKNOWN |
| 未防御 ASR | NOT_MEASURED |
| RAGDefender 后 ASR | NOT_MEASURED |
| QA accuracy | NOT_MEASURED |
| 峰值 VRAM / 墙钟 | Claim 未运行，没有 Claim 资源曲线。GPU 预检时占用 0 MiB |

## 6. 障碍与下一步

没有环境修复。没有 before/after patch。没有算法或评测语义改动。

| 障碍 | 状态 | 原因 |
| --- | --- | --- |
| 仓库里没有 Claim 运行的批准提交 | BLOCKED | 现行 `current_work_state` 与 `PODR-153` 的范围是 L0，不是 RAGDefender artifact。5090 不能自批 |
| 官方 conda 环境 | BLOCKED | `artifact_acsac` 不存在。`env.yml` 是 linux-64 锁文件，不能在 Windows 原生 conda 上按原文件创建 |
| 生成器权重 | BLOCKED | 配置指向 Llama-2-7B-chat 与 Vicuna-7B-v1.3。本机没有完成许可确认，也没有下载 |
| torch 2.4.0 与 RTX 5090 | UNKNOWN | 官方钉的是 2.4.0。本机只证明了另一个环境里的 torch 2.8.0+cu128 能做一次张量运算。升级 torch 会成为兼容轨道，不能叫原环境复现 |
| Claim 2/3 expected 数值相同 | REPORTED | 上游文件如此。运行前不修改 expected，运行后单独记录差异 |

可继续且不改变实验语义的事：保持这条分支上的审计记录；5060 用只读 `git fetch` 和 `git show` 取文件。

仍需 Owner / 控制面决定后才能做：在 WSL 创建隔离 `artifact_acsac`；确认 Llama 2 与 Vicuna 的本机使用许可；如官方 torch 2.4.0 不能在 sm_120 加载，再单开兼容环境并记录偏差；然后才运行 Claim。未批准前不调用付费 API，不读 D1/D2/D3。

## 7. 环境安装补记（2026-11-04 20:01 UTC+8）

第 6 节是安装前的审计快照。用户随后要求先把环境和依赖装好。Claim 仍然没有运行。

| 项 | 状态 | 结果 |
| --- | --- | --- |
| 官方环境 `artifact_acsac` | VERIFIED | 在 WSL Ubuntu 24.04 的 Miniforge 里按 `artifacts/env.yml` 创建。第一次因 strict channel priority 失败；隔离 CONDARC 重试 EXIT 0。没有改用户 condarc |
| 官方 torch 2.4.0+cu121 | BLOCKED | 能看到 RTX 5090，capability (12, 0)，一次 CUDA 张量运算报 no kernel image。这个环境没有升级 |
| 兼容环境 `artifact_acsac_compat` | VERIFIED | 官方环境的副本。只在这个副本里换成 torch 2.8.0+cu128。一元素 CUDA 求和为 1.0。这不是作者环境 |
| 兼容栈其余差异 | VERIFIED | triton 3.4.0、sympy 1.14.0、bitsandbytes 0.45.5。官方环境仍是 0.43.1 / triton 3.0.0 / sympy 1.12 |
| faiss | VERIFIED | 两个 wheel 都在。`import faiss` 解析到 faiss-cpu 1.8.0，CPU 索引可建 |
| xformers 0.0.27.post2 | REPORTED | 装在兼容环境里，但 CUDA 扩展对不上 torch 2.8。artifact 代码不导入它 |
| `ragdefender` 0.2.0 | VERIFIED | 只在兼容环境做了 editable 安装，导入成功 |
| 权重与 Claim | BLOCKED / NOT_RUN | 没有下载 Llama-2 或 Vicuna。没有 ASR，没有准确率 |

## 文档收口

- human_ledger_checked = true；human_ledger_updated_if_required = true
- agent_ledger_checked = true；agent_ledger_updated = true
- current_work_state_updated = true
- execution_log_appended = true
- experiment_master_condition_evaluated = true；已追加一条无指标的 R0 索引
- owner_decision_condition_evaluated = true；没有新的 Owner 决定，登记册不改
- stage_process_condition_evaluated = true；没有新的论文阶段关闭，不改
- lessons_condition_evaluated = true；没有可复用的新方法学结论，不改
- research_authority_condition_evaluated = true；冻结合同未进入仓库，不改研究计划权威
- readme_condition_evaluated = true；导航入口未改

5060 只读获取：`git fetch origin research/paper1-ragdefender-repro-5090`，然后 `git show origin/research/paper1-ragdefender-repro-5090:docs/paper1/dual_machine/repro5090/W1_5090_R0_INITIAL_STATUS.md`。不要合并这条分支。
