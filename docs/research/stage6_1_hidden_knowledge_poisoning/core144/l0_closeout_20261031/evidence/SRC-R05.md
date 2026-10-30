# L0 R05 显式展开 GQA 后的 efficient SDPA 预检

任务 `P1-L0-R05-EXPLICIT-GQA-EFFICIENT-SDPA-PRECHECK-01`。工作目录 `VACE-L0-D1-20261030-R05-PRECHECK` 只在本机。没有新的 PODR 或 Owner 决定编号。代码基线是 `71b0b111591b9c2a621a78995c72bad0ed860bbd`。模型、权重、tokenizer、prompt、parser、bf16、确定性、30 GiB 预留上限和完整证据都保持冻结。没有下载、安装、量化、CPU offload 或截断。

状态：**R05_PRECHECK_BLOCKED / OWNER_REVIEW_REQUIRED**。没有启动 D1 预测、评分、R06、VACE-LM 或 D2/D3。

## 1. 测到的结果

显式按头连续重复 7 次后，float32 math 与原生 GQA math 的差是 0。bf16 efficient 对展开 math 的 max_abs 最大为 0.0078125，落在比较前固定的 0.02 窗口内。

模型 prefill 与 decode 都走了适配器。持久 cache 保持 4 头。CUDA kernel 是 `PyTorchMemEffAttention` 的 `fmha_cutlassF_bf16_aligned_64x128_rf_sm80`。没有 math softmax，没有 flash，没有 cuDNN attention。第一次自动布尔值是 false，因为 dispatcher 算子自己没有 kernel；这个误判保留在原 JSON，没有改数值门后重跑。

同一虚构输入的两次完整生成 token 序列相同。

合成输入 26493 token 加 1024 个新 token，冷启动峰值预留 21281898496 字节，相对 30 GiB 余量 10930356224 字节。8192 与 16384 同样在合同内。`min_new_tokens=1024` 只属于这次容量测试。240 包的长度是 1294–26493，都落在这个长度包络里。没有逐包预测。

## 2. 为什么停

长短交替且不调用 `empty_cache` 时，预留从 15416164352 升到 17437818880，短输入再跑一次后保持不变。增长是 1928 MiB，超过预先固定的 512 MiB 阈值。峰值仍远低于 30 GiB。没有放宽阈值，也没有重跑。

R01、R02 的 HARD_STOP 和 R03 的 COMPLETE、CONFIG_LOCK，以及 R04 报告，运行前后哈希不变。R03 的本地完成记录没有在这里重写或补充分数。R04 仍只在本机。
