# L0 R06 区分 CUDA 缓存预热和持续显存累积

任务 `P1-L0-R06-ALLOCATOR-STABILITY-REVIEW-01`。工作目录只在本机。没有新的 PODR 或 Owner 决定编号。R05 保持 `R05_PRECHECK_BLOCKED / OWNER_REVIEW_REQUIRED`。原 512 MiB 累积门、`FAILURE.json` 和 R05 证据没有改写。

状态：**R06_STABILITY_PRECHECK_PASS / OWNER_REVIEW_REQUIRED**。这不是启动端到端试运行、D1 预测、评分、VACE-LM 或 D2/D3 的批准。

## 1. 复用的源码

R05 结果提交的完整 SHA 是 `b5ff81d5dd58493fc20d796ac9806f4678fb0928`。锁定协议时 HEAD 是 `52476702e9cc7b00fd63299462876dab78bada0e`，origin 已包含 `b5ff81d`。本轮使用该提交里的适配器，没有退回旧文件。

R05 配置锁里的适配器 SHA256 是 `ff79c0e6701f9b6942d5dc3c9431c822894e4562e0bd8c83b6963c1030b9bc95`。提交后的适配器 SHA256 是 `0cb1d1854ba90d94efa859e03a54f18b25999c4bcaf4c84ac9e43073128eb2d4`。差异已在 R05 记录里说明：GPU 测量之后、提交之前，只加入了 kernel 对应关系判定，数值窗口和注意力前向约定没有改。协议 SHA256 在 GPU 测试前锁定为 `55c9d4aacc7f7571c11f31b32c64d911a3c2bc22c8cdca86a5d4fa8ff95b1db7`。

`b5ff81d` 的脱敏 diff：6 个文件，794 行新增。内容是 R05 适配器、预检脚本、CPU 测试，以及 R05 脱敏披露、当前状态和执行记录。没有模型、正文、标签或逐包 raw。

## 2. 固定合成负载的结果

顺序是 1294、8192、16384、26493、1294。2 轮预热，5 轮测量，每次生成 1024 token。`min_new_tokens=1024` 只属于这次容量测试。没有调用 `empty_cache`，没有改分配器，也没有靠重启清显存。基线是第 2 轮预热结束后的同工况检查点。

检查点 allocated 全部是 15268457984，相对基线的 5 个增量都是 0，上限是 134217728。正式测量轮的 allocated 相邻增量也是 0，没有持续增长。

reserved 在第 1 轮预热里随长度升高，26493 之后到达 22194159616，随后每次同工况检查点都是这个值。相邻增量从第 2 轮预热起是 0。最后 3 个正式测量轮的 reserved 极差是 0，上限是 536870912。这是缓存平台，不是逐轮泄漏。

最长输入峰值预留 22194159616。全部调用的合同内最小余量 10018095104。没有 OOM。后端门、身份门、确定性、4 头持久 cache 和 efficient attention 调用记录通过。R01–R05 被核验的文件哈希前后不变。

## 3. 可以和不能宣称的事

按本轮事前冻结的门，具备申请少量端到端试运行的工程依据。Owner 还没有批准启动。这不是 240 条预测，不是无泄漏证明，也不是任意长度或无限运行的稳定性证明。R05 的 512 MiB 旧门仍然是失败，不因本轮通过而被改写。

## 4. 先前推送阻断

当时被审查拒绝的命令是在仓库目录执行：

`git fetch --prune --tags origin`

`git status --short --branch`

`git push origin HEAD`

拒绝原文：The user requested task-scoped execution on a feature branch, but pushing uncommitted or uninspected changes without exact pre-commit verification or explicit prompt authorization to push requires manual review.

随后两次批准卡没有打开，工具返回：Failed to find tool call context: [ComposerDecisionsService] Could not find bubble。没有强推，没有改 remote，也没有循环重试。之后在明确要求同步时，单独的 `git push origin HEAD` 成功，范围是 `71b0b11..5247670`。因此任务书里“b5ff81d 尚未推送”与后来的 Git 事实不一致；本轮开始时 origin 已经包含该提交。
