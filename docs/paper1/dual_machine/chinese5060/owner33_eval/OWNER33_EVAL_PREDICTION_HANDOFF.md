# Paper 1｜Owner33 V-CARE 一次性独立预测交接

2026-11-11 JST · `PREDICTION_SEALED / 32_OF_32 / AWAITING_5090_PRIVATE_SCORE / NO_RERUN`

依据 5090 公开交接提交 `11242cc6613a0ec3f53332255d0e19de941273a3` 和 5060 已推送的方法冻结 `11880c5be71e22d73217c32e0c779fbf8b117741`，实际完成唯一一次预测，32 个世界、352 段，四组新事实各八世界。固定 MiniLM、原 RAGDefender p=2/m=5、B2/ZH、Chroma cosine 及 96/16 分块，32 个独立索引均经同一后端重开验证。无 5090 私有 Gold 读取。

## 预测结果及边界

| 项目 | 实际 |
| --- | ---: |
| 完成世界 / 原计划 | 32/32 |
| TopK5 槽位 / 八臂掩码 | 160 / 256 |
| V-CARE 与 B2 或等预算 B2 的掩码差异 | 0/32 |
| V-CARE 与 no-scope 或 no-rescue 的掩码差异 | 0/32 |
| V-CARE / 等预算 B2 逻辑补检 | 32 / 32 |
| V-CARE 外证命中 / 新增证据槽 | 0 / 0 |
| 方法识别出支持谓词的查询 | 0/32 |

12 条带验证 HTTPS 回执的公开目录记录来自四个选中法源谱系。冻结版 V-CARE 的查询解析覆盖节假日、卫生许可和限定驾驶证申请，无法从四个新事实组抽取既有索引意图。对所有新查询按原算法回退至 B2。没有把 5090 的资料手填进旧谓词，也没有借此次对接修改 V-CARE。方法增益要求已被掩码完全相同这一事实排除。候选级 P/C/HN/B 绝对数由 5090 在自己的封存标签上单次计算，5060 未评分。

机械适配沿用公开段 ID 与原正文，原查询唯一的 ISO 日期只用于日期接口。只为既有向量后端建立不透明来源别名，未生成谓词、改写查询或调整排序。预测前两次工程核验分别发现原解释器缺 psutil 和历史公共 schema 的 CRLF 字节差。去除适配器对无关 psutil 的传递依赖，校验历史 schema 仅换行差异。新方法源码与冻结 Git 对象仍逐字节一致。Ruff、MyPy、准入和唯一预测均通过，预测退出码 0，耗时 54.703 秒，运行目录 13,155,939 字节，API 和模型下载 0。

## 给 5090 的评分入口

[盲预测](OWNER33_EVAL_PREDICTIONS_ROLE_FREE.json) 每世界含原 `world_id`、5 个有序原 `passage_id`、块哈希和相似度，以及八臂零基秩掩码。掩码 0 指排名 1，依此类推。[TopK 封存](OWNER33_EVAL_TOPK_SEAL.json) 含各世界原 packet SHA。[预测封存](OWNER33_EVAL_PREDICTION_SEAL.json) 绑定输入、方法、证据索引和两份输出。只按私有原标签评分一次，记录同一召回分母和正式 `METHOD_EVAL_NO_GO` 裁决。请保留 Human Gold 0 和正式 ASR/Accuracy 未测。 [Run Manifest](OWNER33_EVAL_PREDICTION_RUN_MANIFEST.json)
