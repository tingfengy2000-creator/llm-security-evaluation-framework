# 分批复现审批包

2026-11-05 许可回传之后：Vicuna、Contriever、MiniLM 和三个 BEIR 子集的研究使用已被 Owner 接受。Llama 2 只是申请已提交。每一批的执行状态仍然不是下载或 Claim 许可。BEIR 在解压硬停冻结前不能下载。

每一批的执行状态都是 `NOT_APPROVED`。本文件不启动下载、解压或 Claim。结果层级保持分开：论文发表数字 `NOT_MEASURED`，作者 `expected/result.txt` 是 `AUTHOR_EXPECTED`，未来兼容环境复现是 `NOT_RUN`，中文迁移是 `OUT_OF_SCOPE`。

## A — 许可与身份

前置：Owner 已于 2026-11-05 回传。
状态：许可回传已记录。下载和 Claim 仍是 `NOT_APPROVED`。
Llama 2 为 `APPLICATION_SUBMITTED`。Meta 若获批，下一条只记 `待审批`。
Vicuna、Contriever、MiniLM、HotpotQA、NQ、MS MARCO 为 `OWNER_ACCEPTED`。Contriever 的权重覆盖是 Owner 认定，模型卡字段仍为空。NQ 的 CC BY-SA 3.0 和 MS MARCO 条款是 Owner 陈述，不是本轮新的网页摘录。
MiniLM 禁止 `trust_remote_code`。标准加载失败必须停下。
停止条件：解压硬停未冻结时不得下载 BEIR。Llama 未获批且分片大小未知时不得下载 Llama。其余模型即使许可已接受，也要等单独的下载批。

## B — 模型固定修订下载

状态：`BLOCKED / OWNER_DECISION_REQUIRED`。
白名单只允许下面的修订。路径必须在 D 或 E，`HF_HOME` 必须先指到该路径。C 上已有缓存不得被这次下载使用。

| 资产 | 修订 | 上限 | 阻断 |
| --- | --- | --- | --- |
| `meta-llama/Llama-2-7b-chat-hf` | `f5db02db724555f92da89c216ac04704f23d4590` | `usedStorage` 53908103645 字节；逐文件字节 `UNKNOWN` | 门禁未由 Owner 完成，且分片大小未冻结 |
| `lmsys/vicuna-7b-v1.3` | `236eeeab96f0dc2e463f2bebb7bb49809279c6d6` | 树合计 13477481966，`usedStorage` 26954326092。两个数不一致，上限先取较大者 | 非商业条款未接受 |
| `facebook/contriever` | `2bd46a25019aeea091fd42d1f0fd4801675cf699` | 树合计 438708755，`usedStorage` 875963049 | 权重许可 `UNKNOWN` |
| `sentence-transformers/paraphrase-MiniLM-L6-v2` | `c9a2bfebc254878aee8c3aca9e6844d5bbb102d1` | 已知 safetensors 加列出的小文件 91571678；整库 `usedStorage` 1111304665 | Apache-2.0 未接受；必须排除 onnx、openvino 和 tf，否则按整库上限 |

下载后要比对修订 SHA。不匹配就删除该目录并停止。超时建议按文件大小另批，本轮不设已生效时限。不运行模型。

## C — 三个 BEIR zip

状态：`BLOCKED / OWNER_DECISION_REQUIRED`。按数据集分开，不要三个一起默许。
URL 只允许本轮 HEAD 过的三个达姆施塔特 zip。NQ 498307926 字节，ETag `6075b282-1db39356`。HotpotQA 654025350，ETag `60019b87-26fba286`。MS MARCO 1082258632，ETag `6074501d-4081f4c8`。
解压体积 `UNKNOWN`。建议硬停是解压字节超过压缩长度的 8 倍、路径跳出目标目录，或目标盘剩余低于 20 GiB。这是控制建议，不是体积估计。
NQ 和 MS MARCO 的数据许可仍是 `UNKNOWN`。HotpotQA 数据集 README 写 CC BY-SA 4.0，但 Owner 还没接受。目标路径是 D 上克隆里的 `artifacts/datasets`。

## D — Claim 1 单格预检

状态：`BLOCKED`。只有 A、B、C 里该格需要的许可、修订和 NQ 语料都通过，并且 `HF_HOME` 不在 C，才可以另批。
候选格子：NQ、Contriever、`llama7b`、附加 0、seed 12、`top_k` 5、`adv_per_query` 5、split `test`、`M` 10、`repeat_times` 10。计划分母 100，不是实测。
环境只能是 `artifact_acsac_compat`。不要调用整份 `run.sh`，否则会连跑 24 格并可能自行下载。
建议超时 60 分钟，尚未生效。OOM、写 C、出现下载、日志目录没生成，都立即停。显存峰值 `UNKNOWN`。科学等级是未来的兼容复现，不是论文原数字。

## E — 其余 Claim 格子

状态：`NOT_APPROVED`。
Claim 1 剩余 23 格、Claim 2 的 6 格、Claim 3 的 6 格分开批准。Claim 2 在目录差异被决定前保持阻断。可选处理是先创建 `logs/main_logs_tan_12`，或改一行创建目录的路径。两者都还没批准，也都不是算法补丁。
`eval.py` 的表必须重定向到 D 或 E 的日志。作者预期文件不能当成这次输出。

## F — 补充表

状态：`NOT_APPROVED`。
表 5 要另下 DPR 和 ANCE，并改被注释的循环。表 7 和表 8 要改源码才能变成命令。表 6 是聚类语义更改，不能和表 5 的配置开关放在同一批。表 2 和表 3 没有自动汇总。表 4、13B 和商业 API 不在这些批里。

任何一批若脚本仍会自动下载、不能保证避开 C、许可仍是 `UNKNOWN`，或解压上限没有冻结，就保持阻断，不用试跑来补证据。
