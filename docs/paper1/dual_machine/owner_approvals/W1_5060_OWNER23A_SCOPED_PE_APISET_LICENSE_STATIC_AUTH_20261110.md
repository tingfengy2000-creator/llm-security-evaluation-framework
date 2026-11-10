# Paper 1｜Owner23A：已下载运行时的收敛式静态 PE/API-set/许可审计

**PO-MHEP Issue ID：** `W1-OD-20261110-5060-OWNER23A-SCOPED-STATIC-23A`  
**日期：** 2026-11-10 JST  
**唯一分支：** `research/paper1-chinese-defense-5060`  
**正式状态：** `OWNER_EXPLICITLY_APPROVED / SCOPED_STATIC_PE_APISET_LICENSE_AUDIT_ONLY`  
**授权时远端基点：** `3f88a8a880e2182df5ccba75fc9ee7b97dec51e3`。  
**Owner 原话：** “现在进度到什么程度了，你如果有大把握就不用我审批直接给出5060的命令即可，我这次批准Owner23A”。授权严格指前一轮 `Gate23A` 只读收敛式静态复核；一般工程事项允许代理在该既定任务内自主修复，不自动扩展到模型加载、推理、新资产下载、科学试次或合并。后述高风险门仍遵循既有Owner合同。

## PO-MHEP 十二字段

1. **Issue ID**：`W1-OD-20261110-5060-OWNER23A-SCOPED-STATIC-23A`。
2. **问题**：Owner22 下载的权重和运行时 SHA256 已 PASS，但原静态分析从全部 PE 扩张系统导入图，触及512节点限额，其中387为未映射 API-set、29项为未遍历前沿，无法完成实际目标`llama-cli.exe`的运行前静态评估；包内组件第三方许可和VC要求未闭合。
3. **发现阶段**：Owner22 `W1-5060-OWNER22-QWEN-GGUF-ASSET-STATIC-20261110-01`，提交`34b83aefcc3b6fa59482843403a9c85d59cdbc4e`，审计`OWNER22_ASSET_STATIC_INSPECTION_BLOCKED`；监督复核`W1_5060_OWNER22_ASSET_STATIC_BLOCKED_SUPERVISOR_REVIEW_20261110.md`确认原实现`inspect_pe`从所有包内PE导入递归System32，512为算法节点预算，并非512缺失DLL，29也不是已确认缺失。
4. **事实/推断/未知**：`OBSERVED` Qwen GGUF 1,117,320,736 bytes sha256`6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`；llama b12242 ZIP 24,931,401 bytes sha256`4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0`；52成员/51 PE/9测试通过，未加载；`INFERENCE` 将仅CLI及必要CPU后端闭包作为审计范围可能减少系统API-set图遍历噪声；`UNKNOWN` CLI实际运行、动态后端选择、最低VC版本、最终完整许可与峰值内存。
5. **既有约束**：双机研究合同、AGENTS、PO-MHEP；Rule-V1/V2与Owner20 NO_GO不可改，旧73和新100+20已暴露，S1 FAIL/R2 K1-C保持；P0可信来源、D1_DEV_EXPOSED、D2/D3隔离、Human Gold0、正式ASR/Correctness NOT_MEASURED；5090 Llama2 Claims仍锁，S2–S5锁；Owner22下载额度已使用完，不得追加文件正文。
6. **必要性**：减少不必要的静态闭包假阴性，以已有资产和标准库解决可控工程审计阻断，为未来单独决定受控加载提供证据；停止无目的审批循环。
7. **风险**：错误缩小CLI启动路径、漏查GGML动态CPU DLL、误把Windows API-set虚拟合约视为实体文件或反之、静态导入不代表运行时完整、忽略BoringSSL/OpenMP许可证、VC最小版本未知、扩大静态脚本触碰未授权系统区域、QA临时残留。
8. **可选方案**：A **Owner批准**：用已有文件进行有界、非执行性、目标路径静态再核验，算法和普通单测工程缺陷可在限定范围自主修复/复测；B维持BLOCKED不工作；C未经前置闭合直接执行smoke/下载新依赖（明确禁止）。
9. **建议**：执行A。仅以`llama-cli.exe`为主起点，保留包内51个PE总表，但与本任务无关的server/RPC/其他21工具无需成为CLI本次smoke前置依赖。针对API-set通过Windows官方公开文档/可审计只读系统信息进行语义映射、按分类记录未证项；对动态后端及静态链接notice明确保留UNKNOWN。不要通过简单增加512预算伪造完成。
10. **信心与可逆性**：PE分析器实际根集合/截断行为证据高；目标CLI闭包能否全部静态闭合未知。新任务仅产生可逆的新脚本、新日志与新Manifest，不改原资产/原审计失败。
11. **已批准/仍待批**：`OWNER23A_SCOPED_STATIC_REAUDIT=APPROVED`、`BOUNDED_ENGINEERING_REPAIR_WITHIN_SCOPE=DELEGATED_TO_5060`；`MODEL_EXECUTION/LOAD/SMOKE/INFERENCE=NOT_APPROVED`、`NEW_PACKAGE_DOWNLOAD/INSTALL/BUILD=NOT_APPROVED`、`NEW_SCIENTIFIC_TRIAL/NEW_BLIND_TEST=NOT_APPROVED`、`S2_S5=LOCKED`、`D2_D3=LOCKED`、`5090_CLAIMS=LOCKED`。Owner通用授权不得解释为可绕过既有重大研究变更门。
12. **允许/禁止与STOP**：
    - 允许：先只读验证本地两个固定资产哈希及授权D盘目录；以已有`owner22_static_inspection.py`为只读参照新建 `Owner23A` 独立静态检查器/测试；只读解析本地PE及既有Windows API-set schema/系统DLL文件的静态证据；分析CLI直接/延迟导入、包内直接DLL、必要GGML CPU动态后端候选、KnownDLL与前向导出、VC runtime本地版本/可获得的最低约束、所有已分发组件的具体license/notice；检查D盘临时残留；对工程性脚本、单测、格式和逻辑错误在新代码中自主修复并复测（不修改旧Owner22报告、不重新运行旧科学试次）。可以整理公开官方文档文字，不下载新资产。
    - 禁止：执行甚至`--help`/`--version`任意新下载的EXE/DLL、`LoadLibrary`或注入DLL、GGUF模型创建/推理/内存smoke、额外网络二进制下载、安装依赖、外发私有数据、无白名单系统根全盘扫描、Rule-V2历史修复、访问D2/D3/5090、S2–S5、合并main。
    - 门控：以不超过2048个**相关非API-set实体**、时间/磁盘/文件大小明确预算实施静态闭包，不得仅调高原512而把全部System32全遍历当完成；API-set进行独立映射表，无法核查则UNKNOWN而不是假PASS，记录闭包remaining frontier和原因。许可证无法闭合也只报UNKNOWN，不伪造可用性。
    - STOP：任一原始hash/路径不符、需要额外二进制/下载/运行、权限超出/不安全动态加载、P0新语义或科研参数变更、正在写入不可变旧档案、D盘风险或系统变更，即`HUMAN_DECISION_REQUIRED / AUTO_CONTINUE=NO`。

## 交付和结束

建议Run ID `W1-5060-OWNER23A-SCOPED-STATIC-20261110-01`（无科学实验），报告CLI路径的实际静态依赖矩阵与根证据、API-set解析/不明项、CPU后端动态导入风险、最低VC依赖、组件许可逐项表、原512前沿和差异、QA外侧D盘残留检查、静态指标`PASS/UNKNOWN/BLOCKED`、无需新增资产或模型的事实、private archive SHA、Git完整commit/push与远端状态。可在本批任务中自主消除脚本BUG/单测问题，但不能修改冻结资产或扩大研究试次。
`OWNER23A_STATIC_REPORT_READY / OWNER23B_SMOKE_NOT_AUTHORIZED / MODEL_EXECUTION_NOT_AUTHORIZED / SCIENTIFIC_RUNS=0 / AUTO_CONTINUE=NO`。
