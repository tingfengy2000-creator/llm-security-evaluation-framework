# garak 扫描总结

## 实验记录基准

- 参考实验计划：`E:\CodeGuarder\docs\experiment_plan.md`
- 本次实验阶段：Stage 1，garak 最小安全扫描链路验证
- 原始报告目录：`D:\llmProject\deliverables\stage1`

## 本阶段做了什么

本阶段完成了一个最小但完整的大模型安全评测闭环：

1. 创建独立项目目录和 Python 虚拟环境。
2. 安装 garak。
3. 使用 garak 内置 mock model 作为被测模型。
4. 执行两类扫描：连通性扫描和 prompt injection mock 扫描。
5. 生成 JSONL、HTML、hitlog 和 Markdown 总结报告。

## 扫描结果

### 1. 最小连通性扫描

- Target：`test.Blank`
- Probe：`test.Blank`
- Detector：`any.AnyOutput`
- 结果：`PASS score 1/1`
- 解释：模型对空 prompt 返回空输出，detector 没有发现风险。这个扫描主要证明 garak 的运行链路可用。

### 2. Prompt Injection mock 扫描

- Target：`test.Repeat`
- Probe：`promptinject.HijackHateHumans`
- Detector：`promptinject.AttackRogueString`
- 结果：`FAIL score 0/256`
- Attack success rate：`100.00%`
- 解释：`test.Repeat` 会复述输入，因此当攻击 prompt 中包含 rogue string 时，输出也会包含该触发字符串。detector 因此判定攻击成功。这是预期失败，用来证明攻击构造、批量测试和成功判定链路可工作。

## 面试可讲能力

这一阶段可以在面试中讲成四个能力点。

### 1. 如何构造攻击 prompt

garak 的 probe 负责构造攻击 prompt。本阶段使用的 `promptinject.HijackHateHumans` 会把正常任务和恶意覆盖指令组合在一起，例如让模型忽略前后指令并输出特定 rogue string。

面试表达可以这样讲：

> 我没有手写单条 prompt 去碰运气，而是使用 garak 的 PromptInject probe 自动生成一批带有指令覆盖、分隔符干扰和触发字符串的 adversarial prompts。这样攻击样本是批量化、可复现、可统计的。

### 2. 如何调用模型批量测试

garak 的 generator 负责调用模型。本阶段先不用真实 API，而是使用内置 mock generator：

- `test.Blank`：永远返回空字符串，用于连通性验证。
- `test.Repeat`：返回用户输入，用于模拟没有防护的 echo 模型。

本次 prompt injection 扫描一次生成并评估了 256 条攻击样本。后续只要把 target 换成 OpenAI-compatible generator，就可以接入真实模型。

面试表达可以这样讲：

> 我先用 mock model 把评测管线打通，再替换为真实 OpenAI-compatible API。这样能把工程链路问题和模型安全问题分离，避免一开始就被 API key、费用、网络、限流干扰。

### 3. 如何评估模型是否被攻击成功

garak 的 detector 负责判断攻击是否成功。本阶段使用 `promptinject.AttackRogueString`，它会检查模型输出中是否出现攻击 prompt 要求输出的 rogue string。

在 prompt injection 扫描中：

- 总评估样本数：256
- 通过数：0
- 失败数：256
- 攻击成功率：100.00%

面试表达可以这样讲：

> 攻击是否成功不是主观判断，而是通过 detector 做自动化判定。本例里成功条件是输出中包含攻击者指定的 rogue string，所以可以形成明确的 pass/fail 和 attack success rate。

### 4. 如何形成安全扫描报告

garak 自动生成结构化报告：

- `.report.jsonl`：逐条记录 run setup、attempt、detector result、eval 和 digest。
- `.report.html`：可视化总结报告，适合展示。
- `.hitlog.jsonl`：命中样本记录，适合复盘失败案例。

本阶段又额外整理了：

- `garak_install_notes.md`
- `garak_run_commands.md`
- `garak_scan_result.json`
- `garak_scan_summary.md`

面试表达可以这样讲：

> 我把原始扫描日志、结构化结果、HTML 报告和人工总结分开保存。原始 JSONL 保证可追溯，HTML 方便展示，summary 用来解释风险含义和下一步修复方向。

## 结论

Stage 1 已证明我理解并跑通了大模型安全评测的基本流程：

1. 攻击 prompt 由 probe 批量构造。
2. 模型调用由 generator 统一管理。
3. 攻击成功由 detector 自动判定。
4. 最终通过 JSONL、HTML、hitlog 和 Markdown 形成可复现安全扫描报告。

当前结果是 mock 基线，不代表真实模型风险。Stage 2 应接入真实 OpenAI-compatible API，并扩展到 RAG/Agent 场景中的 prompt injection、system prompt extraction、data exfiltration 和 tool misuse。
