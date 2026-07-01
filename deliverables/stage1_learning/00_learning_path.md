# Stage 1 学习路线图

## 这门实验课的目标

你现在不是在“赶项目”，而是在建立一套能讲给面试官听的大模型安全评测知识体系。

Stage 1 的学习目标只有一个：理解 garak 如何把一次大模型安全测试拆成可复现的工程流程。

你最后应该能独立回答：

1. garak 是什么，为什么企业需要它。
2. Probe、Generator、Detector、Harness、Evaluator、Report 分别做什么。
3. 一条扫描命令从输入到报告，中间发生了什么。
4. 为什么 Stage 1 用 mock model，而不是直接测真实大模型。
5. 如何向面试官解释“我不是随便问了几个攻击 prompt，而是做了自动化安全评测”。

## 先建立一个直觉

如果你第一次接触 garak，可以先把它想成“大模型安全领域的自动化测试框架”。

普通软件测试里，我们会有：

- 测试用例
- 被测系统
- 断言条件
- 测试运行器
- 测试报告

garak 里对应的是：

- Probe：生成攻击测试用例
- Generator：调用被测模型
- Detector：判断攻击是否成功
- Harness：把 Probe、Generator、Detector 串起来运行
- Report：保存测试过程和结果

所以 Stage 1 不是“跑了一个工具”，而是在学习大模型安全测试的基本分层。

## Stage 1 学习顺序

### 第 0 章：学习路线图

文件：`00_learning_path.md`

你现在正在读的就是这一章。

这一章回答：

- 我们到底要学什么。
- 为什么不能直接去写 Stage 3。
- Stage 1 每份学习文档之间是什么关系。

你要掌握的核心句子：

> garak 把大模型安全评测拆成攻击构造、模型调用、结果判定和报告生成四个环节。

### 第 1 章：garak 是什么

文件：`01_what_is_garak.md`

这一章会讲：

- garak 是什么。
- 为什么会出现 garak。
- 企业为什么需要 garak。
- garak 解决什么问题。
- 它和 Promptfoo、Inspect AI、PyRIT、DeepTeam 有什么区别。

你要掌握的核心句子：

> garak 的价值不是“发 prompt”，而是把大量安全攻击样本系统化、自动化、可报告化。

### 第 2 章：garak 架构

文件：`02_garak_architecture.md`

这一章会讲：

- Generator 是什么。
- Probe 是什么。
- Detector 是什么。
- Harness 是什么。
- Evaluator 是什么。
- Report 是什么。
- 它们之间如何调用。

你要掌握的核心句子：

> Probe 负责问什么，Generator 负责问谁，Detector 负责怎么判定，Report 负责留下证据。

### 第 3 章：第一次扫描命令分析

文件：`03_first_scan_analysis.md`

这一章会结合你已经跑通的 Stage 1 命令逐行解释：

- 每个参数是什么意思。
- 为什么使用 `test.Blank`。
- 为什么使用 `test.Repeat`。
- 为什么 prompt injection 会 100% 成功。
- garak 最终生成了哪些文件。

你要掌握的核心句子：

> Stage 1 的 mock 扫描不是为了证明真实模型不安全，而是为了证明评测链路能跑通。

### 第 4 章：输出文件分析

文件：`04_stage1_output_analysis.md`

这一章会讲：

- `.jsonl` 是什么。
- `.html` 报告怎么看。
- `.hitlog.jsonl` 是什么。
- `entry_type`、`attempt`、`eval`、`digest` 分别是什么意思。
- 如何从报告里找到攻击 prompt、模型输出和 detector 结果。

你要掌握的核心句子：

> 安全评测必须可追溯，所以原始样本、模型输出、判定结果和汇总报告都要保存。

### 第 5 章：Stage 1 面试讲法

文件：`05_stage1_interview.md`

这一章会讲：

- 面试时怎么介绍 Stage 1。
- 面试官可能追问什么。
- 如何解释 mock model。
- 如何解释 attack success rate。
- 如何避免把 Stage 1 讲成“只是跑了个工具”。

你要掌握的核心句子：

> 我先用 mock model 建立可复现的安全评测基线，再把同一套流程迁移到真实 OpenAI-compatible API。

## 这一步和上一阶段交付物是什么关系

你之前已经有了运行结果：

- `deliverables/stage1/garak_run_commands.md`
- `deliverables/stage1/garak_scan_result.json`
- `deliverables/stage1/garak_scan_summary.md`
- `deliverables/stage1/prompt_injection_samples.md`

这些是“实验结果”。

现在的 `stage1_learning/` 是“理解材料”。

两者的关系是：

- 结果文件回答：我跑出了什么。
- 学习文档回答：为什么这样跑、怎么理解、怎么讲给别人听。

企业项目里也会这样分开：

- 原始日志用于审计和复现。
- 总结报告用于决策。
- 学习/设计文档用于团队交接和面试讲解。

## 企业里为什么这样学

企业不会只关心“你能不能跑通一个命令”。

企业更关心：

1. 你是否知道测试对象是谁。
2. 你是否知道攻击样本从哪里来。
3. 你是否知道成功/失败如何判定。
4. 你是否能复现问题。
5. 你是否能把结果变成防护建议。

所以我们按章节学习，是为了让你能从工程执行者变成安全评测负责人。

## 面试官可能问什么

面试官可能会问：

1. garak 和你自己写 prompt 脚本有什么区别？
2. 为什么 Stage 1 不直接接真实模型？
3. 为什么你用了 `test.Repeat`？
4. 全部攻击成功说明什么？
5. 你怎么证明结果不是偶然的？
6. 你怎么从 garak 报告里找到失败样本？
7. 后续怎么迁移到真实模型？

这些问题后面每章都会逐步拆开。

## 第一次接触最容易误解哪里

### 误解 1：garak 是一个攻击工具

更准确地说，garak 是安全评测框架。它不仅生成攻击 prompt，还负责调用模型、判定结果和生成报告。

### 误解 2：攻击成功率高就说明真实大模型不安全

不一定。Stage 1 用的是 mock model。mock model 的作用是验证流程，不是代表真实模型能力。

### 误解 3：Detector 就是模型裁判

Detector 不一定是另一个大模型。很多 detector 是规则、字符串匹配、相似度匹配或专门逻辑。

### 误解 4：HTML 报告就是全部证据

HTML 适合展示，但真正可追溯的数据在 JSONL 里。面试时你要知道两者区别。

### 误解 5：Stage 1 太简单，没有价值

Stage 1 的价值是建立基线。没有这个基线，后面接 Groq、RAG、Agent 时就不知道问题出在工具链、API、模型，还是 detector。

## 本章你需要掌握的最小知识

读完本章，你至少要能说出：

1. Stage 1 是为了理解 garak 的基本评测流程。
2. garak 的核心流程是 Probe -> Generator -> Detector -> Report。
3. mock model 的作用是先验证评测链路。
4. Stage 1 的结果文件是证据，学习文档是理解和表达材料。
5. 下一章要学习 garak 本身是什么，以及它在企业安全评测中的定位。

## 给你的自检问题

在继续下一章前，你可以先试着回答：

1. 如果面试官问“你这个项目第一阶段到底做了什么”，你会怎么说？
2. 如果面试官问“为什么不直接测 Groq”，你会怎么说？
3. 如果面试官问“garak 和普通 prompt 脚本有什么区别”，你目前能说出几个点？

如果这三个问题还答不上来，没关系。下一章开始我们会逐个拆。
