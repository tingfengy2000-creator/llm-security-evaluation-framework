# Stage 6.1：隐蔽知识污染检测

## Metadata

- stage_id: `S6.1`
- canonical_name: `Hidden Knowledge Poisoning Detection`
- canonical_slug: `stage6_1_hidden_knowledge_poisoning`
- legacy_paths: 无；尚未实施。
- status: `planned`
- objective: 构建中文隐蔽污染基准与多视角检测。
- source_locations: 未来 `src/llmguard/domains/retrieval/` 插件。
- data_locations: 未来独立版本数据集。
- test_locations: 未来 Stage 6.1 测试。
- script_locations: 尚未创建。
- deliverable_locations: 尚未创建。
- evidence_locations: 暂无运行证据。
- conclusion_boundary: 规划不等于已实现的检测算法。
- next_stage: `S6.2 stage6_2_trustworthy_retrieval`

本阶段只会以 `EvidenceSignal` 的增量扩展接入，不改写 Stage 6 Runner 或泄露 Ground Truth。
