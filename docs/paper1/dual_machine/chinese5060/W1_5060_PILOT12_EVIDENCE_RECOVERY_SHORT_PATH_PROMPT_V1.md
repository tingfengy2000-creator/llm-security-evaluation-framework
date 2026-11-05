# Paper1 / 5060｜Pilot12 卡点证据恢复：短路径执行指令 V1

**任务级别：继续 Owner11 已批准的离线证据恢复，不申请或扩展任何真实调用权限。**
- 来源：Owner 在监督会话收到 `FAST_UNBLOCK_PARTIAL_BLOCKED` 结果后明确要求“那继续”；本指令把后续工作限定在原 `W1-OD-20261105-5060-FAST-UNBLOCK-11` 的**无新模型/API、无新科学资产变更**范畴，不创设新的自动live许可。
- 分支：仅 `research/paper1-chinese-defense-5060`；本续行前源HEAD `dde903470c877de92df46d8dd2c8348df6d39600`，原Fast-Unblock源码 `43be925d57ef6fbe9cbb27d22c7f1495373c6204`。
- 不变：V1原始方案SHA `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`；V2单字段方案SHA `e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e`；V2私有108 wire plan `0920add3e5b5383a9b685207cabeb539bb3d414ee1db30c6f7a313d37469bbcc`，有序grid SHA `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c`。不重写原P2/PAIR01/Fast C/Pilot12、所有参数、模型或数据；不碰D2/D3/Reviewer/GT/5090/main。108真实生成均未运行，HumanGold0、正式ASR/QA未测。
- 上限：真实模型/API/线上count-tokens/余额探测/免费试探**0次**；不得下载/安装新模型、Tokenizer或依赖，不新增第三方原文外传；C盘不新增项目可控文件，新生成仅D/E且余量≥20GiB。禁止重演或新建另一套Runner。

## 0. 先做Context Recovery，但不要重做方法设计

读AGENTS.md与PO-MHEP/Owner11、Current Work State和`fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md`、`FAST_UNBLOCK_MANIFEST.json`、源码`fast_unblock_evidence.py`、`d1_access.py`及冻结P2/PAIR01证据；检branch/upstream/clean/fetch/最近15个commit，仅允许安全ff-only，不stash/reset/rebase/force push。对发现的私有审阅素材只读D/E allowlist，拒绝role、target、expected答案流入Generator。报告只需三项具体成果+余下最少Owner输入，不做再一轮抽象方案评审。

## 1. A门：追溯46个发送来源，不把“29未匹配”误判为“29未授权”

目前实际108请求涉及46个`source_document_hash`，17个hash能匹配原`SOURCES.json`快照，29个不匹配。先从**冻结的36份CHUNKS_PRIVATE.json、原D1_SOURCE/污染构建链与原合法manifest**追踪这29个hash对应的`chunk_id`、来源URI/作者或发布者、生成/改写/注入链、owner或许可依据以及实际进入哪几个世界。**SHA查找失败不代表没有权利**，也不代表它一定是伪造文本。以字节可核的原始路径证明归属，不要凭任务角色猜测或新生成语料。
- 分类最多四种：`OFFICIAL_LEGAL_NORM_TEXT`、`OFFICIAL_EXPLANATORY_OR_OTHER_WEB`、`OWNER_CREATED_OR_LICENSED_SYNTHETIC`、`UNKNOWN_OR_RESTRICTED`。只允许有源证据时归类；若攻击片段为Owner自有合成文本，可依据确实存在的构建证据标注，不默认污染=非法或恶意。
- 官方法规、国家机关具有立法行政司法性质的文件及正式译文依中国著作权法第5条一般不受该法保护（https://www.ncac.gov.cn/xxfb/flfg/flfg_532/202103/t20210309_50530.html）；**这不自动涵盖官方解读/网页编排/个人信息或第三方推理外传**。仅在确属该类别时做有根据的版权判断。其余依实际许可或Owner原创依据。
- 逐源形成`SOURCE_ORIGIN_RECONCILIATION_PRIVATE.json`和脱敏汇总：46已追溯数、17旧snapshot匹配、29重建出来数、真正source-identity未知数、逐类权利结论/敏感性复核进度。无需要求Owner给46条独立签名，仍不能凭空授予缺失使用权。生成器/公开Git不含role/答案/真实片段。
- 只给出**一个**Owner可能需要决定的简短表：还差哪些实际来源、其外传权限与指定地域，若0则PASS；不因一项未知阻断B/C/D的离线处理。

## 2. B和D门：利用已核账户事实，禁止重新问用户“你的费用多少”

独立查阅官方公开说明（无需API）：https://www.alibabacloud.com/help/en/model-studio/base-url ，https://www.alibabacloud.com/help/en/model-studio/regions ，https://www.alibabacloud.com/help/en/model-studio/qwen3-7-plus 和原Chat API文档。官方base-url列出按region的专属host模板，需用实际账户的region和WorkspaceId填写本地受控`ENDPOINT_PRIVATE.json`，**不要根据用户所在地、客户端IP或任何别的资料猜region**，也不要把真实workspace ID贴Git。优先从已有D/E配置/本机环境中**仅只读**查出账户已经确认的region、host、rate和ledger（禁止打印key、账号、余额）。找不到就保留最多一个简短的`OWNER_INPUT_REQUIRED`汇总，不重复索取截图或密钥。

预算按V2固定`max_completion_tokens=256`，官方文档提示可能差最多10，当前`266`是**待账号语义核实的保守候选**，不能称独立证明的总计费硬上界。计算108×输入4096+输出候选266的全部上界（或已独立证明的更强上界）、≥20% reserve，明确分类`PUBLIC_LIST_PRICE_REFERENCE` / `OWNER_ATTESTED_PRIVATE_VALUE` / `VERIFIED_ACCOUNT_LEDGER`，不混用。用Decimal复核原CNY7.611826、Owner7.528095914和差额0.083730086、全工作线pending、FX、余额、USD25警戒/28停批/30硬限。不可把虚构Mock报价视为真价；私有数值不提交公开仓库。若账本缺字段给Owner一份**只包含必需项目名称**的脱敏填表说明，不再设计新账本模块。

## 3. C门：优先研究短请求的合理准入，而非等待一个可能不公开的Tokenizer

已知最大实际消息UTF8约2444 bytes；现有`UTF8+512`是经验代理，不是严格上界。阿里云公开文档 `qwen3.7-plus` 给出最大输入长度991808 tokens（https://www.alibabacloud.com/help/en/model-studio/qwen3-7-plus），故本Pilot约束4096是**项目自行设置的预算/安全门**，不等于模型物理上下文极限。Qwen公开技术文档对相关模型描述byte-level BPE（https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md），但是**不能未经身份确认就把Qwen3的公开Tokenizer性质或Chat template等同于闭源Qwen3.7 Plus**。
请仅用既有已合法本地文件或官方公开不含模型调用的资料尝试： (a) 对V2完整system/user/服务端chat framing证明一个具有前提的严格token上界；(b) 若缺模型同源证据，则如实`STRICT_TOKEN_BOUND_UNPROVEN`，不可通过互联网下载tokenizer、不能调用服务器count-tokens，也不可标全108 PASS。
**同时交出一份不执行的科研可行性替代准入提案**：`C_GATE_RISK_ACCEPTANCE_OPTION.md`，用实际2444-byte最大输入和模型context 991808作量级核验，说明更保守的`byte+BPE+chat overhead`启发式与剩余不确定性；提出若Owner未来另行明确同意，可把“108格形式严格4096证明”更换为“固定请求字节/保守超量预算+一次请求后审真实usage，>4096即首错STOP且保留该请求账单”，清晰说明**首个超阈值请求不能被事前阻止**，所以不是形式安全等价替代。给出潜在风险、降风险条件和需Owner签认的单句，不得自行更改目前4096严格门。不能单靠此提案打开live。

## 4. 成果、决策终点、禁止再循环

交付一个增补到原`fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md`的`Evidence Recovery Addendum`，少量必要附录：
- `fast_unblock/evidence_recovery/SOURCE_ORIGIN_RECONCILIATION_SUMMARY.md`（从29追溯到根源、真实仍未知数）
- `fast_unblock/evidence_recovery/ACCOUNT_AND_LEDGER_RECOVERY.md`（已核资料实际复用、仅需Owner最小字段，脱敏）
- `fast_unblock/evidence_recovery/C_GATE_STRICT_PROOF_OR_RISK_OPTION.md`（是否严格证明可得，若不能，清楚提出更适合Pilot的可审批替代办法、绝不私自生效）
- `fast_unblock/evidence_recovery/FINAL_EVIDENCE_RECOVERY_QA.json`（只读输入SHA、新输出Sha、zero provider calls、静态/隔离测试）
各文件须以具体发现、证据SHA/已解项/未解项为主，避免新增五份功能重复的Owner审批包；如果能在现有Frozen资料中证明来源，就一次完成，不能仅再次写“需要许可”而没有尝试追踪。保持所有原V2 SHA不动，不新增科学试次、不修改预算或源输入。需要访问非allowlist或需要上传原文才能继续时及时记录`PO_MHEP_NEEDS_OWNER`，不越权。

完成仅5060分支合法commit/push、远程HEAD和clean/0:0核实后**STOP**。返回最多三个真正卡点和最短Owner下一步。终态`EVIDENCE_RECOVERY_COMPLETED_OFFLINE`或`EVIDENCE_RECOVERY_PARTIAL_BLOCKED`；实际API0、108真生成NOT_RUN、费用0、HumanGold0、TargetedASR/正式QA NOT_MEASURED，5090/D2/D3不受影响。
