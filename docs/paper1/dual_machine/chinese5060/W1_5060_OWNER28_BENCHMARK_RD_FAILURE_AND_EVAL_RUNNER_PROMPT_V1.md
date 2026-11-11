# 5060 Codex｜Owner28独立中文基准小样本：失败图谱 + 冻结评估器

**依据**：`docs/paper1/dual_machine/owner_approvals/W1_OWNER28_BENCHMARK_INDEPENDENT_PILOT_20261111.md`，PO-MHEP ID `W1-OD-20261111-PAPER1-OWNER28-BENCHMARK-INDEPENDENT-PILOT`。
**先做**：在`research/paper1-chinese-defense-5060`读`AGENTS.md`、Owner28合同、Owner27报告和manifest、相关治理与Tracker；`git fetch origin`,确认本合同、`git status`,仅clean时ff-only,不合并。回传 HEAD 和执行机身份。不再次请求Owner26入账或商业API。
**交付A（立即，无新科学试次）**：
1. 以Git封存Owner27 manifest为主复算全部既有7臂指标，提供分母、每事实组、每情境、所有21臂配对掩码差异及结论。标 `READ_ONLY_SEALED_DEV_ANALYSIS`；若不能访问私有353...zip原文，Git manifest局限写清。
2. 按原错误案例提供至少6种分层失败类型：`CURRENT_CLEAN_OVERDELETE`,`VALID_HISTORICAL_HN_OVERDELETE`,`SCOPE_HN_OVERDELETE`,`FORGED_UPDATE_SURVIVES`,`PARAPHRASED_COLLUSION_SURVIVES`,`5_OF_5_NOT_RETRIEVED`，每例绑定匿名world/hash/TopK ranks，区分可验事实与agent暂定角色；从Git summary能推的写AGGREGATE_ONLY，不得臆造具体原文和UID。
3. 做`RECEIPT_PROVENANCE_LEAKAGE_AUDIT.md`：检查`normalized_value_sha256`、`scope`、`version`、`start/end`是否来自DEV真值卡/造数者，是否构成部署不可获得的Oracle输入；要求把`LOCAL_SYNTHETIC_RECEIPT`与`REAL_SIGNED_RECEIPT`严分，报告信息增益和漏标。检查`JOINT_NO_SCOPE`事实上也可恢复异scope HN、相同掩码下scope机制不可识别。仅静态审查，不改Owner27代码或再跑它的科学试次。
4. 在`OWNER28_BENCHMARK_PILOT_PROTOCOL.md`写一句核心科研问题：中文版本与scope下，RD-zh相对B2对Poison/Clean/HN如何权衡？与无过滤和仅日期基线的候选级真实收益是什么？主表单列检索召回，不把召回失败算检测成功，论文负结果也要保留。

**交付B（可以开发，但仅synthetic fixture测试，不是科学样本运行）**：
5. 从Owner27已通过的runner逻辑复用查询/TopK/role-free预测/evaluator封存与模型SHA，开发可接收5090后续独立role-free包的generic runner。固定4臂`NONE,RD_B2,RD_ZH,DATE_ONLY`，严禁新增或调优算法/阈值、更改模型/tokenizer/TopK/索引/检索参数。不要读取5090 Gold或打开其EVAL标签路径；不得查看5090来源候选名单后选择参数。
6. 给公共接口schema、`run`命令示例、role-free schema检查与双向SHA收据、盲预测封存和`PREDICTION_READY_FOR_INDEPENDENT_5090_EVAL`标准；以invented test snippets验证命令能跑通，用mock只做软件集成；不得冒称EVAL已完成或结果复现。
7. 真正收到4090? **注意应为5090** role-free包后，先核Owner28 G1-G3；合法且与5090签名、来源权利及Role隔离俱全则在本授权内**一次性**32主世界同TopK四臂预测，预测hash封存后由5090私有评价进程独立评分。不能使用曾暴露的四文档谱系及任何DEV原世界填补EVAL；无法严禁泄漏即STOP。实际未收到包时仅交付A+B，不空耗研究资源。

**交付文件**：`OWNER28_DEV_FAILURE_ATLAS.md`,`OWNER28_RECEIPT_PROVENANCE_LEAKAGE_AUDIT.md`,`OWNER28_BENCHMARK_PILOT_PROTOCOL.md`,`OWNER28_BENCHMARK_RUNNER_MANIFEST.json`（由实际代码/测试状态填写）、独立代码/测试文件、治理日志/Tracker增量。将源码、Model/bytes/权限/命令、重复试次状态精确记录。仍不得D2/D3/HOLD8/Owner26/商业API/5090 Claim/主线merge。当前0新性能结果可如实标 `RUNNER_READY / EVAL_NOT_RUN`。只推5060分支、工作树clean后STOP。
