# L0-F5 / L0-Oracle停在虚构合成语义门，D1未测量

**L0-F5：NOT_EXECUTED；L0-Oracle：NOT_EXECUTED。S1/S2/S3、Recall、FPR、Precision、弃权率、三元组和区间均未测量，不能填0或沿用V03。**
2026-10-29 JST；Task `P1-VACE-L0-F5-ORACLE-STRONG-BASELINE-01`；Run `VACE-L0-D1-20261029-R01`；PODR-151 / OR-107 / REL-2026-0122。
这是5090 Worker的真实硬门停机，不是强基线成绩，也不是提示词修订建议。

## 1. Issue ID

`L0-SYNTHETIC-SEMANTIC-GATE-BLOCKER-01`。

## 2. 问题名称

官方Qwen2.5-7B已在指定RTX5090上加载，虚构合成门5题中SYN-3判决与冻结期望不一致，脚本按硬门停止。D1的240条没有开始。

## 3. 发现阶段 / 任务

设备、隔离依赖、官方模型hash、配置冻结和模型加载均已通过。失败发生在D1之前的虚构合成语义门。
执行源码固定 `a83437ab0a685d69114093fd4bd0e6ab22f354aa`（detached worktree）。记录提交时研究分支先端为后续纯文档提交 `9831d62`，实验没有改用该先端。
5090本机证据目录 `D:\paper1\VACE-L0-D1-20261029-R01` 含权重、私有输入、合成门全文和日志；`experiments/` 被忽略，这些原文不进Git。本文件是给5060控制面的Git事实记录。

## 4. 事实分类

| 类型 | 事实 |
| --- | --- |
| OBSERVED_FACT | `nvidia-smi` 仅GPU0 NVIDIA GeForce RTX 5090，32607 MiB，驱动610.88。主机名DESKTOP-B5PNBNC |
| OBSERVED_FACT | 只读预检退出码0，状态 `NEEDS_ISOLATED_SETUP`。任务目录内新建隔离venv，未改全局或驱动 |
| OBSERVED_FACT | `ENV_READY.json`：`CUDA_KERNEL_PASS`；Torch 2.8.0+cu128，CUDA 12.8，Transformers 4.57.1，Accelerate 1.10.1，NumPy 2.2.6，Safetensors 0.6.2；Python 3.13.9；算力(12, 0)；`isolated=true` |
| OBSERVED_FACT | 模型 `Qwen/Qwen2.5-7B-Instruct` revision `a09a35458c702b33eeacc393d103063234e8bc28`。四份权重SHA256与仓库清单一致：`a1333e62…aba7`、`f5d25a27…6185`、`8efdec4c…bfd5`、`1a72d403…879bd` |
| OBSERVED_FACT | 加载为bfloat16、SDPA、device_map仅GPU0、`max_position_embeddings=32768`、确定性算法开启。加载后空闲/总显存17120100352/34190458880。无CPU offload |
| OBSERVED_FACT | 合成门 `all_pass=false`。SYN-1/2/4/5判决等于期望；SYN-3期望`SUPPORT`、解析判决`CONTRADICT`、`error=null`。SYN-1贪婪重复的原文与第一次相同 |
| OBSERVED_FACT | 推理子进程09:45:59Z–09:46:38Z，退出码1，异常 `SYNTHETIC_GATE_FAIL_NO_PROMPT_TUNING`。编排器随后退出码1 |
| OBSERVED_FACT | `D1_not_loaded_yet=true`；`raw/` 为0个文件；无 `PREDICTION_LOCK.json`、`COMPLETE.json` 或 `L0_RETURN_NO_WEIGHTS.zip` |
| SOURCE_DERIVED_FACT | PODR-151允许普通阶段连续执行，但合成语义门失败必须保存INCIDENT后停止，不得改prompt/解析器追通过，也不得自动重跑 |
| INFERENCE | 本次不能解释成5090不存在、CUDA kernel失败、权重hash错误或D1检出率低 |
| UNKNOWN | 若将来更换合成门定义会得到什么D1分数。当前没有这个授权，也不预测 |

SYN-3的判决键是`CONTRADICT`，理由正文却称2010年版陈述与证据一致、并不矛盾。门只比较判决与冻结期望，因此整门失败。这不是JSON解析失败。

## 5. 受影响约束

合成语义门、冻结源码/模型/提示词，以及“失败后不追通过”。D1_DEV40组120条13家族、8组24条HOLD、F5/Oracle同条件、先封存后评分仍然有效，但本轮没有进入封存。

## 6. 为什么必须现在处理

`HARD_STOP.json` 已存在。同一工作目录再启动会被脚本拒绝为 `PRIOR_HARD_GATE_FAILURE_REQUIRES_OWNER_DECISION_NO_AUTORETRY`。5060若不收到这份记录，会继续以为Worker尚未启动。

## 7. 下游风险

工程：工作目录保留约24GiB限额内的环境与官方权重，不能当垃圾删除后静默重跑。实验：没有240条预测，不能与V03比较。论文：不得把合成门失败写成D1 Recall，也不得把SYN-1至SYN-5的通过题写成模型已具备事实核验能力。复现：源码、权重、依赖和生成配置已冻结在本机 `CONFIG_LOCK.json`，Git只保存其身份摘要。

## 8. Owner选项

### A. 接受本次硬停，维持协议不变（与现合同一致）

两条件继续NOT_EXECUTED。不改prompt、解析器、证据或模型，不删除 `HARD_STOP.json` 后重跑。

### B. 另行批准新的合成门或新Run（本记录不批准）

只有新的Owner决定才能改变门或开启新的Run ID。不能把该决定推断为本文件已授权。

### C. 保持暂停并只审阅本记录

5060用本文件核对身份；完整合成门JSON和stderr留在5090工作目录，不把权重、标签、候选或raw推上Git。

## 9. Worker建议

采用A/C。本轮不改代码、不重跑、不补D1分数。D2/D3分工与数据门不变。

## 10. 理由与确定性

判决不等与期望是合成门文件中的直接字段，确定性高。D1性能没有测量，确定性同样高。不对SYN-3做事后解释来改规则。

## 11. 本机证据身份（原文不入库）

| 文件 | SHA256 |
| --- | --- |
| CONFIG_LOCK.json | b8eddcaef02b50dbab201a2ceb8d39caa6c57a9136e273c6a79f8e72be01da58 |
| ENV_READY.json | 3879877583d9b4bab2788b9b3e69c11128ba21e355154b15339d9bb9a0d8a3ed |
| GPU_LOAD_RECEIPT.json | ce3c032945f73f0e34982b9a3bdead2dd6c2c7e7c29c24fada231f73698d4e35 |
| SYNTHETIC_GATE.json | 2d625ba6d7078fd0bd59c5090a9fcf9641138731ae8f998adff0a307c921b654 |
| HARD_STOP.json | 67152d26f9708b98e4ff7870897c0fe4f84a2675ff8a355e1813c1ef983d0629 |
| logs/infer-1793267159843561800.stderr.txt | 664e21af610c13ef3f5a9a7a553889d0c3c0166cf0845c4a3d335fe4155c58d5 |

依赖冻结SHA256 `b0ef38f3b78c36eb4451aa164bcfeb19841c7e49badf1c82b63b3e5e6609f005`。私有ZIP仍为2,204,548字节，SHA256 `03fae845b50d669373d3b08776caf5a1b2cf068ea7aa5b60dea89a65177e3eb2`；bundle manifest `a7e05d2ebedbc68abc21fff46a0ad1597747712020957ac30cf1445353714a60`。

## 12. 状态

`L0_STRONG_BASELINE_SYNTHETIC_GATE_BLOCKED / HUMAN_DECISION_REQUIRED`。不是 `L0_STRONG_BASELINE_D1_DEV_COMPLETE`。无正式GT/split、训练或VACE-LM。
