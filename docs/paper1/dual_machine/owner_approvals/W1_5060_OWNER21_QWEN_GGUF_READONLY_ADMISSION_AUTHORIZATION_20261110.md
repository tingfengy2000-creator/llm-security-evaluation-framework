# Paper 1｜Owner21：停止纯规则主抽取路线 + Qwen2.5-1.5B GGUF 只读准入审计授权

**Owner decision ID:** `W1-OD-20261110-5060-QWEN-GGUF-READONLY-21`  
**Date:** 2026-11-10 JST  
**Approval:** `OWNER_EXPLICITLY_APPROVED / STOP_RULE_ONLY_PRIMARY / QWEN_GGUF_READONLY_ADMISSION_ONLY`  
**Authorized branch:** `research/paper1-chinese-defense-5060`  
**Approval-preceding remote HEAD:** `e8ec35a2c4a3ce626d843928a1e5660fcbe2f148`  
**Owner response:** “批准”，明确指向紧邻监督端唯一提议：“批准 5060 停止纯规则主抽取路线，并只读核验官方 Qwen2.5-1.5B GGUF 的资产、许可证、运行时与资源条件。这一次不批准下载、不批准推理，也不提前消耗新数据。”
**Status at issuance:** Owner20 `FEASIBILITY_NO_GO`；5090 Meta Llama 2 权限未有确认通过的证据，Claims1–3 NOT_RUN。该授权本身不代表只读审计已运行或通过。

## PO-MHEP 十二字段决策

1. **Issue ID**：`W1-OD-20261110-5060-QWEN-GGUF-READONLY-21`。
2. **Issue**：旧73开发集上的Rule-V2点估计与新100合成可行性验证显著不一致。是否停止将纯规则作为主要事实候选抽取器并准入唯一Qwen2.5-1.5B GGUF的只读官方元数据/本机资源审计。
3. **Discovery stage**：Owner20 `W1-5060-S1B-RULE-ONESHOT-20261110-01` 已封存 `FEASIBILITY_NO_GO`。Owner20新100主集Rule-V1值命中0/70、严格正确0/100、错抽2/2；Rule-V2值命中5/70、严格正确1/100、错抽10/11。两臂新120视图均只执行一次，各120/120。HumanGold0、正式ASR/答案准确率未测。
4. **Evidence separated**：
   - `OBSERVED_FACT`：报告的NO_GO、无标题主例全部UNKNOWN、V2另有40个有标题主例在主体/属性识别阶段拒识；R2 K1-C；旧73与新100+20从此均为已暴露开发/诊断数据，绝不能重复称未见测试。
   - `SOURCE_DERIVED_FACT`：官方`Qwen/Qwen2.5-1.5B-Instruct-GGUF`模型卡标明Apache-2.0并列出Q4_K_M文件；官方`ggml-org/llama.cpp`发布页存在Windows x64 CPU构建。来源：https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/main 与 https://github.com/ggml-org/llama.cpp/releases 。截至Owner21授权时，**具体不可变模型commit、所有所选文件与官方权重SHA、CPU运行时固定发布/二进制哈希仍待5060核查与封存**。
   - `INFERENCE`：规则的自然中文主体/属性、条件及证据span绑定缺乏足够的未见覆盖，继续针对已暴露样本扩张规则的科研净收益低；本地量化小模型值得按成本/风险有界验证，但尚无有效能力证据。
   - `UNKNOWN`：Windows CPU实际峰值RAM、CPU/内存/磁盘兼容性、固定GGUF在该机能否安全运行、模型抽取准确率、生成时延以及P0下的真实防御收益。
5. **Affected accepted constraints**：PO-MHEP / AGENTS、D1_DEV_EXPOSED、D2/D3隔离、5090 Compute-only/模型许可独立审批；旧S1 FAIL、Owner18暴露开发、Owner19和20所有不可变封存保持；RAGDefender B2/RD-zh基线与P0可信来源/版本/范围边界不改；S2–S5新审批门关闭。
6. **Why now**：已有具代表性的离线负结果，模型准入资源/许可事实是下一次低成本开发试验的真正阻断；先核完权重/运行时再批准资产，避免重复写规则/过早消耗测试集。
7. **Downstream risk**：Q4_K_M量化损失、模型幻觉、未证新版或跨scope幻觉式归因、未授权自动下载/动态`main`、有副作用的安装、外传私有数据、Windows C盘隐性缓存、运行时RAM与磁盘溢出、以及X-MADAM/MADAM已有结构提取工作重叠；“提取成功”仍不等于可信来源真伪核验成功。
8. **Options**：
   - A **OWNER APPROVED**：停止纯规则作为主抽取器、保留V1/V2作冻结对照/确定性span+scope校验，5060仅只读核验一个官方Qwen GGUF Q4_K_M模型与`llama.cpp` Windows CPU可执行资产，提交单模型准入包。无新模型费用/权重与依赖变更，允许回退；不能保证可用。
   - B 继续拓展Rule-V2（不需新权重，但加重过拟合与时间风险），未选。
   - C 直接批准GGUF下载并调用（更快产出数值，但来源/硬件/PO-MHEP尚未闭合），未选，**明确禁止**。
9. **LOCAL recommendation**：Owner确定A，核验顺序：官方模型仓库与不可变commit/许可证/单文件SHA和大小 → 官方llama.cpp固定tag/commit、Windows CPU二进制与许可证依赖/哈希 → 5060现有OS/架构、CPU指令集、可用RAM、D/E与C盘临时目录风险 → 上界预算和停止门 → **只读** Owner单模型资产申请。若Qwen Q4_K_M不满足资源门，提交替代选项分析，不自动切换到0.5B/UIE或另一量化。
10. **Rationale/confidence**：Owner对停止纯规则主抽取和只读核验的授权高置信；官方存在可下载GGUF与Windows CPU运行时的外部元数据证据可核；实际单机可用性、安全表现及收益未知，不得在只读阶段预判。
11. **Approved and still pending**：
   - `RULE_ONLY_PRIMARY_EXTRACTION=STOP_APPROVED`；`RULE_V1_V2_FROZEN_COMPARATORS=RETAIN`；`DETERMINISTIC_SPAN_SCOPE_VERIFIER=RETAIN_WITHOUT_SEMANTIC_PATCH`。
   - `MODEL_METADATA_LICENSE_RUNTIME_RESOURCE_READONLY_AUDIT=APPROVED`（仅`Qwen/Qwen2.5-1.5B-Instruct-GGUF`的Q4_K_M + 官方`llama.cpp` Windows x64 CPU候选）。
   - `MODEL_ASSET_DOWNLOAD/INSTALL/LOAD/INFERENCE=NOT_APPROVED`；`MODEL_DEVELOPMENT_INFERENCE=NOT_APPROVED`；`NEW_INDEPENDENT_VALIDATION=NOT_APPROVED`；`S2,S3,S4,S5=NOT_APPROVED`；`D2,D3=LOCKED`；`5090_LLAMA2_CLAIMS=NOT_APPROVED`。
12. **Allowed/prohibited work/stop**：
   - Allowed: 5060在唯一批准分支，只读访问官方HF模型卡、tree、具体文件Git LFS/Xet *metadata*、官方commit/README/LICENSE、官方llama.cpp release/tag/commit及其发布许可、二进制文件列表/散列元数据；只读Windows`systeminfo`/`Get-CimInstance`/`Get-Volume`/CPU feature、RAM/D/E/C空闲与已存在缓存元数据（命令需不产生额外可控文件）。列精确文件白名单及文件数/字节量、模型及运行时官方SHA、发行身份、来源使用条款、runtime兼容性、离线无额外请求方案、预计上下文长度/CPU线程/内存上界与磁盘余量、无C盘可控缓存措施、超限立即STOP。
   - Prohibited:下载任何权重、量化文件、Tokenizer、运行时二进制、源码包、依赖/工具/新数据；任何`pip/winget/choco/curl|sh`安装、`git clone`、`hf download`、`llama-cli -hf`、`ollama pull`、环境/注册表/PATH变更；加载或调用**包括已有缓存**的新模型、创建本地模型服务或外发实验原文、访问未授权私有GT、复测旧100+20、改Rule-V1/V2/GOLD、运行S2–S5或5090 Claims、跨分支merge。
   - STOP:若官方不可变版本/sha/模型权重与授权许可不可验证、RAM/D/E余量不足、CPU指令集/运行时依赖不闭合、出现下载提示或实际网络副作用、元数据与已冻结事实冲突，停止资产准入、保留`UNKNOWN/BLOCKED`。将升级问题交Owner，`Auto Continue=NO`。

## Expected deliverables, no scientific run

只读审核Run ID（建议`W1-5060-OWNER21-QWEN-GGUF-ADMISSION-20261110-01`）、固定源revision + Q4_K_M文件名/大小/LFS SHA及许可链接、llama.cpp CPU发行/二进制/依赖固定身份与哈希、Windows CPU/RAM/磁盘/离线cache安全预算、风险与未知清单、逐项`PASS/UNKNOWN/BLOCKED`、唯一单模型资产下一审批卡、实际下载/安装/模型加载/推理/API/费用计数均为0、脱敏证据SHA、按AGENTS的条件式治理同步、Git提交推送并核远端一致后STOP。
**本授权不包含下载或任何模型调用。**
