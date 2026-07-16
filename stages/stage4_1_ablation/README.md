# Stage 4.1：Guard 消融实验

目标：在相同 prompt 下分离验证 Input Guard 与 Output Guard 的贡献。

- 学习顺序：[实验设计](../../deliverables/stage4_ablation/01_experiment_design.md) → 输出侧分析 → 结果比较；
- 代码：[独立消融 Proxy](../../llm-security-stage1/scripts/guard_proxy_ablation.py)；
- 数据：与 Stage 4 相同的两条 smoke 攻击；
- 安全复跑：`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\llm-security-stage1\scripts\run_stage4_ablation_safe.ps1`；
- 原始证据：[Stage 4.1 交付物](../../deliverables/stage4_ablation/)；
- 结论边界：四组为 `passthrough`、`input-only`、`output-only`、`full-guard`；仅能说明当前两条 smoke 的行为；
- 面试重点：output-only 必须先调用上游、记录原始输出 hash，再做替换。
