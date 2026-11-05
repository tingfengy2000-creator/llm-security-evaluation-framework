# Owner 本人要完成的许可操作

本文件只给项目负责人自己用。5090 没有登录、没有点同意、没有提交申请、没有保存 token。Owner 愿意申请，也不等于已经获准，更不等于可以下载或跑 Claim。

每项只需回传：`已提交`、`获批`、`未获批` 或 `需补充信息`，以及确认适用的条款名称。不要把 token、密码、邮箱正文或申请表全文发回仓库。

## Llama 2 7B chat

| 项 | 内容 |
| --- | --- |
| 官方入口 | 模型页 `https://huggingface.co/meta-llama/Llama-2-7b-chat-hf`。本轮核实的修订是 `f5db02db724555f92da89c216ac04704f23d4590`，不要用浮动的 `main`。许可文本来自 `meta-llama/llama-models` 的 Llama 2 Community License，SHA-256 `e30d9339da533205f88140009e32d62c1d73911b8a0bef0d0b252f549ed8e9c4`。模型仓库里的 `LICENSE.txt` 返回 401，没有读取 |
| 账户操作 | 由 Owner 自己登录 Hugging Face，打开该修订的许可，自己决定是否同意，然后提交访问申请并等待 Meta。Worker 不代点 |
| 许可内容 | 协议日期 2023-07-18，覆盖训练权重。再分发要附带 Community License 声明。月活超过 7 亿需要另向 Meta 申请。本机是否已经同意仍是 `NOT_ACCEPTED/UNKNOWN` |
| 需填资料类别 | 名、姓、出生日期、国家、所属单位，以及是否接受许可和 Meta 隐私政策。这里只列类别 |
| 回传 | 申请已提交、获批、未获批或需补充。不要回传表单内容 |
| 待确认 | 获批后的冻结修订仍必须是上面的 SHA。获批本身不批准下载 |
| 不要共享 | 账号邮箱、token、登录状态、出生日期和申请正文 |

## Vicuna 7B v1.3

| 项 | 内容 |
| --- | --- |
| 官方入口 | `https://huggingface.co/lmsys/vicuna-7b-v1.3`，修订 `236eeeab96f0dc2e463f2bebb7bb49809279c6d6`。代码仓库 `https://github.com/lm-sys/FastChat` 的 LICENSE 是 Apache-2.0，那是代码许可 |
| 账户操作 | 页面不是手动门禁。Owner 自己阅读模型卡上的 Non-commercial 声明并决定本研究是否符合。不需要 Worker 代为联系 LMSYS |
| 许可内容 | 模型卡写 Non-commercial license，微调自 LLaMA（arXiv 2302.13971，Llama 1，不是 Llama 2）。不得换成更新版本 |
| 需填资料类别 | 无公开申请表。若 Owner 认为必须另询权利人，由 Owner 自己联系 |
| 回传 | 是否接受该非商业条款用于这项研究复现 |
| 待确认 | FastChat 的 Apache-2.0 不能当成权重许可 |
| 不要共享 | 任何私信原文和账号标识 |

## Contriever

| 项 | 内容 |
| --- | --- |
| 官方入口 | 权重页 `https://huggingface.co/facebook/contriever`，修订 `2bd46a25019aeea091fd42d1f0fd4801675cf699`。代码仓库 `https://github.com/facebookresearch/contriever` |
| 账户操作 | 没有门禁按钮。Owner 需要决定代码仓库的许可是否覆盖这份权重。若决定联系作者，由 Owner 自己通过官方仓库联系，Worker 不发邮件或私信 |
| 许可内容 | 代码 LICENSE 开头是 Attribution-NonCommercial 4.0 International，文本 SHA-256 `c1ff5b40378d5dc3126d708bc9291a4c0c4101002f7bab9e344ec01e18b6e957`。GitHub 给出的 SPDX 是 `NOASSERTION`。HF 模型卡没有 license 字段，所以权重许可仍是 `UNKNOWN` |
| 需填资料类别 | 若联系作者，只说明用途是复现公开论文，不附带本项目私有数据 |
| 回传 | 权重许可是否被 Owner 接受，以及依据是代码 LICENSE 还是作者答复 |
| 待确认 | 在 Owner 写明依据前，下载批保持阻断 |
| 不要共享 | 私信、邮箱和任何访问令牌 |

## paraphrase-MiniLM-L6-v2

| 项 | 内容 |
| --- | --- |
| 官方入口 | `https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2`，修订 `c9a2bfebc254878aee8c3aca9e6844d5bbb102d1`。这不是 `all-MiniLM-L6-v2` |
| 账户操作 | 仓库不是门禁。Owner 自己确认是否接受模型卡上的 `apache-2.0`。作者脚本写了 `trust_remote_code=True`，真正运行前还要单独决定是否允许执行仓库代码。本轮没有加载 |
| 许可内容 | 模型卡 license 字段是 apache-2.0。README SHA-256 `8de1a9ab4f83f29f1ea01d12b4e1c03d18781d3c0fabbd4044c01bd67dd40f78` |
| 需填资料类别 | 无申请表 |
| 回传 | 是否接受该修订的 Apache-2.0，以及以后加载时是否允许 `trust_remote_code` |
| 待确认 | 接受 Apache-2.0 仍然不批准下载 |
| 不要共享 | token |

## BEIR 三个子集

| 项 | 内容 |
| --- | --- |
| 官方入口 | 代码 `https://github.com/beir-cellar/beir`，Apache-2.0，只覆盖代码。数据 zip 在达姆施塔特公开目录。BEIR 自述不声称用户已经获得数据许可 |
| 账户操作 | 没有统一申请按钮。Owner 按子集分别决定。HotpotQA 自己的 README 写数据集是 CC BY-SA 4.0。NQ 的 README 没有写数据许可，仓库 SPDX Apache-2.0 不能自动覆盖 BEIR 副本。MS MARCO 本次读到的 README 也没有数据许可 |
| 许可内容 | NQ 与 MS MARCO 的数据许可是 `UNKNOWN`。HotpotQA 数据集许可有明文，但是否用于本研究仍未由 Owner 接受 |
| 需填资料类别 | 若某个子集要求单独协议，由 Owner 在官方页面填写。不要把协议正文放进 Git |
| 回传 | 三个子集各自是接受、拒绝或仍未知 |
| 待确认 | 解压体积未知。即使许可通过，也要先冻结解压硬停才能下载 |
| 不要共享 | 账号、协议附件和任何数据样本 |

申请进度不能自动打开下载或 Claim。
