# Stage 6.2：多证据可信检索

## Metadata

- stage_id: `S6.2`
- canonical_name: `Multi-Evidence Trustworthy Retrieval`
- canonical_slug: `stage6_2_trustworthy_retrieval`
- legacy_paths: 无；尚未实施。
- status: `planned`
- objective: 研究多证据聚合、冲突感知重排与低置信拒答。
- source_locations: 未来 `src/llmguard/domains/retrieval/trust/`。
- data_locations: 复用并扩展 Stage 6.1 版本化数据。
- test_locations: 未来 Stage 6.2 测试。
- script_locations: 尚未创建。
- deliverable_locations: 尚未创建。
- evidence_locations: 暂无运行证据。
- conclusion_boundary: 规划不等于生产级可信检索。
- next_stage: `S7 stage7_agent_security`

本阶段以透明基线和研究插件增量实现，不能绕过 RetrievalEvidence 或直接访问 Ground Truth。
