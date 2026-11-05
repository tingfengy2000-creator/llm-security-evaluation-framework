# 5060 Codex｜Paper1 Pilot12 最小端到端RAG有条件真实执行合同 V1

**必须整篇读取执行，勿使用聊天附件替代或擅自浓缩。**

- **唯一 Owner 授权**：`W1-OD-20261105-5060-PILOT12-CONDITIONAL-LIVE-10`；十二字段正式记录 `docs/paper1/dual_machine/owner_approvals/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_AUTHORIZATION_20261105.md`，登记 Git commit `74c816e264a94a7ec2013d0d5127ac4df3720944`。
- **唯一授权分支**：`research/paper1-chinese-defense-5060`；原 Runner 验收 HEAD `ce90a34348dff093e132e6f9823ad9b84e4f67d9`。
- **任务范围**：实现和核查一个仅百炼官方端点的真实Transport；对静态冻结108格的Token/输出计费/数据外传/全工作线预算做证据级准入。只有各门在实际运行前**独立机器核验全部PASS**，才按照固定序列发送首3格；全部工程检查通过后继续剩下最多105格，不再请求新Owner批准。任一异常立刻停止且不重试。**本合同当前状态CONDITIONAL_APPROVAL_GATES_PENDING，不代表已经可以连网。**

## 0｜开工恢复、证据锚点与范围

执行AGENTS.md全套Context Recovery（12字段）、PO-MHEP、FORWARD_RISK_REVIEW/PAPER_RISK_REVIEW；按权威文件顺序读取context_authority_map、current_state、PROJECT_MASTER_CONTEXT、Owner Register、长期需求、Experiment Master、路线、research_log、最近15个Git commit、原Runner QA和完整Owner10授权。Git preflight：fetch、worktree/branch/upstream/clean状态、HEAD、log、只在安全clean+单纯fast-forward下pull --ff-only；异常STOP，不用stash/reset/rebase/cherry-pick/force push。

逐字读取：
- `docs/paper1/dual_machine/chinese5060/pilot_design/PILOT_EXECUTION_PROPOSAL.json` 文件SHA256 `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`；
- 私有原108格计划SHA256 `7db82812f893fc0384b2896c98bb5c779504e19a5c45a097945962e840999c96`；
- `pilot_runner/OWNER_LIVE_RUN_APPROVAL_PACKET.md`、`pilot_runner/PROVIDER_MODEL_TOKEN_BUDGET_GATE.json`、`pilot_runner/DRY_RUN_AND_QA.json`及 `1a11fd2ef4802d5029619acb3e65c5ad09a4a57e` 源码；
- 原P2/PAIR01/FASTC seals及报告。禁止修改这些旧文件或语料/索引/方法参数/模型身份/提问方式。

固定模型`qwen3.7-plus-2026-05-26`，原36世界各G0/G1/G2 108格、80个唯一prompt_hash、不去重，G0原TopK5、G1/G2原PAIR01已删上下文，顺序严格`world_original_order, G0, G1, G2`。任何模型/方案/Token cap、system、query、chunk或rank变更必须STOP并新Owner裁决。生成端不能读取事实参考、role或target。

## 1｜实现真实Transport（先离线审核）

1. 限定`src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/`与`scripts/research/`增量新增/受控修改。此为唯一允许的真实Transport变更，不得修改上游RAGDefender、旧P2/PAIR01/b12/filter算法、原已封存Builder或请求内容。
2. 保持FakeTransport的Mock默认。真正联网必须经多重条件：`Owner10授权Git原件`、批准范围与模型/region官方host、`immutable RUN_ADMISSION_MANIFEST`绑定源码/环境/108请求SHA/Token证据/私有费用账本/外传合规/运行目录、单独本地Checker全面PASS、显式run模式；不允许仅靠`--live`、一个环境变量、可伪造的Owner字符串或改布尔值解锁。不可假冒Owner额外签名；本Owner10**已经是**有条件执行许可，Checker只认先验冻结合同和实际证据。
3. 原Runner存在CPython socket/DNS audit deny hook。仅为受审真实发送路径创建受控网络例外（例如小型专用Transport/独立进程，限制请求体与方法），绝不可整个进程全面关安全钩子。官方合法region需由Owner既有attestation及环境/文档双重一致定位，不得根据IP、浏览器所在地或猜测设置。只允许HTTPS TLS验证、单个明确官方host、POST `/compatible-mode/v1/chat/completions`、不使用环境proxy、不允许HTTP 3xx自动重定向、DNS/证书异常STOP。SDK自动retry=0（可用纯标准库单发HTTP以避免隐式SDK），无其他网络。发送前在日志写`send_intent`并落盘，防止timeout/断电重复支付。
4. 预冻结wire JSON中请求参数：模型字面不变；system+user冻结消息；temperature=0、top_p=1、`enable_thinking=false`、`enable_search=false`、tools空、`stream=false`、`response_format={"type":"json_object"}`、输出`max_tokens=256`（原候选）。核百炼官方文档该endpoint/region对非思考JSON和这些字段的支持；OpenAI SDK仅使用extra_body传递非标准参数，原生HTTPS直接body顶层，不能混写。**`max_completion_tokens`与`max_tokens`是语义不同参数**：若必须改，不能擅自切换，先PO-MHEP上报Owner。官方关于`max_completion_tokens`“最多10 Token差异”不是原`max_tokens`可用的严格计费界；须对使用中的旧字段取得可信上界证据，否则`WIRE_GATE_BLOCKED`，绝不先发1格试验探测。
5. 实际响应要严格审核HTTP状态/ID/model字面/usage.prompt/completion/total+cached与reasoning字段/finish_reason/JSON键`status answer citations`和citations引用存在性，无隐含thinking、无外部搜索。模型别名、被截断、超额、未知扣费或缺usage均异常STOP；若实际模型响应不可验证，保留原字节hash/脱敏状态，不伪造usage。

## 2｜真实调用前五类证据硬门（任意UNKNOWN则0 POST）

**A　科学输入和独立性 PASS**
- SHA核P2封存、PAIR01/B0/B1/B2、proposal、108格私有文件、全部prompt/hash/system、运行代码源和内部固定配置；独立QA检查全108请求与预注册一致，不能把role/reference/target交给生成器；检查空上下文、单chunk及29Hit/7MISS分母。80唯一prompt不得去重或复用答案。临时参考JSON与Reviewer/GT路径不可在Builder/LiveTransport的可读白名单。
- D1合法外传检查：待发原问题与TopK保留文本（包括每格污染候选如有）仅传授权百炼地域；对私有/个人信息、版权/来源许可、第三方数据传输范围做静态审计记录。材料需改写才能安全外传时**阻断**，不静默修改冻结科学输入。

**B　模型、Wire及传输 PASS**
- 公开官方信息/本机受控配置确定**唯一**region endpoint+exact model、JSON+nonthinking+输出256真实硬上界（含计费/隐藏token）及其他固定参数支持、返回字段用量标准；如有兼容疑点不可用真实请求作为验证手段。
- Source code/依赖/static QA覆盖：TCP连接仅一个合法host，标准证书验证、无代理/redirect/retry/二次请求、无凭证落日志、无自动fallback、单并发、10s连接/60s读取/90s总上限。未来生成器一旦失败不重试。

**C　输入Token PASS**
- 不允许把当前静态`UTF8字节+512`规划单位当精确数。需要**已经在D/E合规存在**且身份可核的同模型离线Tokenizer+Chat template，或具有来源和形式论证的保守Token上界，逐一证明所有108条完整system/user消息（包含chat framing）`<=4096`；完整参数、算法SHA、逐格检查与最大值封存。
- 缺可证明上界时保留`TOKEN_GATE_BLOCKED`，不能调用在线count-tokens、安装/下载tokenizer或把用户的“不担心费用”作为跳过证据门。

**D　USD预算/资源 PASS**
- 读取D/E受控私有`BUDGET_PRIVATE.json`及SHA，Owner已核账户/模型/地域/费率/余额属于`OWNER_ATTESTED`，无需再次索要截图/密钥；但必须取得计算所需的实际数值或有来源可复核的保守上界。账本纳入所有工作线已结算+未结算+失败在途与历史人民币7.611826/7.528095914差额，不以旧1USD=6CNY作为当前汇率。
- 基础按全108上界：输入`442368 tokens`（单请求4096），输出原计划`27648 tokens`（256×108）只在**确证256总计费硬上界**后可做最终上界，否则加够被证明的额外token上界；≥20%预留同时需覆盖账单不确定性。模型/地域/计费币种、input/output未缓存价、FX、账本、余额均保存hash且时间有效。只有`all_stream_settled_usd + pending_usd + whole_batch_reservation_usd <28`，且`available_funding`覆盖预留及未结算，才准入。预测>=25报告预警、>=28不开新批/请求、累计30不可越。不要把Mock USD0.63误作真实预算。
- 输出目录、进程cwd、temp/cache及WSL宿主盘均D/E，预留20GiB。禁止C盘新项目可控文件、环境迁移和下载/安装依赖。

**E　不可变Owner授权绑定与QA PASS**
- 本次Owner10 Git原件/提交hash、当前branch、最终真实Transport源码commit/hash、完整proposal/真实108格manifest/模型wire/hash/Token上界/预算数值hash/外传范围/日志目录，须形成`RUN_ADMISSION_MANIFEST.json`并由**独立本地 Checker**核签（只对静态证据判定，不能虚构Owner签字）；任何补丁导致SHA变化必须重新跑离线QA并重封存。
- 真实运行前先执行所有旧29项回归/新live transport单测、Ruff/MyPy、模拟3格+108格+超时+usage缺失+模型错配/JSON错、目录/泄露/计费失败、安全行为、同输入不复用以及`LIVE_DENIAL_WHEN_GATE_FAILED`。保留项目历史8过1旧失败，但本轮新增治理违规必须0，旧master文件不许为了消除红灯改实验历史。
- **只有ABCDE全部PASS并绑定独立先验授权，才能把live硬锁转换成“本次特定manifest限定的单次发送路径”**。不准Agent临时伪造签章、标记未知为PASS、自动扩大调用权。否则报`LIVE_GATE_BLOCKED_NO_REQUESTS`；程序实现可照常提交，但真实请求=0。

## 3｜条件运行：首3格工程检查→余105格

1. 仅当上述硬门全部PASS，生成一次唯一`LIVE_RUN_ID`、全108有序状态表及send_intent事务日志，锁定三臂冻结序列；**最多108个真正HTTPS POST**，首3格必须就是原队列1、2、3，不是任意换题后的三个，且计在108内。单格超时/HTTP错误/usage未知可实际计费，须留失败预留，不可重发。
2. 发1→核合法HTTPS/返回model/status/JSON/引用/usage/输出token+隐藏token、费用/余额、日志落盘/response hash→发2→同检→发3→同检。只检查工程指标，**不依赖答案是否正确、不读取AI暂定参考**。每个必须完整工程`SUCCESS`且没有任何风险报警，才能允许第4格。预算达到USD25 warning必须记录Owner警戒；如警戒制度要求暂停新批，则遵循原合同，>=USD28停发。
3. 满足首3工程门后，按原预登记序列4…108逐格同样核对预算/硬停，无实时内容选择、无动态删除、无调参或补采。对相同prompt_hash也发送各自一次，不缓存跨格答案。
4. **全程首个异常立即停止**：超时、HTTP/空响应、非预期model、缺/错usage、thinking/计费超限、JSON失败、finish_reason=length、未知/超预算、SHA漂移、外传风险或写C。自动重试0；不可继续剩余格，不可申请Agent自行补跑；保留`SUCCESS/FAIL/NOT_RUN`全部108及第一错误位置、请求意图、实际返回/缺失证据、已结算/在途费用。若第1格失败即0成功+1失败+107 NOT_RUN，不因异常丢失分母。任何部分完成后的新一批重新执行都不在本次授权范围。
5. 真实全部状态/原始输出/Run Manifest/费用和响应摘要hash先封存锁定，再由隔离Evaluator**按之前准许的D1暂定评价边界**审阅。未经单独开放的HumanGold/attack target/正式ASR/C3仍NOT_MEASURED；输出的`PROVISIONAL_REFERENCE_CONSISTENCY`是D1探索信号，不是论文级准确率/防御成功率。若Evaluator独立Gate没有充分批准，则只归档，后续评分维持NOT_RUN。

## 4｜材料、PO-MHEP、归档与STOP

主交付路径建议：
- `docs/paper1/dual_machine/chinese5060/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_REPORT.md`
- `docs/paper1/dual_machine/chinese5060/pilot_live/ADMISSION_GATE_MATRIX.json`（5门，来源/证据hash/条件/拒绝理由/最终结果）
- `.../pilot_live/FINAL_LIVE_RUN_AUTHORITY_AND_MANIFEST_INDEX.json`（OwnerID、git SHA、私有准入manifest SHA、runID、D/E范围）
- `.../pilot_live/LIVE_3PLUS105_EXECUTION_SUMMARY.json`（已请求/成功/失败/NOT_RUN/首3状态/总用量及成本；未发送记0而不是空想）
- `.../pilot_live/BUDGET_LEDGER_AND_STOP_SUMMARY.md`（真实 vs Mock，USD30/25/28）
- `.../pilot_live/EVALUATION_ISOLATION_AND_RESULT_LIMITS.md`；
- `.../pilot_live/FAILURES_AND_PO_MHEP.json`、`.../pilot_live/FINAL_QA.json`、`.../pilot_live/FINAL_GIT_DELIVERY.json`。
- 私有D/E新Run根目录保存：108个冻结请求的哈希索引与输入字节（有隐私/许可限制）、源码及环境hash、真实post send_intent/deliver/response、原始模型输出与usage、HTTP错误且无自动retry、账单/余额/FX证据、全108状态、每项独立seal、Reviewer/GT隔离证据、命令stdout/stderr/status/timestamps、首3 PASS checkpoint、最终归档zip和sha。
- 一律不公开提交API Key、私有完整原文/角色映射、参考答案、HTTP认证头、整份日志、实际返回模型原文或财务敏感信息；Git只放脱敏数量/SHA/失败原因/证据索引、合规代码、正式Owner授权、治理更新。

状态严格四选一：
`LIVE_GATE_BLOCKED_NO_REQUESTS`；
`LIVE_INITIAL3_STOPPED`；
`LIVE_PARTIAL_STOPPED`；
`LIVE_PILOT108_COMPLETED_PENDING_PROVISIONAL_EVAL`（合规隔离评价完成可再后缀`_D1_PROVISIONAL_EVAL`）。
**任一状态下按AGENTS/PO-MHEP完整报告、恢复原任务STOP边界、仅push自身5060分支、验证本地/远程HEAD一致/worktree clean/0:0，然后STOP。**
禁止任何后续B5/B6、D1-40/D2D3/Reviewer/GT、5090 Claims、新方法开发、调阈值/重试/扩充语料、跨分支合并。别把一次真实D1 Pilot声称成正式论文结论。
