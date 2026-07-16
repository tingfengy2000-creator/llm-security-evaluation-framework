# A1R Namespace 迁移说明

## 目标

将已完成的 Stage 6 Task 1–3 规范实现从
`codeguarder.stage6_rag` 迁移至 `llmguard.domains.retrieval`，并使旧 import 保持同一对象
identity：

```python
from codeguarder.stage6_rag.contracts import DocumentRecord as OldType
from llmguard.domains.retrieval.contracts import DocumentRecord as NewType

assert OldType is NewType
```

## 依赖方向

```text
llmguard.core
      ↑
llmguard.domains
      ↑
llmguard.compatibility
      ↑
legacy codeguarder facade
```

`llmguard` 不得 import `codeguarder`。旧 facade 只允许导入和 re-export `llmguard` 的公开对象；
不得复制 dataclass、校验逻辑、加载器或攻击矩阵。

## 本轮范围

迁移 Stage 6 Task 1–3 已有的 contracts、schema、attack renderer、attack matrix 与公开/评测
数据加载逻辑。不会创建 Embedding、VectorStore、Retriever、ContextBuilder、EvidenceSignal
计算、Trust、Generator、Evaluator、Runner、ChromaDB 或 Groq 调用。

推荐结构中的 `document.py`、`query.py`、`attack.py`、`dataset.py`、`ground_truth.py` 和
`corpus/` 在当前尚无独立实现。A1R 保留经验证的 `models.py` 与 `attack_matrix.py` 作为唯一
实现，避免为目录外观拆分、复制或制造空模块；后续 S6-T4 及之后按功能增量细分。

## Stage 5 的受保护例外

`src/codeguarder/` 当前还含有 Stage 5 与 Stage 5 Paper 的历史业务实现。它们处于 Stage 1–5
保护范围，直接移动或重写会破坏历史可复现性，且复制会违反“单一规范实现”。A1R 因此只新增
`llmguard` 作为新规范空间、迁移允许的 Stage 6 Task 1–3，并冻结旧 Stage 5 路径。该例外被
精确记录在 rename ledger 和 allowlist；以后所有新增业务代码不得再进入 `codeguarder`。
