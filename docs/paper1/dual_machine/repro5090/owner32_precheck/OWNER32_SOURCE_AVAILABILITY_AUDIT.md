# Owner32 来源可用性预检

状态 `SOURCE_GATE_NO_GO / SOURCE_CURATION_BLOCKED / SCIENCE_NOT_RUN / HUMAN_GOLD=0`。
这是获批前的只读核查。没有新的 DEV 或 EVAL，没有改 Q-CER，没有下载页面，也没有制作正确答案卡。

来源登记取自 5060 提交 `2f8c4c2ebe79d3711cb107519869e7fbf8f1f1b0` 的 `docs/paper1/dual_machine/chinese5060/PUBLIC_VERSION_SOURCE_REGISTER_DRAFT.json`，文件 SHA256 `63253845e0691aa50aacdbae63bd666376c0e6c5f34cb830befa7aa25bd93778`。登记里的 10 条版本记录全部检查。Owner27 私有预测包不在本机，5090 私有标签没有打开，所以没有另抽带角色的删除片段。

可用独立证据 `0/10`。进入下一步需要至少 3 条同时具备可核文档字节、独立读取收据、版本窗口和 scope。当前是 0，来源门关闭。

## 十条记录

下表的时间窗口和 scope 是登记里的未复核元数据，不是新的事实答案。`sealed_record_sha256` 是该条登记原文的哈希。没有一条有官方页面字节哈希。

| 记录 | 版本出处 | 生效 | 替换点 | 可用 | 证据哈希 |
| --- | --- | --- | --- | --- | --- |
| HY-1987 | `https://xzfg.moj.gov.cn/mobile/law/detail?LawID=784` | 1987-04-01 | 2016-02-06 | NO | `d99a79b0389bbd826cf8ac11365572d8d676601bec37d63c5e3f025626de163a` |
|  | scope：条例第二条列举的公共场所，卫生许可须与第八条的场所例外或备案条件合读。 |  |  |  | `8362b3febd7a40ba78e6de92c67962cf4702fe8cdcc3103b14ad1763af986f74` |
| HY-2016 | `https://xzfg.moj.gov.cn/mobile/law/detail?LawID=785` | 2016-02-06 | 2019-04-23 | NO | `2c5717a29ce2334e7e33fa466eca9314312f2e0db06e800b0399ed4af67604fb` |
|  | scope：条例第二条列举的公共场所，卫生许可须与第八条的场所例外或备案条件合读。 |  |  |  | `9a93fa013fe1e047c9da1833287a779de4292c8b29dadc6f53cae5958e81b378` |
| HY-2019 | `https://xzfg.moj.gov.cn/mobile/law/detail?LawID=120` | 2019-04-23 | 2025-01-20 | NO | `f95c8762beccecb3952e7d0c16d9e95168748b9eae727278d7e4c80cf8e06796` |
|  | scope：条例第二条列举的公共场所，卫生许可须与第八条的场所例外或备案条件合读。 |  |  |  | `dadfb1888aafb55e9c5c445fb3a0a5463e96505813b8797a8e66cc23ba8b91cc` |
| HY-2024 | `https://xzfg.moj.gov.cn/mobile/law/detail?LawID=1755` | 2025-01-20 | 未登记 | NO | `b90483d992407924194e34b6225e4d293bbbbdbc1b7f03bcb4f8de5639883c55` |
|  | scope：条例第二条列举的公共场所，卫生许可须与第八条的场所例外或备案条件合读。 |  |  |  | `b3ba5980a682cf361c701a4ac86846c9584f37429bf6f24d0cf0ee21562a2ee8` |
| DRUG-2024 | `https://www.nhsa.gov.cn/art/2024/11/28/art_104_14886.html` | 2025-01-01 | 2026-01-01 | NO | `b62441056db938494133e956bcafc0ad8e26a043a4f14ead08d7191bb2b9da43` |
|  | scope：基本医疗、工伤、生育保险目录；当批续约失败调出的协议期内谈判药单独适用过渡支付。 |  |  |  | `7d4b859c381da59639fadb439eeaab868e098c5ea9da4c38c89b72b3ceb3c329` |
| DRUG-2025 | `https://www.nhsa.gov.cn/art/2025/12/7/art_104_18970.html` | 2026-01-01 | 未登记 | NO | `d199d1a1d5799fc0217df606086aea58457ec18eb8bdd0d937136ebc7fd3d835` |
|  | scope：基本医保目录与商保创新药目录分列。商保创新药目录内药品不由医保基金支付；该批符合条件的调出谈判药另有过渡支付。 |  |  |  | `76c70ab95893a344f957955dfd0e34224ecdfd5e840ce61395fcb3e643bda64b` |
| HOL-2013 | `https://xzfg.moj.gov.cn/mobile/law/detail?LawID=6` | 2014-01-01 | 2025-01-01 | NO | `4725a864faf4249cbef34b43819b587270f7074a4756bc7aa0e05dfc4ff0319f` |
|  | scope：全国法定节假日，第二条适用全体公民，须区分法定天数、年度调休安排及第三条部分公民假日。 |  |  |  | `aaf1abce2547cd6fffa5eb47cd76c0d1c07d999bc297f32572c25c264d37ad39` |
| HOL-2024 | `https://xzfg.moj.gov.cn/mobile/law/detail?LawID=1737` | 2025-01-01 | 未登记 | NO | `f67f7c672c22dd24285ed19c9c198a726bc6587d0e5cd657ab3fd2a25e7a2df3` |
|  | scope：全国法定节假日，第二条适用全体公民，须区分法定天数、年度调休安排及第三条部分公民假日。 |  |  |  | `b846aff5b4e43c317abd25a5c26f126c21730a9b488eba4c9701a9cc5c4020a7` |
| DRV-162 | `https://gat.hubei.gov.cn/bmdt/ztzl/2021n/jgywzl/zcfg/202201/t20220111_3959754.shtml` | 2022-04-01 | 2025-01-01 | NO | `affb2a45d30ecd45bd2a0d812eb3e8a966c56de6ccc671a197a80192848d25e7` |
|  | scope：第十四条驾驶证申请的年龄条件，须按准驾车型与申请者类别区分，不延伸到存量持证人年龄条件。 |  |  |  | `9bea6a7c6f7df35238a33d96d7b3a838454d621dc9150deb3eb9c03731316f48` |
| DRV-172 | `https://jtgl.beijing.gov.cn/jgj/jgxx/flfg/gabgz/543498902/index.html` | 2025-01-01 | 未登记 | NO | `14f1a2be419238fd53fa58a9e7e913a526752acdc34ff7222dd8d81d589e1e4a` |
|  | scope：第十四条驾驶证申请的年龄条件，须按准驾车型与申请者类别区分，不延伸到存量持证人年龄条件。 |  |  |  | `f863d4a0560ba8355d2a51995fc900562fae15e15be56473afe23d33b6941a2c` |

## 不能核验的原因

十条原因相同，逐条都成立：

- 权利状态不是 `RIGHTS_CLEARED`，登记写的是 `RIGHTS_UNKNOWN`。因此本次不下载正文，也不做 TLS 读取。
- 出站状态是 `NOT_AUTHORIZED`，访问记为 `NOT_ATTEMPTED`。
- 独立读取收据是 `NOT_FROZEN`。没有可复核的采集收据。
- 登记没有 `document_sha256`，也没有 `tls_receipt_sha256`。现有哈希只覆盖登记文字，不能证明官方页面字节。
- 卫生、节假日和驾驶证三条谱系已经进入 Owner27 开发材料。药品目录没有进入那次运行，但它同样没有冻结的文档字节和独立收据，所以也不能当作未见独立证据。

Owner31 的 32 个虚构世界继续封存，不拿来冒充外部法规证据。

## 只读设计

可用性函数只看一条来源记录自身的字段。它拒绝带有正确答案、攻击值或角色的字段。虚构单测覆盖通过、缺文档哈希和答案卡三种情况，不访问网络。
Owner32 仍是 `DESIGN_DRAFT / OWNER_APPROVAL_PENDING`。在正式批准前不启动科学试次。`AUTO_CONTINUE=NO`。Claim1–3 仍是 `NOT_RUN`。
