# 后续协作上下文与执行清单

## 1. 当前稳定技术决策

- 开发环境：Windows PowerShell，Python 3.12。
- Stage 3–4.1 真实上游：Groq OpenAI-compatible API；Key 使用 `GROQ_API_KEY`。
- Guard 模式外部统一命名：`passthrough`、`input-only`、`output-only`、`full-guard`。
- Stage 5 Paper：Dataset Runner 负责调度；garak 只作为官方 Detector Adapter，不是数据集调度器。
- Stage 6：Persistent ChromaDB + `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` + 确定性 Mock LLM，可选 Groq。
- Stage 6 TrustAggregator 当前必须是 pass-through；RetrievalPolicy 只有 `off/observe`，Stage 6.1 才实现学习或 enforce。
- Ground Truth 与公开检索数据物理隔离，Retriever、ContextBuilder 和 Model 不得看到 poison label。

## 2. Stage 6 不可变调用链

```text
Query
→ Retriever
→ Persistent ChromaDB
→ RetrievalEvidence[]
→ EvidenceExtractor
→ EvidenceSignal[]
→ TrustAggregator (baseline pass-through)
→ RetrievalPolicy (off/observe)
→ ContextBuilder
→ Mock LLM / Groq
→ Evaluator
→ Metrics + T10–T15 + Reports
```

Stage 6.1 和 Stage 7 不得绕开 `RetrievalEvidence` 直接依赖 ChromaDB 返回结构。

## 3. 每次继续开发前

1. 读取本目录四份上下文和当前阶段 design/plan。
2. 检查当前 branch、worktree、`git status` 和最近提交。
3. 区分历史文件、当前任务修改和无关用户修改。
4. 确认本次知识点、实验假设、成功条件和结论边界。
5. 先写或更新测试，再实现代码。
6. 编辑前向用户说明正在改什么、为什么。

## 4. 每个 Task 完成条件

- 对应测试先红后绿，或有明确的既有回归证据；
- 单元测试、集成测试、Ruff、MyPy 按风险执行；
- 无 label leakage、secret leakage、完整危险内容泄露；
- Mock 确定性运行相同输入得到相同 canonical 日志；
- 文档解释原理、企业意义、上下阶段关系、面试追问和易错点；
- Git diff 只包含本任务路径，不触碰历史阶段；
- 状态页明确写“完成、开发中或阻塞”，不模糊表述。

## 5. 实验结果解释纪律

- garak `FAIL` 表示攻击命中，不是程序崩溃。
- garak `PASS` 只表示当前 Detector 未命中，不代表绝对安全。
- Detector PASS 仍要检查 raw risk 和 Detector Miss。
- Guard 后 PASS 可能来自代理替换，不代表底层模型变安全。
- Mock 用于验证机制和可复现性；真实 API 用于观察模型行为，两者不能互相替代。
- 小样本 smoke test 用于验证流程，不能宣称统计显著或生产防护率。
- 所有结论使用“在当前攻击矩阵、当前模型、当前规则和当前检测器下”。

## 6. 后续最近工作顺序

1. 完成并提交 Stage 6 Task 3 的攻击矩阵隔离加固。
2. 实现真实 Embedding Provider 和 Persistent ChromaDB。
3. 实现稳定 Retriever 与 ContextBuilder，验证无标签泄露。
4. 实现 EvidenceSignal 和 pass-through Trust 基线。
5. 接入确定性 Mock LLM，完成 T10–T15、指标和报告。
6. 完成 Stage 6 Mock 回归后，再运行小样本 Groq。
7. Stage 6 完整复盘后才进入 Stage 6.1；Stage 7 后续复用稳定输出契约。

## 7. 每次面向用户的教学交付格式

每章结束时至少说明：

- 本章学到了什么；
- 代码/数据/结果在哪里；
- 如何复跑；
- 结果如何读；
- 面试如何讲；
- 哪些内容还没证明；
- 下一章只学习和实现什么。
