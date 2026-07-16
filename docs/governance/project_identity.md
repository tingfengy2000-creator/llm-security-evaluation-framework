# LLMGuard 项目标识

## 正式名称

- 英文正式名称：**LLMGuard Research Framework**；
- 中文正式名称：**LLMGuard 大模型安全评测与可信检索研究框架**；
- 项目简称：**LLMGuard**；
- Python distribution：`llmguard-research-framework`；
- 规范 import namespace：`llmguard`；
- 旧兼容 namespace：`codeguarder`；
- 当前远端仓库：`tingfengy2000-creator/llm-security-evaluation-framework`；
- 建议的后续远端仓库名称：`llmguard-security-research-framework`。

远端仓库尚未重命名。只有本地迁移、兼容测试、静态检查、Git remote 备份均通过并由用户单独
批准后，才可把建议名称应用到 GitHub；本机父目录与 worktree 根目录不在本轮改名。

## 名称消歧

LLMGuard Research Framework is an independent research and evaluation project. It
is not affiliated with or derived from Protect AI's llm-guard project.

LLMGuard Research Framework 是独立的大模型安全评测与可信检索研究项目，与 Protect AI
的 llm-guard 项目不存在隶属、继承或官方关联关系。

因此 distribution 不得使用 `llm-guard` 或 `llm_guard`，避免与第三方项目产生包名或项目
身份混淆。

## 研究范围

LLMGuard 面向可复现的 LLM、RAG 与 Agent 安全评测。它以 Stage 1–5 的历史实验为证据基础，
以 Stage 6 的 Retrieval Security Baseline、Stage 6.1 的隐蔽知识污染检测、Stage 6.2 的多
证据可信检索、Stage 7 的 Agent 安全为后续研究路线。

本项目不执行真实破坏性工具；第三方 Provider 凭据继续使用其标准变量，例如
`GROQ_API_KEY`，不复制为自定义凭据名。项目自身的运行时变量使用 `LLMGUARD_` 前缀，例如
`LLMGUARD_LOG_LEVEL`、`LLMGUARD_RUNTIME_DIR`、`LLMGUARD_MODEL_CACHE` 和
`LLMGUARD_EXPERIMENT_CONFIG`。
