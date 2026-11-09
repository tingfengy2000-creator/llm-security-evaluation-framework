# W1-OD-20261109-5060-S1B-FEAS-DATA-19｜Owner 路线 A：可行性数据准备与严格分离（非一次性测试许可）

**日期**：2026-11-09 JST  
**状态**：`OWNER_EXPLICITLY_APPROVED / S1B_FEASIBILITY_DATA_PREPARATION_ONLY / EVALUATION_NOT_AUTHORIZED`  
**唯一研究分支**：`research/paper1-chinese-defense-5060`  
**执行前核验 HEAD**：`632e59e0685abfae70296511b56da38cc390bccd`。  
**Owner原话**：“批准，验证阶段我希望数据集用D1或者用公开数据集或者llm生成的符合要求的，等到可行性分析过了正式阶段在人工标注。”其“批准”指前一监督决定中路线A先行准备新语义案例，**并在另批审批后实施一次规则盲评**。本授权仅放行数据准备、预注册和封存，不自动越过先前已冻结的一次性验证审批门。

## PO-MHEP 十二字段

1. **Issue ID**：`W1-OD-20261109-5060-S1B-FEAS-DATA-19`。
2. **Issue**：在不消耗正式Human Gold与S3留出的条件下，准备Rule-V1/Rule-V2的低成本、可复核中文事实抽取可行性验证数据与协议。
3. **Discovery/task**：Owner18 Rule-V2开发在旧73暴露例上完成（值59/61、决定后错抽1/59；不算独立），固定实现commit `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`；UIE权重许可未闭合，Qwen资产未批；路线A此前被建议为先行验证选项。
4. **事实/推断/未知**：`OBSERVED` 旧73与D1均已暴露，旧S1 FAIL、R2 K1-C、Human Gold0、S2–S5无许可；`SOURCE_DERIVED` CMRC2018官方公开问答/原文answer_start，发布许可CC BY-SA4.0，但未提供VESA需要的生效时间、版本/可信来源统一Gold；`INFERENCE` 新生成的范围/版本场景可快速测使能能力，但会受生成模板偏差和标注自证影响；`UNKNOWN` 新样本难度与覆盖、Rule-V2未见性能及任何真实RAG防御收益。
5. **冻结合同边界**：D1_DEV_EXPOSED、独立D2/D3永不访问、旧108/B2/R2/S1/RULE-V2迭代不可改写、P0不升权、主研究分支不得合并、5090独立线、S2–S5不得自动启用、HumanGold0。
6. **紧迫性**：不再等待UIE/Qwen许可证，先用现有规则版低成本检验是否在未见中文版本/scope场景中存在可转化能力；明确先可行性后人工审核，避免过早消耗人审资源。
7. **前瞻风险**：Codex同一Agent造题和写算法不构成人类独立盲审；训练/测试泄漏、模板化样本、LLM幻觉式Gold、问法与旧73近重复、同义改写虚增独立分母、公开集缺version scope、网络/许可或数据隐私、先见结果再调整Gold/评分都将误导。
8. **Option**：Owner选`PATH_A_FAST_FEASIBILITY`。允许以(a)新AI/Agent生成的合成案例为主、(b)权利明确的公开数据集作额外压力测试、(c)D1作开发回归，准备材料；正式独立人审留待可行性成功后。优点：少费用快；缺点：不代表真实世界外推和独立人工真实性；可逆，不触任何冻结科学测试。
9. **LOCAL建议**：创建≥100个**不同语义事实或应拒识决策**，建议70可回答/30应拒识，另20个从属自然化/显式配对视图（总执行位120、主分母100）；独立source family/domain，特别包含版本冲突、生效期、条件/例外、跨scope、伪修订、合法重复值、原文span歧义、多事实与网页模板。由`source-truth ledger -> evidence text -> query -> oracle expected slots/span`产生受控合成样本，全部自动校验span与版本适用；AI暂定Gold必须显示`AGENT_GENERATED_PROVISIONAL / NOT_HUMAN_GOLD`。禁止把同义改写计入100。
10. **权衡/信心**：Owner路线A及“暂不人工标注”意图明确；数据准备授权高可信；合成Golden答案和Rule-V2外推可信度有限，必须明确最小证明等级。
11. **Owner已决/待决**：`DATA_PREPARATION=APPROVED`；`AGENT_SYNTHETIC_GENERATION_IN_EXISTING_CODEX_SESSION=APPROVED`，不等于许可通过API调用其他模型；`D1_READONLY_REGRESSION=APPROVED_WITH_EXPOSED_DEV_LABEL`（仅可设计/执行旧集回归，禁止修改原实验）；`CMRC2018_BOUNDED_PUBLIC_DATA_ACQUISITION=CONDITIONALLY_APPROVED` 仅在源/版本/许可/大小/下载哈希封存且D/E盘可控时允许，且仅辅助未见/领域外压力测试，不能伪造时态/scope标签；`RULE_V1_V2_NEW_DATA_ONE_SHOT_EVALUATION=NOT_APPROVED`，待另行Owner核准封存清单；`MODEL_DOWNLOAD/LOAD/INFERENCE=NOT_APPROVED`；`NEW_EXTERNAL_LLM_API=NOT_APPROVED`；S2–S5与5090 Claim未批准。未来正式人工标注的具体范围仍由Owner后续决定。
12. **允许/禁止**：
   - **允许**：在5060专用D/E受控目录以现有Codex会话**文本生成**全新合成事实及自然化证据（这不是授权另起API或模型）；构造严格分离的输入、暂定标签、私有source-truth与可容许证据span清单，哈希封存；查阅公有许可证与元数据，若确需CMRC2018公开子集，只限已核官方或官方HFL镜像的固定版、下载白名单及总量（压缩≤50MiB、解压≤200MiB）、来源许可和hash预先记录，不能安装依赖、转取其他链接或抓取整站；D1/旧73仅只读开发回归，数据来源分层记；提前写完对等span判分和错误种类、Coverage/UNKNOWN/wrong/decided等score规则；测试数据格式与不含Gold的接口unit tests；私有封存与脱敏Git索引。
   - **禁止**：用Rule-V2预测挑改测试集、查看新测试预测后再次选择数据、在新100主样本上运行Rule-V1/Rule-V2或其他抽取器、实际评分/揭盲/调阈值，直到另批One-shot批准；不能将D1或旧73算作100新语义/独立测试；不下载/安装/加载/调用任何新模型及额外LLM API、不改变固定Rule-V1/Rule-V2、防御过滤、生成或检索，不触D2/D3/未来S3留出/5090、S2–S5、旧108、主分支合并、Human Gold伪造。

## 数据级别与标签用词

- `D1_DEV_EXPOSED`：既有可重复开发/回归证据，不能作为未见独立验收。
- `PUBLIC_DATASET_PROXY`：公开已有来源答案/span可作为公开任务指标；scope/version、真实性/授权不可自动补标。
- `AGENT_GENERATED_PROVISIONAL_FEASIBILITY`：新合成输入与oracle，弱独立性；如果算法开发者与数据作者同一个Agent，诚实标`NOT_INDEPENDENT_AUTHOR`，即使预测进程封存也不是外部盲审；可以称`ROLE_SEPARATED_SEALED`，不能称`INDEPENDENT_HUMAN_VALIDATION`。
- `HUMAN_GOLD=0`，`FORMAL_ASR/ANSWER_ACCURACY=NOT_MEASURED`，与真实可信source receipt无关；模拟来源只能称`SYNTHETIC_SOURCE`，不可冒充真正官方可信源。

## 生成与评估的两道硬门

### Data-prep gate（本次许可）
- 提交数据来源与许可登记、语义簇去重（old73、D1、旧108仅在合规隔离界限内交叉检查，禁止越权读D2/D3）、70/30数量、至少4个主题领域/10个不同source families、100主语义+20从属视图、固定原文与可接受span判分约定、真值与输入单独seal，hash与不可变提交、运行清单及输入/GOLD隔离验证；
- S1-B GATE 3 的实际单次推理评价与模型公平四臂尚未放行；Rule-V2锁定`da3cbd9f...`，原V1 SHA严格冻结；
- 任何未证新版/跨scope误答=0仍是建议安全指标、尚不是新的Owner正式验收门。原开发门准确率≥90%、wrong/decided≤2%、不可all-UNKNOWN必须保留为未来单次验证的参考门，不得把AI Gold高分冒称正式论文达标。

### One-shot gate（未来单独审批）
- Owner看过数据manifest（不含Gold或私有原文）、许可/来源类别、Git SHA、100个语义slot、20从属视图、评分口径、程序可重复性与独立性等级后决定是否批准一次运行；先全量预测不可变封存，再Evaluator开标，必须报告每个来源层而非混在一起；
- 如评估后任何样本/规则被改，该数据集转为开发集，不能再次代表未见测试。
- 无论单次可行性`FEASIBILITY_GO`还是`NO_GO`，都只引导申请下一阶段，不自动开放S2–S5和正式人工审稿/标注门。

## STOP与收口

若需要新权重/API/新依赖/不明许可、不安全数据访问、无法封存非重复Gold/span、dataset有明显来自旧73内容改写、发生标签泄露、索引覆盖历史Run等，立即`HUMAN_DECISION_REQUIRED / Auto Continue=NO`。本批结束只交付数据包及哈希、预注册评分脚本/验证器测试、协议、错误/失败、Git push和下轮Owner审批卡。不得输出新验证性能数字。
