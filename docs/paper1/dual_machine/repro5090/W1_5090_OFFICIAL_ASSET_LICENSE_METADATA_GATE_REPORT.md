# W1 5090 官方资产与许可准入

状态：`PARTIAL_METADATA_BLOCKED`。任务 `P1-RAGDEFENDER-5090-OFFICIAL-METADATA-GATE-01`，活动 `W1-5090-OFFICIAL-METADATA-20261105-01`。
Owner 授权 `W1-OD-20261105-5090-ASSET-GATE-07`。这是元数据核验，不是实验。三个 Claim 都是 `NOT_RUN`。无防御 ASR、有防御 ASR 和问答准确率都是 `NOT_MEASURED`。新增模型和 BEIR 下载为 0。付费 API 为 0。

## 1. 启动

分支 `research/paper1-ragdefender-repro-5090` 在执行前干净，落后远端 5 个治理提交，已 `git pull --ff-only` 到 `1cb3445d2815815684e839e9f7564656c05dae82`。没有碰 5060，也没有 merge。
上游仍是 `ba2a17efba165d45409114df2d70b030ade1e1b8`。作者源码没有改。
风险审查：本轮只允许小型公开 JSON、HTML 和文本，以及不带正文的 HEAD。脚本拒绝了对权重和 zip 的 GET。Windows 对 BEIR 的 HEAD 因证书失败，随后只用 WSL 对同一官方 URL 做了 HEAD。Llama 的逐文件树请求 TLS 中断，没有改用镜像。

## 2. 许可结论

Owner 自己要做的步骤在 [手动操作](official_asset_gate/OWNER_MANUAL_LICENSE_ACTIONS.md)。全部接受状态是 `NOT_ACCEPTED/UNKNOWN`。

Llama 2 的修订 `f5db02db724555f92da89c216ac04704f23d4590` 已由模型 API 再次核对，门禁类型是 manual。公开许可文本已取到。模型仓库里的 `LICENSE.txt` 返回 401。
Vicuna 修订 `236eeeab96f0dc2e463f2bebb7bb49809279c6d6` 的模型卡写非商业，并写明来自 Llama 1。FastChat 的 Apache-2.0 只是代码许可。
Contriever 修订仍是 `2bd46a25019aeea091fd42d1f0fd4801675cf699`。代码 LICENSE 是 CC BY-NC 4.0，模型卡没有 license 字段，所以权重许可保持 `UNKNOWN`。
MiniLM 的正式仓库是 `sentence-transformers/paraphrase-MiniLM-L6-v2`，修订 `c9a2bfebc254878aee8c3aca9e6844d5bbb102d1`，模型卡为 apache-2.0。它不是 `all-MiniLM-L6-v2`。
BEIR 代码是 Apache-2.0，而且 README 写明这不表示用户已经获得数据许可。HotpotQA 数据集 README 写 CC BY-SA 4.0。NQ 和 MS MARCO 的数据许可在本次读到的 README 里没有出现。

## 3. 体积与 Claim

逐项字节、冗余文件和硬停在 [资产矩阵](official_asset_gate/OFFICIAL_ASSET_METADATA_MATRIX.json)。BEIR 压缩长度和 ETag 已用 HEAD 复核，解压体积是 `UNKNOWN`，见 [语料边界](official_asset_gate/BEIR_LICENSE_AND_UNPACK_BOUNDARY.json)。
Claim 1 仍是 24 格，Claim 2 和 Claim 3 仍是各 6 格且只有 100%。Tan 目录差和表 7 的缺失参数都再次定位，没有改源码。见 [静态审计](official_asset_gate/CLAIM_STATIC_SIDE_EFFECT_AUDIT.md)。
盘符见 [缓存预检](official_asset_gate/DRIVE_CACHE_PATH_PREFLIGHT.md)。C 的用户 TEMP 和现有 HF 缓存没有搬动。
下一批全部 `NOT_APPROVED`，见 [审批包](official_asset_gate/BATCHED_REPRO_OWNER_APPROVAL_PACK.md)。

原始访问日志在 Git 外，SHA-256 `5d99fc412406e8dcb90815008f78eb2cb1302f8f1fbc59fac20242b1952c473c`。脱敏索引是 [访问日志](official_asset_gate/OFFICIAL_SOURCE_ACCESS_LOG.json)。

## 4. 文档收口

- human_ledger_checked = true；human_ledger_updated_if_required = true
- agent_ledger_checked = true；agent_ledger_updated = true
- current_work_state_updated = true
- execution_log_appended = true
- experiment_master_condition_evaluated = true；没有实测，不追加 OR
- owner_decision_condition_evaluated = true；授权已在 `W1-OD-20261105-5090-ASSET-GATE-07`，本轮不新编 PODR 编号
- stage_process_condition_evaluated = true；不是新的 Stage 6.1 试点，不改
- lessons_condition_evaluated = true；许可缺口留在本报告，不单独立成跨论文方法学
- research_authority_condition_evaluated = true；冻结合同未改
- readme_condition_evaluated = true；导航入口未改

完成后停止。不自动下载，不自动跑单格或三条 Claim。
