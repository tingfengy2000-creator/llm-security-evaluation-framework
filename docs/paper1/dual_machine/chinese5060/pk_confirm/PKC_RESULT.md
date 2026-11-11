# Paper 1｜PK-CONFIRM 执行结果

**2026-11-12 JST。单次实跑完成，待 5090 独立评分。** 已核对 5090 提交 `092efe9e8626d68a7172b0b3ade6b9f888cbf398` 的三份封存 SHA256，并绑定评审提交 `87864727a5130ec14822852671aebdbc25af429d`。按原片段顺序使用 36 个问题、80 个世界。NONE、冻结 RD_B2 和冻结 QAG 提示词的 QWEN_VERIFY 均产生 80/80 个有效掩码，共 240 个。未核实本机非 Qwen 接口的模型权限与费率，OTHER_VERIFY 跳过。

| 请求 | 成功 / 计划 | 输入 Token | 输出 Token | USD 用量估算 |
| --- | ---: | ---: | ---: | ---: |
| 闭卷两轮 | 72/72 | 3,546 | 159 | 0.001153755 |
| QWEN_VERIFY | 80/80 | 16,025 | 827 | 0.005333427 |
| **合计** | **152/152** | **19,571** | **986** | **0.006487182** |

固定 `qwen3.7-plus-2026-05-26`、temperature 0、非思考，重试 0。核验了 152 个唯一服务请求 ID；单次最大输入 238、输出 24 Token。预留 USD 0.647727024，上限 USD 1。费用为回包用量按公开费率估算。[百炼费率](https://www.alibabacloud.com/help/en/model-studio/model-pricing)

两次闭卷回答在 31/36 题上逐字一致。闭卷正误、K／UNK 有效分母、D3 主门槛及 D1 次门槛均由 5090 评分，当前无 GO／NO_GO 裁决。Human Gold=0。

**评分交接** `PKC_5090_HANDOFF_PRIVATE.zip`（4,317 字节），SHA256 `bef15e1863b1702569e99d44badf6396b76b67e17ad2395462204c07ced0f1b1`。包内 72 条闭卷原话可按原始 `question_id` 与 `repeat` 配对，80 个世界按原始 `world_id` 对接零基保留掩码。答案 SHA256 `fb5e23d0b33ccb842db581941d42d2198b683da9961e803dec5e650bc04b7e17`，预测 SHA256 `18f59b12baf29b1085e153373af0f2910cefd358199c34490e9862d251d97e0e`。原话与逐世界结果留在私有包。

冻结代码 `6cd9f2361f92f5f4e6779055fad4fa1586bce72e`，真实请求计划 SHA256 `a1b540d91691b8d7ba7c4b321b1c6bda9b12f4cc822c0e94b959f90be42d3b77`。Ruff、MyPy、152 格离线模拟、单次运行保护及私有包读回复核通过。
