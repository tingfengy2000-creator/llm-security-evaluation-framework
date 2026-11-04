# 复现分类与五栏差异

日期：2026-11-04。分类依据是上游 `docs/reproducing-paper.md`、`claims/`、`artifacts/` 和本机已有证据。没有运行 Claim。没有把 Smoke 或作者 `expected/result.txt` 写成论文数字。

上游 `ba2a17efba165d45409114df2d70b030ade1e1b8`，`git describe --tags --always` 为 `v0.2.0-2-gba2a17e`，许可证 MIT。工作区 `git status` 有 2919 行 `M`。`git diff --ignore-cr-at-eol --shortstat` 为空，所以这些 `M` 是 Windows/WSL 换行符，不是内容改动。本轮没有重写源码。

## 1. 图表分类

| 对象 | 分类 | 活跃脚本实际覆盖 | 没覆盖 |
| --- | --- | --- | --- |
| Claim 1 / 图 4 第 1 列的开源 7B 行 | `AUTOMATED_ORIGINAL_ARTIFACT` | NQ、HotpotQA、MS MARCO，Llama-2-7B-chat 与 Vicuna-7B，Contriever，100/200/400/600%，seed 12，重复 10，每轮 M=10，计划每格 100 条 | GPT-4o；DPR；ANCE |
| Claim 2 / 图 4 第 3 列 | `AUTOMATED_ORIGINAL_ARTIFACT` | 三个数据集、两个 7B、Contriever、只有 100% | 200/400/600%；并且日志目录名和评测脚本不一致 |
| Claim 3 / 图 4 第 2 列 | `AUTOMATED_ORIGINAL_ARTIFACT` | 同样只有 100% | 200/400/600% |
| 图 4 的 GPT-4o 格子 | `COMMERCIAL_API` | 无 | 需要自备配置和钥匙。本项目默认不调用付费接口 |
| 图 5 的 7B | 随 Claim 1 产生两个 7B 的四档强度 | 作者没有写明图 5 用哪一档强度，所以档位是 `UNKNOWN` | 不能从 Claim 1 的 24 格里挑一格冒充图 5 |
| 图 5 的 13B | `REQUIRES_CONFIG` | 仓库没有 13B 配置。Tan/GARAG 里有被注释掉的 `vicuna13b` | 权重、显存和命令都要另批 |
| 图 5 的 GPT-4o 与 Gemini-1.5-pro | `COMMERCIAL_API` | 无 | 不列入首轮 |
| 表 2 时间与费用 | `REQUIRES_PATCH` | 循环里有计时痕迹，`eval.py` 不汇总 | 不把作者口头成本写成实测 |
| 表 3 显存 | `REQUIRES_PATCH` | 作者要求跑 Claim 时手工看 `nvidia-smi` | 作者写 RAGDefender 一行应为 0。那是作者陈述，不是本机测量 |
| 表 4 多架构 | `EXTERNAL_REPO` | 仓库里没有 BlendedRAG、REPLUG、SELF-RAG | 不凭空补齐 |
| 表 5 DPR/ANCE | `REQUIRES_CONFIG` | `run_poisonedrag.py` 里 DPR/ANCE 循环被注释。`eval.py` 也把 PoisonedRAG 限成 Contriever | 需要额外模型和脚本开关。还不是算法语义补丁 |
| 表 6 聚类替换 | `REQUIRES_PATCH` | 现用路径把 `AgglomerativeClustering(n_clusters=2)` 写死 | 换成 K-Means 或 DBSCAN 要改源码，单列等 Owner |
| 表 7 `p`/`m` | `REQUIRES_PATCH` | 文档写给 `main_abl.py` 传 `--p` 和 `--m`。该文件的参数表没有这两项。TF-IDF 切片写死 5，频率分写死 `sim * sim` | 文档和源码冲突。不能靠现成命令复现这张表 |
| 表 8 分阶段 | `REQUIRES_PATCH` | Claim 路径始终走 artifact 自己的合并实现 | 只跑第一阶段或只跑第二阶段都没有开关 |
| 中文迁移 | `OUT_OF_SCOPE` | 无 | 属于以后的 R3，不由这份计划授权 |

`claim1` 的 `claim.txt` 写了 Contriever、DPR、ANCE。可执行循环只有 Contriever。以循环为准。

三条 Claim 的状态都是 `NOT_RUN`。无防御 ASR、有防御 ASR、问答准确率都是 `NOT_MEASURED`。`expected/result.txt` 只记了 SHA-256，等级是 `AUTHOR_EXPECTED`。

## 2. 五栏实现边界

| 点 | 论文公式与硬件 | 作者 legacy artifact | 开源库 v0.2 | 本机 RTX 5090 | 未来中文迁移 |
| --- | --- | --- | --- | --- | --- |
| 机器 | 一台 Quadro RTX 8000，约 48 GB，作者文档说论文非量化 | 文档说 8-bit 是为了 16 GB 显卡，数字会略有不同 | 库本身不绑定这张卡 | 32607 MiB。官方 torch 2.4.0+cu121 看见 sm_120 但没有 kernel。兼容环境 torch 2.8.0+cu128 做过一次求和 1.0 | 未批准，未定义 |
| 浓度分组 | 论文 Eq. 3 是均值和中位数都超过阈值才计数 | `artifacts/main.py` 用 OR，阈值是 `(median+mean)/2`，并在 `global_mean >= global_median` 时用总数去减 | `ConcentrationBasedGrouping` 保留同一套 legacy 行为，并写明不要静默改成论文公式 | 离线 Smoke 只在虚构向量上跑过空输入和一组假样本，不是这条公式的论文核对 | 不能把中文语料直接套上这条有偏差的实现后称作论文复现 |
| 8-bit | 论文原设置不是这条 artifact 的 8-bit 路径 | LLaMA 加载器写死 `load_in_8bit=True`。Vicuna 配置写 `False`，上限 5 GiB | 包的公开 API 不负责加载这两个生成器 | 兼容环境的 bitsandbytes 是 0.45.5，官方环境仍是 0.43.1。8-bit 数字以后只能标兼容复现 | 未测 |
| 第二阶段 | 论文有识别对抗段落的步骤 | `main.py` 自己算配对数并取前 `N_adv`，不调用 `ragdefender` 包 | v0.2 的 `defend()` 会调用 `IdentifyAdversarial`。v0.1.1 只做截断 | Claim 脚本将来跑的是 artifact 文件，不是包的 `defend()` | 未批准 |
| 嵌入器 | 算法文档写论文用 Stella，v0.2 默认改到 `minilm-all`，Stella 留到 Phase 6 | Claim 路径加载 `paraphrase-MiniLM-L6-v2` | 默认预设不是 Stella | 这个 MiniLM 还没获准下载，体积和许可都是 `UNKNOWN` | 中文嵌入器会再引入一层偏差 |
| 检索器 | 论文还有 DPR、ANCE 和多架构 | 活跃 Claim 只有 Contriever。表 5 要改注释 | 包不下载 Contriever 权重 | Contriever 许可字段缺失，未下载 | 未批准 |
| 结果等级 | 论文原数字 | 作者预期文件 | 库的单测不等于 artifact Claim | 以后若获批，等级最高是 `COMPATIBILITY_ARTIFACT_REPRO`，不是原机严格复现 | 独立协议，不自动继承 R1 |

兼容环境与官方环境的 20 个包差异仍在此前的审批门里。torch、CUDA、cuBLAS、cuDNN、triton 和 8-bit 库都可能改变以后的数字。FAISS 导入仍落到 CPU。本轮没有重跑 Smoke，也没有安装 pytest。
