# 5060｜Owner22 两项资产获取与静态验包

2026-11-10 JST · `W1-5060-OWNER22-QWEN-GGUF-ASSET-STATIC-20261110-01`。**`OWNER22_ASSET_STATIC_INSPECTION_BLOCKED / MODEL_EXECUTION_NOT_AUTHORIZED / PEAK_MEMORY_NOT_PROVEN / AUTO_CONTINUE=NO`**。两项本地字节身份、GGUF 元数据和 ZIP 安全检查均通过。整包许可与完整 PE 依赖仍未闭合。 [Owner22 授权](../../owner_approvals/W1_5060_OWNER22_FIXED_QWEN_GGUF_ASSET_ACQUISITION_STATIC_INSPECTION_AUTH_20261110.md)

| 门 | 实际状态 | 依据 |
| --- | --- | --- |
| ASSET_BYTES | PASS | 两件 SHA256、长度和发布者身份一致 |
| GGUF_METADATA | PASS | GGUF v3、Q4_K_M、内嵌 tokenizer 和模板头已解析 |
| STATIC_ZIP_SAFETY | PASS | 52/52 个成员安全列出、解包并核哈希 |
| PACKAGE_LICENSE | UNKNOWN | 主项目、BoringSSL 及 LLVM OpenMP 文本定位。整包逐组件条款覆盖未证 |
| PE_DEPENDENCY | UNKNOWN | 51 个 PE 的包内静态导入已核，系统 API-set、传递前沿、最低 VC 版本、动态后端未闭合 |
| ACTUAL_RUNTIME_MEMORY | NOT_MEASURED | 运行内存未测 |
| MODEL_COMPATIBLE_LOAD/INFERENCE | NOT_TESTED | 执行、加载、推理、安装及新科学试次均为 0 |

## 资产获取

| 文件 | 官方固定身份 | 正文与本地文件字节 | 本地 SHA256 |
| --- | --- | ---: | --- |
| `qwen2.5-1.5b-instruct-q4_k_m.gguf` | `Qwen/Qwen2.5-1.5B-Instruct-GGUF@91cad51170dc346986eccefdc2dd33a9da36ead9` | 1,117,320,736 | `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e` |
| `llama-b12242-bin-win-cpu-x64.zip` | `b12242@3b4d6ab3f79651935fba1dd93732f29022a7f5f5`，release 439859799，asset 729746535 | 24,931,401 | `4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0` |

固定 HF 版本重新核验 Apache-2.0、LFS 摘要与长度；GitHub tag、commit、asset ID、官方 release/asset 摘要一致，仍为可变预发布。实际开始 12:58:13 JST，结束 13:03:29 JST。两件各一次固定长度完整响应，合计 **1,142,252,137 字节**，等于上限。重试及额外资产正文 0。两个固定发布地址分别只跟随一次 HTTPS 重定向到 `us.aws.cdn.hf.co` 与 `release-assets.githubusercontent.com`。默认 TLS 证书及主机名校验启用，实际 TLS 版本和对端证书摘要在 Manifest，未公开签名 URL 查询。首次无正文 HEAD 因本地白名单尚未列出 HF CDN 而停止，随后用官方文档与固定源响应证明主机后完成无正文预检。没有消费或重试资产正文。 [固定模型文件](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/blob/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf) · [HF 官方 CDN 表](https://huggingface.co/docs/hub/models-downloading) · [固定发布](https://github.com/ggml-org/llama.cpp/releases/tag/b12242)

## 静态检查

- **GGUF。** v3，`general.architecture=qwen2`、`general.file_type=15`、339 个 tensor 描述项、26 个元数据键。张量描述偏移对齐检查通过，未解析张量正文。28 层、嵌入宽度 1536、12 Q／2 KV 头、文件声明 context 32768。文件的 `general.size_label` 原文为 `1.8B`，锁定模型的官方 repo 与文件仍为 1.5B 名称，资产实际哈希匹配。内嵌 tokenizer `gpt2 / qwen2`，151,936 tokens、151,387 merges。模板 2,509 字节，SHA256 `d5495a1e5db0611132a97e46a65dbb64a642a499421228b9c8b93229097fa9a4`，未渲染模板。
- **ZIP。** 中央目录在解包前检查 Windows 路径、大小写冲突、设备名、ADS、重解析属性、链接、加密、压缩比和容量。52 件，含 22 EXE、29 DLL、1 个许可证文件。解包 **64,352,541 字节**，上限 512 MiB。最大压缩比 3.401，门为 200。每个成员的相对路径、原始和压缩字节、CRC32、SHA256 已列入 Manifest。任何 EXE/DLL 均未启动或加载。
- **许可。** 唯一独立文档 `LICENSE-LLVM-OpenMP` 与 Owner21 固定 SHA 一致，OpenMP 随包提供 `libomp.dll`。在 `llama.exe` 与 `llama-connect.exe` 静态找到与 Owner21 许可文本去首尾空白后逐字节匹配的 llama.cpp MIT 和 BoringSSL 文本。该证据只能说明对应文本存在，完整组件归属、UI/静态链接第三方 notice 尚未闭合。未补下任何许可或依赖文件。
- **PE。** 51 个包内 PE 全为 AMD64 PE32+，常规和延迟导入表均记录。直接依赖去重 38 名，其中包内 14、System32 命中 12、API-set 合约未映射 12；没有直接导入名在三类外。宿主 `msvcp140.dll`、`vcruntime140.dll`、`vcruntime140_1.dll` 版本均 14.50.35719.0，最低 VC 需求未证明。`llama-cli.exe` 无 PE 证书目录，未作 Authenticode 验证。含 server、RPC 与 connect 工具，CLI 的静态路径包含 `llama-server-impl.dll`，保留其依赖证据，未启动任何服务。
- **PE 边界与失败记录。** 首次全量脚本在扩展 Windows 系统依赖图时触及 512 节点预算并退出 1。保留原日志、已验 GGUF 和已解包字节，随后只读重核 ZIP 与成员哈希，补存 512 节点和 29 个未访问前沿，未重新下载或解包。512 节点包括 System32 101、包内 14、未映射 API-set 387、固定搜索目录中无实体文件 10（均为间接 `ext-ms-*` 名称，不能据此判需下载 DLL）。动态后端选择和 loader 绑定仍未验证。 [PE 格式](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) · [固定发布构建](https://github.com/ggml-org/llama.cpp/blob/3b4d6ab3f79651935fba1dd93732f29022a7f5f5/.github/workflows/release.yml)

## 存储、验证与封存

资产和原始证据位于 `D:\experiments\paper1_chinese5060\owner22-assets`。创建前核 NTFS、祖先路径及无重解析点，资产根只允许当前用户、SYSTEM 和 Administrators。下载暂存和最终文件以同卷重命名，末态暂存为空。运行子进程的 TEMP/TMP、HF 和 llama 缓存、USERPROFILE 及 AppData 重定向到该 D 盘根，没有持久环境修改。首轮纯工程 QA 临时目录使用 D 盘仓库忽略区，随后收纳到批准根。无 C 盘可控资产或缓存写入。预检、传输分段、解包和封存均检查容量。封存后根逻辑字节 1,313,540,345，D 盘余量 331.53 GiB，满足新增 4 GiB／保留 10 GiB 的约束。

下载／首轮静态代码 Git `6e31dbdbaf9bd537f27b409882bfbdc18d84fe8f`，PE 补存代码 `160e9194948ecd27ad037fa1483e6b973bfe9957`。下载、首轮静态、PE 补存退出码依次 0、1、0，命令与 stdout/stderr 封存。初版 ZIP 路径单测因 Windows fixture 自动规范反斜线未触发，修正 fixture 后 9 项单测通过，Ruff、MyPy 通过。无模型 API、无安装、无新实验，费用 USD 0。

私有元数据与日志归档 `seals/OWNER22_PRIVATE_AUDIT.zip`，43 件，SHA256 `faa281e7e4a14f2bc11a292b6e42e94f42421c7a4152ec55f4212ad01a708247`，不包含权重、发行 ZIP 或 EXE/DLL 正文。 [完整脱敏 Manifest](W1_5060_OWNER22_QWEN_GGUF_ASSET_STATIC_RUN_MANIFEST.json)

## PO-MHEP 下一道受控加载 smoke 卡（待批，准入前置未闭合）

1. **Issue ID** `W1-PENDING-5060-QWEN-GGUF-RAM-SMOKE-AFTER-OWNER22`。
2. **待决** 核闭整包 notices 与 CLI 运行依赖后，是否允许一次最小本地 CPU 加载资源检查。
3. **阶段** Owner22 两资产字节已核，静态总体 BLOCKED。
4. **事实和未知** 静态权重、ZIP 和 PE 见上；实际加载、内存峰值、CPU 动态选择、完整运行条款和依赖未知。
5. **继承** 不换资产，不追加依赖，D 盘边界、无出站、旧 NO_GO、R2 K1-C 与 S1 FAIL 保留。
6. **目的** 区分已确认的字节完整性和仍未知的安全加载条件。
7. **风险** 未解析导入、最低 VC 版本、未证 notice、系统内存、程序自动联网与模型输出混淆。
8. **选项** A 保持阻断，先审阅并补齐静态证明。B 仅在闭合后另签一次受限 smoke。当前无执行许可。
9. **建议** 先闭合静态缺口，后续若批准加载，沿用 512 context、6 线程、CPU 单序列和 D 盘落点，验证 OS 出站阻断；加载与生成授权分离。
10. **信心** 固定资产身份高，完整许可与运行闭包未知，实际峰值和推理能力未测。
11. **所需批准** 明确唯一 GGUF、ZIP/成员 SHA、仅本地加载资源检查、5 GiB 进程限额、可用物理 RAM 和提交余额各 ≥9 GiB、主机余量 4 GiB、超时和隔离执行方案。无生成、无开发数据、无服务。
12. **停止** 任何证据缺口、摘要漂移、依赖缺失、非法指令、内存、I/O、超时或联网异常即停。不能从本卡自动执行。

## 恢复与收口

Paper 1 保持 RAG Security 优先，其后为评估平台、Guard 与 Agent Security。已核 AGENTS、权威图、PO-MHEP、动态状态、Owner21 和 Owner22、实验主账、冻结前序结果。独立发布检出无未知修改，从 `91fb7df8` 快进至 `04df96e617fa0fc575dc8c0a0062690f14fe7ed5`，与远端一致。原检出保持原状。FORWARD_RISK_REVIEW／PAPER_RISK_REVIEW 已区分供应链字节、静态数据解释、加载资源与抽取有效性。历史 Owner20 NO_GO、R2 K1-C、S1 FAIL、Human Gold 0、正式 ASR/Accuracy 未测均保留。

Current Work State、Project Master、Experiment Master、Execution Log、Week 1 Tracker、Human/Agent Ledger 同步。Owner Register 无新决定，Stage Process、Lessons、Plan 与 README 无新阶段、验收或合同变更。S2–S5、D2/D3 与 5090 Claims 继续锁定。发布核验后 STOP。

## DOCUMENTATION_CLOSEOUT_CHECKLIST

```text
human_ledger_checked=true
human_ledger_updated_if_required=true
agent_ledger_checked=true
agent_ledger_updated=true
current_work_state_updated=true
execution_log_appended=true
experiment_master_condition_evaluated=true
owner_decision_condition_evaluated=true
stage_process_condition_evaluated=true
lessons_condition_evaluated=true
research_authority_condition_evaluated=true
README_condition_evaluated=true
cross_document_current_task_consistent=true
cross_document_status_consistent=true
cross_document_next_action_consistent=true
cross_document_blocker_consistent=true
markdown_links_valid=true
```
