# Paper 1｜K1-C 后路线监督评估与最小验证建议

日期：2026-11-08 JST  
状态：`SUPERVISOR_RECOMMENDATION / PENDING_OWNER_CONFIRMATION / NO_NEW_EXECUTION_AUTHORITY`  
依据：R2 实验 `W1-5060-R2-FAIRCTRL-20261108-02`，证据提交 `5968369eaa1b3f8d1af2d9262ef5f3f145c4a83c`，Owner15 仅覆盖已完成四臂。

## 1. 确认事实与决策

- R2 K1-C 符合预注册：`RD_ZH_TEMPLATE` Clean 删除 5/10，而可比的被删候选 0；可信来源锚 0/180；原 D1 只能保持 `D1_DEV_EXPOSED` 的开发诊断地位，不再用于后验调 tokenizer、mask、threshold 或 M1/M2/M3 规则。
- 固定 36 世界 B2 删除 81/180、Poison 2/10、Clean 4/10、HN 2/9；char2 删除 112/180、Poison 4/10、Clean 5/10、HN 4/9；仅模板清洗无变化。char2 是迁移公平参照，不是新增方法收益。
- D1 中 query/scope 可作用池为当前抽取器可观察不足，不等于文本语义上无事实。S1 必须验证抽取器而不能通过 D1 标记回填修规则。
- RAGDefender v0.2.0 `ClusteringBasedGrouping.estimate_n_adv` 对 single-hop TopK5 强制二簇，并由 TF-IDF 多数决定删除小簇/大簇；`IdentifyAdversarial.select` 根据相似对频率和 `N_adv` 删除索引；`defender.defend(query, R)` 中 `query` 在核心检测器不被使用。当前机制不直接核验 query 相关答案值、版本、生效时段、来源独立性或可信凭据。原论文已讨论自适应攻击，不得把 majority attack 说成作者完全未研究。
- P0 必须继续强约束：无独立可信来源锚时不得仅凭同值/多数/自称权威提高信任；生产主臂在缺证明时只能保守 fallback/标 UNKNOWN。不能将“没有新删除”或“保留污染”自动解释为安全或正确。

## 2. 最小研究路线（Owner 确认后才能执行）

**方向保留：** 中文 RAG 检索后、生成前的版本/范围感知隐蔽知识污染防御。以 M3 作用域/版本的可信来源绑定和 P0 攻击者可控信号不升权为主；M1 同值恢复为残余风险探索臂，M2-detect 与 M2-vote 分开；M2-value-group 本身与 X-MADAM-RAG 重叠，不能单列创新。RAGDefender 的语义不敏感是研究动机，不足以自动构成论文贡献。

**实验路线：**
1. `S1` 优先：至少 60 个与 D1/D2/D3/旧108 评价分离的中文事实抽取实例，独立核验可见 span。必须有显式答案模板与自然化去模板配对、正文/导航交错、主体属性与时间/版本/scope 冲突、否定/例外、不足证据和 UNKNOWN。记录 `wrong/total`、`wrong/decided`、coverage/abstain、四类错误分解、Wilson 区间。仍守原硬门：accuracy >= 0.9；用于 M1-safe 的 decided 错误率 <= 0.02，且不允许 all-UNKNOWN。失败即停止 M1-safe 正向主张，向 Owner 报告，不得在旧 D1 上后验修规则。
2. `S2` 仅在 S1 合格与 Owner 另行放行后：保留 10 组事实、A–I 全场景、H4+1/H5+0、自然化和多版本/伪修订、独立 source receipt 有/无双分层以及合法重复引用 I；各臂使用同一 TopK/查询/嵌入/生成输入边界。至少报告 `B2_RAW`、`RD_ZH_ONLY`、`RD_ZH_TEMPLATE` 和 M1-safe/M2-detect/M2-vote/M3/P0 主臂；成功必须与修正基线 RD-zh 相比，不以弱 B2 为主。未预先绑定独立真实来源的样本不得冒用 `TRUSTED`。
3. `S3` 由独立人/Owner 另指定的隔离方在 S2 冻结后构造，必须保留独立性和单次评估；本 memo 不指定 5090 或解封任何 S3。
4. `S4` 原 D1 仅在另批批准后用于冻结开发场景的适用性/不退化诊断；不是独立测试，不消耗新数据的 Gold/role。S5 付费 API 与正式 ASR、Answer Accuracy 单独审批。

## 3. 快速 go/no-go

- **Gate 1：S1 失败**：不继续打磨 D1；停止基于规则抽取的 M1/M2 正面性能主张，保留失败，向 Owner 提交是否更换已获批准的独立抽取方案的决策卡。
- **Gate 2：S1 合格但 S2 有锚主臂无相对 RD-zh 的 Clean/HN 可用性改善，或任何 Poison/伪版本/多数毒安全门恶化**：判本方法当前版本未证明增益，保留失败，不进入 S3/S5。
- **Gate 3：S1 与 S2 预注册门全部合格**：冻结算法、测试来源和参数；再由 Owner 另外决定 S3 独立方，之后申请单次 S3，不能自动续做。
- 所有方案必须保持 D1/D2/D3 数据隔离、历史 B2/R2 immutable、零新的商业 API/5090 Claim 权限。2.5pp 安全退化、拒答率、ASR/正确率和效率预算的正式合同不变；未测项不可声明达标。

## 4. 监督人待 Owner 决策

`OPTION_B_RECOMMENDED`：先用现有 R1/R2 设计启动有界 S1 事实值与 scope 抽取门；不要先对旧 D1 人工补写“可信锚”，也不直接启动 S2、S3 或 S5。其优势是先检验 VESA 真正的使能依赖，费用与返工风险最低；局限是无可靠来源链就无法主张真实世界 P0 证据重放的正向收益。S1 构造/执行权限、来源权、独立标注和样例范围应另形成精确 Owner 签署授权。

本文件是控制面建议，不是 `ACCEPTED` 的科研路线变更，也不是新的实验执行许可。当前 5060 维持 STOP。
