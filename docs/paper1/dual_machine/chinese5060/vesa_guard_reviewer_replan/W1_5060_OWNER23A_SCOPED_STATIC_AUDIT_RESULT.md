
# 5060 Owner23A 收敛式静态审计结果

2026-11-10 JST · `W1-5060-OWNER23A-SCOPED-STATIC-20261110-01` · `W1-OD-20261110-5060-OWNER23A-SCOPED-STATIC-23A`

`OWNER23A_STATIC_COMPLETE / OWNER23B_SMOKE_PENDING_OWNER / MODEL_LOAD_INFERENCE_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO`。

| 准入项 | 状态 | 证据边界 |
| --- | --- | --- |
| `STATIC_CLI_DEPENDENCIES` | **PASS** | 以 `llama-cli.exe` 为根，9 个包内实体的 122 条直接导入、0 条延迟导入，2,911/2,911 个声明符号静态解析成功，78 个符号经过转发。未决前沿 0。 |
| `API_SET` | **PASS** | 本机 v6 schema 有 985 个条目。CLI 路径 15 种合约、73 个「调用方 × 合约」配对均映射到本机实体。 |
| `VC_COMPAT` | **UNKNOWN / SMOKE_REQUIRED** | 当前 VC/UCRT 目标的 1,152 个声明符号都能定位。最低 VC 版本与真实加载兼容仍待核验。 |
| `DYNAMIC_CPU_BACKEND` | **UNKNOWN / SMOKE_REQUIRED** | Haswell 356/356、x64 358/358 个符号静态解析成功。实际 GGML 后端选择和初始化未观测。 |
| `PACKAGE_LICENSE` | **UNKNOWN** | 固定主项目、LLVM OpenMP、BoringSSL 的文本证据已核。完整组件清单及第三方 notice 的分发覆盖未闭合。 |
| `ACTUAL_RUNTIME_MEMORY` | **NOT_MEASURED / SMOKE_REQUIRED** | 本轮只做文件字节和注册表读取。 |

## 静态依赖与 API-set

从 AMD64 PE32+ 的普通和延迟导入描述符提取名称与 ordinal，解析目标导出并有界跟随转发。先遍历 CLI 引用的包内 DLL，对 System32 只查询实际所需导出与其转发目标。KnownDLL 来自 64 位只读注册表。发现同名冲突时保留未决状态。API-set 读取 `apisetschema.dll` 的 `.apiset` 节，按 importer 别名或默认宿主解析。修订号查找采用 schema 记录的 `HashedLength`，仅对唯一可匹配的合约前缀生效。工具保留 `MAPPED_HOST`、`CONTRACT_PRESENT_UNMAPPED`、`HOST_NOT_PRESENT`、`NOT_APPLICABLE`、`UNKNOWN` 等状态。

本机 Windows 11 25H2，构建 `26200.9711`。schema SHA256 `568c72f6216d83a716d6fa9bec59ae8d93e6728062d969ac362013f3910c0007`。69 条直接描述符经 API-set 定位，另外 4 个配对来自转发。CRT 合约映射到 `ucrtbase.dll`，4 个转发使用的 Core 合约映射到 `kernelbase.dll`。Manifest 含合约、实际 schema 条目、宿主和涉及调用方数。 [Windows API sets](https://learn.microsoft.com/windows/win32/apiindex/windows-apisets) · [PE 格式](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format)

| CLI 最小静态依赖 | 类型 | 实际证据 |
| --- | --- | --- |
| `llama-cli.exe → llama-cli-impl.dll` | `DIRECT_STATIC / PACKAGE` | 根有 8 条直接描述符，其中 1 条包内、1 条 KnownDLL、1 条 VC、5 条 CRT API-set。 |
| `llama-cli-impl.dll → llama-server-impl.dll, llama-common.dll, llama.dll` | `DIRECT_STATIC / PACKAGE` | `llama-server-impl.dll` 有 2 个直接导入符号。是否运行任何服务逻辑仍未观测。 |
| `llama-server-impl.dll → llama-common.dll, mtmd.dll, llama.dll, ggml-base.dll, ggml.dll` | `DIRECT_STATIC / PACKAGE` | 继续验证 `mtmd.dll`、`llama.dll` 和 GGML 依赖。 |
| `ggml-base.dll → libomp.dll` | `DIRECT_STATIC / PACKAGE` | 7 个直接导入符号均解析。其余包内边见 Manifest。 |
| 实体系统 DLL、KnownDLL 与合约宿主 | `DIRECT_STATIC / SYSTEM32 / KNOWN_DLL / SYSTEM_API_SET` | 122 条描述符拆分为包内 19、KnownDLL 13、System32 21、API-set 69。 |
| Haswell 和 x64 | `POSSIBLE_DYNAMIC_BACKEND` | 包内共 14 个 CPU 后端。两候选分别检查，每条路径均有 28 条直接导入描述符。Ryzen 7 5700X 有 AVX2/FMA/BMI2/F16C，AVX512F 和 AVX-VNNI 未检出。 |
| 独立 server EXE、RPC/连接工具、运行时其他动态调用及系统 DLL 的初始化路径 | `NOT_OBSERVED` | 保留 Owner22 全部 51 个 PE 的原库存。静态结果不覆盖 OS loader 搜索重定向、延迟运行路径及运行时动态插件选择。 |

实体上限 2,048，深度 20，单 PE 128 MiB，墙钟 120 秒。最后一轮 1.266 秒，共读到 23 个命名实体，含两个后端和 VC 库库存。越限会记录 `ANALYSIS_BUDGET_EXHAUSTED` 与未解析前沿。Owner22 从整包导入递归扩展至 512 项，387 项为未映射 API-set，29 项是尚未走访的前沿。Owner23A 改用 CLI 限定根、导入符号与本机 schema，保留原结果。首次 Owner23A 仍有 58 个 `PE_PARSE_UNKNOWN`、12 个合约未解析符号。实际最长 C++ 导出名为 3,865 字节，原解析上限为 1,024。将有界上限设为 8,192，并依据 schema 修正修订号查找后，最终未解析符号为 0。

本机 `msvcp140.dll`、`vcruntime140.dll`、`vcruntime140_1.dll` 的文件版本均为 `14.50.35719.0`，对应 CLI 488、111、3 个声明绑定。UCRT 文件版本 `10.0.26100.9711`，550 个绑定均解析。`msvcrt.dll` 留存版本与哈希库存。最低可用 VC 版本和当前 Windows loader 实际行为仍未知。

## 许可证证据

| 组件 | 固定来源及分发方式 | 义务和已验范围 |
| --- | --- | --- |
| llama.cpp | b12242 对应源码 `3b4d6ab3f79651935fba1dd93732f29022a7f5f5`，EXE 与共享 DLL | MIT 需随分发保留版权和许可文本。封存的官方文本和 `llama.exe`、`llama-connect.exe` 中的完整文本匹配。 [固定 LICENSE](https://raw.githubusercontent.com/ggml-org/llama.cpp/3b4d6ab3f79651935fba1dd93732f29022a7f5f5/LICENSE) |
| GGML | 同一固定源码树 `ggml/`，包内 GGML 共享 DLL 与动态 CPU 后端 | 主项目 MIT 文本已匹配。仍需将 GGML 子树的版权、供应商组件和适用 notices 按实际构建产物关联。 |
| LLVM OpenMP | LLVM 20.1.8，`libomp.dll` 由 `ggml-base.dll` 引用 | Apache-2.0 with LLVM Exceptions 及附带第三方声明。随包 `LICENSE-LLVM-OpenMP` 与固定官方文本字节一致。 [OpenMP 固定文本](https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-20.1.8/openmp/LICENSE.TXT) |
| BoringSSL | 源码构建规则固定 `0.20261105.0`，包中无独立 BoringSSL DLL | 按该版本组合许可逐项保留其版权与通知。 `llama.exe`、`llama-connect.exe` 的完整文本与固定官方文本匹配。CLI 路径的具体静态链接归属仍待产物级证据。 [BoringSSL 固定文本](https://boringssl.googlesource.com/boringssl/+/refs/tags/0.20261105.0/LICENSE?format=TEXT) |
| cpp-httplib、nlohmann、sheredom 及其余嵌入组件 | Owner21 封存的固定 CMake 记录中有链接或许可登记线索 | 需固定组件清单、各实际许可/NOTICE 以及产物级链接或包内分发对应证据。整包覆盖判 `UNKNOWN`。 |
| Microsoft VC/UCRT | 只从本机 System32 定位 | 已核本机文件与绑定。Owner22 ZIP 未包含这些 Microsoft DLL。未对重新分发授权做结论。 |

最小未结项是固定构建产物的组件对照清单，以及 CLI 相关 DLL 对 BoringSSL 和 vendored 依赖的链接与 notice 覆盖。许可证不确定性须由后续 Owner 决策明确处理，静态 PASS 不提供整包分发放行。

## 证据、QA 与治理

- Owner22 的 GGUF、ZIP、52 个解包成员和历史私有 ZIP 均重核 SHA256。旧 51 项 PE 库存、第一次验包退出 1 及其补充日志保留。Owner23A 最终静态命令、输入 SHA、代码 SHA、stderr/stdout、历轮结果及单测日志均有逐件索引。
- D 盘新增独立私有证据目录。盘符路径与资产根、新输出根 ACL 检查通过，余量超过 10 GiB。旧仓库外侧 QA 原路径已消失，Owner22 staging 为 0。迁入目录存在更宽的历史 ACL，原样保留，需由有权限的保管人决定是否收紧。该目录未作新证据存放点。
- 最终 pytest 5/5，Ruff 通过，MyPy 通过，分析器在 `python -I -S -B` 下运行。QA 迭代保留了稀疏检出找不到历史测试、Mypy 类型错误和打包清单预检的初次失败。没有更改 Owner22 源码、清单或结果。
- 私有 `OWNER23A_PRIVATE_AUDIT.zip` 含 73 件，322,419 字节，SHA256 `fcde11120eecca20a1ea8398f22db35175853b4a5c9f200314cb46befa0bc589`。封存后逐成员重读校验。 [脱敏 Run Manifest](W1_5060_OWNER23A_SCOPED_STATIC_RUN_MANIFEST.json)
- 下载、安装、运行发行版 EXE/DLL、模型加载、推理、API、新科学试次均为 0。旧 Owner20 `FEASIBILITY_NO_GO`、旧 S1 FAIL、R2 K1-C、Human Gold 0 和正式 ASR/Accuracy 未测保留。D1 开发数据、D2/D3、5090 和旧逐格输出未访问。

## Owner23B 待批最小方案

| PO-MHEP 字段 | 拟议边界 |
| --- | --- |
| Issue ID | 待 Owner23B 登记，引用本次 Run ID。 |
| 问题 | 动态 CPU 后端、VC 初始化、模型加载与 RAM 仍需一次受控观测。 |
| 发现阶段 | Owner23A 静态收口，当前 `SMOKE_PENDING_OWNER`。 |
| 事实、推断与未知 | CLI 静态闭包与 API-set PASS。Haswell 和 x64 仅为静态候选，实际后端、加载和峰值未测。 |
| 既有约束 | 同一固定资产和 D 盘私有路径，CPU、无网络、零实验输入、无分发。 |
| 必要性 | 采集已加载模块、模型加载返回状态和峰值内存，解除静态方法无法验证的运行前门。 |
| 风险 | 入口可能隐式启动 warm-up、解码或联网，内存可能越限，整包许可仍未闭合。 |
| 选项 | 一次固定版本的本地 load-only 入口，或维持暂停直到许可证和入口证据补齐。 |
| 建议 | 先在固定源码上验证入口只做 CPU 后端初始化、模型打开和释放，代码与可执行身份须在批准前冻结。若现有 CLI 无可证路径，可另批仅用现有工具链和原 DLL 的 load-only harness。不能仅用 `-n 0` 推定零解码。 |
| 信心与可逆性 | 仅一次隔离进程，无数据写回。进程级限制和异常停止方案待预冻结。 |
| 已批与待批 | Owner23A 已结束。Owner23B 须明确同意本机用途的剩余许可风险及一次执行与模型加载权限。 |
| 执行与 STOP | 提议 CPU-only，D 盘输出，进程级禁网与 Job 对象；开跑前可用 RAM 和 commit 余量各 ≥8 GiB、D 盘余量 ≥10 GiB。仅一个进程、一次，90 秒或 4 GiB 私有 commit 即停。记录实际加载 DLL、峰值 commit/working set、返回值、退出码及日志 SHA。哈希偏差、额外依赖、warm-up 或 decode 迹象、网络、超时及异常立即停并封存，无自动重试。 |

## 文档收口

Human Ledger、Agent Ledger、Current Work State、Research Execution Log、Project Master、Experiment Master 和 Tracker 更新本次实际证据与下一门。Owner Decision Register 的 Owner23A 原授权保持为决策事实，本次无新增决定。Stage Process、Canonical Lessons、Research Plan Authority、README 均已检查，本次无新研究阶段、方法契约或导航变化。交叉检查当前任务、结论、阻断和下一步一致性，并按独立分支提交规则停止。

DOCUMENTATION_CLOSEOUT_CHECKLIST

    human_ledger_checked = true
    human_ledger_updated_if_required = true
    agent_ledger_checked = true
    agent_ledger_updated = true
    current_work_state_updated = true
    execution_log_appended = true
    experiment_master_condition_evaluated = true
    owner_decision_condition_evaluated = true
    stage_process_condition_evaluated = true
    lessons_condition_evaluated = true
    research_authority_condition_evaluated = true
    README_condition_evaluated = true
    cross_document_current_task_consistent = true
    cross_document_status_consistent = true
    cross_document_next_action_consistent = true
    cross_document_blocker_consistent = true
    markdown_links_valid = true
