# Paper 1｜Owner24 Fast-Track F0 停止记录

2026-11-10 JST · `W1-5060-OWNER24-F0-20261110-01` · `W1-OD-20261110-5060-FASTTRACK-CONDITIONAL-24`

**`F0_BLOCKED / HUMAN_DECISION_REQUIRED / AUTO_CONTINUE=NO`。** 现有 Windows 执行环境的出站隔离无法证实。未触发一次性 F1，后续科学阶段未运行。

[执行合同](W1_5060_OWNER24_FASTTRACK_MULTI_STAGE_EXECUTION_PROMPT_V1.md) · [Owner24 原授权](../owner_approvals/W1_5060_OWNER24_FASTTRACK_LOCAL_MODEL_EXTRACTION_CONDITIONAL_AUTH_20261110.md) · [脱敏 Run Manifest](W1_5060_OWNER24_FASTTRACK_RUN_MANIFEST.json)

## F0 已取得证据

- **Git 与治理。** 仅快进 5060 独立发布工作树，执行基点 `ed9aa4bb101158c87bf4def77bf7441bf7c47b03`。合同提交 `4ff5fd9736e13821e1ca872ee6df4dd66943d142`，Owner 授权提交 `bcbdc711b3ba63dc805b11ea0d299f790c7cec42`。原独立工作树及 Owner22、Owner23A、Owner20 历史产物未修改。
- **资产。** 固定 Qwen GGUF 1,117,320,736 B 和 llama.cpp b12242 ZIP 24,931,401 B 的 SHA256 复核通过。对照 Owner22 清单复核 52/52 个原 ZIP 条目和已解包文件，保留 51 PE 的原始库存。Owner22 和 Owner23A 的私有 ZIP SHA256 复核通过。
- **实际执行入口的静态路径。** 以 `llama-completion.exe` 为根。入口 SHA256 `b1f64db0d032dfb5c78ce016ff4e922d47c333be7691a510e6cfb41efd8ba034`。Windows `26200.9711`，7 个包内 PE，80 条直接导入、0 条延迟导入，1,601/1,601 个符号绑定解析，50/50 条 API-set 映射，未决前沿 0。静态检查退出 0。程序实际启动、动态后端、模型加载、输出和峰值内存均未测。执行合同区分了 `llama-cli.exe` 内置 HTTP 路径与本轮固定的 completion 入口。最终执行命令、Job Object 和进程监测方案在停止点前未完成冻结。
- **资源。** 检查时可用物理 RAM 9,478,918,144 B、可用 commit 17,855,447,040 B、D 盘可用 355,844,206,592 B，分别超过 8 GiB、8 GiB、10 GiB 准入门。D 盘新证据目录及使用的旧资产根均检查了重解析点与最小 ACL，临时、缓存和配置文件落点在 D 盘。旧迁移宽 ACL 目录未作为输入或证据。
- **出站隔离。** 只读查询显示 Domain、Private 的有效默认出站策略是 AllowOutbound，Public 防火墙关闭。出站规则清单按固定入口及项目名称检索的匹配数为 0。有效令牌为 Medium，管理员组为 deny-only。未发现可用 Windows Sandbox 入口，且没有已验证的无外网执行区。只读查询正常退出，未修改防火墙、未做主动联网探测。
- **许可与风险。** 沿用 Owner24 对本机受控、不再分发用途的有限授权，整包 notice 仍未知。Forward Risk Review 确认静态入口和资产身份明确，网络控制与运行时行为仍是独立前置。Paper Risk Review 保留 F2 已暴露开发、F3 同 Agent 暂定、F4 D1 离线代理的边界。静态结果不支持抽取效果、污染过滤收益或泛化结论。

## 阶段、资源与费用账本

| 阶段 | 状态 | 实际完成量 |
| --- | --- | --- |
| F0 | `BLOCKED` | 完成资产与 PE 静态核验。出站隔离未验证，NEW60+10 及其 Gold 封存未创建。 |
| F1 | `NOT_RUN` | 模型启动 0/1，首次单 token smoke 尚未消耗。 |
| F2 | `NOT_RUN` | 模型开发调用 0，完整开发回放 0/193 视图。 |
| F3 | `NOT_RUN` | 新合成暂定评价 0/60 主案例、0/10 从属视图，未揭盲。 |
| F4 | `NOT_RUN` | D1 离线过滤诊断 0 个世界，未访问 D1 原正文、标签或冻结 TopK。 |

新增下载、安装、发行程序启动、模型加载、本地推理、输出 token、商业 API 和新科学试次均为 0，新增费用 USD 0。Human Gold 保持 0，正式 ASR/Accuracy 为 `NOT_MEASURED`。保留 Owner20 规则 `FEASIBILITY_NO_GO`、旧 S1 FAIL、R2 K1-C。D2/D3、5090、正式 S2–S5 锁定。

私有 `OWNER24_F0_PRIVATE_EVIDENCE.zip` 含 6 件，34,216 B，SHA256 `a656251ca9704f77d9acf477c53883f2643f5e53d0a2f7621cd7e78567518980`。逐项重读核验通过，内容含只读命令、退出码、stdout/stderr、每符号记录和输入身份。复用静态解析器单测 5/5、Ruff、MyPy 均通过，独立 QA 结果哈希见 Manifest。

## PO-MHEP 决策记录

| 字段 | 记录 |
| --- | --- |
| 1. Issue ID | `W1-5060-OWNER24-F0-OUTBOUND-ISOLATION-20261110` |
| 2. Issue | 当前无法证明固定模型入口默认拒绝外联。 |
| 3. Discovery | F0，完成 Git 同步及启动前只读预检。 |
| 4. Evidence | `OBSERVED_FACT` 防火墙默认允许出站、固定路径规则检索 0 匹配、当前无管理员令牌。 `SOURCE_DERIVED_FACT` Owner24 要求外网隔离先于任何模型进程。 `INFERENCE` 当前证据无法支持 deny-by-default。 `UNKNOWN` 真实运行时网络行为及既有可替代隔离区。 |
| 5. Constraints | 仅固定 5060 资产及 CPU 入口，F1 单次、≤1 token、≤6 GiB private commit、≤180 秒。D 盘私有区，F0 RAM/commit 各≥8 GiB、D 余量≥10 GiB。 |
| 6. Why now | 隔离为先验硬门。启动后观测无法替代启动前证据，且会消耗唯一 smoke。 |
| 7. Downstream risk | 越门会产生外联与数据出域风险，破坏可复现性，消耗唯一 smoke，并使 F2–F4 的证据失去有效前置。整包仍仅限受控内部用途。 |
| 8. Options | A 由 Owner 提供已存在的、无外网及 DNS 出站的隔离区或等效预配置策略，保留固定二进制与 D 盘证据边界。复核成本低于切换运行时，须重新核验同一套身份和资源。B 保持暂停并保留首试额度，当前零新增成本，科研进度等待可用环境。 |
| 9. Recommendation | A。先给出隔离生效证据，继续完成 F0 剩余项，再按原上限启动唯一 F1。 |
| 10. Rationale and confidence | 对当前隔离无法证明的判断置信高。模型是否能启动与中文抽取质量仍未知。 |
| 11. Owner decision | 确认可用于原 Owner24 边界的已隔离执行区或等效预配置策略，并给出可独立验证的网络与 DNS 边界。 |
| 12. While stopped | 允许只读核验、封存、治理和 Git 收口。模型、科学试次、防火墙变更、安装、下载与外部 API 停止。 |

下一项科研裁决仍取决于 F2 严格证据绑定及 F3 未见合成点估计。恢复时先补 F0 隔离、启动器与 NEW60+10 前封存。F1 成功只解锁开发评估，F2/F3 依合同数值与安全门决定是否进入下一阶段。F4 仍使用原 D1 TopK 和预注册的 12/36 世界规则。

## 文档收口

更新 Human Ledger、Agent Ledger、Current Work State、Research Execution Log、Project Master、Experiment Master 和 Tracker。Owner Decision Register 保留原授权，本轮没有新决定。Stage Process、Canonical Lessons、Research Plan Authority、README 的触发条件已检查，未进入新阶段、未改变已冻结方法或导航。

    human_ledger_checked = true
    human_ledger_updated_if_required = true
    agent_ledger_checked = true
    agent_ledger_updated = true
    current_work_state_updated = true
    execution_log_appended = true
    experiment_master_condition_evaluated = true
    owner_decision_condition_evaluated = true
    stage_process_condition_evaluated = true
    lessons_condition_evaluated = true
    research_authority_condition_evaluated = true
    README_condition_evaluated = true
    cross_document_current_task_consistent = true
    cross_document_status_consistent = true
    cross_document_next_action_consistent = true
    cross_document_blocker_consistent = true
    markdown_links_valid = true
