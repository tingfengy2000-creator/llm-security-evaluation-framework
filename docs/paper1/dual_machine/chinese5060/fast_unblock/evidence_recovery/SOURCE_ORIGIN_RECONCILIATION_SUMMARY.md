# Pilot12 来源追溯摘要

**46/46 个待发送文档的字节身份已恢复。** 原先 17 个匹配 `SOURCES.json`，另 29 个均从已签署的 D1 开发候选正文恢复，文档身份未知 0。检查以原 P2 seal 指向的 36 份 chunk 和 36 份 TopK 为准，逐世界对齐 PAIR01 的 G1/G2 保留片段，再对齐 108 格 V2。381 次片段出现全部复核，29 个 D1 候选正文分别出现在 29 个世界，合计 75 个请求格、75 次片段出现。来源相同的片段也逐次核对原 rank 和字符区间。

| 证据分类 | 数量 | 可复用依据与仍缺材料 |
| --- | ---: | --- |
| `OFFICIAL_LEGAL_NORM_TEXT` | 15 | 角色盲官方快照、出处与正文属性可核。著作权法第 5 条仅适用于可确认的法规或国家机关文件正文，页面编排、解释、个人信息和处理范围需独立判断。 |
| `OFFICIAL_EXPLANATORY_OR_OTHER_WEB` | 2 | 官方出处可追溯，现有记录不足以将整个快照归为第 5 条正文。 |
| `OWNER_CREATED_OR_LICENSED_SYNTHETIC` | 0 | 未取得足以确认此类别的个人创作、转授或当前许可记录。 |
| `UNKNOWN_OR_RESTRICTED` | 29 | `CANDIDATES_ONLY_V1.jsonl` 与原 F5 中的候选正文字节一致，签署范围为 `D1_DEV_ONLY`。可证明它们是冻结项目候选及 P1/P2 的注入位置，正文生成前的作者/原 URI/编辑链和本 Pilot 的处理权仍缺可核材料。 |

29 个原未匹配项的完整连接为签署清单 → 原候选正文 → F5 同一正文 → P1 生成的 `source_id` 和 `parent_doc_id` → P2 逐字符 chunk → V2 请求。签署清单、原候选、F5、P2 与 PAIR01 SHA 见 QA。17 个背景快照也都与旧 F5 evidence 正文字节吻合。因此两类文本都可复用旧北京 D1 验证的来源证据。旧运行授权的处理目的为历史事实核验，当前 Pilot12 的 query/TopK 和处理范围仍须确认。六类模式筛查曾为 0 命中，语境敏感性与外传范围等待合并复核。

私有 `SOURCE_ORIGIN_RECONCILIATION_PRIVATE.json` SHA256 `21db4e4feebf39df6410ae4b2954542b5c2e30d3bf176f9b8c8e105122e05a26`，记录源哈希、原 URI 或候选根证、每次世界/请求/rank/片段哈希及签署范围。只需一次合并裁决冻结 108 格是否可交已确认地域和处理方，优先补充 29 个 D1 项目的创作/使用依据和 2 个官方网页的使用范围。[著作权法第 5 条](https://www.ncac.gov.cn/xxfb/flfg/flfg_532/202103/t20210309_50530.html) · [复核 QA](FINAL_EVIDENCE_RECOVERY_QA.json)
