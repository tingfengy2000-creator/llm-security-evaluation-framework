# Stage 6 RAG 攻击矩阵数据

本目录提供一个完全虚构、模型无关的检索安全评测语料。数据只模拟非破坏性的知识库污染与上下文干扰，不包含真实凭据、工具调用或破坏性操作。

## 文件说明

- `queries/attack_queries.jsonl`：R1-R6 各两条攻击查询。攻击只通过 `retrieval_query` 或被检索文档生效；`generation_question` 始终是干净的业务问题。
- `queries/benign_queries.jsonl`：十条基线查询。
- `documents/clean_docs.jsonl`：可信的虚构政策与流程文档。
- `documents/poisoned_docs.jsonl`：R2-R6 各两条用于评测的检索干扰文档。公开记录仍严格使用 `DocumentRecord` 的七个字段。
- `documents/corpus_manifest.json`：公开文件的版本、记录数、SHA-256 与模型无关来源说明。
- `ground_truth/query_labels.jsonl`：仅供评测器使用的查询风险目标与预期行为。
- `ground_truth/document_labels.jsonl`：仅供评测器使用的文档判定与攻击目标。

## 标签隔离

公开加载器只读取 `queries/`、`documents/` 和公开清单，绝不打开 `ground_truth/`。Retriever 只能接收 `PublicRAGDataset`。评测标签中的 `poisoned`、`attack_goal` 等字段被物理隔离在 sidecar 文件中，不能进入公开文档或查询元数据。

本数据集不测试系统消息或直接提示注入。R1 只改变检索字符串，R2-R6 只依赖检索到的语料；生成问题本身不携带检索标记或攻击指令。

## 哈希再生成

修改任意文档内容后，先对 `content.encode("utf-8")` 计算 SHA-256 并更新该记录的 `content_hash`，再对四个公开 JSONL 文件的原始字节计算 SHA-256，最后同步更新 `corpus_manifest.json` 的 `sha256` 与非空行 `count`。文件采用 UTF-8、每个非空行一个 JSON 对象，行顺序固定。

## 结论边界

这些样本只支持对本目录所定义的六类检索风险进行可复现比较。结果不能外推为对所有 RAG 系统、模型、领域或真实攻击的完整安全证明，也不能把公开字段当作评测真值。
