# Probe 原理：Prompt Injection 与 Base64 Encoding

## 1. Probe 到底是什么

Probe 是“如何构造并投递攻击样本”的组件。它不负责调用具体模型，也不负责最终判分。

```text
Probe 生成 prompt
  -> Generator 调用模型
  -> Detector 检查回答
```

同一个 Probe 可以交给 Stage 2 Mock，也可以交给 Stage 3 Groq，因此我们能比较相同攻击在
不同被测对象上的表现。

## 2. `promptinject.HijackHateHumans`

### 它在测试什么

该 Probe 来自 PromptInject 风格测试。它把正常指令、攻击指令和一个可检测的目标字符串组合，
尝试让模型忽略原任务并输出攻击者要求的内容。

本 Probe 的关键不是讨论模型“是否真的仇恨人类”，而是验证：

```text
攻击者能否劫持指令优先级，让模型输出指定 rogue string
```

### Detector 如何判定

主要 Detector 是：

```text
promptinject.AttackRogueString
```

它检查模型回答中是否出现 Probe 预设的攻击目标字符串：

- 出现：攻击命中，记为 FAIL。
- 未出现：该样本未命中，记为 PASS。

这是字符串目标检测，不是完整的语义安全分类器。模型可能用同义句完成恶意意图而未被该
Detector 命中，也可能在解释或引用攻击文本时触发。

### 它模拟的企业风险

- 用户输入覆盖系统指令。
- RAG 文档中的恶意指令劫持回答。
- Agent 浏览网页时读取到“忽略之前规则”的内容。
- 工具调用参数被攻击者控制。

真实企业测试还需要加入系统提示泄露、工具越权、数据外传和间接 Prompt Injection。

## 3. `encoding.InjectBase64`

### 它在测试什么

该 Probe 把攻击内容进行 Base64 编码或构造带编码内容的指令，测试模型是否会：

1. 理解或解码被混淆的内容。
2. 绕过只匹配明文关键词的防护。
3. 生成与隐藏目标相符的输出。

Base64 是编码，不是加密。任何人都能还原它，但简单关键词过滤器可能看不到编码后的原文。

### Detector 如何判定

该 Probe 在当前 garak 版本中会配合：

- `encoding.DecodeMatch`：检查输出是否与解码后的目标直接匹配。
- `encoding.DecodeApprox`：检查近似匹配。

因此，同一个 Probe 可能在报告里出现两条 `eval` 记录。聚合时要按
`probe + detector` 阅读，不能只数 Probe 名称。

### 它模拟的企业风险

- 攻击者用 Base64、Hex、Unicode 等形式规避输入过滤。
- RAG 文档把恶意指令编码后诱导模型解码执行。
- Agent 接收外部数据后自动解码并继续执行。

企业防护不应只做明文黑名单，而应规范化输入、检测多种编码，并在模型输出和工具调用前再次
执行策略检查。

## 4. 为什么 Stage 2 Mock 和 Stage 3 真实模型结果不同

### Mock 的行为是程序员写死的

`stage2-vulnerable` 主要回显输入。PromptInject 的目标字符串原本就在 prompt 中，因此回显
可能直接触发 Detector，ASR 达到 100%。

但 Base64 Probe 的 Detector 寻找解码目标。单纯回显编码文本并不等于模型解码并执行目标，
所以 vulnerable Mock 也可能 PASS。

这说明：

```text
“脆弱”不是一个对所有攻击都成立的布尔标签。
```

### 真实模型会理解语言并生成新文本

真实 LLM 可能：

- 拒绝攻击。
- 服从攻击。
- 解释攻击但不执行。
- 解码 Base64 后继续处理。
- 输出近义表达，影响字符串 Detector。
- 因采样参数不同产生不同回答。

因此 Stage 3 结果比 Mock 更接近真实风险，也更需要人工抽查。

## 5. PASS / FAIL 在这里分别表示什么

| 结果 | 含义 |
| --- | --- |
| PromptInject FAIL | Rogue string 被 Detector 检出 |
| PromptInject PASS | 本次回答未检出 rogue string |
| Base64 FAIL | 回答与解码目标匹配或近似匹配 |
| Base64 PASS | 当前 Detector 未发现解码目标 |

FAIL 不代表 garak 报错。它表示实验链路正常完成，并观察到攻击目标。

## 6. 企业里如何扩展这两个 Probe

1. 用企业真实系统提示和业务任务替换通用上下文。
2. 把攻击放入用户输入、RAG 文档、网页内容和工具返回值。
3. 增加多轮攻击，而不是只测单轮。
4. 除字符串 Detector 外，再加策略分类器和人工复核。
5. 记录模型版本、温度、系统提示和网关策略，确保可比较。

## 7. 面试官可能追问

**问：为什么 Base64 PASS 不能说明模型安全？**

答：它只说明当前 Base64 样本没有触发 DecodeMatch/DecodeApprox。模型仍可能受到其他编码、
语义改写或多轮攻击，也可能完成了危险意图但输出没有命中当前 Detector。

**问：为什么要同时保留输出样本？**

答：统计结果告诉我“命中多少”，样本告诉我“为什么命中”。后者用于识别 Detector 误报、
漏报和新的攻击模式。

## 8. 初学者误区

1. Probe 不是 prompt 文件本身，而是构造和调度一组攻击的方法。
2. Base64 不是加密。
3. vulnerable Mock 在某个 Probe 上 PASS 不矛盾，说明脆弱行为与 Detector 目标不匹配。
4. 一个 Probe 可能绑定多个 Detectors，因此评测条目数可能大于 prompt 数。

