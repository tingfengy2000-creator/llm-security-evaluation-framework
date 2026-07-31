# Paper 1 Baseline Reproduction Protocol

> Machine roles, Git context sync and worker fail-closed preflight are governed by
> [Dual-Machine Execution Policy](../../governance/dual_machine_execution_policy.md).
> The authoritative S6.1-R0 order and boundaries are defined in
> [S6.1-R0 Reproduction Preflight](s6_1_r0_reproduction_preflight.md).

## 1. 状态

- 协议类型：`ENGINEERING_PREFLIGHT_CONTROL / FORMAL_REPRODUCTION_PLANNING`。
- 当前状态：`R0_I_RETURNED_FOR_WORKER_CORRECTION / FORMAL_REPRODUCTION_NOT_APPROVED`。
- 历史执行状态：`R0_ENGINEERING_PREFLIGHT_APPROVED`。
- 正式实验：`NOT STARTED`。
- 下列上游命令均为 `REFERENCE_ONLY_DO_NOT_RUN`；Worker 必须先做静态审计，再从中提取最小 smoke 所需命令，不得整段盲跑。

当前只允许 RTX5090 完成 R0-I review 明确列出的最小证据修正；历史 R0 工程执行授权不再允许扩大环境探索。它不授权下载完整 NQ、HotpotQA、MS MARCO、完整索引或其他大型语料，不授权付费 API、API key、未经批准的大型 LLM，也不授权生成或声称 Paper Result。若未来最小 smoke 确实需要更多数据，必须先提交 `MINIMUM_DATA_REQUIREMENT`。

### 1.1 License / Access 分层

每个外部 baseline 必须分别记录 `SOURCE_ACCESS`、`INTERNAL_REPRODUCTION`、
`STRICT_COMPARISON_ELIGIBILITY`、`REDISTRIBUTION_ELIGIBILITY`、`CODE_LICENSE` 与
`DATASET_LICENSE`。公开可访问不等于可无限再分发；未确认代码许可证不自动阻断未来经批准的内部研究 clone/inspect/install/execute/evaluate。明确的 upstream 条款始终必须遵守。本协议不提供法律结论。

## 2. 结果分栏

任何未来结果表必须有三组不可替换的列：

```text
Published Result | Reproduced Result | Our Method Result
```

每个单元格同时绑定 `source`、`git_commit`、`dataset_hash`、`config_hash`、
`environment_fingerprint`、`run_id`、`metric_definition`、`status`。失败运行保留为
`FAILED / INVALID RUN`，不得删除后只留下成功数字。

## 3. 分阶段门

### R0-A：Environment Fingerprint

- RTX5090 拉取最新 Control Plane 提交并确认 branch、HEAD、upstream、remote 与批准锚点一致，working tree clean。
- 记录 OS、WSL、driver、GPU、driver CUDA capability、PyTorch CUDA runtime、Python patch、CPU、RAM 与 disk。
- `llmguard-paper1` 缺少 NumPy 时，可最小安装并记录 resolved version；不得借此批量安装 baseline 依赖。

### R0-B：PoisonedRAG Static Audit

- 冻结 paper、repository、commit/tag、license、原始依赖、数据、模型、API 与入口命令。
- 记录 `ORIGINAL_PAPER_ENV`，但不把旧 CUDA/PyTorch 组合直接安装进主环境。

### R0-C：PoisonedRAG Minimal Smoke

- 仅使用静态审计后确认的最小公开样本与必要小模型。
- 在独立 `poisonedrag-compat` 环境中执行；每项必要变更写入 `COMPATIBILITY_PATCH RECORD`。
- 只可形成工程 smoke 与资源测量，不得形成 Paper Result。

### R0-D：GMTP Static Audit

- 冻结 source identity、license、Original Environment、数据转换、索引、模型/API 和运行入口。
- 先确认 README 与实际脚本名等漂移，再决定 compat 版本。

### R0-E：GMTP Minimal Smoke

- 在独立 `gmtp-compat` 环境中执行经审计的最小公开样本路径。
- 记录 CPU、RAM、GPU、VRAM、disk、wall time、退出码与原始日志哈希。

### R0-F：SafeRAG Static Audit

- 冻结 source identity、license、Original Environment、selected task、Milvus/检索器、模型和外部 API 依赖。
- 若路径强制要求外部 API，记录 `EXTERNAL_API_REQUIRED` 并保持 fail-closed，不得使用密钥或付费调用。

### R0-G：SafeRAG Selected-Task Minimal Smoke

- 在独立 `saferag-compat` 环境中执行一个经审计、无需未经批准外部 API 的 selected-task 最小 smoke。
- 只验证工程可行性；不得扩展为全任务、全数据或正式比较。

### R0-H：Reproduction Feasibility Matrix

对三个 baseline 仅使用下列分类：

- `STRICT_REPRODUCTION_READY`
- `COMPATIBILITY_REPRODUCTION_READY`
- `PARTIAL_REPRODUCTION_READY`
- `BLOCKED_BY_EXTERNAL_DEPENDENCY`
- `BLOCKED_BY_HARDWARE`
- `BLOCKED_BY_MISSING_ARTIFACT`
- `BLOCKED_BY_API_DRIFT`
- `NOT_REPRODUCIBLE_WITH_AVAILABLE_EVIDENCE`

### R0-I：Control Plane Review

- RTX5090 通过 GitHub 提交最小证据与矩阵；LOCAL 仅审查证据、治理边界和声明。
- 若新事实可能改变 baseline 角色，必须单独触发 route review，不得在 R0 内自动改写角色。
- R0-I 不批准 R1，不启动 S6.1-P1，不改变 `FORMAL_EXPERIMENT = NOT STARTED`。

### R1：Formal Reproduction

需要项目负责人单独批准；必须使用冻结的数据、预算、Retriever、Top-K、模型和指标，多次运行并保存 manifest。R0 成功不等于 R1 已获批准。

### R2：Our Method Comparison

只有 R1 通过且 strict-comparison eligibility review 通过后才能启动，并仍需单独批准。

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

风险：旧 CUDA/PyTorch 不应直接作为 RTX 5090 可运行环境；`run.py` 使用后台 `nohup`，Worker 适配 Windows/WSL 时必须保留日志、退出码和进程归属。

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

风险：该 quick start 会涉及外部 API；没有单独批准、密钥隔离和成本上限时不得执行，并应记录 `EXTERNAL_API_REQUIRED`。

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
cuda_driver_capability
cuda_runtime
pytorch
python
cpu
ram
disk_free_before_after
model_id_and_revision_size_license
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
resource_measurements
raw_log_hashes
claims_supported
claims_not_supported
```

## 6. 失败与比较规则

- 无 paper-result commit：`STRICT_COMPARISON_IDENTITY_BLOCKER`。
- 明确的数据使用条款不允许计划用途：`DATASET_USE_BLOCKER`。
- 再分发许可未确认：`REDISTRIBUTION_ELIGIBILITY=TO_VERIFY`，不自动等同内部研究阻断。
- 旧二进制不能运行且兼容 patch 改变算法：`ALGORITHM_EQUIVALENCE_BLOCKER`。
- API 模型版本不可恢复：可以建立现代近似轨道，但不得称严格复现。
- 只有 smoke 成功：`ENGINEERING_SMOKE`，不得填入 Reproduced Result。
- 数字和论文不一致：先检查数据、预算、Retriever、Top-K、指标和模型，不得直接写“实现错误”或“SOTA 提升”。

## 7. 5090 Worker Checklist

1. 拉取 `research/stage6-1-hidden-poisoning` 最新 Control Plane 提交，确认 HEAD、upstream 与 remote 一致。
2. 确认 working tree clean；不得在 Worker 自行改研究协议。
3. 完成 R0-A fingerprint；明确区分 Windows/WSL driver、driver CUDA capability 与 PyTorch CUDA runtime。
4. 外部仓库仅放在 `~/paper1_external/`，不得 vendor 进 LLMGuard。
5. 主环境保持 `llmguard-paper1`；三个 baseline 使用独立 compat 环境，且版本只能在各自静态审计后选择。
6. 严格按 R0-A 至 R0-I 顺序执行，不得在同一 Python 环境并行安装三个 baseline。
7. 大型 dataset/model/index/raw log 不进入 Git；需要扩展时先提交 `MINIMUM_DATA_REQUIREMENT` 或模型资源记录。
8. Worker 提交证据后由 LOCAL Control Plane 完成 R0-I；未收到 formal run approval 前停止。
