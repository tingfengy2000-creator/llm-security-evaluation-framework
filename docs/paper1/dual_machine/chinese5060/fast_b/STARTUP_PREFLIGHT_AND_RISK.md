# Fast-Track B 启动、资源和风险核验

日期2026-11-05 JST；控制面 `f491c0a507e5555e9611c022cfba66980ad8cbca`，仅5060独立研究分支。
授权 [FAST-B-04](../../owner_approvals/W1_FAST_TRACK_B_OWNER_AUTHORIZATION_20261105.md) 与
[RESOURCE-REPRO-05](../../owner_approvals/W1_STORAGE_AND_REPRO_RESEARCH_DIRECTION_20261105.md)。
工作树启动clean，behind7，逐项核验均为已知Owner治理提交后仅ff-only同步；同步后0/0，无跨分支操作。
优先级仍为RAG安全研究、评测平台、护栏工程、Agent扩展；正式实验NOT_STARTED。

## 事前资源冻结

本次允许继续的本地审计/盲审材料支路：新增存储峰值64MiB（含临时与ZIP副本），RAM512MiB，CPU1线程，
wall300秒；开始/结束均验证D盘剩余不少于20GiB+剩余峰值。所有新内容在本worktree下Git忽略的实验目录。
Python使用既有原生Windows解释器，`-B`，TEMP/TMP及HF/Torch/XDG/pip/MPL/cache目录全部重定向D盘；
不调用WSL/Docker/conda/pip安装、不创建VHDX，既有C盘解释器文件只读，不迁移或覆盖旧模型缓存。
操作系统自身写入不作绝对零承诺；不以进程TEMP重定向声称OS级沙箱。
启动观测D盘约311GiB、E盘约337GiB空闲，实际字节另见私有preflight。

未来下载/过滤支路的资源与白名单合同仍须在最终Prompt核对后单独冻结。本记录不批准启动该支路，
不把旧1GiB限制继续施加D/E；250MiB累计网络界和至少20GiB余量保持。

## FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW

1. 只读固定官方源码及原seal逐文件验证；不改源码、模型、TopK、chunk、query、样本或阈值。
2. B1公共v0.2固定模型轨道不等于ACSAC artifacts或严格数值复现；B2只能单变量embedding替换。
3. 原36世界、29命中和7miss保留；不得把检索miss变成检测成功或把部分删除说成完整清除。
4. 独立材料支路只读固定V2卡及批准SOURCES，不读取候选、标签、检索结果、旧预测、两机实验结论或Reviewer。
   原卡可为AI开发草案；审阅者尚未存在/签署，不声称已经完成盲审或产生Human Gold。
5. 审阅包不包含query_id/事实组/角色映射、P2结果、旧AI判断；来源原文、引文、时间/条件不因结果改写。
6. 无商业API、下载、载入模型、额外依赖、T1/T2或新机制；未知执行合同不得自行补齐。

## HUMAN_DECISION_REQUIRED：最终Prompt缺失（十二字段）

1. Issue ID：W1-5060-FAST-B-CONTRACT-01。
2. Issue name：Owner提及随附最终Prompt，但当前会话未收到该附件/路径。
3. Stage/task：Fast-Track B下载和B1/B2正式开发运行前preflight。
4. OBSERVED_FACT：控制面完整SHA及两项Owner授权已核；提交仅含授权/治理文件；本会话附件接口返回空清单。
   SOURCE_DERIVED_FACT：最新指令要求遵循最终Prompt且不得缩减资源/安全/证据门。
   INFERENCE：缺失文件可能包含额外执行门；UNKNOWN：文件内容、身份和额外准入条件。
5. Affected rules：AGENTS、PO-MHEP A/F/G、context recovery和最新Owner指令。
6. Why now：必须在任何模型下载/正式过滤输出前确认合同完整。
7. Risks：擅自推断可能遗漏网络累计计量、磁盘峰值、模型身份或异常停止要求，影响安全/复现/公平性；等待会延迟结果。
8. Options：A提供确切文件后核hash继续，零重复下载、可逆、保留科研边界；B明确两份已提交授权与当前消息就是完整最终合同，
   需Owner确认且不能由Agent自行推断；C自行省略文件直接运行违反当前要求，不执行。
9. LOCAL recommendation：A；先完成互相独立、明确授权的只读核验和盲审材料。
10. Rationale/confidence：缺失附件及Git文件清单高置信，额外合同内容未知；不把未知当作无附加条件。
11. Owner decision：提供最终Prompt确切路径/内容，或明确可执行的完整合同身份。
12. Before decision：下载/模型载入/B1/B2停止；只允许本地审计、盲审材料、证据及Git治理收口；禁止全部未批后续任务。
