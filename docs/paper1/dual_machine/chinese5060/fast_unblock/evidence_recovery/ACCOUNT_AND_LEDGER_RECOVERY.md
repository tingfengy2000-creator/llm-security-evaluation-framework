# 百炼账户与账本复用

**已恢复历史北京 Workspace 的完整 Host。** 从旧 `D1-DEV-BEIJING-CONT-A01/CONFIG_LOCK.json` 按既有 seal 核验字节，确认 `cn-beijing`、HTTPS 专属 Workspace、OpenAI 兼容路径、固定模型及当时处理授权。真实 Host 和 Workspace ID 仅落入 D 盘 `ENDPOINT_PRIVATE.json`，SHA256 `3e84064dbfdcbb13e4d3d5213c3d85158898073bc01e8b41b8067370ddb31882`。本轮固定配置位置和命名环境变量未出现新的地域/Host 绑定。若本 Pilot 继续用该 Workspace，只需确认复用，无需再提供地址或凭证。[百炼 Base URL](https://www.alibabacloud.com/help/en/model-studio/base-url) · [地域与工作空间](https://www.alibabacloud.com/help/en/model-studio/regions)

| 证据等级 | 实际恢复 |
| --- | --- |
| `VERIFIED_ACCOUNT_LEDGER` 的历史用量子账 | 旧 seal 索引中的 361 个预留均有收据。历史输入 2,984,761、输出 205,288，按原费率重算 CNY 7.611826，历史未配对预留 0；1 项异常已有收据，保留在总额内。历史估算尚未与正式账单对账。 |
| `OWNER_ATTESTED_PRIVATE_VALUE` | 复用 Owner 历史 CNY 7.528095914，差额 CNY 0.083730086 不冲销；当时未结算与可用状态声明保留。当前账户确认仍为 Owner attestation，旧 USD 保守换算不作为当前 FX。 |
| `PUBLIC_LIST_PRICE_REFERENCE` | 北京固定快照 256K 以内输入/输出每百万 2/8 CNY，上一档至 1M 为 6/24。108×4096 输入加 108×266 输出，20% 预留后按公开原价算 **CNY 1.337472**。266 是含官方文档可能 10-token 偏差的候选，当前账户账单封顶及折扣未绑定。 |

实际启动要用当前统一账本和日期有效的换算将全线已结算、未结算/失败在途及整批预留折合 USD。25 预警、28 不开新批、30 硬限，余额或有界可用资金覆盖全部未结算和预留。现有历史账可作期初，不从中推断现时余额、pending 或剩余美元。当前机器证据缺项只需一份受控汇总，字段为 **复用 Workspace 确认、计费档及 266 语义依据、结算/在途、可用资金或有界承诺、适用 FX 和时效**。原账本未更新或覆盖。

私有 `ACCOUNT_AND_LEDGER_RECOVERY_PRIVATE.json` SHA256 `63511193ce83635db8a53fb3b5d98361db793969de4aed29a8217a206f57c9b1`。[北京公开费率](https://help.aliyun.com/zh/model-studio/model-pricing) · [V2 字段文档](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions) · [复核 QA](FINAL_EVIDENCE_RECOVERY_QA.json)
