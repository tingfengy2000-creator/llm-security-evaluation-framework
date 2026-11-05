# C 门严格证明复核

**`STRICT_TOKEN_BOUND_UNPROVEN`，0/108 格取得证明。** 已逐格复算冻结 V2 完整 system/user 内容的 UTF-8 字节，最大 2,444、总 199,427。4096 是项目输入门。官方对固定快照的非思考最大输入长度为 991,808 tokens，约为项目门的 242 倍。它只能用于模型尺度判断，无法从字节数推出服务实际用量。[固定快照说明](https://www.alibabacloud.com/help/en/model-studio/qwen3-7-plus)

可成立的条件式证明为：如果该快照采用一字节原子、仅合并非空片段的 byte-level BPE，且服务端规范化不扩张原文本，那么每条消息内容的 token 数至多等于 UTF-8 字节数。另计服务端聊天模板的角色、分隔符、前后缀及隐式指令 token。最大输入只给 framing 或额外内容留 **1,652 tokens**，需要有证上限才能推出 4,096。公开 Qwen3 概念页支持其 BPE 思路，但未将同一 tokenizer 或聊天模板绑定到此闭源 API 快照。本机已知固定资料也未提供这两个证明。若 provider 还添加 1,653 个额外 token，字节原子最坏情形即可越门。原 `UTF8+512` 最大 2,956 属于规划值。[Qwen3 tokenizer 概念](https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md)

更保守的离线诊断 `2×UTF8 + 1024` 最大 5,912，84/108 超过 4,096。它同时容纳字节扩张与更大模板余量，仍属于假设，不能用于准入。私有逐格 `TOKEN_RECOVERY_PRIVATE.json` SHA256 `9607427327265e14d8d6d5ffcc7687d6947c2f539b420144271529191737ccae`，严格字段全部为 null。若无法提供同源证明，当前门保持阻断，风险路径仅供 Owner 另行裁决。[待审替代方案](C_GATE_RISK_ACCEPTANCE_OPTION.md)
