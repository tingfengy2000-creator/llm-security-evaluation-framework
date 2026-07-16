# 项目阶段进度总览

本页依据 `experiments/registry.json`、阶段交付目录、Git 分支和实际测试状态整理。更新时间：2026-07-16。

| 阶段 | 状态 | 核心工作 | 主要证据 | 结论边界 |
| --- | --- | --- | --- | --- |
| Stage 1 | 已完成 | garak 安装；Probe/Generator/Detector/Report 最小闭环；Mock prompt injection | `deliverables/stage1/`、`deliverables/stage1_learning/` | Mock 基础流程，不代表真实模型 |
| Stage 2 | 已完成 | 本地 OpenAI-compatible Mock API；vulnerable/guarded 对照 | `deliverables/stage2/` | 可控 Mock 行为 |
| Stage 3 | 已完成 | Groq 真实 API；PromptInject 与 Base64 smoke scan | `deliverables/stage3/` | 2 个真实模型 Attempt |
| Stage 4 | 已完成 | OpenAI-compatible Guard Proxy；passthrough/full guard A/B | `deliverables/stage4/` | 小样本 rule-based baseline |
| Stage 4.1 | 已完成 | P/I/O/F 四组消融；独立验证 Output Guard | `deliverables/stage4_ablation/` | 2 条 smoke prompt |
| Stage 5 | 已完成（Mock） | 6 类攻击矩阵、正常样本、T1–T9、指标与报告 | `data/stage5/`、`src/codeguarder/`、`deliverables/stage5/` | 离线框架回归 |
| Stage 5 Paper | 已完成（Mock） | A1–A6 跨层模型、P/I/O/F、检测适配器、确定性 AttemptRecord | `src/codeguarder/stage5_paper/`、`deliverables/stage5_paper/` | 22 样本、88 attempts；真实 Groq 尚未运行 |
| Stage 6 | 开发中 | RAG 安全与可信检索基线 | `feature/stage6-rag` worktree | 目前只完成依赖、稳定契约、数据与攻击矩阵基础 |
| Stage 6.1 | 规划中 | 隐蔽知识污染检测、多证据可信检索、冲突感知策略 | Stage 6 接口预留 | 尚未实现 |
| Stage 7 | 规划中 | Agent 安全；复用 Stage 6 脱敏 Evidence 输出 | 架构方向 | 尚未实现 |

## Stage 1：garak 基础安全扫描

- 使用 `test.Blank` 验证最小扫描链路。
- 使用 `test.Repeat` + `promptinject.HijackHateHumans` 验证攻击构造、批量调用、Detector 判定和报告生成。
- 256 个 Mock 攻击样本 ASR 为 100%，这是特意设计的脆弱基线。
- 已形成 garak 架构、命令、JSONL/HTML/hitlog 和面试讲解材料。

## Stage 2：OpenAI-compatible Mock API

- 实现 `/v1/chat/completions`，理解 API Key、base URL、model name 和协议兼容。
- 建立 vulnerable 与 guarded 可控对照，区分接口工程问题与模型安全问题。
- 解释 Base64 样本为什么可能得到不同 Detector 结果。

## Stage 3：Groq 真实模型

- 使用 `GROQ_API_KEY` 接入 `https://api.groq.com/openai/v1`。
- 目标模型为当次实验记录中的 `llama-3.1-8b-instant`。
- PromptInject 攻击成功；Base64 的 garak detectors 判 PASS，但人工复核发现模型已经识别并部分解码危险内容。
- Attempt 口径 ASR 为 1/2，即 50%；该结果不能外推为模型整体安全水平。

## Stage 4：真实 API Guard A/B

- 调用链为 `garak → Guard Proxy → Groq`。
- 控制组和实验组经过相同代理，只切换 Guard 行为。
- 输入侧检测 prompt injection、jailbreak、encoding bypass；输出侧检测危险载荷并替换为拒答。
- 日志记录 guard 开关、是否调用上游、拦截位置和最终决策。

## Stage 4.1：Guard 消融

- 对外名称固定为 `passthrough`、`input-only`、`output-only`、`full-guard`。
- `full-guard` 是实验名称；内部可映射到历史实现 `guarded`。
- Output-only 必须先调用 Groq、记录原始输出 hash，再执行输出检测。
- 当前两条 smoke prompt 中，Input Guard 与 Output Guard 都将 ASR 从 50% 降为 0%；这是当前规则和样本下的结果，不是生产防护率。

## Stage 5 / Stage 5 Paper：系统化评测框架

- 攻击矩阵覆盖 prompt injection、role confusion、encoding obfuscation、context injection、data exfiltration、tool injection。
- Failure Taxonomy 覆盖 T1–T9，包括 Detector Miss、Guard Bypass、Over-blocking 和 Tool Side-effect Risk。
- 固定四种 Guard 配置，校验 prompt hash parity、output-only 行为、秘密泄露和报告完整性。
- Stage 5 Paper 使用独立 Dataset Runner，不让 garak 充当调度器；garak 只作为官方 Detector 来源之一。
- 最新注册记录为 22 个样本、88 个 attempts，来自确定性 Mock。

## Stage 6 当前真实进度

Stage 6 位于 `D:/llmProject/.worktrees/stage6-rag` 的 `feature/stage6-rag` 分支。已经完成并提交：

- 固定依赖与独立虚拟环境；
- `QueryRecord`、`DocumentRecord`、`RetrievalEvidence`、`EvidenceSignal`、`TrustAssessment` 等稳定契约；
- R1–R6 数据集基础与 Ground Truth 物理隔离；
- Attack Matrix loader/renderer 及标签泄露加固测试。

最近一次验证为 Stage 6 测试 `104 passed`，Ruff 和 MyPy 通过。当前仍有 Task 3 的加固修改未提交，因此不能宣称 Stage 6 已完成。

尚待实现：

- SentenceTransformers embedding provider；
- Persistent ChromaDB 与稳定 Retriever；
- EvidenceSignal 提取、pass-through TrustAggregator、off/observe RetrievalPolicy；
- ContextBuilder、确定性 Mock LLM、可选 Groq；
- RPR/CIR/Faithfulness/RMSR/Cross-layer Leakage 与 T10–T15；
- 报告、热力图、运行脚本和完整交付文档。

## Stage 6.1 与 Stage 7 的预留关系

- Stage 6.1 只能通过新增 EvidenceSignal、TrustAggregator 算法和 `enforce` Policy 增量扩展。
- Retriever 和 Model 不得读取 poison label；只有 Evaluator 能访问 Ground Truth。
- Stage 7 必须消费脱敏的 `RetrievalEvidence`/安全信封，不直接耦合 ChromaDB 内部结构。
