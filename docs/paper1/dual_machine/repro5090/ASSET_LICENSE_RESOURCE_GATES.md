# 资产、许可与资源门

日期：2026-11-04。这是准备记录，不是下载许可，也不是 Claim 许可。
监督：`W1-OD-20261105-RESOURCE-REPRO-05`，控制面提交 `f491c0a507e5555e9611c022cfba66980ad8cbca`。
本机只读核对了已经提交的体积数字，没有登录、没有下载、没有联网查询。缺许可一律写 `UNKNOWN / OWNER_DECISION_REQUIRED`。

## 1. 资产

| 资产 | 仓库与修订 | 许可 | 本机 | 最小文件 | 体积 |
| --- | --- | --- | --- | --- | --- |
| Llama-2-7B-chat | `meta-llama/Llama-2-7b-chat-hf`。配置写 `revision=main`。上次只读看到的提交是 `f5db02db724555f92da89c216ac04704f23d4590`，还没冻结 | Llama 2 Community License，Hugging Face 手动门禁 | 未下载。本机账号是否已接受许可是 `UNKNOWN` | 单份 F16 权重加分词器。仓库里还有第二套副本，不是最小集 | 仓库 `usedStorage` 53908103645 字节，约 50.21 GiB。单份 F16 约 13476835328 字节，约 12.55 GiB |
| Vicuna-7B-v1.3 | `lmsys/vicuna-7b-v1.3`，上次只读提交 `236eeeab96f0dc2e463f2bebb7bb49809279c6d6`。配置写 `main` | 模型卡写 Non-commercial。微调自 Llama 1。不得换成卡片里的新版本 | 未下载。本机是否接受非商业条款是 `UNKNOWN` | 两片 pytorch bin 中实际被加载的那一套 | `usedStorage` 26954326092 字节，约 25.11 GiB |
| Contriever | `facebook/contriever`，提交 `2bd46a25019aeea091fd42d1f0fd4801675cf699` | 模型卡没有 license 字段。缺字段不是许可 | 未下载 | 该提交的模型与分词器 | 875963049 字节，约 835.6 MiB |
| 段落嵌入器 | `paraphrase-MiniLM-L6-v2`。`artifacts/main.py` 在 Claim 路径里直接构造它，并带 `trust_remote_code=True` | 本轮没有联网核许可，所以是 `UNKNOWN` | 未作为本任务的资产清点到本地可用副本 | 该模型的本地快照 | 压缩和解压体积都是 `UNKNOWN` |
| DPR | `sentence-transformers/facebook-dpr-ctx_encoder-single-nq-base` | `UNKNOWN` | 未下载。当前循环没有调用它 | 该模型快照 | `UNKNOWN` |
| ANCE | `sentence-transformers/msmarco-roberta-base-ance-firstp` | `UNKNOWN` | 未下载。当前循环没有调用它 | 该模型快照 | `UNKNOWN` |
| BEIR `nq` | `https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nq.zip` | 本轮没有重新核数据许可，沿用“需另批” | `artifacts/datasets` 不存在 | zip 和解压后的 corpus/queries/qrels | 压缩 498307926 字节。解压峰值 `UNKNOWN` |
| BEIR `hotpotqa` | 同一站点 `hotpotqa.zip` | 同上 | 未下载 | 同上 | 压缩 654025350 字节。解压峰值 `UNKNOWN` |
| BEIR `msmarco` | 同一站点 `msmarco.zip`。脚本把 split 改成 `train` | 同上 | 未下载 | 同上 | 压缩 1082258632 字节。解压峰值 `UNKNOWN` |

三个 zip 合计 2234591908 字节，约 2.08 GiB。这只是压缩长度。解压后的体积没有测，不能把 2.08 GiB 写成磁盘峰值。

已经在克隆里、本轮没有复制进研究 Git 的作者文件：每个数据集 100 条目标问题；PoisonedRAG 的 `poisoned_corpus/*/gpt4` 各 100 个文件；Tan 各 100 个文件；GARAG 的 nq 118 个、hotpotqa 100 个、msmarco 101 个。这些计数不是评测结果。

## 2. 加载器会做什么

`Llama.py` 不读配置里的 `load_8bit=False`，而是写死 `load_in_8bit=True`，并从环境变量 `HUGGINGFACE_HUB_TOKEN` 取令牌。配置里的钥匙字段是占位符，不是可用令牌。
`Vicuna.py` 读取配置。当前配置是 `load_8bit=False`、`max_gpu_memory=5GiB`、`cpu_offloading=True`。5 GiB 放不下完整 7B float16，实际卸载没有测。
`load_beir_datasets_md` 在 `artifacts/datasets/<name>` 不存在时下载达姆施塔特 zip 并解压。当前目录不存在，所以未来一次未加防护的 Claim 会自己发起下载。
Contriever、DPR、ANCE 和 MiniLM 的构造函数都没有 `local_files_only=True`。

三条 `run.sh` 都是 `set -euo pipefail`。内层 `subprocess.run(..., check=True)`。没有重试。第一次失败会停掉该 Claim 的后续格子。`eval.py` 的表打到标准输出，脚本没有把这段输出重定向到文件。

`run_tan.py` 创建的目录是 `logs/main_tan_<seed>`，真正写入和 `eval.py` 读取的目录是 `logs/main_logs_tan_<seed>`。这是静态缺陷。本轮不改源码。

## 3. 盘符

2026-11-04 23:30 UTC+8 的只读读数：

| 位置 | 可用 | 总容量 | 本轮动作 |
| --- | --- | --- | --- |
| C | 99.3 GiB | 300 GiB | 不新增项目可控内容 |
| D | 739.1 GiB | 931.5 GiB | 研究仓库和上游克隆已经在这里 |
| E | 725.7 GiB | 1607.3 GiB | WSL Ubuntu-24.04 的宿主路径在 E |

WSL 根文件系统显示约 839 GiB 可用，挂在 E 的虚拟磁盘上。Windows `TEMP` 在 C。Windows 用户目录下已经存在 Hugging Face 缓存和 pip 缓存，都在 C；本轮不搬迁。`HF_HOME`、`HUGGINGFACE_HUB_CACHE`、`PIP_CACHE_DIR`、`CONDA_PKGS_DIRS` 都没有设置。WSL 里这些变量也没有设置，默认缓存会进 WSL 家目录，也就是 E 上的虚拟磁盘。

项目可控写入包括模型、语料、缓存、临时解压、conda/pip 下载和结果。这些以后只能落在 D 或 E。操作系统自己的日志和元数据不算项目可控写入，本文件不承诺 C 的绝对零增长。只要某次操作不能保证项目可控部分不写 C，就停止该操作。

D 和 E 不再使用先前的 1 GiB 全局新增上限。这不是无限写盘。下一次真正下载或运行之前，必须先冻结路径、压缩峰值、解压峰值、临时文件峰值，并留下至少 20 GiB 可用空间。解压峰值现在是 `UNKNOWN`，所以下载批还不能冻结。

显存硬停仍是这张 RTX 5090 的 32607 MiB。出现 OOM 就停，不改量化、不改环境来继续。官方环境保持 torch 2.4.0+cu121，它不能在 sm_120 上执行 CUDA kernel。

## 4. 建议的独立审批批

这些批都还没有被批准。顺序是建议，不是执行。

1. 许可批：确认本机可以接受 Llama 2 门禁、Vicuna 非商业条款，并对 Contriever 的空许可字段和 MiniLM 的未核许可作出决定。
2. 模型批：只下载已经冻结的修订，`HF_HOME` 必须先指到 D 或 E。Llama、Vicuna、Contriever、MiniLM 分开列清单。DPR 和 ANCE 不进入这一批。
3. 语料批：三个 BEIR zip。开始前要有解压峰值或一个会触发硬停的字节上限。路径是上游克隆里的 `artifacts/datasets`，位于 D。
4. 单格预检：模型和语料都到位之后，只跑 Claim 1 的一个格子，NQ、Contriever、`llama7b`、`additional_adv_per_query=0`、seed 12。不调用整份 `run.sh`。预检没有作者给出的单格时限；建议 Owner 先冻结 60 分钟，超时即停。这个 60 分钟是待冻结的建议，不是已经生效的限额。
5. Claim 1 其余 23 格、Claim 2、Claim 3 各自单独批准。Claim 2 在目录缺陷被 Owner 决定如何处理之前不能算可跑。
6. Table 5、7、8 和 Table 6 再往后。Table 6 是源码语义更改，必须单独审核。

任何一批出现许可冲突、缓存落到 C、OOM、磁盘余量低于 20 GiB，或脚本试图下载未列入该批的文件，都按 PO-MHEP 停止该批。
