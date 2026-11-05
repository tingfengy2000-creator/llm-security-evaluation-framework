# Claim 静态副作用

上游 `ba2a17efba165d45409114df2d70b030ade1e1b8`。六个入口用 `ast.parse` 通过，没有生成 pyc，也没有 import。三条 `run.sh` 此前 `bash -n` 已通过，本轮没有重跑 Smoke。

所有格子都是 `NOT_RUN`。下面的命令文本不是批准，也没有执行。

## 格子

Claim 1 的活跃循环是 3 个数据集 × 2 个 7B × 4 个附加强度，共 24 格。检索器只有 `contriever`。`dpr` 和 `ance` 在 `run_poisonedrag.py` 第 78 行被注释。seed 12，`repeat_times` 10，`M` 10，计划每格 100 条。NQ 与 HotpotQA 的 split 是 `test`，MS MARCO 是 `train`。NQ 的 `top_k` 和 `adv_per_query` 是 5，附加值 0/5/15/25。另外两个数据集是 2 和 0/2/6/10。评测比例公式给出 100/200/400/600%。这不覆盖图 4 的 GPT-4o，也不覆盖图 5 的 13B 和商业模型。

Claim 2 和 Claim 3 各 6 格，附加强度只有 0，所以只有 100%。日志目录分别按脚本写成 `logs/main_logs_tan_12` 和 `logs/main_logs_GARAG_12`。JSON 在 `results/query_results/` 下。作者 `expected/result.txt` 仍只算 `AUTHOR_EXPECTED`。

`eval.py` 把结果打到标准输出，`run.sh` 没有重定向这段输出。`set -euo pipefail` 加上 `check=True`，第一格失败会停掉同一次 Claim 的后续格子。没有重试循环。

## 会自己联网的调用

`load_beir_datasets_md` 在 `artifacts/datasets/<name>` 不存在时下载 zip。当前该目录不存在。Contriever、DPR、ANCE 用 `from_pretrained` 或 `SentenceTransformer`，没有 `local_files_only`。`main.py` 第 142 行和 `main_abl.py` 第 148 行构造 `paraphrase-MiniLM-L6-v2`，并带 `trust_remote_code=True`。`Llama.py` 第 19 行写死 `load_in_8bit=True`，并读取 `HUGGINGFACE_HUB_TOKEN`。这些调用本轮都没有执行。

## 需要单独决定的差异

| 点 | 位置 | 最小选项 | 对数字的影响 | 状态 |
| --- | --- | --- | --- | --- |
| Tan 目录 | `run_tan.py` 第 37 行创建 `logs/main_tan_<seed>`，第 50 行写入 `logs/main_logs_tan_<seed>`。`eval.py` 第 136 行也读后者 | 先只建目标目录，或改一行路径。两者都还没做 | 不改公式，但第一格会在写日志时失败，后面的格子不会跑 | 单独批准前 Claim 2 不可跑 |
| 表 7 | 文档要求 `--p` 和 `--m`。`main_abl.py` 的参数止于 `--method`。TF-IDF 在 `main.py` 第 50 行切片 5。频率分在第 247 行是 `sim * sim` | 要暴露参数就必须改源码 | 会改变分组和打分，不能和默认 Claim 混成同一结果 | `REQUIRES_PATCH` |
| 表 5 | 循环和 `eval.py` 第 208 到 210 行都把检索器限成 Contriever | 取消注释并另下 DPR、ANCE | 换检索器，不是聚类公式补丁，但仍要新权重和新许可 | `REQUIRES_CONFIG` |
| 表 6 | `main.py` 第 59 行把 `AgglomerativeClustering(n_clusters=2)` 写死 | 换成 K-Means 或 DBSCAN 是源码语义更改 | 不能当成普通配置 | 单独 Owner 审核 |
| 表 8 | Claim 路径始终先估计对抗数量再做配对筛选 | 只跑一段没有开关 | 和论文分阶段表不是同一条命令 | `REQUIRES_PATCH` |
| 表 2 和表 3 | `eval.py` 不汇总时间和显存 | 跑 Claim 时另做记录 | 没有自动表 | 不把作者说的 0 显存当成实测 |

## 环境

官方环境仍是 torch 2.4.0+cu121，此前在 sm_120 上没有 kernel。兼容环境是 torch 2.8.0+cu128 和 bitsandbytes 0.45.5。本轮没有再做 GPU 测试。先前记录的 FAISS 导入落到 CPU，xformers 的 CUDA 扩展在 torch 2.8 上不能加载。Vicuna 配置是 5 GiB 上限和 CPU offload，LLaMA 加载器忽略配置里的 8-bit 开关。这些都会让以后的数字偏离论文原机。等级最高只能是未来的兼容复现，现在仍是 `NOT_RUN`。

单格候选是 NQ、Contriever、`llama7b`、100%、seed 12。显存和时间都没有实测。作者对整份 Claim 1 的估计是 4 到 5 小时，不能拆成单格实测。建议的 60 分钟上限还没有生效。
