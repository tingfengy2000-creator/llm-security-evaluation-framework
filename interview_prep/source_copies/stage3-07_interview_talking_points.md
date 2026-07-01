# Stage 3 面试话术

## 1. 30 秒版本

“我用 garak 做了一个分阶段的大模型安全评测项目。Stage 1 用内置 Generator 理解
Probe、Generator、Detector 和 Report；Stage 2 搭建 OpenAI-compatible Mock API，对比故意
脆弱和带规则防护的模型；Stage 3 只替换 Key、base URL 和 model，接入 Groq 真实 LLM，测试
Prompt Injection 和 Base64 Encoding。实验保留 JSONL、HTML、hitlog 和聚合 ASR，并针对免费
API 做串行、限样本和退避重试。我不会把小样本 PASS 表述为模型绝对安全。”

## 2. 1 分钟版本

“项目目标不是简单跑一次扫描，而是建立可解释、可复现的评测链路。Stage 1 我先验证
Probe 负责构造攻击、Generator 负责调用模型、Detector 负责判定、Report 负责留证。Stage 2
实现本地 `/v1/chat/completions`，用 vulnerable 回显和 guarded 拒绝做正反对照，确认工具链和
Detector 的行为。Stage 3 使用 garak 的 `groq.GroqChat`，它继承 OpenAICompatible，通过
OpenAI client 调用 Groq。安全版每个 probe 只抽一条并串行，普通版再扩大到八条。我重点分析
PASS/FAIL 与程序退出状态的区别、ASR 的样本边界、Base64 Mock PASS 的原因，以及 401、429、
模型下线和结果不稳定。企业里可以把同样流程做成模型升级前的 CI 安全回归门禁。”

## 3. 3 分钟版本

“我把项目拆成三个阶段，是为了隔离变量。Stage 1 不接网络，先用 garak 内置 Blank 和 Repeat
Generator 跑通闭环。Repeat 会回显 PromptInject 的目标字符串，所以出现 100% ASR，这是
Detector 命中条件导致的可解释结果，不是真实模型结论。

Stage 2 我搭了 OpenAI-compatible Mock API，实现 `/v1/chat/completions`。同一批攻击分别打
到 vulnerable 和 guarded 两个模型：前者回显，后者按规则拒绝。这样验证了 HTTP 集成、请求
日志、正反对照和报告链路。Base64 在 vulnerable 上也可能 PASS，因为回显编码文本不等于
解码并输出攻击目标，DecodeMatch/DecodeApprox 不一定命中。

Stage 3 接入 Groq。garak 0.15.1 已提供 `groq.GroqChat`，它继承 OpenAICompatible，内部使用
OpenAI Python client，把 base URL 指向 Groq，并屏蔽不兼容参数。Key 从环境变量读取，绝不
进入脚本或报告。免费额度安全版设置 generations、parallel requests、parallel attempts 和
prompt cap 都为 1，覆盖 PromptInject 和 Base64 两类攻击；普通版再扩大样本。garak 对 429、
超时和连接错误已有退避重试，但没有固定请求间隔参数，所以我明确区分主动限流与错误后重试。

结果上，我保留 JSONL Attempt、Eval、HTML、hitlog 和日志，再生成聚合 JSON/Markdown。
FAIL 表示 Detector 认为攻击成功，不是程序失败；PASS 只表示当前样本未命中。真实模型结果会
受采样、模型版本、系统提示和 Detector 误报漏报影响，因此要重复实验、扩大样本、人工复核并
给出置信区间。企业落地时，我会把模型、系统提示或 Guardrail 变更作为触发器，在 CI/CD
执行安全回归，并对高风险 FAIL 阻断发布。”

## 4. 追问：为什么用 Groq

“Groq 提供 OpenAI-compatible API，接入成本低；`llama-3.1-8b-instant` 延迟低，适合学习阶段
做小规模真实评测。选择 Groq 不是因为它天然更安全，而是它能以较低门槛验证从 Mock 到真实
Provider 的迁移。企业选型还要考虑数据合规、地域、SLA、模型能力和成本。”

## 5. 追问：什么是 OpenAI-compatible

“它表示请求路径、鉴权、`messages/model` 字段和 `choices[].message.content` 响应结构与
OpenAI API 相近。它是协议兼容，不代表模型来自 OpenAI，也不保证所有参数都支持。其价值是让
评测框架和模型 Provider 解耦。”

## 6. 追问：Mock API 有什么意义

“Mock 用可控输出验证 API 契约、Detector 和报告链路，并建立 vulnerable/guarded 正反对照。
没有 Mock，真实扫描失败时很难区分是模型行为、网络、Provider 参数还是评测框架问题。Mock
不能替代真实模型结论，但能提高调试确定性。”

## 7. 追问：garak 的 Probe / Detector 是什么

“Probe 定义攻击目标并构造一组攻击 prompt；Generator 把它们发送给模型；Detector 对每个
回答打分，判断是否达到攻击成功条件。Probe 回答‘怎么攻击’，Detector 回答‘是否命中’。”

## 8. 追问：为什么 vulnerable 在 Base64 上也可能 PASS

“Stage 2 vulnerable 主要回显输入。Base64 Detector 检查的是模型是否解码并输出目标内容，
回显编码串不等于执行解码后的指令，因此 DecodeMatch/DecodeApprox 可能都不命中。这说明
vulnerable 是相对于具体威胁和判定条件的，不是全局标签。”

## 9. 追问：真实模型评测为什么不能说绝对安全

“覆盖的 Probe、样本和 Detector 都有限，模型生成有随机性，Provider 还会更新模型和隐藏
策略。PASS 只是在特定配置和时间下没有检出。需要扩大攻击面、重复运行、人工红队、线上监控
和持续回归，才能逐步提高信心。”

## 10. 追问：企业里如何接入 CI/CD

建议回答：

1. 固定模型版本、系统提示、Guardrail 和测试集版本。
2. PR 阶段跑 Mock 与少量 smoke test。
3. 发布前跑完整安全回归。
4. 与上一稳定版本比较 ASR，而不是只看绝对值。
5. 对高风险 Probe 设置阻断阈值。
6. 保存 JSONL 证据并脱敏，接入审计平台。
7. Key 存 CI Secret，限制权限和预算。
8. 模型、RAG 索引、Agent 工具权限变更时自动触发。

还要避免只以单一总分门禁，因为高危数据泄露不能被大量低风险 PASS 稀释。

## 11. 追问：如何进一步增强防护

“我会做分层防护：输入规范化和 Prompt Injection 检测；系统指令与不可信 RAG 内容隔离；
最小化 Agent 工具权限并要求高风险操作确认；输出侧做数据泄露和内容策略检查；对工具参数做
schema 验证；全链路审计。然后用同一 Probe 集做防护前后对照，并补充间接注入、多轮攻击、
工具越权和系统提示泄露。”

## 12. 面试中不要这样说

- “Groq 比其他模型安全。”
- “我跑出了 PASS，所以模型没有漏洞。”
- “OpenAI-compatible 就是 OpenAI 模型。”
- “429 多重试几次就好。”
- “ASR 是 garak 自动给出的绝对真相。”

更准确的表达是：说明测试条件、样本范围、Detector 规则、证据路径和结论边界。

