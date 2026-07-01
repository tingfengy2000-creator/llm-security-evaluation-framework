# 输入与输出 Guard 规则

## 1. 规则目标

规则不是判断“文本是否邪恶”，而是判断是否出现本实验关心的攻击信号。每条命中返回稳定规则名，
便于日志统计和消融。

## 2. 输入侧 Prompt Injection

主要规则：

```text
prompt_injection.ignore_previous
prompt_injection.nevermind
prompt_injection.system_prompt
```

示例信号：

- ignore previous instructions
- disregard prior rules
- nevermind
- reveal the system prompt

Stage 3 的 PromptInject 样本同时命中 `nevermind` 和 `ignore_previous`，因此 guarded/input-only
会在调用 Groq 前返回拒绝 completion。

### 为什么规则有窗口限制

正则使用“关键词之间最多相隔若干字符”，避免：

- 只要文章同时出现 ignore 和 instruction 就误报。
- `.*` 跨越超长文本导致性能和误报问题。

但窗口规则仍可被分词、同义改写和多语言绕过。

## 3. 输入侧 Jailbreak

主要规则：

```text
jailbreak.developer_mode
jailbreak.dan
jailbreak.bypass_safety
```

示例：

- enable developer mode
- you are DAN / do anything now
- bypass safety policy

Jailbreak 和 Prompt Injection 有交集：

- Prompt Injection 强调覆盖现有指令层级。
- Jailbreak 强调让模型脱离安全与行为约束。

企业分类可以分开，但最终可能由同一个策略动作处理。

## 4. Encoding Bypass

流程不是“看见 Base64 就拒绝”，而是：

```text
识别 Base64 候选
  -> 严格解码
  -> 检查可打印比例
  -> 检查解码后危险模式
```

危险模式包括：

```text
<script
javascript:
alert(
<?php
解码后的 instruction override
```

所以：

- `SGVsbG8gd29ybGQ=` 解码为 Hello world，允许。
- Stage 3 Base64 攻击解码后包含 script/javascript/alert，拦截。

这比“任何 Base64 都拦截”误报更少，但仍只处理单层标准 Base64。

## 5. 输出侧规则

```text
output.rogue_hate_string
output.script_payload
output.prompt_leakage
```

用途：

- 捕捉 PromptInject 的 rogue string。
- 捕捉模型生成的 XSS/脚本载荷。
- 捕捉明显的 system/developer prompt 泄露表述。

命中后，Proxy 替换最终 `choices[0].message.content`，但保留 completion 结构。

## 6. 输入和输出为什么都要有

输入侧优势：

- 明显攻击不调用上游，节省额度。
- 危险内容不进入模型上下文。

输入侧局限：

- 攻击可通过改写绕过。
- 无法判断模型最终是否真的会服从。

输出侧优势：

- 能拦截输入规则漏掉、但模型实际生成的危险内容。

输出侧局限：

- 已经产生模型调用成本。
- 对 Agent 来说，工具副作用可能已经发生。
- 输出替换可能影响正常代码、教育和安全研究内容。

## 7. 阈值与动作

当前规则是布尔命中：

```text
任一高风险规则命中 -> block
```

没有风险分数、用户角色、业务场景和例外策略。这正是它只能叫 baseline 的原因。

生产策略更可能是：

```text
rule/classifier signals
  -> policy engine
  -> allow / redact / ask confirmation / block / human review
```

## 8. 最容易误解

- Base64 检测不是“解码即危险”，要看解码内容。
- 输出 Guard PASS 不证明输出语义安全，只说明规则未命中。
- refusal 由 Proxy 生成，不是 Groq 的自然安全能力。
- 规则命中率不能替代最终业务风险评估。

