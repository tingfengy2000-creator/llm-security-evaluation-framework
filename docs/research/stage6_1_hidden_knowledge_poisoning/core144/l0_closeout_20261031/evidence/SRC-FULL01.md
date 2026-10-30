# L0 完整 D1 开发实验授权

任务 `P1-L0-D1-FULL-EXECUTION-01`。Run `VACE-L0-D1-20261030-FULL01`。Owner 批准用 R06 已通过的显式 GQA efficient 适配器做 240 条开发预测、封存、独立评分和归档。

批准基线是 `fdf77cff25158c731a3fdb2dde70a5ad27b0c77d`。适配器 SHA256 保持 `0cb1d1854ba90d94efa859e03a54f18b25999c4bcaf4c84ac9e43073128eb2d4`。R05 仍是阻断，R06 仍是通过，两份结论不改写。

本文件写在执行前。指标在运行封存前是 NOT_MEASURED，不能填 0。这是 D1 开发结果，不是正式测试、泛化或部署有效性。不启动 VACE-LM、D2/D3 或下一轮。

冻结条件：原 Qwen2.5-7B-Instruct、bf16、GPU-only、batch 1、seed 20261029、do_sample false、num_beams 1、确定性硬开关、TF32 关闭、max_context 32768、max_input 31744、max_new_tokens 1024、12 小时、30 GiB 预留上限。不带入容量测试的 min_new_tokens=1024，不继承 R03 的 7200 输入上限。不截断、不量化、不 CPU offload、不改分配器、不调用 empty_cache。reserved 相对冷启动的增长不再单独停机。

合成语义门继续只作诊断，工程身份失败仍然硬停。普通解析失败和模型给出的 INSUFFICIENT 按原策略留下并继续。

## 封存结果

执行提交是 `830bb5b3eb950f30494c9e3ef6affdcc8efc7dcb`，它的祖先包含上面的批准基线。更早的 `b058601fd0ee4b68cb57ce85f5bbd9784e6bedea` 在写出运行目录前因目录参数遮住父检查模块而退出，没有 HARD_STOP，也没有预测。实际执行没有改代码、没有 pull。

状态是 `L0_D1_DEV_FULL_COMPLETE / OWNER_REVIEW_REQUIRED`。240 条新预测已封存并独立评分。合成语义仍是 4/5，工程门通过，不把已知的语义差异改写成通过。R05 仍阻断，R06 仍通过。

这是 D1 开发结果。下面的数字来自私有指标文件，正文、标签、逐条 raw 和私有归档不进 Git。

| 条件 | S1 | S2 | S3 | 总体 Recall | Clean FPR | HN FPR | Precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0-F5 | 3/12 = 0.250 | 0/15 = 0 | 2/13 = 0.154 | 5/40 = 0.125 | 1/40 = 0.025 | 1/40 = 0.025 | 0.714 |
| L0-Oracle | 5/12 = 0.417 | 5/15 = 0.333 | 4/13 = 0.308 | 14/40 = 0.350 | 4/40 = 0.100 | 2/40 = 0.050 | 0.700 |

判决：F5 为 SUPPORT 70、CONTRADICT 7、INSUFFICIENT 43。Oracle 为 SUPPORT 83、CONTRADICT 20、INSUFFICIENT 17。

Wilson 95%：F5 总体 Recall 0.055–0.261，Clean FPR 与 HN FPR 都是 0.004–0.129，Precision 0.359–0.918。Oracle 总体 Recall 0.221–0.505，Clean FPR 0.040–0.231，HN FPR 0.014–0.165，Precision 0.481–0.855。

13 家族、2000 次 bootstrap：F5 总体 Recall 0.028–0.231，Oracle 总体 Recall 0.171–0.542。Oracle 减 F5 的配对区间：总体 Recall 0.100–0.405，HN FPR −0.050–0.121，Clean FPR −0.059–0.209。F5 减历史 V03 的配对区间：总体 Recall −0.211–0.167。历史 HN 在 F5 上是 11 条里 INSUFFICIENT 8、SUPPORT 2、CONTRADICT 1；在 Oracle 上是 SUPPORT 10、CONTRADICT 1。严格三元组 F5 为 1/40，Oracle 为 8/40。

输入拒绝为 0。解析与引用校验失败：F5 有 1 条 JSON 和 39 条引用校验，Oracle 有 5 条 JSON 和 12 条引用校验。没有输出错误、由模型自己给出证据不足的条数：F5 为 3，Oracle 为 0。这些失败留在分母里，没有重跑。

model_called 为 240。输入 token 合计 2174399，输出 token 合计 45451。生成耗时合计 2517.82 秒。逐条峰值 reserved 的最大值是 31249661952 字节，低于 32212254720 的 30 GiB 上限。240 条都记录了 efficient 前向的 prefill 和 decode。

CONFIG_LOCK SHA256 `628cd01fe0a26e525b28d0ad2a70afd80ceab7708d12f2a9725ad31de065ba4d`。GenerationConfig SHA256 与 R01 相同，为 `2e667e6e68c069bac62b13dfb7359b6b8f0e6c96c3664f9af7db27b68521d542`。预测文件 SHA256 `be87b3fd4457ee212b43bf2f709ded476858e16beb665705c5996f4089604138`。PREDICTION_LOCK SHA256 `fb848531e804eb8a21cd9c8b9540d1f7e72a2c56ce726e4febe3e834474a3026`。私有证据索引 RETURN_INDEX SHA256 `f1d9751ece14aa70fdd28c029958dd55d94edca802d100ca59b6635948f73fd0`。私有归档 SHA256 `f5fd259601e9be80e616fdf765da84dbae8f17d40838fe3cc606b869f2e62562`。

不因这些分数修改 prompt、parser、数据或重跑。不启动 VACE-LM、D2/D3 或下一轮。
