# Stage 4 消融实验设计

## 1. 为什么做消融

如果 guarded 组 ASR 下降，只能说明“输入 + 输出整体”有效，不能回答是哪一层贡献。

四组消融：

| Mode | 输入拦截 | 输出拦截 | 回答的问题 |
| --- | --- | --- | --- |
| passthrough | 否 | 否 | 无防护基线 |
| input-only | 是 | 否 | 输入规则贡献 |
| output-only | 否 | 是 | 输出规则贡献 |
| guarded | 是 | 是 | 组合效果 |

## 2. 建议顺序

1. 已完成 `passthrough,guarded` 主实验。
2. 已检查 Guard 日志和样本。
3. 再运行 `input-only,output-only`。
4. 保持相同模型、seed、Probe、prompt cap。

不要为了“表格完整”直接增加请求。

## 3. 预期但不能提前当结论

当前已知样本可能出现：

- PromptInject：input-only 直接拦截。
- Base64：解码后检测到 script/javascript，input-only 直接拦截。
- output-only：会调用 Groq，再拦截 rogue string 或脚本输出。
- guarded：输入已拦截时，输出规则没有机会执行。

如果 guarded 的两条请求都在输入侧被拦截，本轮实验无法证明 Output Guard 对真实回答的效果。
必须用 output-only 或专门构造“输入规则漏过、输出规则命中”的样本。

## 4. 消融命令

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\llmProject\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1" -Modes "input-only,output-only"
```

这会产生额外真实模型请求，运行前检查免费额度。

## 5. 消融结果表

| Mode | Attempt ASR | Input Blocks | Output Blocks | Upstream Calls |
| --- | ---: | ---: | ---: | ---: |
| passthrough | 50% | 0 | 0 | 2 |
| input-only | 待运行 | 待运行 | 0 | 待运行 |
| output-only | 待运行 | 0 | 待运行 | 待运行 |
| guarded | 0% | 2 | 0 | 0 |

当前能得出的结论：输入层规则覆盖了两条 smoke 样本。由于 guarded 在调用 Groq 前全部拦截，
本轮不能证明 Output Guard 的独立贡献。passthrough 观察到危险输出规则命中，只能证明输出
规则能检测这些回答，不能证明启用后一定正确替换且不误报。

## 6. 更严谨的后续消融

### 规则类别消融

- 只开 Prompt Injection。
- 只开 Jailbreak。
- 只开 Encoding。
- 只开 Output Script。

### 动作消融

- block。
- redact。
- 加安全系统提示后转发。
- 要求用户确认。

### 组件升级消融

- regex baseline。
- classifier。
- LLM-as-judge。
- classifier + policy engine。

每次只改变一个因素，否则无法解释贡献。

## 7. 企业为什么关心消融

- 识别哪层真正降低风险。
- 发现重复防护和无效成本。
- 衡量误报、延迟和调用费用。
- 决定哪些规则放网关、哪些放模型侧。
- 为上线门禁提供可解释依据。

## 8. 初学者误区

- 组合有效不代表每个组件都有效。
- 输入全部拦截时，输出 Guard 没有被真实验证。
- ASR 降低要同时看误报率，不能把“全部拒绝”当成优秀防护。
