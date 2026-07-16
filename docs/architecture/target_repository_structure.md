# LLMGuard 目标仓库结构

## 规范实现与历史证据分离

```text
src/llmguard/
├── core/
│   ├── contracts/
│   ├── providers/
│   ├── guards/
│   ├── detectors/
│   ├── evaluation/
│   ├── reporting/
│   ├── experiments/
│   └── audit/
├── domains/
│   ├── runtime/
│   ├── retrieval/
│   └── agent/
└── compatibility/
    ├── garak/
    ├── stage1_4/
    ├── stage4_guard/
    ├── stage5/
    └── stage6_rag/

src/codeguarder/       # legacy namespace；Stage 5 历史例外与 Stage 6 facade

stages/                 # 只做导航，不复制代码
experiments/            # 注册表、声明式配置和运行清单
data/                   # 合成/脱敏数据、Ground Truth vault 输入
tests/                  # 单元、集成、回归、泄露与完整性测试
scripts/                # 可复跑入口
deliverables/           # 脱敏报告和学习材料
runtime/                # 可重建运行状态，不进入 Git
provenance/             # manifest、hash、correction ledger
interview_prep/         # 面试复习索引
docs/                   # ADR、研究路线、公开治理
```

## 迁移映射

| 当前资产 | 未来规范位置 | 迁移方式 |
| --- | --- | --- |
| `src/codeguarder/stage6_rag/contracts/` | `src/llmguard/domains/retrieval/contracts/` | A1R 已移动实现，旧路径为 facade |
| `src/codeguarder/stage6_rag/attacks/` | `src/llmguard/domains/retrieval/attacks/` | A1R 已移动实现，保持 R1–R6 |
| 未来 Embedding/Chroma | `src/llmguard/domains/retrieval/embedding/`、`vectorstore/` | 从 S6-T4 起只在新路径实现 |
| 未来 Retriever/Context | `src/llmguard/domains/retrieval/retrieval/`、`context/` | 从 S6-T5 起实现 |
| 未来 Trust | `src/llmguard/domains/retrieval/trust/` | 从 S6-T6 起实现 |
| Stage 5 Paper | `src/codeguarder/stage5_paper/` | 受保护历史源码，不迁移、不复制 |
| Stage 4 Guard | `src/llmguard/compatibility/stage4_guard/` | 未来适配器，不复制 GuardEngine |
| garak | `src/llmguard/compatibility/garak/` | 未来适配器封装调用 |

## 目录职责检查

- `core/` 不含 RAG 专有字段；
- `domains/retrieval/` 不含 Ground Truth 运行时泄露；
- `compatibility/` 不含重复业务实现；
- `stages/` 只包含导航 README；
- `runtime/` 不进入 Git；
- 历史 Stage 1–5 文件保持原路径。
