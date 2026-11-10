# 5060｜Owner21 单模型资产准入包

2026-11-10 JST · `W1-5060-OWNER21-QWEN-GGUF-ADMISSION-20261110-01`。**只读审计完成，资产与执行准入均未放行。** 本包只涉及 Qwen 官方 Q4_K_M 和 llama.cpp 官方 Windows x64 CPU 构建。旧 Owner20 `FEASIBILITY_NO_GO`、S1 FAIL、R2 K1-C 保留。 [Owner21 授权](../../owner_approvals/W1_5060_OWNER21_QWEN_GGUF_READONLY_ADMISSION_AUTHORIZATION_20261110.md)

## 结论

| 门 | 状态 | 依据与缺项 |
| --- | --- | --- |
| ASSET_IDENTITY | PASS（发布者元数据） | 两件候选都有固定内容 SHA256、精确字节和官方来源，实际资产字节未读取 |
| LICENSE | UNKNOWN（整包） | Qwen 权重 Apache-2.0、llama.cpp 源码 MIT、LLVM OpenMP 许可文本已核。CPU ZIP 全量第三方 notice 与成员对应待核 |
| RUNTIME | BLOCKED | ZIP 发布身份闭合，源码与主机静态指令集匹配。内部成员、PE 导入、VC 运行库最低版本和 DLL 全量依赖未证 |
| RESOURCE | BLOCKED | 实时主机余量通过规划阈值，静态预算最高约 4.51 GiB。完整运行峰值上界 UNKNOWN，需独立许可后的受控证明 |

## 唯一资产白名单

| 类型 | 固定身份 | 精确文件 | 字节 | SHA256 |
| --- | --- | --- | ---: | --- |
| Qwen 官方 GGUF | `Qwen/Qwen2.5-1.5B-Instruct-GGUF@91cad51170dc346986eccefdc2dd33a9da36ead9` | `qwen2.5-1.5b-instruct-q4_k_m.gguf` | 1,117,320,736 | `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e` |
| llama.cpp CPU x64 | `b12242@3b4d6ab3f79651935fba1dd93732f29022a7f5f5`，Release 439859799 / Asset 729746535 | `llama-b12242-bin-win-cpu-x64.zip` | 24,931,401 | `4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0` |

- **模型身份。** 固定树 LFS `oid` 为表中内容 SHA256。对固定 `resolve` URL 只发不跟随重定向的 HEAD，`X-Repo-Commit`、`X-Linked-Size` 和 `X-Linked-ETag` 与树一致，权重正文传输 0。Git pointer blob SHA‑1 `eca68f83004d8b86fa1742ee507ddee8f4b2abce` 和 Xet 对象标识 `6ca5463cf24c16cd56d7ad7461524d813b07b3f29889b2fbdbb8286a7e97a14a` 分开保存。未发现单独权重签名。官方用法只选一个 GGUF，树无单独 tokenizer 文件。本文件的嵌入词表及模板实际字段待后续静态检查。 [固定文件页](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/blob/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf) · [固定树元数据](https://huggingface.co/api/models/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/91cad51170dc346986eccefdc2dd33a9da36ead9?recursive=true&expand=true)
- **权重条款。** 固定模型卡与同 revision 的 Apache-2.0 LICENSE 一致，许可证文本按 Git blob 与树交叉验证，SHA256 `832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e`，11,343 字节。后续分发应保留许可、适用 NOTICE 和归属，标明修改，保留商标及专利条款边界。本包仅提议本机内部使用。 [固定模型许可](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/blob/91cad51170dc346986eccefdc2dd33a9da36ead9/LICENSE)
- **运行时身份。** 选定 `b12242` 当次官方 CPU x64 发布，属于预发布，GitHub `immutable=false`。发布与单资产 REST 元数据的摘要一致，官方 SLSA provenance 的 subject 摘要及 gitCommit 与表中匹配，源提交的 GitHub 验签状态为 verified。这里仅对比证明内容与发布元数据，未用本地资产进行签名／证明校验。未来以固定 tag、提交、资产 ID、大小和摘要一起拒绝漂移。 [固定发布](https://github.com/ggml-org/llama.cpp/releases/tag/b12242) · [单资产元数据](https://api.github.com/repos/ggml-org/llama.cpp/releases/assets/729746535) · [发布证明](https://api.github.com/repos/ggml-org/llama.cpp/attestations/sha256:4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0)
- **构建与依赖。** 实际发布 workflow 用 Windows 2025、VS 18 工具环境、Clang x64 工具链，启用 `GGML_BACKEND_DL`、x64 CPU 全变体、OpenMP 和 BoringSSL，打包整个 `build/bin/Release`。固定源码可确认 `llama-cli` 目标、CPU 后端动态库变体、LLVM OpenMP 20.1.8 的 `libomp.dll` 和 `LICENSE-LLVM-OpenMP` 复制规则。Haswell 档需 SSE4.2、AVX、F16C、FMA、AVX2、BMI2，本机均支持。更高变体出现在构建矩阵中，本机 AVX-512F 不可用。精确变体选择、ZIP 内 EXE／DLL 的名称、大小、摘要和传递 PE 导入均待静态验包，本次未从 ZIP 读取。 [固定构建](https://github.com/ggml-org/llama.cpp/blob/3b4d6ab3f79651935fba1dd93732f29022a7f5f5/.github/workflows/release.yml) · [固定 CPU 与 OpenMP 配置](https://github.com/ggml-org/llama.cpp/blob/3b4d6ab3f79651935fba1dd93732f29022a7f5f5/ggml/src/CMakeLists.txt)
- **运行时许可。** 主项目 MIT LICENSE SHA256 `94f29bbed6a22c35b992c5c6ebf0e7c92f13b836b90f36f461c9cf2f0f1d010d`。OpenMP 许可为 Apache-2.0 with LLVM Exceptions，官方许可文本 SHA256 `fdad1758a9e1f9d5a81e18879b3406772115edc92c24bfa36b70c654f325e8e4` 与构建 pin 相同。构建提到的 LLVM 安装器 pin 属上游构建输入，不在本机白名单。cpp-httplib 路径静态编入 BoringSSL `0.20261105.0`，需保留其 LICENSE/归属，完整 notices 待验包。系统已有 x64 `vcruntime140.dll`、`vcruntime140_1.dll`、`msvcp140.dll`（14.50.35719.0）及 UCRT。文件存在不能证明具体二进制所需最低版本满足，亦不授权 VC Redist、LLVM 或 BoringSSL 另取另装。 [llama.cpp 许可](https://github.com/ggml-org/llama.cpp/blob/3b4d6ab3f79651935fba1dd93732f29022a7f5f5/LICENSE) · [LLVM OpenMP 许可](https://github.com/llvm/llvm-project/blob/llvmorg-20.1.8/openmp/LICENSE.TXT) · [BoringSSL 许可](https://boringssl.googlesource.com/boringssl/+/refs/tags/0.20261105.0/LICENSE) · [微软运行库说明](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

## 主机与资源门

2026-11-10 12:08 JST 采样。Windows 11 Pro x64 build 26200，Ryzen 7 5700X 8 核 16 线程，SSE4.2、AVX、AVX2、FMA、F16C、BMI1/2 可用。可见物理内存约 31.92 GiB，性能计数器可用 12.80 GiB、提交额度剩余约 22.14 GiB。C/D/E 为 NTFS，空闲约 66.45 / 332.76 / 336.57 GiB。CIM 和计数器的可用值采样时刻不同，启动门须重新采样。PATH 无目标 llama 可执行项，继承的 E 盘 HF cache 未发现固定 revision 的确切快照文件。这是定向检查。继承 TEMP/TMP、LOCALAPPDATA、USERPROFILE 位于 C，LLAMA_CACHE、HF_HOME、XDG_CACHE_HOME 未设。本次只给审计进程设置 D 盘 TEMP/TMP，未改持久配置。

| 总 context | 输入含模板上限 | 输出上限 | F16 KV 原始值 | scratch 预留 | 规划峰值 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 512 | 384 | 128 | 14 MiB | 512 MiB | 4.10 GiB |
| 1024 | 896 | 128 | 28 MiB | 640 MiB | 4.23 GiB |
| 2048 | 1920 | 128 | 56 MiB | 896 MiB | 4.51 GiB |

单序列，6 线程，batch 64、ubatch 32，K/V 均 F16。模型架构参考为 28 层、2 KV 头、head dimension 128。每 token KV 为 28 × 2 × 128 × 2（K/V）× 2 字节 = 28,672 字节，再向上取整至 4 MiB 粒度计入预算。峰值规划计两份权重字节（装载与文件／暂存重叠）、对齐 KV、表中 scratch、512 MiB 运行时及词表和 1 GiB 风险余量。scratch 和重排内存是保守预留，无法由公开元数据证明完整 GGML 计算图、分配器和 DLL 峰值，因此保持 `RESOURCE_GATE_BLOCKED`。 [官方架构配置](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/989aa7980e4cf806f80c7fef2b1adb7bc71aa306/config.json) · [固定 KV 源](https://github.com/ggml-org/llama.cpp/blob/3b4d6ab3f79651935fba1dd93732f29022a7f5f5/src/llama-kv-cache.cpp)

拟设运行监督上限 5 GiB，启动需可用物理 RAM 和提交余额各 ≥9 GiB，留 4 GiB 主机余量。未来同时看私有提交、工作集及系统余量，任一越限、明显分页、OOM、加载异常、非法指令、超时或不预期出站立停。5 GiB 是拟定执行边界，不是已经证明安全的峰值。后续须另批资源 smoke，短上下文起步，保存峰值证据后才讨论开发推理。

两项资产传输硬上限 **1,142,252,137 字节**。D 盘单目录拟设 `experiments/paper1_chinese5060/owner21-assets`，下载、最终权重、ZIP、解压目录、日志和临时缓存各独立子目录，总新增预算 4 GiB、ZIP 解包上限 512 MiB、完成后盘余量 ≥10 GiB。两份 GGUF、两份 ZIP 与解包及日志预算纳入总额。后续逐一解析最终和临时路径，拒绝穿越、链接／重解析点及重名。TEMP/TMP、HF_HOME/HF_HUB_CACHE、LLAMA_CACHE、XDG_CACHE_HOME 与进程工作目录固定 D 盘，禁止环境继承引发 C 盘落点或模型缓存回退。本次未创建未来资产目录。

## 纸面数据流与后续门

如资产另获许可，只对两项白名单固定来源传输，匹配字节、SHA、发布证明后，离线枚举 ZIP、查路径安全及展开大小，核每项 SHA／许可并静态解析 EXE/DLL 的 PE 导入闭包。任何缺失依赖均暂停。资产阶段不启动模型程序。再经独立许可才可用绝对本地路径运行单进程 CLI，拟配置 `--offline --device none -ngl 0 --fit off --load-mode none --lazy-mode off --no-warmup --no-context-shift -t 6 -tb 6 -b 64 -ub 32 -ctk f16 -ctv f16 -n 128`，另以固定 `-c` 与明确本地 `-m`、输入文件接线。禁止网络模型参数、服务器、RPC、自动换设备、在线缓存回退和工具调用。进程级离线参数须配合可验证的 OS 出站隔离。 [固定 CLI 参数](https://github.com/ggml-org/llama.cpp/blob/3b4d6ab3f79651935fba1dd93732f29022a7f5f5/tools/cli/README.md)

模型输入仅 `query + original evidence`。生成结构化候选值、单位、主体属性、版本与生效时间、条件、范围、原文引文和位置线索。确定性校验核原文字节、字符位置、范围及时态绑定，无法唯一绑定则 UNKNOWN，始终保持 `UNVERIFIED_TEXT_ONLY`。开发只可在另批的已揭盲旧73与 Owner20 100+20 上和冻结 Rule-V1/V2 比较；未来未见验证须新数据、独立审批。正式防御与 M3/P0 的可信凭证另有门。

## PO-MHEP 下一道单模型资产决策卡（待决）

1. **Issue ID** `W1-PENDING-5060-QWEN-GGUF-ASSET-AFTER-OWNER21`。
2. **问题** 是否放行两项固定资产的隔离获取与静态验包。
3. **发现阶段** Owner20 NO_GO 后的 Owner21 只读审计，当前模型运行能力未知。
4. **事实与未知** 发布身份与核心许可已核，主机静态匹配和资源有余量；第三方 notices、ZIP 内 PE 闭包、权重内部元数据和峰值待证。
5. **涉及约束** D/E、出站隔离、无 C 盘可控缓存、冻结基线、无私有输入出站、D2/D3 与 5090 隔离。
6. **为何现在** 获取固定字节后才能封闭包内容与依赖，静态审计已经给出唯一候选和预算。
7. **下游风险** 预发布变动、归档解包风险、VC/DLL 版本差、CPU 后端误选、内存峰值超预期、量化损失和误绑定。
8. **选项** A 待 Owner 独立批准两项资产获取与静态验包。B 保持阻断，待发布者提供完整清单后复核。
9. **建议** A 仅限资产和静态核验，核验遇阻退回 Owner。运行峰值证明另走受控 smoke 审批。
10. **信心** 发布者元数据高，实际加载依赖与资源未知，抽取性能未知。
11. **待决** 是否批准精确两件资产、规定 D 盘根、传输及磁盘硬上限，以及只做哈希、许可证、ZIP 与 PE 静态核验。后续加载、推理、数据与科学试次仍待独立决定。
12. **停止** 摘要或版本漂移、许可证／依赖不闭合、路径逃逸、额外下载、磁盘或运行门越限立停。无替换模型、无重试科学任务、无自动启用 S2–S5。

## 恢复与证据

Paper 1 保持 RAG 安全优先，后续评估平台、Guard 和 Agent Security。核对 AGENTS、PO-MHEP、权威地图、Owner21、动态状态、R1/R2 历史边界、实验与执行记录。隔离发布检出在干净状态从 Owner20 快进到 `169d0df261dff6031dacc4b0f2d97b59ea574f94`，同步无冲突、无未提交／未推送修改；原检出保留。FORWARD_RISK_REVIEW／PAPER_RISK_REVIEW 关注资产可变、供应链、量化偏差、来源信任和实验外推。只读审计无模型效果结论。

私有 D 盘任务目录内 `READONLY_METADATA_PRIVATE.zip` 封存 36 件官方元数据、固定源码文本、许可、系统查询和审计记录，SHA256 `7895f7ef2c28e6b7411112bf71140b17cd6b1160b614fc6662b4b132ebf4a816`。公开[脱敏 Manifest](W1_5060_OWNER21_QWEN_GGUF_READONLY_MANIFEST.json)。初始沙箱 CIM 拒绝，授权的只读查询成功；初次 F16C 查询类不存在，改用 CPUID 位。运行时资产正文、权重、分词器和安装器下载均为 0，安装、加载、推理、模型 API、费用和新试次均为 0。仅发生 Git 与官方公开元数据／文档读取。

Current Work State、Project Master、Experiment Master、Execution Log、Tracker 与 Human/Agent Ledger 按条件更新。Owner Register 无新决定，Stage Process、Lessons、Plan 与 README 无新阶段、验收或合同变更。Human Gold 0，正式 ASR / Answer Accuracy 未测，S2–S5 与 5090 Claims 保持锁定。只读任务收口后 STOP。

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
