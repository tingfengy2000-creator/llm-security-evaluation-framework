# Paper 1｜Owner22：两项固定模型资产受限获取与静态验包授权

**PO-MHEP ID**：`W1-OD-20261110-5060-QWEN-GGUF-ASSET-22`  
**日期**：2026-11-10 JST  
**唯一分支**：`research/paper1-chinese-defense-5060`  
**Owner当前指令**：“请继续”，明确承接5060完成Owner21只读审计后所提出的下一道唯一待批事项：“仅获取这两项固定资产并静态验包，传输上限1,142,252,137字节”；本许可**只**是下载+静态验证，不是模型加载许可。若现场Owner/合同权限指向存在不一致立即停止上报。  
**批准状态**：`OWNER_EXPLICITLY_APPROVED / TWO_ASSET_DOWNLOAD_AND_STATIC_INSPECTION_ONLY`，`MODEL_LOAD_INFERENCE=NOT_APPROVED`，`AUTO_CONTINUE=NO`。  
**授予前远端 HEAD**：`91fb7df8cf2542bddd9063d21a93c31829426a11`；现有5090远端 `dbd91f3667964baca69aeb82a6292c4fe193c965`。  
**直接先决证据**：`docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER21_QWEN_GGUF_SINGLE_MODEL_ADMISSION_PACKET.md`、`W1_5060_OWNER21_QWEN_GGUF_READONLY_MANIFEST.json`。Owner21审计 `READONLY_AUDIT_COMPLETE`；ASSET_IDENTITY仅发布者元数据层PASS，`LICENSE=UNKNOWN_PACKAGE_COMPLETE`、`RUNTIME=BLOCKED_MEMBER_AND_PE_DEPENDENCY_PROOF`、`RESOURCE=BLOCKED_PEAK_UNPROVEN`。

## PO-MHEP 十二字段

1. **Issue ID**：`W1-OD-20261110-5060-QWEN-GGUF-ASSET-22`。
2. **Issue**：是否对已锁定单模型及唯一Windows CPU运行时进行最小可控资产获取和静态哈希、许可证、ZIP成员、PE依赖检查，以解除模型/整包身份的不确定性，而不承担运行风险。
3. **Discovery**：Owner20 Rule-V1/V2在全新100合成语义主集 `FEASIBILITY_NO_GO`；Owner21只读审计完成并明确下一步只需两个文件的静态获取，尚无资产字节/实测RAM证据。
4. **Observed / derived / inferred / unknown**：
   - `OBSERVED` 5060 Owner21公开审计报告锁定：
     - 官方模型 `Qwen/Qwen2.5-1.5B-Instruct-GGUF@91cad51170dc346986eccefdc2dd33a9da36ead9`，唯一文件 `qwen2.5-1.5b-instruct-q4_k_m.gguf`，**1,117,320,736 bytes**，官方LFS SHA256 `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`，模型Apache-2.0。
     - 官方 `ggml-org/llama.cpp` tag `b12242` / commit `3b4d6ab3f79651935fba1dd93732f29022a7f5f5` / asset ID `729746535`，唯一ZIP `llama-b12242-bin-win-cpu-x64.zip`，**24,931,401 bytes**，官方Release digest `4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0`，源码MIT。GitHub预发布`immutable=false`，故运行时实际资产哈希必须再次逐字节校验；不因tag稳定而默认资产稳定。
     - 先前采样RAM可用12.80GiB、D/E有空间、CPU AVX2；内存规划峰值4.10/4.23/4.51GiB为估算，不是实测。
   - `SOURCE_DERIVED` 经官方发布元数据再次核对Windows CPU ZIP 24,931,401 bytes与sha256与Owner21一致；HF固定文件页可核对内容SHA256；上述只是发布者证据，不等于真实传输/解压后本地校验。
   - `INFERENCE`：购买/下载两个文件进行非执行性静态检查，可补全发布物证据链；模型效果仍未知。
   - `UNKNOWN`：ZIP内容/第三方notice/PE闭包、GGUF内嵌tokenizer配置与无危险格式、实际加载和推理峰值、未来抽取质量。
5. **Inherited constraints**：双机合同、AGENTS、PO-MHEP、Owner16–21、P0不升权、R2 K1-C、S1 FAIL、Owner20 NO_GO均冻结；旧73与新100+20只能作已暴露开发材料；D2/D3/5090 Claims不触、S2–S5未批准；正式ASR/AnswerAccuracy NOT_MEASURED、HumanGold=0。
6. **Why now**：唯一运行时实际字节尚未核验，PE/DLL/Notice阻断静态准入，无法负责地申请内存smoke或推理；该操作不消耗科学试次或额外模型推理费用。
7. **Risks**：固定HF URL/发行ZIP被替换、重定向至非批准来源、ZIP slip/zip bomb/符号链接、Win可执行不安全/签名不明、C盘继承TEMP或缓存、未授权附带下载与安装、第三方许可缺失、版本差导致动态依赖缺口；解包不等于执行安全。
8. **Options**：A **Owner批准**两个指定文件单次下载与静态验包，0运行/0模型调用，低研究和经济成本但引入有限供应链风险；B持续只读等待发布者更多清单，风险小但不产生内容证据；C下载后立刻smoke/推理，权限和资源门未闭合，**禁止**。
9. **Recommendation**：固定D盘隔离目录、精确白名单、预算、哈希，不安装和不运行任何EXE/DLL或权重；静态验ZIP条目、许可证、PE导入，列所有阻断；如缺依赖只报缺口，不自动下载。
10. **Confidence**：资产公开元数据身份高，静态包是否自洽未知，执行安全性、实测RAM及事实抽取能力无证据；其结果不得提高现有科研结论等级。
11. **Owner explicit decisions**：
    - `ALLOW_EXACT_TWO_ASSET_DOWNLOAD=YES`；
    - `ALLOW_STATIC_GGUF_HEADER_TOKENIZER_METADATA_READ=YES`（禁止模型加载、解析时需要注意不可信输入）；
    - `ALLOW_ZIP_LIST_SAFE_UNPACK_TO_D_AND_OFFLINE_PE_IMPORT_INSPECT=YES`；
    - `ALLOW_LICENSE_AND_THIRD_PARTY_NOTICE_AUDIT=YES`；
    - `ALLOW_MODEL_LOAD/LLAMA_CLI_EXECUTION/INFERENCE/SMOKE=NO`；
    - `ALLOW_NEW_DEPENDENCY_DOWNLOAD/INSTALL/BUILD/PIP/WINGET/CHOCOLATE=NO`；
    - `ALLOW_ASSET_SUBSTITUTION_OR_EXTRA_QUANTIZATION=NO`；
    - `ALLOW_NEW_SCIENTIFIC_TRIAL/S2_S5/D2_D3/5090=NO`。
12. **Allowed / prohibited / stopping**：
    - **White list** only:
      1. `https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf` → basename exact, bytes 1,117,320,736 and sha256 `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`.
      2. `https://github.com/ggml-org/llama.cpp/releases/download/b12242/llama-b12242-bin-win-cpu-x64.zip` → basename exact, bytes 24,931,401 and sha256 `4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0`.
    - 两个实际**资产正文成功下载字节**相加必须恰为`1,142,252,137`；这也是合计资产正文**硬传输上限**（不包含正常协议头的元数据流量，但不得借此下载其它文件）。仅各一次完整传输，禁止自动重试、自动替代镜像、增量diff、动态`main`、自动hub client多文件缓存和获取副资产。若链路失败/半成品、上限将超出或官方重定向目标无法核验，立即STOP登记失败；不能自行重新开始完整下载。
    - 全部资产、暂存、日志、解包与受控证据必须位于`D:\experiments\paper1_chinese5060\owner22-assets\`下，创建前核本机实际D/E挂载、可用空间及reparse/symlink；`TEMP/TMP/HF_HOME/HF_HUB_CACHE/HUGGINGFACE_HUB_CACHE/LLAMA_CACHE/XDG_CACHE_HOME`对本子进程重定向到D盘；不允许将私有原文或模型缓存落C盘，环境修改仅该进程。
    - 总新增D盘占用峰值**≤4 GiB**、ZIP总解压上限**≤512 MiB**、完成后D盘剩余空间**≥10 GiB**；超出必须STOP。分别对两下载字节做本地SHA256后才能打开GGUF头或ZIP；ZIP先只读枚举/验证解压上限、成员路径/重复大小写/绝对路径/..穿越、符号链接、junction/reparse及异常压缩比，记录每文件SHA，再选择受控D盘解包。不得激活系统Shell文件关联/安装程序。
    - 对`llama-cli.exe`与EXE/DLL只做离线PE结构解析、导入DLL列表/版本要求尽可能静态检查，既不执行也不加载、反射调用或通过OS注册模块，禁止启动服务。全包所有Third Party Notice/对应许可必须核对；不确定用`UNKNOWN`。
    - **绝对禁止**：`llama-cli`、`llama-server`、`--help`、`--version`等任何待验可执行文件的启动；加载GGUF进行模型创建/前向推理、GPU/CPU试运行、`pip/winget/choco`安装、下载VC/LLVM依赖、执行脚本、联网自动安装器、额外新模型或Tokenizer下载、访问D1/D2/D3/private GT/5090、旧100样本再测试、S2–S5或主分支合并。
    - 若本机已存在未授权模型文件不得用其替代本次白名单核验；如官方SHA/长度、证书、来源、许可证或ZIP/PE证明不一致`HUMAN_DECISION_REQUIRED / AUTO_CONTINUE=NO`。

## Completion and separation of gates

5060本轮唯一结束状态：`OWNER22_ASSET_STATIC_INSPECTION_PASS`或`OWNER22_ASSET_STATIC_INSPECTION_BLOCKED`，并**永远**附`MODEL_EXECUTION_NOT_AUTHORIZED / PEAK_MEMORY_NOT_PROVEN / SCIENTIFIC_RUNS=0`。交付文件资产长度/SHA、官方再核对、ZIP逐成员清单及sha、全许可证与PE/DLL闭包和缺口、静态GGUF头/嵌入tokenizer证据、资源与缓存目录审计、出站/安装/推理/模型API/费用账本、PO-MHEP下一阶段smoke待批卡、私有哈希归档、Git commit/push/远端SHA。无论成功失败STOP。
