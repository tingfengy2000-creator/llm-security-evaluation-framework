# L0 R02停在D1推理显存硬门，没有检测率

**L0-F5：NOT_EXECUTED；L0-Oracle：NOT_EXECUTED。S1/S2/S3、Recall、FPR、Precision、弃权率、三元组和区间均未测量，不能填0。**
2026-10-29 JST；Run `VACE-L0-D1-20261029-R02`；源码 `a31ade51c2e6923991b81895163060b80db6da4f`；PODR-153 / OR-109 / REL-2026-0124。
这是工程硬停，不是R01恢复成功，也不是D1成绩。

## 1. 已完成的批准步骤

只读预检打印 `R02_CHECK_ONLY_PASS_NO_NEW_MODEL_OR_DEPENDENCY`。同一冻结解释器、官方Qwen目录和R01输入被接受，没有下载或安装。
R02合成门：`engineering_all_pass=true`，`semantic_correct=4/5`，`semantic_all_pass=false`，`all_pass=false`，`execution_gate_passed=true`，贪婪重复原文一致。语义不准按PODR-153只作诊断，没有改判决或期望。

## 2. 停止事实

F5新预测写下 `L0-F5-000.json` 至 `L0-F5-004.json` 后，下一次 `model.generate` 抛出 `torch.OutOfMemoryError`。
GPU 0 总容量 31.84 GiB，当时空闲 2.01 GiB；PyTorch已分配 27.73 GiB，合同允许上限 30.00 GiB；本次尝试再分配 12.21 GiB。
注意力仍是SDPA。没有设置分配器环境变量，没有量化、CPU offload或换模型。
Oracle 0条。无 `PREDICTION_LOCK.json`、`COMPLETE.json` 或 `L0_RETURN_NO_WEIGHTS.zip`。

## 3. 两个门都保留

R01 `HARD_STOP.json` SHA256仍是 `67152d26f9708b98e4ff7870897c0fe4f84a2675ff8a355e1813c1ef983d0629`。
R02新 `HARD_STOP.json` SHA256 `88c2f00fc70a81d54e72774833ac985afcd3c4c296d7987e5fd59422d4c83b71`。
R02合成门 SHA256 `c970884b79927b08d7310f74cf574260755f9efa47a30630db9bff70a7f5d627`。
推理stderr SHA256 `ff87900a49380477f2a7f55ef88b772fa4c6c7b180612da4f72bcbf73decadb2`。
两份门都没有删除。脚本会拒绝在R02硬停之后自动重跑。

## 4. 状态

`L0_STRONG_BASELINE_R02_CUDA_OOM_BLOCKED / HUMAN_DECISION_REQUIRED`。
不是 `L0_STRONG_BASELINE_D1_DEV_COMPLETE`。无正式GT/split、训练或VACE-LM。D2/D3未改。权重、标签、逐样本raw和回传包不在Git。
