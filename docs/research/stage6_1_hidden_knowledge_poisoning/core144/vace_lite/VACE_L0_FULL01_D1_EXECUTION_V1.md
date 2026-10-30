# L0 完整 D1 开发实验授权

任务 `P1-L0-D1-FULL-EXECUTION-01`。Run `VACE-L0-D1-20261030-FULL01`。Owner 批准用 R06 已通过的显式 GQA efficient 适配器做 240 条开发预测、封存、独立评分和归档。

批准基线是 `fdf77cff25158c731a3fdb2dde70a5ad27b0c77d`。适配器 SHA256 保持 `0cb1d1854ba90d94efa859e03a54f18b25999c4bcaf4c84ac9e43073128eb2d4`。R05 仍是阻断，R06 仍是通过，两份结论不改写。

本文件写在执行前。指标在运行封存前是 NOT_MEASURED，不能填 0。这是 D1 开发结果，不是正式测试、泛化或部署有效性。不启动 VACE-LM、D2/D3 或下一轮。

冻结条件：原 Qwen2.5-7B-Instruct、bf16、GPU-only、batch 1、seed 20261029、do_sample false、num_beams 1、确定性硬开关、TF32 关闭、max_context 32768、max_input 31744、max_new_tokens 1024、12 小时、30 GiB 预留上限。不带入容量测试的 min_new_tokens=1024，不继承 R03 的 7200 输入上限。不截断、不量化、不 CPU offload、不改分配器、不调用 empty_cache。reserved 相对冷启动的增长不再单独停机。

合成语义门继续只作诊断，工程身份失败仍然硬停。普通解析失败和模型给出的 INSUFFICIENT 按原策略留下并继续。
