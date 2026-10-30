# Oracle 逐断言对齐对照结果

任务 `P1-L0-ORACLE-CLAIM-ALIGNMENT-COMPARISON-01`。Run `VACE-L0-D1-20261030-ORACLE-ALIGN01`。执行提交 `4f4ece34e434d21b9c2dc076d53efe1587470594`。状态 `ORACLE_CLAIM_ALIGNMENT_DEV_COMPLETE / OWNER_REVIEW_REQUIRED`。

研究判断：`TRADEOFF_FPR_INCREASED`。总体检出的点估计从 14/40 增到 15/40，但 Clean 误报从 4/40 增到 6/40，HN 误报从 2/40 增到 5/40。不能只凭 Recall 上升宣称成功。事前规则“检出增加且 Clean/HN 误报不增加”没有得到支持。

这是 D1_DEV 上的一次固定提示对照。不是最终方法、正式测试、泛化证据或创新性证明。正结果和负结果都能结束本任务。没有第二版提示，没有重跑 F5，没有启动 VACE-LM、D2/D3 或新模型。

## 身份

完整 system 是原 `SYSTEM_PROMPT` 加一个换行再加固定后缀。完整 system SHA256 `e0300d58710cbbe0e83c588103b7d448e791570f5b0eec67b154cd3c2463f684`。后缀 SHA256 `373b1dd47fd85a9c8a5358fb64f57bdbb8c5a371c78fbb07bc0015815ad402dd`。原文在协议里。Parser SHA256 `e4e5967ee040caa44ac615a3b571f2227b0e2f3f6ac8bd1517438272bdfb4db9`。适配器 SHA256 `0cb1d1854ba90d94efa859e03a54f18b25999c4bcaf4c84ac9e43073128eb2d4`。GenerationConfig SHA256 `2e667e6e68c069bac62b13dfb7359b6b8f0e6c96c3664f9af7db27b68521d542`。Oracle 输入 SHA256 `0d3db8ed3d0049ba7998ec91d51bcbeae7901014ee3be6b2c38a2fe9cd89d7fb`。CONFIG_LOCK SHA256 `db852563b2ab24067ac815b2d52aa50200a2f13459cc1b73bba1426052266121`。新预测 SHA256 `37f2c941b585e325fbb1051c4c1f7ffd6ec2d990eb46277245ac19ea43e691a3`。预测锁 SHA256 `09b0ea5d237158e5472b12cffe5ed3d8807c99bdbce809e9c216896f3d57fda5`。120 条 raw 与锁一致。输入超限 0，最大输入 16894 token，上限 31744。

FULL01 预测和预测锁仍是 `be87b3fd4457ee212b43bf2f709ded476858e16beb665705c5996f4089604138` 与 `fb848531e804eb8a21cd9c8b9540d1f7e72a2c56ce726e4febe3e834474a3026`。FULL01 仍是 272 个文件。离线审计原件抽查一致。

## 指标

新条件相对 FULL01 Oracle。Wilson 区间是 95%。配对区间是 13 个家族、2000 次、seed `20261029` 的新条件减 FULL01 Oracle。

| 指标 | 新条件 | FULL01 Oracle | 差值区间 |
| --- | --- | --- | --- |
| S1 Recall | 4/12 = 0.333，Wilson 0.138–0.609 | 5/12 = 0.417，Wilson 0.193–0.680 | −0.385–0.182 |
| S2 Recall | 6/15 = 0.400，Wilson 0.198–0.643 | 5/15 = 0.333，Wilson 0.152–0.583 | 0.000–0.214 |
| S3 Recall | 5/13 = 0.385，Wilson 0.177–0.645 | 4/13 = 0.308，Wilson 0.127–0.576 | −0.250–0.300 |
| 总体 Recall | 15/40 = 0.375，Wilson 0.242–0.530 | 14/40 = 0.350，Wilson 0.221–0.505 | −0.103–0.116 |
| Clean FPR | 6/40 = 0.150，Wilson 0.071–0.291 | 4/40 = 0.100，Wilson 0.040–0.231 | 0.000–0.132 |
| HN FPR | 5/40 = 0.125，Wilson 0.055–0.261 | 2/40 = 0.050，Wilson 0.014–0.165 | −0.059–0.209 |
| Precision | 0.577（15/26），Wilson 0.389–0.745 | 0.700（14/20），Wilson 0.481–0.855 | 未单列 |

Poison 最终 SUPPORT：新条件 15，对照 19。三态：新条件 SUPPORT 72、CONTRADICT 26、INSUFFICIENT 22；对照 83、20、17。严格三元组两边都是 8/40。历史 HN 共 11 条：新条件 CONTRADICT 3、SUPPORT 7、INSUFFICIENT 1；对照 SUPPORT 10、CONTRADICT 1。

输入失败两边都是 0。JSON 失败：新条件 3，对照 5。引用失败：新条件 16，对照 12。模型自身 INSUFFICIENT：新条件 3，对照 0。输出失败合计：新条件 19，对照 17。120 条都在 EOS 停止，没有一条截断到 1024 token。

配对：新增检出 4，丢失检出 3，新增误报 6，消除误报 1。最终判决从 FULL01 Oracle 到新条件：SUPPORT→SUPPORT 66，SUPPORT→CONTRADICT 9，SUPPORT→INSUFFICIENT 8，CONTRADICT→CONTRADICT 16，CONTRADICT→INSUFFICIENT 4，INSUFFICIENT→SUPPORT 6，INSUFFICIENT→CONTRADICT 1，INSUFFICIENT→INSUFFICIENT 10。没有 CONTRADICT→SUPPORT。

## 成本

模型调用 120。输入 token 510139，对照 465859。输出 token 21390，对照 21735。生成 863.32 秒。峰值 reserved 21657288704 字节，allocated 18651179520 字节，低于 30 GiB 上限。没有 OOM、身份失败或后端回退。

## 仍未知

总体 Recall 的配对区间跨过 0，Clean FPR 区间的下沿是 0。点估计不是统计结论，也不是泛化结论。Poison 错误 SUPPORT 从 19 降到 15，同时弃权和误报都增加。更多弃权不是事实核验提升。另一段指令、F5 或正式测试都没有做，也不从这次负向权衡自动开始。

私有归档 SHA256 `62a1f7ff35ce1df39865b4280a51780636f8a21d6baf318fa2444c3d4480cce7`，841374 字节。私有索引 SHA256 `011e3f96ca1b624cb679929172816c6e25020dae0907e63e8b1b2eb8540111d3`，140 个工作目录文件。二者留在本机，不进入 Git。
