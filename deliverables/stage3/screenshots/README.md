# Stage 3 截图目录

建议保存以下证据：

1. `01_safe_run_terminal.png`：安全版命令、garak 版本和运行结果。
2. `02_promptinject_report.png`：PromptInject HTML 报告。
3. `03_base64_report.png`：Base64 HTML 报告。
4. `04_summary.png`：`groq_scan_summary.md`。

安全规则：

- 不截图 Key 设置命令。
- 不执行或截图 `$env:GROQ_API_KEY`。
- 不截图 Groq Console 的 Key 页面。
- 截图前检查终端、路径和浏览器开发者工具是否显示 Authorization header。

截图是展示材料，不是原始审计证据。原始证据保存在 `runs/` 的 JSONL 和 HTML 中。

