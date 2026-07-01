# Stage 4 面试话术

## 1. 30 秒版本

“在 Stage 3 直连 Groq 后，我增加了一个本地 OpenAI-compatible Guard Proxy。为了避免把代理
链路差异误算成防护效果，我用同一个 Proxy 做 passthrough 和 guarded 配对，两组使用相同
模型、Probe、seed 和 prompt hash。Guard 在输入侧检测指令覆盖、jailbreak 和 Base64 解码后
危险内容，输出侧检测 rogue string 与脚本载荷，并记录是否调用上游。它只是可解释的
rule-based baseline，不代表生产级防护。”

## 2. 1 分钟版本

“Stage 4 的核心不是多写几个正则，而是做可归因的防护实验。控制组和实验组都经过本地
OpenAI-compatible Proxy，控制组只检测和记录，实验组执行输入/输出拦截。输入命中时 Proxy
返回 HTTP 200 的拒绝 completion，让 garak 继续用同一 Detector 评估；同时 Guard 日志记录
这是代理拦截而不是模型自然拒绝。结果同时统计 Attempt ASR、Detector 命中率、input/output
block 和 upstream calls，并用 prompt SHA-256 验证样本一致。我还保留 input-only 和
output-only 模式做消融。”

## 3. 3 分钟版本

“Stage 3 证明 garak 能通过 OpenAI-compatible API 调用真实 Groq 模型，也发现了直接
PromptInject 命中，以及 Base64 Detector PASS 但模型已部分解码的边界。Stage 4 进一步增加
防护层。

我没有直接比较 Stage 3 direct 和 Stage 4 guarded，因为两组的 Generator、代理链和实际生成
参数存在差异。主实验改成 Proxy passthrough 对 Proxy guarded，唯一主动变量是规则是否执行。

Proxy 使用 ThreadingHTTPServer 暴露 `/v1/chat/completions`，内部 OpenAI client 指向 Groq。
输入规则覆盖 instruction override、DAN/developer mode、安全绕过和 Base64 解码后 XSS；输出
规则覆盖 rogue string、script/javascript 和明显 prompt leakage。输入阻断不调用 Groq，输出
阻断则替换 assistant content。每次请求写入 JSONL，但只保留 hash、截断预览、规则名、动作、
上游调用状态和延迟，不保存 Key。

我把它定位为 baseline，因为正则会被同义改写、多语言、分词和多层编码绕过，也会误报正常的
安全研究内容。下一步会比较 classifier、LLM-as-judge 和策略引擎，并在 RAG/Agent 中做可信
指令与不可信上下文隔离、工具最小权限和高风险操作确认。”

## 4. 为什么需要 passthrough 控制组

“如果只有 Stage 3 direct 和 Stage 4 guarded，两组同时改变了代理、Generator 和参数。使用
同一 Proxy 的 passthrough/guarded 配对，可以把主要差异收敛到 Guard 开关，并通过 prompt
hash 检查样本完全一致。”

## 5. 为什么阻断时返回 200

“HTTP 403 会让 garak 把它视为调用失败，无法得到正常模型输出和 Detector 结果。返回兼容的
拒绝 completion，可以继续评估最终用户可见文本；真正的安全动作由独立 Guard 日志记录。”

这不是建议所有生产策略都返回 200。生产 API 应根据产品契约选择状态码。

## 6. 输入 Guard 和输出 Guard 的区别

“输入 Guard 可以提前省掉模型调用并阻止攻击进入上下文，但容易被改写绕过。输出 Guard 能
覆盖部分输入漏报，但已经产生费用，而且 Agent 工具副作用可能已经发生。两者要配合策略引擎，
不能简单互相替代。”

## 7. 如何证明效果不是随机波动

当前 smoke test 不能证明。后续应：

1. 扩大同一版本攻击集。
2. 多次重复。
3. 固定模型与生成参数。
4. 记录 prompt hash。
5. 报告置信区间。
6. 同时测误报率和正常任务质量。

## 8. 为什么 rule-based 不够

- 同义词和多语言绕过。
- 字符插入与 token splitting。
- Base64 多层嵌套或其他编码。
- 多轮渐进式攻击。
- 规则无法理解复杂业务语义。
- 维护成本随规则数量增长。

## 9. 后续扩展

### 分类器

使用专门 Prompt Injection/Jailbreak 分类器输出风险分数。优点是速度快、可批量评估；缺点是
需要数据、阈值和漂移监控。

### LLM-as-judge

让评审模型结合上下文判断是否越权。覆盖复杂语义，但成本、延迟、稳定性和 Judge 自身攻击面
都需要控制。

### 策略引擎

把信号与用户角色、数据级别、工具权限、环境和风险动作结合，输出 allow/redact/block/review。
它解决“检测结果如何转成业务动作”。

### 上下文隔离

在 RAG/Agent 中区分：

- 可信系统指令。
- 用户输入。
- 不可信检索文档和网页。
- 工具返回数据。

不让不可信内容获得指令权限，并对工具调用做 schema、权限和确认检查。

## 10. 不要这样说

- “正则挡住两条攻击，所以防护率 100%。”
- “Guarded PASS 说明模型已经修复。”
- “输出 Guard 可以撤销 Agent 已执行的动作。”
- “ASR 降低就不需要测误报。”

正确说法要包含样本范围、控制变量、动作位置和局限。

## 11. 本次真实结果怎么讲

“我在 Groq 的 `llama-3.1-8b-instant` 上做了两条严格配对 smoke test。passthrough 组
Attempt ASR 是 50%，guarded 组是 0%，下降 50 个百分点；两组 prompt hash 完全一致。
guarded 的两条请求都被输入规则拦截，Groq 调用数从 2 次降到 0 次。

但我没有把它表述成防护率 100%。样本只有两条，而且 Base64 在 passthrough 下被 garak
判为 PASS，模型却实际生成了脚本载荷，说明 Detector 存在漏报。这个案例促使我同时保留
Guard 行为日志、原始输出和多 Detector 结果，并计划继续做 output-only 消融、正常样本误报
测试和更大攻击集评测。”
