# 5060 Codex｜Owner22 生效：单模型 Qwen GGUF + llama.cpp Windows CPU 两文件获取与静态验包

**Permission**：`W1-OD-20261110-5060-QWEN-GGUF-ASSET-22`，仅**两项固定字节**下载与非执行性静态检查。  
**Not permitted**：安装、执行llama.exe、加载GGUF模型、CPU/GPU smoke、生成/推理、模型API、其它资产下载、科学试次、S2–S5或5090。不要把本轮当作`RUNNABLE`。  
**Read full approval**：`docs/paper1/dual_machine/owner_approvals/W1_5060_OWNER22_FIXED_QWEN_GGUF_ASSET_ACQUISITION_STATIC_INSPECTION_AUTH_20261110.md`。与本文冲突时按更窄的许可，PO-MHEP重大不一致上报。

## 0. Context recovery / preflight

只在`research/paper1-chinese-defense-5060`，先读取AGENTS.md、PO-MHEP、Owner21完整[准入包](docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER21_QWEN_GGUF_SINGLE_MODEL_ADMISSION_PACKET.md)（路径相对repo root）、Manifest、最近实验历史、实验主账与治理记录；用独立发布工作树检查git status、HEAD、upstream、branch、近15 commits及远端快进关系，无强制覆盖历史，不cherry-pick到主线。前次Owner21已报告的证据基点HEAD `91fb7df8cf2542bddd9063d21a93c31829426a11`，现在执行前以最新远端为准。独立编写Context Recovery、FORWARD_RISK_REVIEW、PAPER_RISK_REVIEW，旧Owner20`FEASIBILITY_NO_GO`、R2 K1-C、S1 FAIL与HumanGold0不变。

## 1. 字节级白名单（不可变）

只允许下列**两个**实际大资产（其余资料只可查询公开元数据，不能另外获取内容资产）：

| Purpose | Official frozen source | Exact basename | Exact bytes | SHA256 |
| --- | --- | --- | ---: | --- |
| Qwen GGUF | `https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf` | `qwen2.5-1.5b-instruct-q4_k_m.gguf` | 1,117,320,736 | `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e` |
| llama.cpp CPU ZIP | `https://github.com/ggml-org/llama.cpp/releases/download/b12242/llama-b12242-bin-win-cpu-x64.zip` | `llama-b12242-bin-win-cpu-x64.zip` | 24,931,401 | `4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0` |

模型revision唯一`91cad51170dc346986eccefdc2dd33a9da36ead9`；llama.cpp tag`b12242` commit`3b4d6ab3f79651935fba1dd93732f29022a7f5f5`、GitHub Release ID`439859799`、Asset ID`729746535`。该发布`prerelease=true, immutable=false`；必须始终逐字节比对摘要。不得以任何新GitHub release、Qwen其它量化、其他GGUF或自动安装包替代。官方模型页公开权重SHA及Apache-2.0，运行时源码MIT；ZIP第三方notice待本次验包。

**传输硬上限**：模型正文 + ZIP正文下载字节总计`1,142,252,137`，不含少量必要HTTP metadata头，但禁止第三资产正文；各一次固定长度完整传输，关闭自动下载重试、自动hub Xet缓存预热和多镜像分片重下；无法满足固定字节或断线即STOP，不自动重新开始。任何官方重定向须HTTPS且最终来源可以被证明是相应HF/GitHub发布资产的合法下载目标；无法核实时STOP。不得跟随网页README中示例命令自动`llama-cli -hf`、`winget`、`pip`、`ollama pull`等自动联网行为。TLS证书校验不可关闭。

## 2. 文件路径与准入配额

唯一资产目录：
`D:\experiments\paper1_chinese5060\owner22-assets\`
建议仅固定`download/ staging/ unpacked/ logs/ seals/`独立子目录。真实新可控资产的TEMP/TMP、HF_HOME、HF_HUB_CACHE、HUGGINGFACE_HUB_CACHE、LLAMA_CACHE、XDG_CACHE_HOME、USERPROFILE的副作用路径必须静态预判；能临时重定向的仅本子进程D盘重定向；不可避免写C盘即STOP，禁止永久修改OS环境/PATH/注册表，不安装工具。

新的D盘占用（含下载临时、完整权重、ZIP、解压内容、hash记录和归档）峰值 ≤4 GiB；ZIP解压总大小 ≤512 MiB；工作完成D盘仍≥10GiB剩余。预先检查实际盘符、重解析点/junction/symlink、ACL和可用容量。不能信任外部文件名或ZIP条目自行构造脱离根路径；不使用系统Shell双击或执行发布的二进制。

## 3. Stage A：只下载和字节核验（禁止运行）

先审查固定HF模型文件页的license/size/LFS SHA与GitHub固定Release asset REST digest（资产pre-release可变，记录核对时间、SHA和release id）。仅以严格限制的网络流读取允许两个固定asset内容，实时统计actual response bytes和上界，拒绝额外附带正文。使用当前机器已经许可、无需安装的内置标准库/平台网络能力；禁止获取任何新工具、pip依赖、额外license asset或新权重。下载完成与官方字节数严格相等、立即计算本地sha256，不一致先封存失败日志后STOP，不能静默重新下载/镜像替换、跳过或自动修复。

对权重只可在哈希PASS后以非执行性方法读取GGUF头、metadata键、模型架构、内嵌tokenizer/chat template元数据，记录证据而不执行模型加载或向任何模型框架提供文件。不要扫描大块权重内容造成额外内存/磁盘预算失控。

## 4. Stage B：ZIP与许可证静态审计（禁止执行任何EXE/DLL）

哈希核验通过后，先只读列出ZIP全部成员、compressed/uncompressed sizes、CRC、路径、重复大小写、绝对路径/..、Windows设备名、符号链接、reparse points、炸弹比和总解包容量，若异常STOP；仅在全部清单通过后才安全解包至D盘。不得把ZIP交给默认安装器或加载DLL。

静态提取：每成员相对路径、文件大小和SHA256；`llama-cli.exe`/EXE/DLL清单；可以使用安全现有Windows只读API或已有无副作用的Python标准库PE读取代码查看PE头和依赖导入，但不得调用Windows LoadLibrary、启动exe，甚至`--help`或`--version`。分析imported DLL与现有OS DLL的名称/架构/版本（只读），若传递依赖或最低VC runtime版本证据不足标`UNKNOWN/BLOCKED`，**不得自取VC runtime**；模型相关server/RPC/自动更新组件若存在仅记录，不得运行。
检查ZIP包含的license、NOTICE和第三方归属与官方源码构建引用的LLVM OpenMP、BoringSSL等对应关系；整包许可不能靠主项目MIT自动判PASS。对缺失条款进行诚实列示；不自动补下任何license文件或源码。

## 5. 准入决定、审计边界、治理

**本轮不是运行时smoke。** 结束仅可判：
- `ASSET_BYTES=PASS|BLOCKED`
- `STATIC_ZIP_SAFETY=PASS|BLOCKED`
- `PACKAGE_LICENSE=PASS|UNKNOWN|BLOCKED`
- `PE_DEPENDENCY=PASS|UNKNOWN|BLOCKED`
- `GGUF_METADATA=PASS|UNKNOWN|BLOCKED`
- `ACTUAL_RUNTIME_MEMORY=NOT_MEASURED`
- `MODEL_COMPATIBLE_LOAD/INFERENCE=NOT_TESTED`
- `MODEL_EXECUTION_NOT_AUTHORIZED`

预期输出：run ID建议`W1-5060-OWNER22-QWEN-GGUF-ASSET-STATIC-20261110-01`，下载源/两项原文SHA/长度，发行与证书证据、每成员清单/哈希、第三方许可证说明、PE静态导入闭包、GGUF内嵌metadata、所有disk/cache路径与真实bytes账本，测试/secret scan、单次操作与失败记录、最终资产包静态评级和**下一Owner受控加载smoke审批卡（待批、不执行）**。Git中只发布脱敏摘要/哈希/脚本及权威治理日志；D盘私有GGUF和ZIP不得提交仓库、不能暴露私有数据，做Git commit/push后核远端分支无差异。

如果下载中断、hash漂移、恶意/超大ZIP、无权获取某依赖、上限超出、无法保持路径或不慎启动模型，立即STOP并登记PO-MHEP事件。完成后 `ASSET_STATIC_INSPECTION_PASS`或`BLOCKED / INFERENCE=0 / MODEL_LOAD=0 / COST_USD=0 / AUTO_CONTINUE=NO`。不得从资产PASS自动进入`RAM_SMOKE`、开发推理、验证、S2–S5、5090 Claim或主分支合并。
