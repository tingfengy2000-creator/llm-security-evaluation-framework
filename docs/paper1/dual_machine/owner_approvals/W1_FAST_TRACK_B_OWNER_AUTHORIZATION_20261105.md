# Paper 1 · Week 1 Fast-Track B — Owner 受限执行授权

- **Owner授权身份（跨分支唯一）**：`W1-OD-20261105-FAST-B-04`
- **日期**：2026-11-05 JST
- **状态**：`OWNER_EXPLICITLY_APPROVED / CONDITIONAL_ASSET_DOWNLOAD_AND_D1_DEV_OFFLINE_BASELINES`
- **授权原始来源**：Owner 在本项目 ChatGPT 监督会话中明确同意 Fast-Track B；本文为脱敏、可追溯的授权转录，不冒充原始聊天字节或科研结果。
- **执行分支**：`research/paper1-chinese-defense-5060`
- **授权前可核远程 HEAD**：`3ca27c9416ea630e7f82c5b98ceed93099bd57ac`
- **既有 P2 执行源码 SHA**：`9aa21be13ae206dbbadb03b99528e362eba29378`
- **P2 检索输出封存 SHA-256**：`4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`
- **原 Pilot12 选择哈希**：`2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`
- **模型资产唯一批准来源**：`sentence-transformers/all-MiniLM-L6-v2`，`revision=1110a243fdf4706b3f48f1d95db1a4f5529b4d41`，官方 `https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41`。
- **先行治理**：按 AGENTS.md、Context Authority Map、PO-MHEP 和既有不可变实验约束执行；本文件为最新明确 Owner 决定但不得覆盖更高层法律、安全、证据与隔离规则。双方分支保持独立；`PODR-154` 历史编号有冲突，跨机关联一律使用本 W1-OD ID 加分支及 SHA。

## PO-MHEP 决策就绪记录（十二字段）

### 1. Issue ID
`W1-OD-20261105-FAST-B-04`。

### 2. Issue name
5060：有界官方模型资产下载与已封存 T0 TopK 上的 RAGDefender v0.2 公开库 B1/B2 零付费离线开发对照；并行准备十二题独立、盲于检索结果的事实/target/C3 裁决资料。

### 3. Discovery stage/task
Paper 1 Week 1 / 5060 P2 真实 T0 检索收口后；P2 状态 `T0_B0_DIAGNOSTIC_COMPLETE / B1_B2_BLOCKED`；本决定不授权 5090 新任务。

### 4. Evidence with confidence
- `OBSERVED_FACT (GIT)`：P2 源码提交、输出 seal、远程报告和测试记录有固定身份；36/36 世界成功生成 TopK5，Candidate Hit@5 29/36（Poison 10/12，Clean 10/12，HN 9/12）；B0 删除0；B1/B2 从未运行。
- `SOURCE_DERIVED_FACT`：官方 Hugging Face 固定 revision 提供该模型资源页面，模型卡标注 Apache-2.0；整仓包含多种权重与导出格式，**不能下载整个仓库**。下载前由执行端对批准 revision 的必要白名单逐文件再核来源、大小和许可证。
- `OWNER_CONFIRMED`：本轮文字明确批准本文的条件式下载、B1/B2 离线比较和独立裁决准备。
- `INFERENCE`：先闭合 B1 资产再进行配对离线过滤，可比提前付费生成更快识别中文迁移风险；但不证明算法优势。
- `UNKNOWN`：尚未有 B1/B2 运行效果、独立人工 Gold、攻击目标接受、完整官方作者环境数值；P2 的7个漏召回语义原因未解决，不可按实验结果改变 TopK。

### 5. Affected rules
AGENTS.md、PO-MHEP、已冻结双机合同、D1开发集隔离、独立 Evaluator/GT Vault、原始证据不可变、无擅自科学语义变化、独立分支 Git、付费限额与审计日志规则。

### 6. Why now
P2 真实检索已完成而 B1/B2 因原版默认模型缓存身份缺失无法测量；限量获取确切公开资产是当前最小化科学阻断的可审计步骤。十二题答案/target/C3 仍需独立裁决，不宜与资产核验串行等待。

### 7. Downstream risks
不当下载（整仓约远超250MiB、重复双权重、ONNX/TF/OpenVINO或pickle）；镜像或 revision 漂移；权重/配置损坏；B1原样语义被补丁破坏；B2多个变量同时变化；P2检索重建造成选择偏差；Retriever读取标签；条件分母与完整分母混淆；AI开发草案被当作 Human Gold；未经批准的付费或商业 API。发生任何身份、许可、资源、证据、隔离或实验语义异常，立即 STOP 受影响支路并给十二字段升级材料。

### 8. Options and tradeoffs
- A **OWNER ACCEPTED**：严格固定 HF 模型 revision，仅下载必需白名单文件，限额内完成身份冻结，复用已封存 P2 TopK 做 B1/B2 非付费对照，另行准备盲裁决卡。优势：最快补上公平基线；劣势：仍缺人工 Gold 和生成级结果；新增授权网络流量 <250MiB、磁盘 <1GiB、商业 API 费用0；可逆且不得改原证据。
- B **NOT CHOSEN**：B1/B2继续 BLOCKED 直到其他外部任务完成。资源零，但延长方法判定时间；可逆。
- C **PROHIBITED**：使用任意现有替代模型、下载整仓、改原 TopK 或先付费取结果。快但不可比、违反授权与复现原则。

### 9. Recommendation
执行 A；下载与模型冻结门未过，B1/B2 不开始；人工裁决准备可与资产核验并行开展；每条工作线独立审计。

### 10. Rationale/confidence
Owner授权事实明确；P2 检索封存的公开聚合已核；HF 仓库身份可由官方网页和执行端再次验证；模型下载与 B1/B2 科研数值尚未实测。禁止把本授权登记本身当作正式实验接受。

### 11. Explicit Owner decisions and remaining gates
**已批准：**
1. 仅在5060原分支，用既有12题 Pilot12 与已经封存的36个 T0 TopK5 **原始字节**；禁止重新建库、补召回、重排、换query、换chunk、改阈值或为结果调参。
2. 仅允许从 **Hugging Face 官方来源**读取/下载 `sentence-transformers/all-MiniLM-L6-v2` 的固定 `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`，以满足原版 v0.2库`minilm-all`默认嵌入资产。执行前先独立核验模型卡/许可、文件清单及逐文件大小、预计总下载、目标磁盘余量。仅下载最小必要白名单（优先`model.safetensors`和必要的 tokenizer/config/Pooling 文件；具体白名单须由执行端静态导入链和 model repository tree 核准）。严禁自动 whole-repo snapshot、`main`漂移、重复`pytorch_model.bin`、`rust_model.ot`、TF/ONNX/OpenVINO/training 文件、额外依赖或镜像/代理/fallback。下载**所有请求响应累计传输量**不超过 250MiB（262144000 字节），**实际新增本地磁盘**不超过1GiB（1073741824字节）；硬门以实际总量（含临时文件和复制）计，不是按单文件单请求重置。任何未知大小/动态扩容/需要其他来源/失败重试超预算即STOP。
3. 资产落在本机受控 Git 外隔离缓存，固定 revision、逐文件 SHA-256、tokenizer、pooling、模型 load kwargs、依赖和许可证身份；网络下载结束后 B1/B2 运行强制离线、禁Hub自动获取、禁外部API。
4. **有条件执行 B1**：未修改 RAGDefender v0.2 公共库的固定源码路径（已知上游 `ba2a17efba165d45409114df2d70b030ade1e1b8`），搭配显式批准的固定原默认模型身份。在最终报告显式声明这是 `B1_PUBLIC_V0_2_PINNED_MODEL`，不是 ACSAC 论文 artifacts/严格数值复现；若公开库仍试图访问 floating main 或与已批固定模型不等价、需要语义代码patch，则 STOP。
5. **有条件执行 B2**：在与 B1 相同的 TopK、库语义、方法参数、预算和输入顺序下，仅将 embedding 改成已冻结、已存在于本机的 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2@16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1`；不能额外改变 TF-IDF、阈值、分组/选择规则、过滤/解析策略或异常路径。
6. 按 **36完整世界** 与 **29个Candidate确实进入TopK的条件性世界**分别报告 chunk 删除和candidate级flag、Poison Recall、Clean/HN误删、未召回 2/2/3、异常、空上下文、延迟。明确各角色12/12/12及命中Poison10/Clean10/HN9的真实分母，不把漏召回记成检测成功；不得在无独立背景GT时给背景强行贴负类标签。
7. 独立材料支路可准备12题事实/有效时间/条件/答案等价类/target/C3边界的**待人工裁决卡**，审阅者需盲于检索结果、候选角色、旧预测、两机结论；AI不能签署 Human Gold/正式答案或根据检索表现更改题目、目标。
8. 成功与阻断、失败尝试均保存命令/exit/stdout/stderr、run manifest、seed、input/topK/source/config、模型hash、私有原始结果与归档hash/index；对外Git只脱敏聚合与hash，自分支规范提交推送、完成 closeout 后 STOP。

**仍禁止／须另批：** 所有付费 API/探测、B3/B4生成或评判、B5/B6新机制、D1-40、D2/D3/Reviewer/未授权GT、T1官方证据信任授予、T2、正式 Ground Truth/正式ASR/Answer Accuracy、5090下载/Claim1–3、任何跨机或主线merge/rebase/cherry-pick、任何超出白名单的新模型/镜像/依赖/数据下载或实验语义变更。

### 12. Allowed/prohibited until next gate
允许本授权所述的短期有界官方资产下载、离线 B1/B2 对照、盲于检索结果的裁决准备，以及脱敏证据治理和本分支Git；若某子任务 fail closed，允许另一独立、合规子任务继续。禁止未批成本、历史改写、静默换模型/改索引、错误指标宣称。
下一门：汇报B1/B2有效诊断及仍有争议的12题裁决卡，Owner/独立审阅再定评价边界；本次**不批准**真实Qwen Pilot 或 D1-40。

## Completion
5060 交付 `W1_5060_FAST_B_B1_B2_OFFLINE_RESULT.md`、模型资产白名单与哈希、完整分母/条件分母、离线日志/hash与私有归档、12题独立待审裁决包、费用零确认、Git HEAD/upstream/clean，完成后 STOP。历史 P2 / B1/B2 BLOCKED 事实作为以前时点快照保留，不因新准入批准而追溯改写。
