# Paper1｜Owner22 静态阻断复核及 Owner23 待决方案

日期：2026-11-10 JST
**状态：SUPERVISOR_REVIEW / OWNER23_DECISION_PENDING / NO_ADDITIONAL_EXECUTION_AUTHORIZATION**
**被审核的5060实验提交：** `34b83aefcc3b6fa59482843403a9c85d59cdbc4e`（核验时与5060远端一致）；5090远端 `dbd91f3667964baca69aeb82a6292c4fe193c965`，无新Claim。
**任务：** `W1-5060-OWNER22-QWEN-GGUF-ASSET-STATIC-20261110-01`
**私有审计封包 SHA256：** `faa281e7e4a14f2bc11a292b6e42e94f42421c7a4152ec55f4212ad01a708247`

## 1. 独立审阅已观察证据

- Qwen固定 GGUF 大小1,117,320,736 bytes，sha256`6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`；llama.cpp b12242 ZIP大小24,931,401 bytes，sha256`4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0`，两件正文合计1,142,252,137字节，等于审批上限，各一次传输、无资产正文重试。
- GGUF v3、Q4_K_M、qwen2 架构、内嵌tokens/merges/chat template元数据核验，未读取张量推理；52 ZIP成员静态路径/CRC/哈希均通过，解包64,352,541字节；51包内PE静态导入索引完成，22 EXE、29 DLL与一份LLVM OpenMP license。
- 原静态依赖处理停在512节点，`System32=101`、`PACKAGE=14`、`API_SET_UNMAPPED=387`、`NOT_FOUND_IN_SYSTEM32=10`（均间接`ext-ms-*`），`FRONTIER=29`。**512是审计算法设置的节点上限，不等于512个真实缺失DLL；29是未遍历的名称，不等于29个缺失依赖**。这项信息来自公开报告及检阅实际源码，不是已执行完成的静态闭包证明。
- 源码 `src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner22_static_inspection.py` `inspect_pe` 行254起将**所有**包内PE的导入集合入队，行265固定 `C:\Windows\System32`，行269后递归扩展所有System32导入，行271用512上限截断。此算法对`llama-cli.exe`所需最小加载闭包过宽，且未解析Windows API-set schema。可能产生虚假“文件未找到”和系统递归爆炸；不能据此断言真正CLI直接依赖已经缺失或可正常运行。
- 微软官方文档明确API-set是逻辑合约，必须经当前Windows schema将`api-*`/`ext-*`映射到host DLL；同名物理文件通常非必要；部分合约也可能不存在，不能反向宣称全部PASS。官方依据：`https://learn.microsoft.com/windows/win32/apiindex/windows-apisets`，`https://learn.microsoft.com/en-us/windows/win32/api/apiquery2/nf-apiquery2-getapisetmodulebasename`。
- llama.cpp MIT、BoringSSL和LLVM OpenMP许可证文本位置已记录，但**整包组件到许可的映射**仍不充分。VC runtime最低版本、目标CPU动态后端选择、强动态导入/间接LoadLibrary/RPC隔离都未证明。ZIP中`llama-cli.exe`无PE签名目录，不能仅依此判来源不可信，发布者发布SHA与attestation是另一证据链；依然禁止执行。
- 初次QA在D盘仓库ignore区生成临时文件而非批准D资产根，后迁移。需再只读清单校验批准目录及外侧该路径无残留/不改变既有证据；属于路径执行纪律的小范围偏差，不隐瞒。
- 9定向测试+Ruff+MyPy已报告PASS，模型文件/ZIP不进入Git，模型执行/加载/推理、API、成本、新科学试次均0。上述仅基于公开Git证据，监督端未打开本机D盘原始二进制与ZIP，不能虚称再次直接核sha。

## 2. 研究裁决

`OWNER22_ASSET_BYTES_PASS`、`GGUF_METADATA_PASS`、`STATIC_ZIP_SAFETY_PASS`；**整体仍 `OWNER22_ASSET_STATIC_INSPECTION_BLOCKED`，不予批准受控加载smoke或模型推理**。不过无法完成静态闭包的主因至少部分是审计器过宽与Windows API-set未映射，未证实全部29余项是真缺失依赖；不应随意增加512上限、以“可执行启动试试”替代静态审计、换模型/运行时或再下载。

**推荐下一道 Gate 23A：只做利用既有资产和已有系统API的范围收敛静态复核**。待Owner批准，暂不执行。预期：
1. 不改旧Owner22完整报告与封存，不修改受审核GGUF/ZIP；新脚本与新Run标识，保留原512退出码1及29前沿。
2. 以`llama-cli.exe`为唯一主加载根；从实际固定源码和静态导入中列出必须的CPU后端及llama-server-impl等动态路径。对所有包内PE保留现有表，但不要求非本任务启动的22个exe/不相关server/RPC的Windows全量闭包决定CLI smoke准入。
3. 显式解析`api-ms-*/ext-ms-*` API-set在当前Windows build的映射，区分静态/延迟导入/动态`LoadLibrary`以及KnownDLL/system forwarders；只使用可审计的Windows官方只读查询或已有离线证据，不执行**任何待验资产EXE/DLL**。若依赖需要新工具/下载或Windows系统API调用超出授权，上报，不自发扩大。
4. 去重、visited与cycle检测，限定根及深度/节点/文件大小/CPU时间，记录BFS闭包、API-set `MAPPED/HOST_MISSING/NOT_IMPLEMENTED/UNKNOWN`、PACKAGE/SYSTEM DLL的身份与位数以及真实命名缺口，保留所有unknown。禁止只调高512预算或因不在System32就判不满足。
5. 单独审阅CLI所需DLL及全部第三方静态/动态组件→MIT、Apache-2.0+LLVM exceptions、BoringSSL等具体许可归属，汇报`COMPONENT_LICENSE_PASS/UNKNOWN/BLOCKED`；缺官方条款不能猜或下载。
6. 分开记录最低VC运行库、静态导入符号可解析性、动态CPU后端选择；无法由静态资料完全证明动态行为时明确留`UNKNOWN_FOR_RUNTIME_SMOKE`，而不是因为理论上无法静态完全证明就无限期阻断。将“静态可确认前置”与“只能受控运行证实”明确分层，`STATIC_ENTRY_RISK_REDUCED`不等于`SMOKE_APPROVED`。
7. D盘根路径、之前外侧QA临时位置只读残留/ACL检查，0新下载、0新依赖安装、0执行模型EXE/DLL、0推理、0新样本/科学试次、0外部LLM/API、0费用；QA代码可运行于现有Python环境，但不得装新库、触私有D1/D2/D3/5090。
8. 提交Gate23A脱敏检查/新manifest+sha、未解决依赖与许可逐项矩阵，针对下一道Gate23B加载smoke的新PO-MHEP待决卡；完工STOP，Auto Continue=NO。

## 3. PO-MHEP 十二字段——下一项待Owner明确授权，不是已生效授权

1. **Issue ID**：`W1-PENDING-5060-OWNER23A-SCOPED-STATIC-PE-AUDIT`。
2. **Issue**：只利用已获得的两件资产，缩减静态依赖图至目标 CLI+必要CPU路径，核API-set/VC/第三方许可，避免512节点工具截断被当作实际依赖缺失。
3. **Discovery**：Owner22两文件字节与ZIP/GGUF通过，PE/package license依旧UNKNOWN，后续smoke尚未批准。
4. **Facts/unknown**：512节点中387个API-set未映射/29待遍历，不能宣称缺失；核心运行时与内存、正式抽取收益未知。
5. **Impacted contracts**：历史Run、SHA、下载上限耗尽不能再追加正文，P0、D2/D3、5090、S2–S5和模型使用权限不变。
6. **Why now**：最小修复为静态检查逻辑，能在零新增模型下载/调用下解除人为分析瓶颈，避免重复申请资产。
7. **Risks**：错误缩减根忽略动态CPU后端、将API-set名字误判为系统文件、误判VC最低版本、遗漏第三方许可证、模型或系统执行副作用。
8. **Options**：A（推荐，待批准）范围收敛的静态复核；B保持冻结等待外部完整静态清单；C直接smoke（当前不满足前置，拒绝自动执行）。
9. **Recommendation**：A，并明示成功也不代表可运行、更不表示可信来源/真实污染防御已解决。
10. **Confidence**：源码中的512截断与遍历策略高；CLI的实际可用性与动态依赖仍未知。
11. **Owner decision required**：是否单独授权`GATE23A_STATIC_ONLY`；如Owner批准，仅这一条生效。`GATE23B_RAM_SMOKE`、模型推理和科学试次仍未批准。
12. **Allowed/prohibited**：未获新批准前只读监督复核和档案记录；禁止执行5060新静态科学试次、加载、执行、推理、额外依赖安装/下载、D2/D3、S2–S5、5090，STOP `AUTO_CONTINUE=NO`。

**Final state：`OWNER22_ASSET_STATIC_INSPECTION_BLOCKED / GATE23A_PENDING_OWNER / MODEL_EXECUTION_NOT_AUTHORIZED / AUTO_CONTINUE=NO`。**
