# Paper 1 第一版 Document Poison Detector 预检报告 V1

## 结论

本轮没有训练模型。Phase A 的输入身份、23-feature parity、72-row parity、R/Oracle 排除、blocking leakage、GT 开发集角色、24 个 matched groups、24-fold LOGO 和每条候选恰好留出一次均通过；唯一 blocking gate 是 missingness policy。

`host_publisher_relation` 与 `publisher_issuer_match` 在冻结矩阵的 72 行全部为 null，对应 availability 全部为 `INPUT_MISSING`。因为训练折中不存在任何已观察值，所以无法计算 mode；Feature Set V1 也没有定义 neutral value。将它们填成 0/-1、删除两列或新增 missingness indicator 都会改变已经冻结的 23-feature/missingness 合同。

最终状态：

```text
PHASE_A_BLOCKED
PHASE_B_NOT_AUTHORIZED
TRAINING_STARTED = FALSE
HUMAN_DECISION_REQUIRED
Auto Continue = NO
```

## 已通过的预检

- Feature Matrix SHA256：`c1a8dfa250ab62843d9234754f27936667c2a760dbdae8be4f5405bb47dc30c0`。
- Feature Set SHA256：`585350c79d014997f649532549703aa57950e2cd35c724fbd9025442db01ce06`。
- Final72 GT SHA256：`9e6224ef2cb2cb8e729f9ab569d09589c951e6df4ed3327c63c82913066d720a`。
- 23 features：S=3、E=9、P=8、T=3；R 与 6 个 Oracle-only Temporal features 均未进入。
- 72 rows、24 groups、24/24/24 Clean/Poison/HN；24 LOGO folds，每折 train=69、validation=3。
- Feature matrix 内 direct/proxy/process/ID/path/label fields 为 0。
- Missingness policy 在加载 class/group/GT 之前物理锁定。
- LR 配置固定且未执行 grid/manual tuning、threshold tuning 或 calibration。

## 未生成的结果

因为 Phase B 未获 gate authorization，以下 artifacts 和指标均不存在：OOF predictions、AUROC、AUPRC、precision/recall/F1、balanced accuracy、HN-FPR、matched margins、view/ablation、coefficient、bootstrap、permutation control。报告 `N/A — NOT EXECUTED` 比伪造数值更符合当前合同。

## Owner 决策选项

1. **推荐：upstream additive repair。** 补充合法 provenance inputs，生成 versioned Feature Matrix V2，再重新预检。科学边界最清晰，但工作量最高。
2. **仅工程诊断：明确授权全局 all-missing constant representation。** 必须版本化 missingness contract，并证明两列恒定、无预测信息；成本低，但改变 V1 语义。
3. **冻结 21-feature V1.1。** 明确排除两列并重建 Feature Set；透明但改变 23-feature/视角预算。

在 Owner 选择前，只允许证据、治理和 Git 收口；禁止任何 Detector fit 或后续实验。
