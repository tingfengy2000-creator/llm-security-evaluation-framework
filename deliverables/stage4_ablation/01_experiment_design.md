# Stage 4.1 实验设计

## 1. 控制变量

四组固定：

- 模型：`llama-3.1-8b-instant`
- Probe：`promptinject.HijackHateHumans`、`encoding.InjectBase64`
- garak seed：42
- 每个 Probe 最多 1 条 prompt
- generations：1
- 并发请求和 Attempt：1
- 相同 OpenAI-compatible Proxy 接口和生成参数

唯一主动变量是 Input Guard 与 Output Guard 是否执行拦截。

## 2. 为什么不是直接比较四次不同扫描

随机抽样或 prompt 不一致会让 ASR 差异失去可归因性。runner 从四组 JSONL 中提取
`probe + prompt_sha256`，排序后逐组比较：

```text
prompt_hash_parity = true
```

只要有一个 hash 不同，整个实验状态就是 `invalid`。

## 3. 四组回答的问题

### passthrough

输入和输出规则只检测、记录，不执行动作。它回答无防护时模型如何响应。

### input-only

只执行输入拦截。它回答攻击进入模型前能否被阻断，以及能节省多少上游调用。

### output-only

输入侧必须放行，真实调用 Groq。模型回答后先保存原始输出 hash，再由 Output Guard
判断是否替换。它回答输出层能否独立兜底。

### full-guard

输入与输出都启用。内部映射到历史实现 `guarded`，但新增产物统一写 `full-guard`。

## 4. 科学有效性门禁

下列任一情况使实验成为 `invalid`：

- 四组 prompt hash 不一致。
- 任一组报告或 Attempt 不完整。
- 日志缺少必需字段。
- output-only 没有调用 Groq。
- output-only 发生输入拦截。
- output-only 调用 Groq 后缺少 `original_model_output_hash`。
- 危险输出命中规则但没有被 Output Guard 替换。

`invalid` 与 `failed` 不同：`invalid` 表示程序可能跑完，但不满足可信比较条件；
`failed` 表示 API、进程或解析过程没有完成。

## 5. 日志字段

每条请求至少记录：

```text
input_guard_enabled
output_guard_enabled
upstream_called
input_blocked
output_blocked
final_decision
original_model_output_hash
```

同时记录实验名称和内部模式。API Key、Authorization 和完整危险输出不会进入日志。
