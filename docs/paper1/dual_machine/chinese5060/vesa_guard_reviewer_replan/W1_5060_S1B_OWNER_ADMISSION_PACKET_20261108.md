# Paper 1｜5060 S1-B Owner 审批包

2026-11-08 JST · `W1-OD-20261108-5060-S1B-B-DESIGN-17` · **S1B_DESIGN_ONLY / MODEL_DOWNLOAD_NOT_AUTHORIZED / MODEL_INFERENCE_NOT_AUTHORIZED / VALIDATION_NOT_AUTHORIZED / S2_S5_LOCKED** · **Auto Continue = NO**。

5060 发布检出干净，从 `39debd9f53d501a4df99f345fdf6d7b80d90d9d7` 快进到授权头 `35bcb797a59163058e4c560890f88c3197f6d343`。原证据工作树保留。研究目标仍为中文 RAG 的版本与范围感知后检索防御，S1-B 只设计抽取模块对照。旧 S1 `S1_FAIL_STOP`（值命中 31/61、已决定错抽 4/34），旧 R2 `K1-C`。本轮只读论文、公共源码/许可证、模型元数据和本机清单。权重下载、安装、加载、推理、试次、新样本、费用均为 0。 [Owner B 设计原件](W1_5060_S1B_LITERATURE_MODEL_RESOURCE_INDEPENDENT_VALIDATION_PROPOSAL_20261108.md) · [旧 S1](W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_RESULT.md)

## 1. 文献与实现复用

| 技术、作者与论文 | 复用结论与 M2 关系 | 代码、数据与权重的许可边界 |
| --- | --- | --- |
| RAGDefender，Minseok Kim、Hankook Lee、Hyungjoon Koo，ACSAC 2025 | **直接复用**已有固定过滤接口与 B2/RD-zh 对照证据。原论文 §4 单跳用聚类加 TF-IDF 估计污染数，多跳用相似度集中度。第二阶段按高相似片段对的频率分数选择删除。2026 v0.2.0 源码用实际索引，修复 v0.1.1 尾部截断。多跳实现的 OR/反转细节应与论文分列。固定单跳路径只将片段传给聚类、计数和打分，`query` 保留在 API 签名，未参与核心判据。原论文用 Stella，5060 B2 用固定多语 MiniLM，两套结果不可混报。 | 固定库 `ba2a17efba165d45409114df2d70b030ade1e1b8` MIT。Stella 当前卡标 MIT（历史论文权重精确快照 UNKNOWN，卡示例请求远程代码，本批不采用），B2 固定 MiniLM 卡标 Apache-2.0。代码许可不转授论文资产与模型。 [论文](https://doi.org/10.1109/ACSAC67867.2025.00093) · [固定官方库](https://github.com/SecAI-Lab/RAGDefender/tree/ba2a17efba165d45409114df2d70b030ade1e1b8) · [入口与参数](https://github.com/SecAI-Lab/RAGDefender/blob/ba2a17efba165d45409114df2d70b030ade1e1b8/ragdefender/defender.py) · [Stella 卡](https://huggingface.co/NovaSearch/stella_en_1.5B_v5) · [B2 固定卡](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1/README.md) |
| X-MADAM-RAG，Yongqi Kang、Yu Fu、Yong Zhao，arXiv:2606.12903v1 | **参考设计**。按文档抽取，缺失候选仅用可见证据修复，标准化后确定性分组，单组答复、多组枚举冲突、无组拒识。标准化、同值分组及冲突汇总与 M2 重叠。自然化子集提示抽取瓶颈，不能作为中文攻击鲁棒性证据。 | 论文 CC BY-SA 4.0。论文所用 Qwen2.5-7B-Instruct 是另一个模型，发布权重声明 Apache-2.0，本文不纳入。作者可核代码、数据许可与锁定实现均 UNKNOWN，**尚无有效实现证据**。 [论文 §4.2](https://arxiv.org/html/2606.12903v1#S4.SS2) · [7B 官方卡](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) |
| MADAM-RAG，Han Wang、Archiki Prasad、Elias Stengel-Eskin、Mohit Bansal，COLM 2025 | **参考设计**。逐文档论证、多轮辩论和聚合器解歧，与 M2 的冲突处理有关；不引入辩论、Judge 或额外调用。 | 作者 RAMDocs 仓 `d44454c9ebb0bf513d8236a03decc9fb58704cad` MIT。数据上游条款另核。论文示例的 Llama 3.3 属 Meta 独立模型协议，其他闭源端点不提供可复用权重；未复现。 [论文](https://arxiv.org/abs/2504.13079v2) · [作者仓](https://github.com/HanNight/RAMDocs/tree/d44454c9ebb0bf513d8236a03decc9fb58704cad) · [Llama 3.3 许可](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct/blob/main/LICENSE) |
| ACL 2022 UIE，Yaojie Lu、Qing Liu、Dai Dai、Xinyan Xiao、Hongyu Lin、Xianpei Han、Le Sun、Hua Wu | **参考设计**。结构化抽取语言和 schema 指令可借鉴。论文是生成式统一抽取，和 PaddleNLP 的候选跨度接口分开核证。 | 作者仓 `c88dd08b8ad0016ec597ebc6f8fff49480367bb2` 明示代码 CC BY-NC-SA 4.0。外链权重许可 UNKNOWN。禁止把其代码条款或权重身份继承到 PaddleNLP。 [论文](https://aclanthology.org/2022.acl-long.395/) · [作者仓许可说明](https://github.com/universal-ie/UIE/tree/c88dd08b8ad0016ec597ebc6f8fff49480367bb2#license) |
| PaddleNLP 中文 UIE，PaddlePaddle/PaddleNLP Authors | **直接复用候选接口**。Taskflow 以 schema 做提示式 span 抽取，能返回 start/end 与分数。分数不是语义、版本或来源证明。复用批准与安装仍在后续门。 | `v2.6.1@fd2bed541ff929f6f8b350001694e553b29d4e9a` 代码 Apache-2.0，BOS 五项资产权重/分词器的明确适用条款 UNKNOWN。项目许可和模型文件清单不能替代权重许可。 [固定代码](https://github.com/PaddlePaddle/PaddleNLP/blob/fd2bed541ff929f6f8b350001694e553b29d4e9a/paddlenlp/taskflow/information_extraction.py) · [代码 LICENSE](https://github.com/PaddlePaddle/PaddleNLP/blob/fd2bed541ff929f6f8b350001694e553b29d4e9a/LICENSE) |
| ODIE，Yizhu Jiao、Ming Zhong、Sha Li、Ruining Zhao、Siru Ouyang、Heng Ji、Jiawei Han，EMNLP 2023 | **参考设计**。从用户指令形成抽取字段和表结构，可借鉴字段约束和显式缺失。 | 作者仓 `549e55d0d866057d75e3aa4cddb132b56d9a0ca0` 有训练/评价代码，完整树未见 LICENSE。代码许可 UNKNOWN，论文 ODIE 基于 LLaMA-7B+LoRA，基础权重与适配器条款各须核实。可直接用于本机的小型中文权重证据 UNKNOWN。 [论文](https://aclanthology.org/2023.emnlp-main.620/) · [作者仓](https://github.com/yzjiao/On-Demand-IE/tree/549e55d0d866057d75e3aa4cddb132b56d9a0ca0) |
| InstructUIE，Xiao Wang、Weikang Zhou、Can Zu、Han Xia、Tianze Chen、Yuansen Zhang、Rui Zheng、Junjie Ye、Qi Zhang、Tao Gui、Jihua Kang、Jingsheng Yang、Siyuan Li、Chunsai Du，arXiv:2304.08085v1 | **参考设计**。任务指令、公开选项、正文和输出结构可借鉴，论文实验主干是 Flan-T5 11B。 | 作者可核仓、适用代码许可、InstructUIE 微调权重许可和固定发行身份 UNKNOWN，**尚无有效实现证据**。基础模型许可不能替代微调权重条款。 [论文](https://arxiv.org/html/2304.08085v1) |

原 ACSAC PDF 用本机既有副本校验 SHA256 `11bb7a9e24620847c54a0748be087ecde23aa7c204c32d912a1bdd7e4c09b573`。固定 Stage 2 相似度是 L2 归一化后的 cosine，既有 B2 不需新增修复臂。版本/时间适用、真实可信凭证及 P0 下的稳健选择仍须另证。CEG-RAG 的 cross-encoder 激活信号只作安全对照文献，S1-B 无 reranker 或 verifier 模型。 [Stage 1](https://github.com/SecAI-Lab/RAGDefender/blob/ba2a17efba165d45409114df2d70b030ade1e1b8/ragdefender/grouping/clustering.py) · [Stage 2](https://github.com/SecAI-Lab/RAGDefender/blob/ba2a17efba165d45409114df2d70b030ade1e1b8/ragdefender/identification/topk.py) · [CEG-RAG](https://proceedings.mlr.press/v318/moradi26a.html)

## 2. 四臂与共同验证器

| 臂 | 拟冻结内容 |
| --- | --- |
| Rule-V1 | 原 `S1_V02_STRICT_SINGLE_SCOPE_V1`，执行源码 `68d34a5d877206f4e6d7d9e2bdda16784145a76a`。只用外层无损格式适配，原失败保留。 |
| Rule-V2 | 仅旧 73 暴露条目作开发反馈，按 query 定槽、多候选抽取、时间/版本/scope/否定与例外绑定、原 span 验证。当前无代码、调参或试次，待冻结。 |
| UIE | 唯一首选 `PaddleNLP Taskflow uie-nano`（官方 BOS `uie_nano_v1.1`），中文 schema 以公开字段名及 query 原文派生短提示，正文原样输入，使用发行版匹配的 UIE tokenizer、vocab 与配置。建议 CPU、batch 1、`max_seq_len=512`、`position_prob=0.5`，禁静态导出与量化。 |
| Qwen-local | 唯一备选/本地对照 `Qwen/Qwen2.5-1.5B-Instruct`，中文固定指令、官方 tokenizer/chat template。建议 batch 1、greedy、`do_sample=false`、不套温度采样、`max_new_tokens=256`、总序列≤2048、seed 0。仅允许候选 JSON 或 UNKNOWN，输出短原文引用和字段，无依据留空，文本内指令不执行。参数和提示字节哈希待开发许可后冻结。 [Qwen2.5 报告](https://arxiv.org/abs/2412.15115) |

所有臂见同一个 `(query, evidence UTF-8 bytes, public schema)`，UIE 的 schema 映射只能来自该输入，禁止逐题人工设答案槽、给某臂加可信来源或补文本。独立保管方在冻结前核查共同长度合同。长文需要共同的确定性窗口和原文偏移映射时，在开发期一次固定并对所有臂应用。静默截断、跨臂不同证据窗口、样本事后删除均失败关闭。

公共 schema 包含 subject、attribute、value、unit、version、effective_from/to、condition、scope、negation、exception、逐字段 span、status 与 UNKNOWN reason。共享确定性验证器核对原文 SHA、字符半开区间与 UTF-8 映射、引文唯一重定位、数值/日期/单位和时间/scope/否定限定词，同一证据区间支持同一候选，禁止拼接不同版本与实体。引文无法唯一定位、多个候选无法绑定、结构错误或未证实的适用性按冻结规则记录 UNKNOWN 或技术失败。模型置信度、生成 URL、常识和自称新版均不提升 P0 信任。原始错误及 verifier 拒识分别保留。

## 3. 资产与资源准入

**UIE 优先完成许可核验。** 官方 v2.6.1 源码映射及 HEAD 核验如下。BOS 发布标识已知，源码 commit 已固定，独立模型卡、权重不可变 revision、发布者 SHA256 和五文件明确许可 **UNKNOWN**。MD5 是旧加载器提供的身份线索，不能替代权重许可或强哈希。权重 HEAD 的 ETag 为非普通 MD5，不能当作文件校验值。候选权重不得镜像、转换、分发或加载，直到 Owner 看到与该发布绑定的条款和强身份。 [官方映射](https://github.com/PaddlePaddle/PaddleNLP/blob/fd2bed541ff929f6f8b350001694e553b29d4e9a/paddlenlp/taskflow/information_extraction.py)

| BOS 相对路径 | HEAD bytes | 官方源码 MD5 |
| --- | ---: | --- |
| uie_nano_v1.1/model_state.pdparams | 71,659,589 | `48db5206232e89ef16b66467562d90e5` |
| uie_nano/config.json | 610 | `e0e0a2c0d9651ed1a8492be5507590a9` |
| uie_base/vocab.txt | 186,807 | `1c1c1f4fd93c5bed3b4eebec4de976a8` |
| uie_base/special_tokens_map.json | 112 | `8b3fb1023167bb4ab9d70708eb05f6ec` |
| uie_base/tokenizer_config.json | 172 | `59acb0ce78e79180a2491dfd8382b28c` |

**Qwen 固定备选。** HF 官方命名空间的 revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306` 经带 blobs 的固定元数据 API 再核。该 revision 的模型 LICENSE 明示 Apache-2.0，保留许可、署名和适用 NOTICE；推理实现 Transformers 的 Apache-2.0 是另一条代码许可。3B 的 Qwen Research License 单列，未纳入。候选白名单 9 文件合计 **3,098,971,928 bytes**（2.886 GiB），排除仓库控制文件及任何替代权重。普通小文件列 Git blob SHA-1，原始文件 SHA256 尚未计算。 [固定模型树](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/tree/989aa7980e4cf806f80c7fef2b1adb7bc71aa306) · [固定 LICENSE](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/989aa7980e4cf806f80c7fef2b1adb7bc71aa306/LICENSE) · [发布者条款对照](https://qwenlm.github.io/blog/qwen2.5-llm/) · [3B LICENSE](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/main/LICENSE)

| 文件 | bytes | 官方标识 |
| --- | ---: | --- |
| model.safetensors | 3,087,467,144 | LFS SHA256 `dd924a11b4c220f385b51ffa522daea7c9f3d850e31b162bb5661df483c6d3ee` |
| LICENSE | 11,343 | `6634c8cc3133b3848ec74b9f275acaaa1ea618ab` |
| README.md | 4,917 | `b3327a17e2ffa52e0fd941a2810b18a9fd0e7d94` |
| config.json | 660 | `f81ead14ab072d65a07817f83a3ee0e5a1890d10` |
| generation_config.json | 242 | `dfc11073787daf1b0f9c0f1499487ab5f4c93738` |
| merges.txt | 1,671,839 | `20024bfe7c83998e9aeaf98a0cd6a2ce6306c2f0` |
| tokenizer.json | 7,031,645 | `443909a61d429dff23010e5bddd28ff530edda00` |
| tokenizer_config.json | 7,305 | `07bfe0640cb5a0037f9322287fbfc682806cf672` |
| vocab.json | 2,776,833 | `4783fe10ac3adce15ac8f358ef5462739852c569` |

| 资源 | 5060 只读实查 | 候选门，均为估算 |
| --- | --- | --- |
| 主机 | Windows x64；Ryzen 7 5700X 8C/16T；物理 RAM 31.92 GiB，当时可用 8.73 GiB。D/E 可用 332.88/336.63 GiB。 | D/E 预留≥20 GiB，在独立目录落实临时、缓存、env、日志与归档。启动前重测。 |
| GPU | RTX 5060，8151 MiB，首测空闲 5480 MiB，驱动 616.92，驱动报告 CUDA 13.4。所用科研环境 Torch `2.12.1+cpu`、`cuda=None`，未发现 PATH 上 nvcc，计算后端与 GPU kernel 未试。 | UIE 首轮 CPU，不申请 GPU。Qwen CPU-first 候选 12–16 GiB 额外可用 RAM，建议低于 12 GiB 不启；FP32 参数约 5.75 GiB，加 BF16 映射及运行开销。若另批 GPU，以原始 BF16/batch 1/2048 估算 4.5–6 GiB 峰值，建议空闲≥6.5 GiB，当前观测不足。不得自动 offload 或换精度。 |
| Paddle CPU 环境 | 现有 Python 3.12.14 中未装 PaddlePaddle/PaddleNLP。候选 PyPI CPU Paddle 2.6.2 cp312 win_amd64 wheel 81,105,769 B，PaddleNLP 2.6.1 wheel 2,682,308 B。其 metadata 固定 protobuf 3.20.2，另有 onnx、paddle2onnx、datasets、HF hub 依赖；既有 NumPy 2.5.0 环境不能直接认定兼容。 | 专用 CPU 环境和完整依赖哈希锁仍 UNKNOWN。UIE 五文件 71,847,290 B；按两份约 137 MiB，再计环境和 scratch，拟上限 5 GiB，RAM 预计 1–3 GiB，建议可用≥4 GiB。无 GPU 自动回退。 [Paddle wheel 元数据](https://pypi.org/pypi/paddlepaddle/2.6.2/json) · [PaddleNLP wheel 元数据](https://pypi.org/pypi/paddlenlp/2.6.1/json) |
| Qwen 环境 | 现有 Transformers 5.12.1、Tokenizers 0.22.2、Safetensors 0.8.0，Accelerate 缺失，固定模型加载与版本配对未测。 | 单设备设计，禁 `device_map=auto`、远程代码、自动装依赖。资产两份约 5.77 GiB，加 scratch 拟 10 GiB（不含新环境，后者须另核）；OOM 首次即停止，保留失败，量化或 GPU 迁移只能另批为不同配置。GPU 软件栈须确证 Windows Blackwell wheel 与 CUDA 版本。 [官方 Windows Paddle Blackwell 说明](https://www.paddleocr.ai/v3.3.0/en/version3.x/installation.html) |
| 缓存与临时目录 | 进程 `HF_HUB_CACHE/TRANSFORMERS_CACHE` 在 E 盘缓存，`TORCH_HOME` 在 E 盘，抽查目录父链无重解析链接。默认 C 盘 Hugging Face 根目录存在且非链接，`HF_HOME/PPNLP_HOME` 未设置，`TEMP/TMP/LOCALAPPDATA` 当前指向 C。抽查的 C/E 标准候选位置未发现这两个缓存；其它位置的缓存身份 UNKNOWN。 | 未来先设置并验证 HF_HOME/HF_HUB_CACHE/HF_XET_CACHE、PPNLP_HOME、PIP/Torch cache、TEMP/TMP 和转换输出都在 D/E。Paddle 的 `task_path` 必须经完整文件前检，Taskflow 自带缺件下载。Qwen 固定本地绝对路径、`local_files_only=True`、`trust_remote_code=False`、safetensors-only。两栈均用 OS 出站拒绝和 Python 网络审计验证，无服务监听。 |

PyPI 两个候选 wheel 的发布 SHA256 分别为 `f90efb319603883ded4210c72f2415ccd9d0b4290ad78d6cf0a2fc67c84661b0`、`75f5c6f805be4f7bcf9a8c58164dae278d1f2511e433d7732f4571a37178d816`。完整 wheel 依赖、实际 CPU/GPU 峰值、运行时延和电价 UNKNOWN。将来须记录单进程峰值 RSS/VRAM、GPU 秒（CPU 则 N/A）、冷/热启动、p50/p95、固定批大小、token 或字符吞吐、每案例实际费用及能源估算口径。商业 API 费用与本地计算代价分别报告。

## 4. 独立验收预注册建议

- **100 个主案例**，100 个不同语义事实或应拒识判断。建议 70 个有答案、30 个应拒识，覆盖自然多事实、单位/时间、跨机构和同名异主体、版本与条件/否定/例外、伪修订、合法正文混页面模板和无答案。**20 个追加显式模板视图**各对应一个既有主案例，组成 20 对；运行清单 120 项，主分母仍为 100，额外 20 只报配对变化。旧 73 仅暴露开发集。
- Owner 先指定独立保管人及两位与 5060 开发隔离的审核者，分歧由独立仲裁人解决。保管人审素材许可、跨 D1/D2/D3/旧 73/旧 108/S3 的不重叠凭据，并按事实与来源家族分组。只由有权侧访问这些排除清单。预先锁输入、源字节、映射、分组、标注和分歧日志哈希。开发侧只收不含 Gold 的公开 schema，固定后只在获准执行入口读角色盲样本。
- 开发冻结源提交、提示字节、revision/文件、运行环境、参数、窗口/解析规则、统一 verifier 和评分源码。独立验证获批后每臂单次，不重试、不补样。先封存全部预测、缺失与错误，再由独立 Evaluator 解锁 Gold。发生漏跑、泄漏或协议漂移时保留 100 主槽的完整账并停止，不能用已运行子集授予 PASS。
- 门槛沿用 **值命中/有答案≥90%**（有答案 UNKNOWN 算未命中）与 **wrong/decided≤2%，且 decided>0**。同时报 wrong/total、覆盖/拒识、应拒识误答、严格 scope/span 一致性、未证新版误答、自然化配对与分层。错误分母须区分无答案与技术失败。二项 Wilson 95% 作为描述；效应差用配对及按来源家族的重采样。即使 100 条均决定且零错，Wilson 上界约 3.70%。未证新版误答=0 只列**候选新 guard**，另批前不作硬门。

## 5. Owner 下一道门

`HUMAN_DECISION_REQUIRED / Auto Continue = NO` 适用于后续资产与试次。本轮前向风险审查确认硬件、依赖及外传三项有独立门。论文风险审查确认 M2 分组有前作、开发与独立结果需分开、增算力有公平性成本。以下沿用原设计的十二字段 PO-MHEP 决策记录，补齐资产核验结果。

1. **立即待决只有一项。** UIE Nano 优先，先补发布者权重和分词器条款、强身份及完整 CPU 依赖锁，再签单模型资产许可。若该链无法闭合，由 Owner 明确改选固定 Qwen 1.5B 作为首个获准资产，并先闭合 RAM/运行环境。两者分别批准。
2. **可并行指定保管人。** 先授权独立数据治理、来源与审核职责。此项不释放验证样本或模型运行。
3. **后续分别签。** 资产完成后才提交开发推理的预算和样本上限；源、模型、配置、独立 Gold 与权限全部闭合后才提交一次独立验收。额外 guard 可在该签署节点单独决定。

许可、revision/哈希、缓存落点、独立标注或运行资源任何一项未闭合即停止对应支路。S1-B 科学 Run 未创建，S2–S5 锁定。
