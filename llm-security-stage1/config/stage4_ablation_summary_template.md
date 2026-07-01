# Stage 4.1 Guard 消融实验摘要

- 状态：`{{STATUS}}`
- 模型：`{{MODEL}}`
- Prompt Hash 完全一致：`{{PROMPT_HASH_PARITY}}`
- 原始运行目录：`{{RUN_DIRECTORY}}`

## 四组统一对比

| 实验名称 | PASS | FAIL | ASR | 上游调用 | 输入拦截 | 输出拦截 | 观察到危险输出 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
{{TABLE_ROWS}}

## 有效性检查

`invalid_reasons`：

{{INVALID_REASONS}}

## 阅读边界

- `full-guard` 是实验名称，内部兼容模式为 `guarded`。
- `output-only` 必须调用 Groq，先记录原始模型输出哈希，再进行输出判断和替换。
- “观察到危险输出”来自 Guard 对原始模型输出的规则检测，用于补充 garak Detector 可能漏报。
- 本实验是两条 smoke prompt 上的 rule-based baseline，不代表生产环境防护率。
- PASS 不代表模型绝对安全，还需检查原始输出哈希、规则命中、误报和正常任务质量。
