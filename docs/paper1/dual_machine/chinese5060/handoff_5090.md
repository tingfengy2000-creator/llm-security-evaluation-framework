# 5090 脱敏交接请求清单

2026-11-04 JST；当前fetch成功，但`origin/research/paper1-ragdefender-repro-5090`未出现。
该结果只表示当时可见remote引用无此分支，不证明5090没有本地工作。
本线不跨分支合并、不复制未批准代码、不自行派发5090实验，不发送消息给第三方。

需要通过Git提供：

1. Owner批准记录、复现分支完整SHA、上游完整SHA、tag与clean状态。
2. `ragdefender/`库vs`artifacts/`论文执行路径，v0.1.1/v0.2语义与Stage2下标定义；论文/代码多跳公式差异处理。
3. 固定embedding/model id+revision、tokenizer/chunk截断行为、task_type、p/m/阈值、TopK/语料/攻击假设。
4. 原实验是否真的执行、published/reproduced/ported边界；环境lock、命令/flags/stdout/stderr/exit与失败，不只最终数字。
5. 脱敏run manifest/数据许可/输入hash/证据index与archive hash，模型和私有原文不入Git。
6. 可用于中文迁移的确定语义定义，以及哪些中文改动只能算B2、哪些须Owner算法决定。
7. API调用默认0；若非0，必须并入5060统一累计账本，不能另开预算。

已可交接本线P0：指定5060分支、工程执行SHA ca75c381546247ad3377013a75bb21133cc078ed、
run W1-5060-20261104-P0-01、[结果入口](W1_5060_P0_INITIAL_STATUS.md)、[信息权限矩阵](baselines_and_fairness.md)。
从本线读取只能视为工程验证和协议草案，不代表批准Worker启动或接受原论文复现。
