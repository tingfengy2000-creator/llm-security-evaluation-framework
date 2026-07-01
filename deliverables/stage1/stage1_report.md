# Stage 1 阶段报告：garak 最小安全扫描

## 阶段目标

本阶段只完成 Stage 1，不实现后续阶段。目标是建立一个可复现的本地项目骨架，初始化 Python 环境，安装并运行 garak，并使用 mock model 跑通最小安全扫描，形成命令记录、结果文件和阶段报告。

## 已完成交付

- 项目目录：`D:\llmProject\llm-security-stage1`
- Python 虚拟环境：`D:\llmProject\llm-security-stage1\.venv`
- Python 版本：`Python 3.12.13`
- garak 版本：`garak 0.15.1`
- 运行脚本：`D:\llmProject\llm-security-stage1\scripts\run_stage1_scan.ps1`
- 命令记录：`D:\llmProject\llm-security-stage1\docs\run_commands.md`
- 结果目录：`D:\llmProject\deliverables\stage1`

## 扫描设计

本阶段使用 garak 内置 mock generator，而不是外部真实 OpenAI-compatible API。这样可以避免 API Key、网络和计费因素干扰，先验证评测链路本身。

扫描 1：最小连通性验证

- Generator：`test.Blank`
- Probe：`test.Blank`
- Detector：`any.AnyOutput`
- 结果：`PASS score 1/1`
- 作用：确认 garak 可以启动、加载插件、生成报告并落盘。

扫描 2：Prompt Injection mock 基线

- Generator：`test.Repeat`
- Probe：`promptinject.HijackHateHumans`
- Detector：`promptinject.AttackRogueString`
- 结果：`FAIL score 0/256`
- Attack success rate：`100.00%`
- 作用：用 echo 型 mock model 构造一个不具备防护能力的基线，证明 garak 的安全探针和 detector 能记录风险命中。

## 结果文件

- `D:\llmProject\deliverables\stage1\stage1_min_scan.report.jsonl`
- `D:\llmProject\deliverables\stage1\stage1_min_scan.report.html`
- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.report.jsonl`
- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.report.html`
- `D:\llmProject\deliverables\stage1\stage1_promptinject_scan.hitlog.jsonl`

## 关键结论

1. Stage 1 工具链已经跑通：项目目录、虚拟环境、garak 安装、插件加载、扫描执行、结果落盘均已验证。
2. `test.Blank` 连通性扫描通过，说明基本执行链路正常。
3. `test.Repeat` 在 prompt injection 探针下 100% 命中风险，这是预期结果，因为 echo 型 mock model 会复述注入指令。
4. 当前结果不能代表真实大模型安全水平，只能作为 Stage 1 的工程基线和评测链路验证。

## 环境处理说明

当前运行环境对默认用户配置/缓存目录存在写入限制。为保证可复现，Stage 1 将 garak 的 XDG 目录固定到：

- `D:\llmProject\deliverables\stage1\xdg_config`
- `D:\llmProject\deliverables\stage1\xdg_data`
- `D:\llmProject\deliverables\stage1\xdg_cache`

同时在本项目虚拟环境中做了兼容性调整，使 garak 使用工作区内目录和包内插件缓存。这些调整只影响当前 `.venv`，不会修改全局 Python 环境。

## 下一阶段计划

Stage 2 建议聚焦“真实目标接入与基线扩展”：

1. 接入一个真实 OpenAI-compatible API，明确模型名、base URL、鉴权方式和调用成本控制。
2. 建立 `config/` 配置文件，避免命令行直接暴露敏感参数。
3. 扩展 probes 到 RAG/Agent 常见风险：prompt injection、system prompt extraction、data exfiltration、jailbreak、tool misuse。
4. 设计最小 RAG 测试样例，包括恶意文档注入、检索上下文污染、引用伪造与敏感信息泄漏。
5. 输出 Stage 2 报告模板，增加风险分级、复现步骤、命中样例、修复建议和复测字段。
