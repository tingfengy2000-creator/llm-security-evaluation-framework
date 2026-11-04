# W1 5090：RAGDefender 主要结果复现准备

日期：2026-11-04。任务类型：`ARTIFACT_REPRODUCTION_PREPARATION / READ_ONLY_OFFLINE_ANALYSIS`。
这不是 Claim 执行许可，也不是基线复现完成。三个 Claim 都是 `NOT_RUN`。无防御 ASR、有防御 ASR 和问答准确率都是 `NOT_MEASURED`。

## 1. 上下文

本分支 `research/paper1-ragdefender-repro-5090` 在动手前与上游一致，HEAD `5def0ffc15b9fe0ea8d713c43489e5f07e965517`，工作区干净。`git pull --ff-only` 为 Already up to date。
Owner 方向 `W1-OD-20261105-RESOURCE-REPRO-05` 只从 5060 提交 `f491c0a507e5555e9611c022cfba66980ad8cbca` 读取，没有合并。
既有环境批准仍是 `W1-OD-20261104-5090-ENV-01`：`artifact_acsac_compat` 是以后的兼容环境，`artifact_acsac` 保持 torch 2.4.0+cu121 的失败记录。
5090 是计算工人，没有自批权。本分支的 `PODR-154` 只表示兼容环境被有条件接受，不用它代替这份新的方向编号。

上游固定在 `SecAI-Lab/RAGDefender@ba2a17efba165d45409114df2d70b030ade1e1b8`。许可证 MIT，文件 SHA-256 `2242ce2d80454d449576d7ac791c22b3ec9d3907877d68a070e4f30a7aaeab41`。`git describe` 给出 `v0.2.0-2-gba2a17e`。换行符造成的 2919 行 `M` 保留，没有通过改写源码消除。

## 2. 主要实验现在能准备到哪里

核心 R1 是三条作者 Claim，覆盖图 4 的开源模型行和图 5 的两个 7B。活跃脚本的格子、命令、日志路径和未覆盖部分在 [覆盖矩阵](CLAIM_COVERAGE_MATRIX.json)。
补充 R2 里，表 5 要改配置并另下检索器；表 7 和表 8 的文档命令与源码不一致，需要补丁；表 2 和表 3 没有自动汇总；表 6 是聚类语义更改；表 4、13B 和商业模型不在首轮。五栏差异在 [分类矩阵](REPRODUCTION_CLASSIFICATION_AND_DIFFERENCE_MATRIX.md)。
资产、空许可字段、C/D/E 盘和硬停在 [资源门](ASSET_LICENSE_RESOURCE_GATES.md)。

作者写 Claim 1 约 4 到 5 小时，Claim 2 和 Claim 3 各约 1 到 2 小时。那是作者机器上的估计，不是本机实测。脚本计划每格 100 条问题，因为本地目标问题文件长度是 100，且 `M=10`、`repeat_times=10`。这是计划分母，不是已经跑完的 `sample_n`。

静态检查没有安装依赖，也没有重跑 Smoke：

| 检查 | 退出码 |
| --- | --- |
| 三条 `run.sh` 的 `bash -n` | 0 |
| 六个 Python 入口的 `py_compile` | 0 |
| 第一次路径被截断的清点脚本 | 非 0，原因是脚本自己的目录名少了末尾字母，不是上游缺失 |

有效清点日志在 Git 外，SHA-256 `cf2bbc9fd241fbf2d51e9777945daf8e18766a8753116e60737062919aec2a01`。失败那次是 `40442fbf6c4ae69f1775500c25aaa3c3ca98d785f8fd71c1801073b0134db156`。

## 3. 下次审批包

1. Issue ID：`W1-5090-MAIN-REPRO-PREP-20261104`
2. 名称：RAGDefender 主要公开实验的分批许可、下载和单格预检
3. 阶段：准备完成。Claim 未运行
4. 事实：脚本格子、目录缺陷、`datasets` 缺失、盘符和换行符差异是 `OBSERVED_FACT`。Llama、Vicuna、Contriever 和三个 zip 的体积来自此前已提交调查，是 `SOURCE_DERIVED_FACT`。MiniLM、DPR、ANCE 和解压后的 BEIR 体积是 `UNKNOWN`。兼容环境数字不等于论文原数字，这是 `INFERENCE`
5. 约束：`W1-OD-20261105-RESOURCE-REPRO-05` 明确不批准下载和 Claim。新的项目可控文件不能写 C。D/E 取消 1 GiB 全局上限，但每一批仍要冻结峰值并保留至少 20 GiB
6. 现在处理的原因：覆盖范围和阻断已经写清。再往前就是许可、下载或真实命令
7. 风险：脚本在语料缺失时自动下载；Windows 默认 Hugging Face 缓存位于 C；Claim 2 目录名不一致导致整批在第一格失败；把 24 格或 Smoke 写成图 4/图 5；Table 6 被当成普通配置
8. 选项：停在本文件；或按资源门里的顺序逐批批准。不批准就没有新的模型、语料和 Claim 进程
9. 建议：先批许可和冻结修订，再批能写明解压上限的语料，然后只批一个 NQ/`llama7b`/100% 格子。置信度高的是源码循环和本机盘符。解压峰值仍然未知
10. 理由：Owner 要求 5090 先把不下载的准备做完，并在准备结束后停止
11. 需要决定的是：四个模型的许可与修订、三个 zip 的解压上限和路径、单格预检的 60 分钟建议是否采纳、Claim 2 的目录缺陷是否允许修改、以及 Claim 1/2/3 是否分别放行
12. 决定前允许保存本记录并推送本分支。禁止下载权重和 BEIR、运行三条 Claim、调用付费接口、读取 D1/D2/D3、修改算法、把规划写成复现结果、合并其他分支

## 4. 文档收口

- human_ledger_checked = true；human_ledger_updated_if_required = true
- agent_ledger_checked = true；agent_ledger_updated = true
- current_work_state_updated = true
- execution_log_appended = true
- experiment_master_condition_evaluated = true；这是准备计划，没有新的实测，也不把未执行矩阵写成新的 OR 编号
- owner_decision_condition_evaluated = true；方向决定已经在 5060 的 `f491c0a507e5555e9611c022cfba66980ad8cbca`。本分支不新编 PODR 编号
- stage_process_condition_evaluated = true；没有新的 Stage 6.1 试点，不改
- lessons_condition_evaluated = true；机器盘符和换行符留在本准备记录里，不单独立成跨论文方法学
- research_authority_condition_evaluated = true；冻结合同未改
- readme_condition_evaluated = true；导航入口未改

原始日志留在研究 Git 之外。完成后停止，不自动进入下载或 Claim。
