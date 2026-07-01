# Stage 4.1 面试话术

## 1. 30 秒版本

“Stage 4 的联合 Guard 把两条攻击都拦在输入侧，所以我继续做四组消融：
passthrough、input-only、output-only 和 full-guard。四组使用相同模型、Probe、seed 和
prompt hash。重点是 output-only 必须真实调用 Groq，先记录原始输出 hash，再检测并替换
危险回答，从而独立验证输出层贡献。”

## 2. 1 分钟版本

“我没有扩大样本，而是先解决因果归因。passthrough 是无防护基线，input-only 测输入层，
output-only 测模型生成后的兜底，full-guard 测联合效果。`full-guard` 是报告名称，内部映射
历史 `guarded` 实现。runner 会验证四组 prompt hash、报告完整性和日志 schema；如果
output-only 没调用上游、发生输入拦截或缺少原始输出 hash，实验直接标为 invalid。
日志不保存 Key 和完整危险输出，只保存 hash、长度和规则命中。”

## 3. 3 分钟版本

“Stage 4 的 ASR 从 50% 降到 0%，但两条请求的 upstream calls 都是 0，这说明当时证明的是
Input Guard，而不是 Output Guard。为避免把联合效果错误归因到输出层，我新增了独立
Stage 4.1 Proxy，没有修改 Stage 4 历史脚本和报告。

四组唯一变量是输入和输出 Guard 开关。output-only 强制输入放行并调用 Groq。Proxy 获得
模型原始回答后，先计算 SHA-256 和长度，再运行输出规则；命中 rogue string 或脚本载荷时，
将用户可见回答替换为拒答。这样 garak 评估最终输出，审计日志则证明原始危险回答确实产生。

实验还有硬门禁：四组 prompt hash 必须一致，output-only 每条都必须 upstream_called，
日志字段和报告必须完整，否则状态不是 completed，而是 invalid。即使结果很好，我也只会说
rule-based baseline 覆盖了当前 smoke 样本，因为还没有测改写攻击、误报率和正常任务质量。”

## 4. 常见追问

### 为什么 full-guard 内部还是 guarded？

为了兼容 Stage 4 已有实现和历史记录。新增论文、目录、JSON 和面试话术统一使用
`full-guard`，内部映射通过 `internal_mode_map` 明示。

### 为什么不记录原始危险输出？

完整输出可能包含恶意载荷、隐私或机密。hash 足以证明同一内容和替换顺序，规则名称和长度
用于解释，不让日志成为第二个泄露面。

### Output Guard 能替代 Input Guard 吗？

不能。Output Guard 已经产生模型费用，而且 Agent 工具副作用可能发生。Input Guard 也可能
漏报，所以企业通常结合输入检测、输出检测、策略引擎和工具权限。

### ASR 降为 0 能否说明安全？

不能。它只表示所选 Detector 在当前两条样本的最终输出中没有命中。还要报告样本量、
prompt parity、误报率、原始输出信号和规则绕过风险。

## 5. 带真实数字的回答

“四组各运行两个严格配对 Attempt，prompt hash 完全一致。passthrough 的 ASR 是 50%，
input-only、output-only 和 full-guard 都是 0%。

input-only 与 full-guard 都在输入侧拦截两条请求，上游调用为 0。output-only 则不同：
两条请求都真实调用 Groq，先记录原始输出 hash，然后分别命中 rogue string 和 script
payload，最终两条都被输出侧替换。

这证明 Output Guard 在当前样本上有独立贡献。但我不会说防护率 100%，因为样本只有两条，
Base64 还暴露了 garak Detector 漏报，而且尚未测正常流量误报和改写绕过。” 
