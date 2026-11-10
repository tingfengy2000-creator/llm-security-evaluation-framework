# 5060 Codex｜Owner23A 收敛式静态 PE/API-set/VC/第三方许可复核（ACTIVE；仅静态）

**Authority**：`W1-OD-20261110-5060-OWNER23A-SCOPED-STATIC-23A`  
**唯一生效授权全文**：`docs/paper1/dual_machine/owner_approvals/W1_5060_OWNER23A_SCOPED_PE_APISET_LICENSE_STATIC_AUTH_20261110.md`。
**工作范围**：已获Qwen Q4_K_M + llama.cpp b12242本机D盘两项资产的**静态审计**、新静态审核脚本和普通QA工程修复。Owner直接批准Owner23A，并授权在这个已确定边界内自修工程问题、重复普通单测与静态分析，不必每一步申请审批；不得扩大为模型执行、运行时smoke、推理、新样本评价或新的权限。

## 0. Context recovery & preflight

在唯一分支 `research/paper1-chinese-defense-5060` 的独立worktree，按`AGENTS.md`→context authority→PO-MHEP→Current Work State→Owner Decision Register→Experiment Master→Owner22实测报告→Owner22静态审查源码与Owner22Supervisor评审→Owner23A授权依次恢复。先核工作树、upstream、remote HEAD、最近15提交和文件/角色隔离；不能reset、stash、force-push未知内容；与新授权冲突时按更窄范围并STOP。

关键入口：
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER22_QWEN_GGUF_ASSET_STATIC_INSPECTION_RESULT.md`
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER22_QWEN_GGUF_ASSET_STATIC_RUN_MANIFEST.json`
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER22_ASSET_STATIC_BLOCKED_SUPERVISOR_REVIEW_20261110.md`
- `src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner22_static_inspection.py`

Owner22旧静态失败和输出不可改。`512`是原脚本预算，`29`是未走完的名称前沿，`387`为API-set未映射项，并非已确认缺失DLL。审计的是`llama-cli.exe`计划启动所需静态路径，需同时披露动态后端选择风险。

## 1. 数据与资产不变性

根目录（实际校验符号链接、ACL、D盘空闲、重解析点）：
`D:\experiments\paper1_chinese5060\owner22-assets\`。

冻结两个原资产内容：
- `qwen2.5-1.5b-instruct-q4_k_m.gguf` — 1,117,320,736 bytes，sha256`6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`；
- `llama-b12242-bin-win-cpu-x64.zip` — 24,931,401 bytes，sha256`4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0`，zip内52件哈希与Owner22 Manifest对齐。
本轮只读取已有副本与既有System32所需文件，不再下载任何大/小资产、权重、Tokenizer、运行库、安装程序或PE解析工具；不能安装或改变C盘可控资产。因旧归档已封存，创建独立`owner23a-* `日志/结果目录及Run ID，不覆盖旧sealed ZIP/GGUF或原失败。

## 2. 静态PE闭包方法改进（无需执行 EXE/DLL）

**目标根**：`llama-cli.exe`，在已有Owner22包内PE索引基础上仅遍历其直接、延迟导入的必需包内/系统实体DLL；通过源码和静态证据单列可能在模型加载时由GGML动态选择的CPU后端（Ryzen 5700X AVX2且无AVX512，候选Haswell/AVX2优先但不能凭猜测选定精确路径）。对于必要的`llama-server-impl.dll`等动态导入，以静态调用线索+未知标记记入候选集合。其他server/RPC/连接工具本次不需要证明能运行；保留原Owner22全包51个PE静态库存，不删除不掩盖。

**API-set与KnownDLL**：与普通DLL分开处理`api-ms-win-*`、`ext-ms-win-*`。可通过Windows既有API-set schema**静态读取**（如可审计的`apisetschema.dll`只读资源或官方文档映射）以及只读注册表/OS版本证据进行映射；不下载/安装解析器，不调用`LoadLibrary`，不执行模型发行EXE/DLL。输出`MAPPED_HOST / CONTRACT_PRESENT_UNMAPPED / HOST_NOT_PRESENT / NOT_APPLICABLE / UNKNOWN`，不要因没有同名实体DLL就判缺失，也不要把逻辑契约自动判PASS。考虑重定向、转发导出和循环依赖；无法静态确认则UNKNOWN并说明需要未来受控smoke验证。

**迭代边界**：最初仅针对根CLI、相关包内依赖和必要OS实体进行有界BFS/DFS，显式visited/set去重、canonical path和跨Dll同名冲突处理。最多2048个有关联的**非API-set实体**、明确最多20层递归、合理单文件体积与墙钟上限（建议本机静态任务总≤120s；如果正常环境不满足则直接STOP记录）。不通过简单将原512改成4096/8192遍历整个System32来假装解决问题。任何超限均明确`ANALYSIS_BUDGET_EXHAUSTED`和剩余前沿，不是`MISSING_DEPENDENCY`。

**依赖检查**：区分`DIRECT_STATIC`、`DELAY_IMPORT`、`POSSIBLE_DYNAMIC_BACKEND`、`SYSTEM_API_SET`、`KNOWN_DLL`与`NOT_OBSERVED`；对确切的DLL版本和CPU位数、现有可见VC runtime文件记录静态证据。最低VC版本和导入符号兼容无法静态证实则`UNKNOWN`，不能“已存在vcruntime140.dll”推定运行PASS。禁止执行`llama-cli.exe --version`或任何`llama-cli.exe`启动和任何新DLL加载。

## 3. 许可证与历史工程路径

根据官方固定源码和本地ZIP的实体清单进行`component -> origin -> bundled/dynamically linked -> license -> required attribution/NOTICE -> evidence`矩阵，至少 llama.cpp MIT、LLVM OpenMP Apache-2.0 with LLVM exceptions、BoringSSL、关联 GGML 组件；无证据标UNKNOWN而不推测全部PASS。可读官方纯文本许可/文档公开元数据，但**不得下载任何新构建资产、包或原始版权数据全集**。

核对Owner22首次QA D盘仓库ignore临时区已迁移/清理（只读列单、sha和ACL），其余Owner22资产根无残留半成品。即使发现残留，先输出风险与建议；只有自己Owner23A新产生的受控临时文件可清理，不触此前证据或他人文件。将C盘的TEMP、缓存等变量对本次工作子进程安全重定向D盘已有授权路径，禁止修改系统持久环境。

## 4. 运行执行治理与自动工程修复

**这是静态QA，不是科学实验。** 允许在当前任务中自主迭代**新Owner23A脚本**、普通单测、类型和风格工具，直至收敛或明确工程阻断；每次开发迭代保留变更记录、QA结论和相关负结果。允许重新读取同一已经落地的合法资产做**非执行性静态分析**，不算第二次科学试次。不得改Owner22脚本与冻结报告/Manifest，更不得在已揭盲旧100上启动任何模型预测。

若需要新PE库、管理员提权、读取未经许可私有磁盘/远程数据、新二进制、实际系统DLL加载或执行，立即`HUMAN_DECISION_REQUIRED`，不要自行安装。所有网络与模型、商业API使用0；Git正常提交推送除外。

## 5. 交付、判定和STOP

Run ID建议`W1-5060-OWNER23A-SCOPED-STATIC-20261110-01`。提交：
- `CLI_MINIMAL_STATIC_DEPENDENCY`矩阵、API-set映射与系统根证据、包内CPU后端候选及动态风险、VC最小版本/导入符号compat的不确定性；
- 许可覆盖矩阵及缺失component/notice的最小可操作清单；原Owner22 512节点与剩余29前沿的原因差异及修复证据；
- D盘独立新QA路径、无外侧临时残留结果、静态工具限制清单、未授权操作零计数；
- `STATIC_CLI_DEPENDENCIES=PASS/UNKNOWN/BLOCKED`、`API_SET=PASS/UNKNOWN/BLOCKED`、`PACKAGE_LICENSE=PASS/UNKNOWN/BLOCKED`、`VC_COMPAT=PASS/UNKNOWN/BLOCKED`、`DYNAMIC_CPU_BACKEND=PASS/UNKNOWN/BLOCKED`和`ACTUAL_RUNTIME_MEMORY=NOT_MEASURED`。对不可静态完成的能力设置`SMOKE_REQUIRED`，不要无期限追加无关递归；
- 新的独立脱敏报告/Manifest、私有ZIP哈希索引、测试+ruff+mypy+secret scan、逐轮工程修复、Git commit+push/远端SHA；给Owner一个**只待批准**的受控加载smoke方案，不进行启动。

成功结束仍是`OWNER23A_STATIC_COMPLETE / OWNER23B_SMOKE_PENDING_OWNER / MODEL_LOAD_INFERENCE_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO`。无论PASS/UNKNOWN/BLOCKED都STOP。绝不自动运行模型、调用API、下载软件或消耗任何新数据。
