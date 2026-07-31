# Paper 1 外部 Artifact 登记册

## 核验口径

- 核验日期：`2026-07-31`。
- commit 来自对官方 GitHub 仓库默认分支执行 `git ls-remote` 后的 HEAD。
- “官方”由论文正文/脚注或论文官方页面的代码链接支持。
- 当前 HEAD 只是本轮准备快照；它不自动等于作者生成论文结果时使用的 commit。
- 未发现根目录 `LICENSE` 时记录为许可 blocker，不推定默认开源许可。

## Artifact

| ID | 角色 | 正式论文 | 官方仓库 | 核验 HEAD | 代码许可 | 当前状态 |
| --- | --- | --- | --- | --- | --- | --- |
| `EXT-P1-POISONEDRAG` | Primary Attack Baseline | [USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag) | [sleeepeer/PoisonedRAG](https://github.com/sleeepeer/PoisonedRAG) | [`f660d72174f06b13fae5163ce656e7b235db858f`](https://github.com/sleeepeer/PoisonedRAG/commit/f660d72174f06b13fae5163ce656e7b235db858f) | MIT | `SOURCE_VERIFIED / NOT_RUN` |
| `EXT-P1-GMTP` | Primary Detection / Defense Baseline | [ACL Findings 2025](https://aclanthology.org/2025.findings-acl.1263/) | [mountinyy/GMTP](https://github.com/mountinyy/GMTP) | [`15b48d150f93711371eb8da22c211cd84a0cf4df`](https://github.com/mountinyy/GMTP/commit/15b48d150f93711371eb8da22c211cd84a0cf4df) | `LICENSE FILE NOT FOUND / BLOCKED_FOR_REDISTRIBUTION` | `SOURCE_VERIFIED / NOT_RUN` |
| `EXT-P1-SAFERAG` | Primary Benchmark / Evaluation Reference | [ACL 2025 Long Paper](https://aclanthology.org/2025.acl-long.230/) | [IAAR-Shanghai/SafeRAG](https://github.com/IAAR-Shanghai/SafeRAG) | [`e8f579743b23e0a3937076dcc0792fe29027cba3`](https://github.com/IAAR-Shanghai/SafeRAG/commit/e8f579743b23e0a3937076dcc0792fe29027cba3) | `LICENSE FILE NOT FOUND / BLOCKED_FOR_REDISTRIBUTION` | `SOURCE_VERIFIED / NOT_RUN` |
| `EXT-P1-ECOSAFERAG` | Deferred reference | `TO_VERIFY` | `OFFICIAL REPOSITORY NOT VERIFIED` | `UNKNOWN` | `UNKNOWN` | `DEFERRED` |

## 数据许可

| 数据 | 一手许可记录 | 当前使用结论 |
| --- | --- | --- |
| Natural Questions | [Google NQ 页面](https://ai.google.com/research/NaturalQuestions/download)记录 CC BY-SA 3.0 | 研究使用前仍需保存具体下载版本和派生语料义务 |
| HotpotQA | [HotpotQA 官方页面](https://hotpotqa.github.io/)记录数据/处理 Wikipedia 为 CC BY-SA 4.0 | 允许研究准备；派生发布必须保留署名和 share-alike 审查 |
| MS MARCO | [Microsoft 官方条款](https://microsoft.github.io/msmarco/)限定 non-commercial research，并不授予底层文档权利 | 只允许非商业研究；公开 Artifact 前独立 legal/license review |
| GMTP 提供的 200 poisoned samples | 仓库未发现 LICENSE | 只做来源核验；复制、修改、再分发前必须取得明确许可 |
| SafeRAG 数据与知识库 | 仓库未发现 LICENSE；README 仍列出未来 Hugging Face release TODO | 只做来源核验；复制、修改、再分发前必须取得明确许可 |

## 源码与论文差异提醒

### PoisonedRAG

- 官方 README 环境为 Python 3.10、PyTorch 1.13.0 + CUDA 11.7。
- 当前 HEAD `f660d72...` 是 2026 年的 results loading bug fix，晚于论文；必须向作者材料或历史 commit
  追溯 paper-result commit，才能建立严格复现身份。
- README 默认 `top_k=5`、`adv_per_query=5`、10 次重复，每次 10 个 target questions。

### GMTP

- 论文脚注明确给出 `mountinyy/GMTP`。
- README 的下载命令拼写为 `donwload_datasets.py`，实际根文件名是 `download_datasets.py`；复现清单必须记录此
  documentation patch，不能静默更改。
- 论文定义 final `k=10`；仓库脚本先 retrieve 20，再 rerank/filter 到 10。两者可以兼容，但 manifest 必须同时记录
  candidate K 与 final K。
- Dockerfile 使用 PyTorch 2.5.1 + CUDA 12.4 + Java 21；requirements 同时列出 GPU/CPU FAISS 变体，依赖并非完整锁文件。
- 根目录未发现 LICENSE。

### SafeRAG

- README quick start 默认 BM25、Top-K 6、Silver Noise、indexing injection，并依赖 API evaluator/generator。
- 论文还覆盖 DPR、Hybrid、Hybrid-Rerank、NLI、SKR 以及 8 个 generator。
- requirements 的 `torch` 未锁版本，模型 revision、API snapshot 和若干依赖未冻结。
- 根目录未发现 LICENSE。

## 仍需向作者或 artifact 补齐

1. PoisonedRAG paper-result commit/tag 和完整依赖锁。
2. GMTP、SafeRAG 代码与数据的明确许可证。
3. 三项工作的精确模型 revision、数据快照 hash 和预处理 hash。
4. PoisonedRAG 的作者运行 GPU/RAM/disk；GMTP/SafeRAG 的 RAM/disk。
5. API 模型的可复现实验 snapshot 或等价的本地模型轨道。
