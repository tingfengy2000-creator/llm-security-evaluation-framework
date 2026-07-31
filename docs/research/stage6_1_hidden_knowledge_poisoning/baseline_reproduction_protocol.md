# Paper 1 Baseline Reproduction Protocol

## 1. 状态

- 协议类型：`PLANNING_ONLY`。
- 当前状态：`DRAFT_FOR_HUMAN_ACCEPTANCE`。
- 正式实验：`NOT STARTED`。
- 下列命令均为 `REFERENCE_ONLY_DO_NOT_RUN`。

本协议不授权下载数据/模型、安装环境、调用 API、生成攻击样本或运行论文结果。

## 2. 结果分栏

任何未来结果表必须有三组不可替换的列：

```text
Published Result | Reproduced Result | Our Method Result
```

每个单元格同时绑定 `source`, `git_commit`, `dataset_hash`, `config_hash`, `environment_fingerprint`,
`run_id`, `metric_definition`, `status`。失败运行保留为 `FAILED / INVALID RUN`，不得删除后只留下成功数字。

## 3. 分阶段门

### R0：许可与源码冻结

- 固定官方 paper URL、repo URL、commit/tag 和 LICENSE。
- 对缺失 LICENSE 的 GMTP/SafeRAG 发起作者确认或法律审查。
- 确认数据与模型条款。
- 找到 paper-result commit；当前默认分支 HEAD 不能自动代替。

通过条件：全部 artifact 可依法用于计划范围，且 commit 身份无歧义。

### R1：Original Environment 复原说明

- 原样记录论文/README 环境，不立即安装。
- 生成 dependency inventory、模型 revision inventory 和已知失效依赖列表。
- 不修改算法、数据、预算、Retriever、Top-K 或指标。

### R2：RTX 5090 Compatibility Environment

- 在 WSL/Linux 优先建立独立环境。
- 只做为 Blackwell 兼容所必需的 PyTorch/CUDA/FAISS/Pyserini patch。
- 每个 patch 记录 old/new version、原因、影响分析和验证。
- 若 patch 改变数值语义或模型，停止并提交 blocker，不继续出结果。

### R3：Engineering Smoke

- 最小公开样本、debug mode、无付费 API。
- 只证明加载、索引、一次检索/过滤和指标代码可运行。
- 状态只能是 `ENGINEERING_SMOKE`。

### R4：Formal Reproduction

需要项目负责人单独批准；必须使用冻结的数据、预算、Retriever、Top-K、模型和指标，多次运行并保存 manifest。

### R5：Our Method Comparison

只有 R4 通过且 strict-comparison eligibility review 通过后才能启动。

## 4. 官方参考命令

### PoisonedRAG

```bash
# REFERENCE_ONLY_DO_NOT_RUN
conda create -n PoisonedRAG python=3.10
conda activate PoisonedRAG
pip install beir openai google-generativeai
pip install torch==1.13.0+cu117 torchvision==0.14.0+cu117 torchaudio==0.13.0 \
  --extra-index-url https://download.pytorch.org/whl/cu117
python prepare_dataset.py
python run.py
```

风险：旧 CUDA/PyTorch 不应直接作为 RTX 5090 可运行环境；`run.py` 使用后台 `nohup`，worker 适配 Windows/WSL
时必须保留日志、退出码和进程归属。

### GMTP

```bash
# REFERENCE_ONLY_DO_NOT_RUN
docker build -t gmtp .
docker run --rm --gpus all -it -v "$(pwd):/app" -w /app gmtp
bash scripts/run_convert_dataset.sh
bash scripts/run_convert_poisoned_dataset.sh
bash scripts/run_faiss_indexing.sh
bash scripts/run_get_avg_mask_probs.sh
bash scripts/run_main.sh
```

README 写作 `donwload_datasets.py`，仓库实际为 `download_datasets.py`。这是待记录的 documentation patch。

### SafeRAG

```bash
# REFERENCE_ONLY_DO_NOT_RUN
pip install -r requirements.txt
milvus-server
python quick_start_nctd.py \
  --retriever_name bm25 \
  --retrieve_top_k 6 \
  --filter_module off \
  --model_name gpt-3.5-turbo \
  --quest_eval_model deepseek-chat \
  --attack_task SN \
  --attack_module indexing \
  --attack_intensity 0.5
```

风险：该 quick start 会涉及外部 API；没有单独批准、密钥隔离和成本上限时不得执行。

## 5. Run Manifest 最低字段

```text
run_id
run_type
paper
repository_url
git_commit
local_patch_commit
working_tree_clean
os
wsl_distribution
nvidia_driver
gpu
cuda_runtime
pytorch
python
cpu
ram
disk_free_before_after
model_id_and_revision
dataset_id_version_hash_license
attack_method_and_budget
retriever_and_revision
embedding_model_and_revision
top_k_candidate_and_final
generator_and_revision
metric_definitions
random_seeds
command
dependency_lock_hash
config_hash
status
raw_log_hashes
claims_supported
claims_not_supported
```

## 6. 失败与比较规则

- 无 LICENSE、无数据权限、无 paper-result commit：`BLOCKED`。
- 旧二进制不能运行且兼容 patch 改变算法：`BLOCKED`。
- API 模型版本不可恢复：可以建立现代近似轨道，但不得称严格复现。
- 只有 smoke 成功：`ENGINEERING_SMOKE`，不得填入 Reproduced Result。
- 数字和论文不一致：先检查数据、预算、Retriever、Top-K、指标和模型，不得直接写“实现错误”或“SOTA 提升”。

## 7. 5090 Worker Checklist

1. 安装 Git 与 WSL2/Linux；登记版本。
2. clone `research/stage6-1-hidden-poisoning`，确认 HEAD 与批准的 manifest commit 完全一致。
3. 确认 working tree clean；不得在 worker 自行改研究协议。
4. 采集 OS、WSL、driver、GPU、CUDA、PyTorch、Python、CPU、RAM、disk。
5. 建立 Original Environment 文档和独立 Compatibility Environment，不混用。
6. 先执行无模型/小样本依赖与 import probe。
7. 再执行显存、RAM、disk 和模型加载 probe。
8. 任何 patch 只提交报告给本机 Control Plane 决策。
9. 大型 dataset/model/index/raw log 不进入 Git。
10. 未收到 formal run approval 前停止。
