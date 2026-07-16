# Stage 2：OpenAI-compatible Mock API

目标：把评测工具与模型随机性分离，理解 vulnerable/guarded 对照。

- 学习顺序：先读 Stage 1，再阅读 [Stage 2 交付物](../../deliverables/stage2/)；
- 代码：[历史脚本与 Mock 服务](../../llm-security-stage1/scripts/)；
- 数据：[Stage 2 结果与说明](../../deliverables/stage2/)；
- 复跑入口：以 [Stage 2 命令记录](../../deliverables/stage2/) 为准；
- 原始证据：[deliverables/stage2](../../deliverables/stage2/)；
- 结论边界：Mock 用于控制变量和接口验证，不代表真实模型安全性；
- 面试重点：解释 OpenAI-compatible、`/v1/chat/completions` 与对照实验的价值。
