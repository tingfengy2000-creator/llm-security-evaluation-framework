# Stage 4.1 局限性

## 1. 样本量

当前只有两个 Probe、每个 Probe 一条 prompt。这是链路和机制 smoke test，不能估计生产环境
防护率，也不适合给出稳定置信区间。

## 2. Rule-based Baseline

当前规则依赖正则、关键词和 Base64 解码，可能被以下方式绕过：

- 同义改写和隐喻。
- 多语言攻击。
- 字符插入、分词和 Unicode 混淆。
- 多层编码或非 Base64 编码。
- 多轮渐进式攻击。
- 业务上下文中的间接 Prompt Injection。

## 3. 误报

全部拦截会降低 ASR，但也可能阻断正常安全研究、代码审计或编码教学请求。Stage 4.1
没有扩大攻击样本，也没有加入正常流量集，因此不能评价误报率和任务可用性。

## 4. Detector 局限

garak PASS 只表示所选 Detector 没有命中。Stage 4 已出现 Base64 Detector PASS、
模型却输出脚本载荷的案例，因此必须联合查看 Guard 规则、原始输出 hash 和人工复核。

## 5. Output Guard 的边界

Output Guard 能替换用户可见文本，但不能撤销模型生成期间已经触发的 Agent 工具调用、
外部写操作或数据发送。生产 Agent 还需要工具权限、参数校验、确认机制和上下文隔离。

## 6. 后续方向

在本阶段理解完成后，可比较分类器、LLM-as-judge 和策略引擎，并补正常样本误报率。
本阶段不进入 RAG，不把后续方向写成已实现能力。
