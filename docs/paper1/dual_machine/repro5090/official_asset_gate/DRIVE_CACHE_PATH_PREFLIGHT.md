# 盘符与缓存预检

读数时间是 2026-11-05 上午。没有搬迁环境，没有改用户或系统的 TEMP。

| 位置 | 可用 | 总容量 | 说明 |
| --- | --- | --- | --- |
| C | 99 GiB | 300 GiB | 用户 TEMP 和机器 TEMP 都在 C。Windows 的 Hugging Face 缓存、pip 缓存、`CONDA_PKGS_DIRS` 和 `PIP_CACHE_DIR` 也在 C。本轮不搬 |
| D | 739.1 GiB | 931.5 GiB | 研究仓库和上游克隆在这里。本轮原始 HTTP 日志也在 D 的 Git 外目录 |
| E | 725.7 GiB | 1607.3 GiB | WSL Ubuntu-24.04 的宿主路径在 E |

`HF_HOME`、`HF_HUB_CACHE`、`HUGGINGFACE_HUB_CACHE`、`TRANSFORMERS_CACHE` 和 `XDG_CACHE_HOME` 都没有设置。因此 Windows 上一次未来的 Hugging Face 调用会默认写到 C 的用户缓存。WSL 里这些变量此前也没有设置，默认缓存会进 WSL 家目录，也就是 E 上的虚拟磁盘。

这次审计进程为了不让 Python 的临时文件落在 C，只在该进程里把 TEMP 指到 D 的审计目录。用户和机器的 TEMP 仍是 C。这个进程覆盖不能当成系统已经改好。

项目可控写入包括模型、zip、解压目录、HF 缓存、pip/conda 下载、临时文件和结果日志。它们以后只能在 D 或 E。操作系统自己的日志不算项目可控写入。只要某条命令不能证明项目可控部分不写 C，就停止那条命令。

已知的仓库上限大约是：Llama `usedStorage` 53908103645 字节，Vicuna 26954326092 字节，Contriever 875963049 字节，MiniLM 1111304665 字节，三个 zip 合计 2234591908 字节。D 的剩余空间大于这些上限再加 20 GiB。这只说明今天装得下这些上限，不说明解压后装得下。解压体积是 `UNKNOWN`，所以语料批的预算还没有冻结。

未来任何获批下载之前，进程必须显式把 `HF_HOME`、`HUGGINGFACE_HUB_CACHE`、`TRANSFORMERS_CACHE` 和 `TMPDIR` 设到 D 或 E 的指定目录，并在开始前打印目标盘剩余空间。剩余低于 20 GiB 就停。不得借用 C 上已经存在的 Hugging Face 缓存。
