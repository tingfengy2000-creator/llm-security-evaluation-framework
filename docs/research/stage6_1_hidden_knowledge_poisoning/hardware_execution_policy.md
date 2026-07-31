# Paper 1 Hardware and Dual-Machine Execution Policy

## 1. 机器角色

### 本机：CONTROL_PLANE

负责 Git 主控、研究问题、taxonomy、标签与数据治理、实验协议、配置、Run Manifest、结果汇总和提交。

### 5090：COMPUTE_WORKER

负责论文源码复现、GPU 环境、Embedding、索引、GMTP/PoisonedRAG/SafeRAG 的经批准运行，以及后续训练和推理。
5090 不是第二个项目控制面；发现协议问题时只输出报告，不自行改研究定义。

## 2. Git 与数据边界

- 源码同步只使用 GitHub。
- 正式运行必须满足：worker HEAD = Run Manifest `git_commit`。
- branch 固定为 `research/stage6-1-hidden-poisoning`，working tree 必须 clean。
- dataset、model、vector index、raw log 不进入 Git。
- Git 只保存 config、manifest、source、small metric summary、redacted report 和 hashes。
- baseline tag 不得移动或重建；本轮核验未发现 `s6-t5-rag-baseline-v1`，保持 `TO_VERIFY`。

## 3. 原环境与兼容环境

每项复现必须同时维护两列：

| 列 | 含义 |
| --- | --- |
| Original Paper Environment | 作者论文/仓库明确记录的环境，不做现代化改写 |
| RTX 5090 Compatibility Environment | 为 Blackwell 可运行性建立的独立环境，逐项记录 patch |

兼容迁移不得改变算法、数据、attack budget、Retriever、Top-K、指标或静默替换模型。

NVIDIA 的 [Blackwell Compatibility Guide](https://docs.nvidia.com/cuda/blackwell-compatibility-guide/) 说明：
只有包含兼容 cubin/PTX 的 CUDA 应用才能运行，否则必须重建；NVIDIA 的
[CUDA architecture matrix](https://docs.nvidia.com/datacenter/tesla/drivers/latest/cuda-toolkit-driver-and-architecture-matrix.html)
记录 Blackwell 的首个 CUDA Toolkit 原生支持是 12.8。当前计划因此把 PoisonedRAG 的 CUDA 11.7 / PyTorch 1.13
和 GMTP 的 CUDA 12.4 / PyTorch 2.5.1 都视为待实测的旧二进制环境，而不是可直接运行的 5090 环境。

## 4. 资源规划

下表是 Control Plane 容量规划，不是作者报告或实测结果。

| Baseline | 作者 GPU | 5090 VRAM 规划 | RAM 规划 | Disk 规划 | 主要风险 |
| --- | --- | --- | --- | --- | --- |
| PoisonedRAG | `NOT REPORTED` | 16-32 GB，取决于本地 generator；API 轨道更低 | 32-64 GB | 150-300 GB | 旧 torch/cu117；百万级 corpus/index；API/model drift |
| GMTP | 单卡 A6000 48 GB | 24-32 GB 起步，必须实测 peak；A6000->5090 不保证等价 | 64 GB | 250-500 GB | 3 个百万级 corpus、多个 FAISS index、梯度+MLM、FAISS/Pyserini/Java |
| SafeRAG | H800 | API/default小模型轨道可尝试；13B/14B FP16 不能假设 32 GB 足够 | 64-128 GB | 30-100 GB | H800->5090、Milvus、未锁 torch、API 与本地模型矩阵 |

估计依据：论文记录的 corpus 数量、模型规模、索引类型和仓库流程。任何论文结果前必须由 worker 用实际数据版本
记录 peak VRAM、peak RAM 和 disk before/after。

## 5. 5090 Blackwell 检查

```text
nvidia-smi
driver version
CUDA runtime reported by torch
torch version and build suffix
torch.cuda.get_device_name()
torch.cuda.get_device_capability()
minimal tensor kernel
FAISS GPU import/search
Pyserini + Java 21 import/search
transformers model load
forward pass
backward/gradient pass for GMTP
peak allocated/reserved VRAM
peak process RAM
disk before/after index
```

旧应用可使用 `CUDA_FORCE_PTX_JIT=1` 做兼容性诊断，但这只判断是否包含 PTX，不证明论文数值可复现。

## 6. 需要 5090 实测的项目

1. PoisonedRAG torch 1.13/cu117 是否立即失败，以及最小兼容升级集合。
2. GMTP 的 PyTorch 2.5.1/cu124、`faiss-gpu-cu12`、Pyserini 0.43.0 与 Java 21 组合。
3. DPR/Contriever + BERT/RoBERTa MLM 的单 query 与 batch peak VRAM。
4. 三个 BEIR corpus 的真实下载、解压、索引容量与耗时。
5. SafeRAG Milvus-lite 在 WSL/Linux 的可重复启动、索引与清理。
6. Qwen 14B、Baichuan 13B、ChatGLM 6B 的加载策略；任何量化都属于显式配置差异。
7. API-only 与 local-generator 轨道的协议等价性。

## 7. 停止条件

- HEAD/manifest 不一致；
- working tree 不 clean；
- 许可未解决；
- 数据或模型 revision 不可确认；
- compatibility patch 改变算法或指标；
- 资源超过批准预算；
- 将 smoke 结果误写为 formal result。

触发后 worker 保存脱敏日志和 blocker 报告，停止运行，由 Control Plane 决策。
